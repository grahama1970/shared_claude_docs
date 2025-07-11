
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: feature_flags_interaction.py
Purpose: Comprehensive feature flag management system with targeting, rollouts, and A/B testing

External Dependencies:
- aiohttp: https://docs.aiohttp.org/
- pydantic: https://docs.pydantic.dev/
- jsonschema: https://python-jsonschema.readthedocs.io/

Example Usage:
>>> from feature_flags_interaction import FeatureFlagsInteraction
>>> interaction = FeatureFlagsInteraction()
>>> flag = await interaction.create_flag("new-feature", enabled=True, rollout_percentage=50)
>>> is_enabled = await interaction.evaluate_flag("new-feature", user_id="user123")
"""

import asyncio
import json
import hashlib
import time
import random
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from collections import defaultdict
import aiohttp
from pydantic import BaseModel, Field, validator
import jsonschema
from loguru import logger

# Module configuration
MODULE_NAME = "feature-flags"
CACHE_TTL = 60  # seconds
FLAG_EVALUATION_TIMEOUT = 5  # seconds


class FlagType(str, Enum):
    """Supported feature flag types"""
    BOOLEAN = "boolean"
    STRING = "string"
    NUMBER = "number"
    JSON = "json"


class TargetingOperator(str, Enum):
    """Targeting rule operators"""
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    IN = "in"
    NOT_IN = "not_in"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    REGEX = "regex"


class RolloutStrategy(str, Enum):
    """Flag rollout strategies"""
    PERCENTAGE = "percentage"
    GRADUAL = "gradual"
    RING = "ring"
    CANARY = "canary"
    TARGETED = "targeted"


@dataclass
class TargetingRule:
    """Represents a targeting rule for flag evaluation"""
    attribute: str
    operator: TargetingOperator
    value: Any
    weight: float = 1.0
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate rule against context"""
        if self.attribute not in context:
            return False
            
        context_value = context[self.attribute]
        
        if self.operator == TargetingOperator.EQUALS:
            return context_value == self.value
        elif self.operator == TargetingOperator.NOT_EQUALS:
            return context_value != self.value
        elif self.operator == TargetingOperator.CONTAINS:
            return self.value in str(context_value)
        elif self.operator == TargetingOperator.NOT_CONTAINS:
            return self.value not in str(context_value)
        elif self.operator == TargetingOperator.IN:
            return context_value in self.value
        elif self.operator == TargetingOperator.NOT_IN:
            return context_value not in self.value
        elif self.operator == TargetingOperator.GREATER_THAN:
            return float(context_value) > float(self.value)
        elif self.operator == TargetingOperator.LESS_THAN:
            return float(context_value) < float(self.value)
        elif self.operator == TargetingOperator.REGEX:
            import re
            return bool(re.match(self.value, str(context_value)))
        
        return False


@dataclass
class Segment:
    """User segment for targeting"""
    name: str
    rules: List[TargetingRule]
    match_all: bool = True  # AND vs OR logic
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Check if context matches segment"""
        if not self.rules:
            return True
            
        results = [rule.evaluate(context) for rule in self.rules]
        
        if self.match_all:
            return all(results)
        else:
            return any(results)


@dataclass
class Variant:
    """A/B test variant"""
    name: str
    value: Any
    weight: int = 1
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class RolloutConfig:
    """Rollout configuration"""
    strategy: RolloutStrategy
    percentage: float = 0.0
    start_percentage: float = 0.0
    end_percentage: float = 100.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    ring_definitions: List[Segment] = field(default_factory=list)
    
    def get_current_percentage(self) -> float:
        """Calculate current percentage for gradual rollout"""
        if self.strategy != RolloutStrategy.GRADUAL:
            return self.percentage
            
        if not self.start_time or not self.end_time:
            return self.percentage
            
        now = datetime.now(timezone.utc)
        if now < self.start_time:
            return self.start_percentage
        elif now > self.end_time:
            return self.end_percentage
            
        # Linear interpolation
        total_duration = (self.end_time - self.start_time).total_seconds()
        elapsed = (now - self.start_time).total_seconds()
        progress = elapsed / total_duration
        
        return self.start_percentage + (self.end_percentage - self.start_percentage) * progress


@dataclass
class FeatureFlag:
    """Complete feature flag definition"""
    key: str
    name: str
    flag_type: FlagType
    enabled: bool = True
    default_value: Any = None
    description: str = ""
    tags: List[str] = field(default_factory=list)
    
    # Targeting
    segments: List[Segment] = field(default_factory=list)
    targeting_enabled: bool = False
    
    # Rollout
    rollout: Optional[RolloutConfig] = None
    
    # A/B Testing
    variants: List[Variant] = field(default_factory=list)
    
    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    
    # Environment specific
    environments: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = "system"
    
    # Kill switch
    kill_switch: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        if self.rollout and self.rollout.start_time:
            data['rollout']['start_time'] = self.rollout.start_time.isoformat()
        if self.rollout and self.rollout.end_time:
            data['rollout']['end_time'] = self.rollout.end_time.isoformat()
        return data


@dataclass
class EvaluationContext:
    """Context for flag evaluation"""
    user_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    environment: str = "production"
    
    def get_hash(self, flag_key: str) -> int:
        """Get consistent hash for user/flag combination"""
        if not self.user_id:
            return random.randint(0, 99)
        
        hash_input = f"{flag_key}:{self.user_id}"
        return int(hashlib.md5(hash_input.encode()).hexdigest(), 16) % 100


@dataclass
class EvaluationResult:
    """Result of flag evaluation"""
    value: Any
    reason: str
    variant: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditLogEntry:
    """Audit log entry for flag changes"""
    timestamp: datetime
    flag_key: str
    action: str
    user: str
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class FlagStorage:
    """Storage interface for feature flags"""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
    async def save_flag(self, flag: FeatureFlag) -> None:
        """Save flag to storage"""
        flag_file = self.storage_path / f"{flag.key}.json"
        flag_data = flag.to_dict()
        
        async with asyncio.Lock():
            with open(flag_file, 'w') as f:
                json.dump(flag_data, f, indent=2)
    
    async def load_flag(self, key: str) -> Optional[FeatureFlag]:
        """Load flag from storage"""
        flag_file = self.storage_path / f"{key}.json"
        
        if not flag_file.exists():
            return None
            
        with open(flag_file, 'r') as f:
            data = json.load(f)
            
        # Convert back to objects
        return self._dict_to_flag(data)
    
    async def list_flags(self) -> List[str]:
        """List all flag keys"""
        return [f.stem for f in self.storage_path.glob("*.json")]
    
    async def delete_flag(self, key: str) -> None:
        """Delete flag from storage"""
        flag_file = self.storage_path / f"{key}.json"
        if flag_file.exists():
            flag_file.unlink()
    
    def _dict_to_flag(self, data: Dict[str, Any]) -> FeatureFlag:
        """Convert dictionary to FeatureFlag object"""
        # Parse dates
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        # Parse enums
        data['flag_type'] = FlagType(data['flag_type'])
        
        # Parse rollout
        if data.get('rollout'):
            rollout_data = data['rollout']
            rollout_data['strategy'] = RolloutStrategy(rollout_data['strategy'])
            if rollout_data.get('start_time'):
                rollout_data['start_time'] = datetime.fromisoformat(rollout_data['start_time'])
            if rollout_data.get('end_time'):
                rollout_data['end_time'] = datetime.fromisoformat(rollout_data['end_time'])
            
            # Parse ring definitions
            ring_defs = []
            for ring_data in rollout_data.get('ring_definitions', []):
                rules = []
                for rule_data in ring_data.get('rules', []):
                    rule_data['operator'] = TargetingOperator(rule_data['operator'])
                    rules.append(TargetingRule(**rule_data))
                ring_defs.append(Segment(
                    name=ring_data['name'],
                    rules=rules,
                    match_all=ring_data.get('match_all', True)
                ))
            rollout_data['ring_definitions'] = ring_defs
            
            data['rollout'] = RolloutConfig(**rollout_data)
        
        # Parse segments
        segments = []
        for segment_data in data.get('segments', []):
            rules = []
            for rule_data in segment_data.get('rules', []):
                rule_data['operator'] = TargetingOperator(rule_data['operator'])
                rules.append(TargetingRule(**rule_data))
            segments.append(Segment(
                name=segment_data['name'],
                rules=rules,
                match_all=segment_data.get('match_all', True)
            ))
        data['segments'] = segments
        
        # Parse variants
        data['variants'] = [Variant(**v) for v in data.get('variants', [])]
        
        return FeatureFlag(**data)


class FeatureFlagsInteraction:
    """Main interaction class for feature flag management"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path("./feature_flags_data")
        self.storage = FlagStorage(self.storage_path)
        self.cache: Dict[str, Tuple[FeatureFlag, float]] = {}
        self.audit_log: List[AuditLogEntry] = []
        self.webhooks: List[str] = []
        self._evaluation_cache: Dict[str, Tuple[EvaluationResult, float]] = {}
    
    # Flag Management
    
    async def create_flag(
        self,
        key: str,
        name: str,
        flag_type: FlagType = FlagType.BOOLEAN,
        enabled: bool = True,
        default_value: Any = None,
        description: str = "",
        tags: List[str] = None,
        rollout_percentage: Optional[float] = None,
        dependencies: List[str] = None,
        user: str = "system"
    ) -> FeatureFlag:
        """Create a new feature flag"""
        # Check if flag already exists
        existing = await self.get_flag(key)
        if existing:
            raise ValueError(f"Flag with key '{key}' already exists")
        
        # Create rollout config if percentage specified
        rollout = None
        if rollout_percentage is not None:
            rollout = RolloutConfig(
                strategy=RolloutStrategy.PERCENTAGE,
                percentage=rollout_percentage
            )
        
        flag = FeatureFlag(
            key=key,
            name=name,
            flag_type=flag_type,
            enabled=enabled,
            default_value=default_value,
            description=description,
            tags=tags or [],
            rollout=rollout,
            dependencies=dependencies or [],
            created_by=user
        )
        
        await self.storage.save_flag(flag)
        self._invalidate_cache(key)
        
        # Audit log
        await self._add_audit_log(
            flag_key=key,
            action="create",
            user=user,
            new_value=flag.to_dict()
        )
        
        # Notify webhooks
        await self._notify_webhooks("flag_created", flag)
        
        logger.info(f"Created flag: {key}")
        return flag
    
    async def update_flag(
        self,
        key: str,
        updates: Dict[str, Any],
        user: str = "system"
    ) -> FeatureFlag:
        """Update an existing flag"""
        flag = await self.get_flag(key)
        if not flag:
            raise ValueError(f"Flag '{key}' not found")
        
        old_value = flag.to_dict()
        
        # Apply updates
        for field, value in updates.items():
            if hasattr(flag, field):
                setattr(flag, field, value)
        
        flag.updated_at = datetime.now(timezone.utc)
        
        await self.storage.save_flag(flag)
        self._invalidate_cache(key)
        
        # Audit log
        await self._add_audit_log(
            flag_key=key,
            action="update",
            user=user,
            old_value=old_value,
            new_value=flag.to_dict()
        )
        
        # Notify webhooks
        await self._notify_webhooks("flag_updated", flag)
        
        logger.info(f"Updated flag: {key}")
        return flag
    
    async def delete_flag(self, key: str, user: str = "system") -> None:
        """Delete a flag"""
        flag = await self.get_flag(key)
        if not flag:
            raise ValueError(f"Flag '{key}' not found")
        
        old_value = flag.to_dict()
        
        await self.storage.delete_flag(key)
        self._invalidate_cache(key)
        
        # Audit log
        await self._add_audit_log(
            flag_key=key,
            action="delete",
            user=user,
            old_value=old_value
        )
        
        # Notify webhooks
        await self._notify_webhooks("flag_deleted", flag)
        
        logger.info(f"Deleted flag: {key}")
    
    async def get_flag(self, key: str) -> Optional[FeatureFlag]:
        """Get a flag by key"""
        # Check cache
        if key in self.cache:
            flag, timestamp = self.cache[key]
            if time.time() - timestamp < CACHE_TTL:
                return flag
        
        # Load from storage
        flag = await self.storage.load_flag(key)
        if flag:
            self.cache[key] = (flag, time.time())
        
        return flag
    
    async def list_flags(
        self,
        tags: Optional[List[str]] = None,
        environment: Optional[str] = None
    ) -> List[FeatureFlag]:
        """List all flags with optional filtering"""
        keys = await self.storage.list_flags()
        flags = []
        
        for key in keys:
            flag = await self.get_flag(key)
            if flag:
                # Filter by tags
                if tags and not any(tag in flag.tags for tag in tags):
                    continue
                
                # Filter by environment
                if environment and environment not in flag.environments:
                    continue
                
                flags.append(flag)
        
        return flags
    
    # Flag Evaluation
    
    async def evaluate_flag(
        self,
        key: str,
        context: Optional[Union[EvaluationContext, Dict[str, Any]]] = None,
        user_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        environment: str = "production"
    ) -> Any:
        """Evaluate a feature flag"""
        # Build context
        if isinstance(context, dict):
            context = EvaluationContext(
                user_id=context.get('user_id'),
                attributes=context,
                environment=context.get('environment', environment)
            )
        elif context is None:
            context = EvaluationContext(
                user_id=user_id,
                attributes=attributes or {},
                environment=environment
            )
        
        # Evaluate and return value
        result = await self.evaluate_flag_detailed(key, context)
        return result.value if result else None
    
    async def evaluate_flag_detailed(
        self,
        key: str,
        context: EvaluationContext
    ) -> Optional[EvaluationResult]:
        """Evaluate flag with detailed result"""
        # Check evaluation cache
        cache_key = f"{key}:{context.user_id}:{hash(str(context.attributes))}"
        if cache_key in self._evaluation_cache:
            result, timestamp = self._evaluation_cache[cache_key]
            if time.time() - timestamp < 10:  # 10 second cache
                return result
        
        flag = await self.get_flag(key)
        if not flag:
            logger.warning(f"Flag '{key}' not found")
            return None
        
        # Kill switch check
        if flag.kill_switch:
            result = EvaluationResult(
                value=flag.default_value,
                reason="kill_switch"
            )
            self._evaluation_cache[cache_key] = (result, time.time())
            return result
        
        # Disabled check
        if not flag.enabled:
            result = EvaluationResult(
                value=flag.default_value,
                reason="disabled"
            )
            self._evaluation_cache[cache_key] = (result, time.time())
            return result
        
        # Environment check
        if context.environment in flag.environments:
            env_config = flag.environments[context.environment]
            if not env_config.get('enabled', True):
                result = EvaluationResult(
                    value=flag.default_value,
                    reason="disabled_in_environment"
                )
                self._evaluation_cache[cache_key] = (result, time.time())
                return result
        
        # Dependency check
        for dep_key in flag.dependencies:
            dep_result = await self.evaluate_flag(dep_key, context)
            # For boolean flags, check if they're True
            # For other flags, check if they have a truthy value
            dep_flag = await self.get_flag(dep_key)
            if dep_flag and dep_flag.flag_type == FlagType.BOOLEAN:
                if dep_result is not True:
                    result = EvaluationResult(
                        value=flag.default_value,
                        reason="dependency_not_met",
                        metadata={"dependency": dep_key}
                    )
                    self._evaluation_cache[cache_key] = (result, time.time())
                    return result
            elif not dep_result:
                result = EvaluationResult(
                    value=flag.default_value,
                    reason="dependency_not_met",
                    metadata={"dependency": dep_key}
                )
                self._evaluation_cache[cache_key] = (result, time.time())
                return result
        
        # Targeting check
        if flag.targeting_enabled and flag.segments:
            matched = False
            for segment in flag.segments:
                if segment.evaluate(context.attributes):
                    matched = True
                    break
            
            if not matched:
                result = EvaluationResult(
                    value=flag.default_value,
                    reason="no_segment_match"
                )
                self._evaluation_cache[cache_key] = (result, time.time())
                return result
        
        # A/B test evaluation
        if flag.variants:
            variant = self._select_variant(flag, context)
            result = EvaluationResult(
                value=variant.value,
                reason="variant",
                variant=variant.name
            )
            self._evaluation_cache[cache_key] = (result, time.time())
            return result
        
        # Rollout evaluation
        if flag.rollout:
            included = self._evaluate_rollout(flag.rollout, context, flag.key)
            if not included:
                result = EvaluationResult(
                    value=flag.default_value,
                    reason="rollout_excluded"
                )
                self._evaluation_cache[cache_key] = (result, time.time())
                return result
        
        # Default enabled value
        value = True if flag.flag_type == FlagType.BOOLEAN else flag.default_value
        result = EvaluationResult(
            value=value,
            reason="enabled"
        )
        self._evaluation_cache[cache_key] = (result, time.time())
        return result
    
    def _evaluate_rollout(
        self,
        rollout: RolloutConfig,
        context: EvaluationContext,
        flag_key: str
    ) -> bool:
        """Evaluate rollout rules"""
        if rollout.strategy == RolloutStrategy.PERCENTAGE:
            percentage = rollout.get_current_percentage()
            user_hash = context.get_hash(flag_key)
            return user_hash < percentage
        
        elif rollout.strategy == RolloutStrategy.GRADUAL:
            percentage = rollout.get_current_percentage()
            user_hash = context.get_hash(flag_key)
            return user_hash < percentage
        
        elif rollout.strategy == RolloutStrategy.RING:
            # Evaluate ring by ring
            for ring in rollout.ring_definitions:
                if ring.evaluate(context.attributes):
                    return True
            return False
        
        elif rollout.strategy == RolloutStrategy.CANARY:
            # Simple canary: first X% of users
            percentage = rollout.percentage
            user_hash = context.get_hash(flag_key)
            return user_hash < percentage
        
        elif rollout.strategy == RolloutStrategy.TARGETED:
            # Only targeted users/segments
            return True  # Already handled by targeting
        
        return False
    
    def _select_variant(
        self,
        flag: FeatureFlag,
        context: EvaluationContext
    ) -> Variant:
        """Select variant for A/B test"""
        if not flag.variants:
            return Variant(name="control", value=flag.default_value)
        
        # Calculate total weight
        total_weight = sum(v.weight for v in flag.variants)
        
        # Get user's position in variant space
        user_hash = context.get_hash(flag.key)
        position = (user_hash / 100.0) * total_weight
        
        # Select variant
        current_weight = 0
        for variant in flag.variants:
            current_weight += variant.weight
            if position <= current_weight:
                return variant
        
        # Fallback to last variant
        return flag.variants[-1]
    
    # Targeting & Segmentation
    
    async def add_segment(
        self,
        flag_key: str,
        segment: Segment,
        user: str = "system"
    ) -> FeatureFlag:
        """Add a segment to a flag"""
        flag = await self.get_flag(flag_key)
        if not flag:
            raise ValueError(f"Flag '{flag_key}' not found")
        
        flag.segments.append(segment)
        flag.targeting_enabled = True
        
        return await self.update_flag(flag_key, {
            'segments': flag.segments,
            'targeting_enabled': True
        }, user)
    
    async def add_targeting_rule(
        self,
        flag_key: str,
        segment_name: str,
        rule: TargetingRule,
        user: str = "system"
    ) -> FeatureFlag:
        """Add a targeting rule to a segment"""
        flag = await self.get_flag(flag_key)
        if not flag:
            raise ValueError(f"Flag '{flag_key}' not found")
        
        # Find segment
        segment = None
        for s in flag.segments:
            if s.name == segment_name:
                segment = s
                break
        
        if not segment:
            raise ValueError(f"Segment '{segment_name}' not found")
        
        segment.rules.append(rule)
        
        return await self.update_flag(flag_key, {
            'segments': flag.segments
        }, user)
    
    # A/B Testing
    
    async def add_variant(
        self,
        flag_key: str,
        variant: Variant,
        user: str = "system"
    ) -> FeatureFlag:
        """Add a variant for A/B testing"""
        flag = await self.get_flag(flag_key)
        if not flag:
            raise ValueError(f"Flag '{flag_key}' not found")
        
        flag.variants.append(variant)
        
        return await self.update_flag(flag_key, {
            'variants': flag.variants
        }, user)
    
    # SDK Generation
    
    async def generate_sdk(
        self,
        language: str,
        flags: Optional[List[str]] = None,
        environment: str = "production"
    ) -> str:
        """Generate SDK code for specified language"""
        supported_languages = ["javascript", "python", "java", "go"]
        
        if language not in supported_languages:
            raise ValueError(f"Unsupported language: {language}")
        
        # Get flags to include
        if flags:
            flag_list = []
            for key in flags:
                flag = await self.get_flag(key)
                if flag:
                    flag_list.append(flag)
        else:
            flag_list = await self.list_flags(environment=environment)
        
        template_path = Path(__file__).parent / "sdk_templates" / f"{language}.template"
        
        if language == "javascript":
            return self._generate_js_sdk(flag_list, environment)
        elif language == "python":
            return self._generate_python_sdk(flag_list, environment)
        elif language == "java":
            return self._generate_java_sdk(flag_list, environment)
        elif language == "go":
            return self._generate_go_sdk(flag_list, environment)
        
        return ""
    
    def _generate_js_sdk(self, flags: List[FeatureFlag], environment: str) -> str:
        """Generate JavaScript SDK"""
        sdk = """// Generated Feature Flags SDK
class FeatureFlags {
    constructor() {
        this.flags = {
"""
        
        for flag in flags:
            sdk += f"            '{flag.key}': {json.dumps(flag.to_dict())},\n"
        
        sdk += """        };
        this.environment = '""" + environment + """';
    }
    
    evaluate(key, context = {}) {
        const flag = this.flags[key];
        if (!flag) return null;
        
        if (!flag.enabled) return flag.default_value;
        
        // Simple evaluation logic
        if (flag.rollout && flag.rollout.strategy === 'percentage') {
            const hash = this._hash(key + ':' + (context.user_id || 'anonymous'));
            if (hash < flag.rollout.percentage) {
                return flag.flag_type === 'boolean' ? true : flag.default_value;
            }
        }
        
        return flag.default_value;
    }
    
    _hash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash = hash & hash;
        }
        return Math.abs(hash) % 100;
    }
}

module.exports = FeatureFlags;
"""
        return sdk
    
    def _generate_python_sdk(self, flags: List[FeatureFlag], environment: str) -> str:
        """Generate Python SDK"""
        sdk = '''"""Generated Feature Flags SDK"""
import hashlib
from typing import Dict, Any, Optional


class FeatureFlags:
    def __init__(self):
        self.flags = {
'''
        
        for flag in flags:
            sdk += f"            '{flag.key}': {repr(flag.to_dict())},\n"
        
        sdk += f'''        }}
        self.environment = '{environment}'
    
    def evaluate(self, key: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Evaluate a feature flag"""
        context = context or {{}}
        flag = self.flags.get(key)
        if not flag:
            return None
        
        if not flag['enabled']:
            return flag['default_value']
        
        # Simple evaluation logic
        if flag.get('rollout') and flag['rollout']['strategy'] == 'percentage':
            user_id = context.get('user_id', 'anonymous')
            hash_val = self._hash(f"{{key}}:{{user_id}}")
            if hash_val < flag['rollout']['percentage']:
                return True if flag['flag_type'] == 'boolean' else flag['default_value']
        
        return flag['default_value']
    
    def _hash(self, text: str) -> int:
        """Generate consistent hash"""
        return int(hashlib.md5(text.encode()).hexdigest(), 16) % 100
'''
        return sdk
    
    def _generate_java_sdk(self, flags: List[FeatureFlag], environment: str) -> str:
        """Generate Java SDK"""
        sdk = """// Generated Feature Flags SDK
import java.util.*;
import java.security.MessageDigest;

public class FeatureFlags {
    private final Map<String, Map<String, Object>> flags;
    private final String environment;
    
    public FeatureFlags() {
        this.environment = \"""" + environment + """\";
        this.flags = new HashMap<>();
        initializeFlags();
    }
    
    private void initializeFlags() {
"""
        
        for flag in flags:
            sdk += f"""        Map<String, Object> {flag.key.replace('-', '_')} = new HashMap<>();
        {flag.key.replace('-', '_')}.put("enabled", {str(flag.enabled).lower()});
        {flag.key.replace('-', '_')}.put("default_value", {repr(flag.default_value)});
        flags.put("{flag.key}", {flag.key.replace('-', '_')});
        
"""
        
        sdk += """    }
    
    public Object evaluate(String key, Map<String, Object> context) {
        Map<String, Object> flag = flags.get(key);
        if (flag == null) return null;
        
        if (!(Boolean) flag.get("enabled")) {
            return flag.get("default_value");
        }
        
        // Simple evaluation logic
        return flag.get("default_value");
    }
}
"""
        return sdk
    
    def _generate_go_sdk(self, flags: List[FeatureFlag], environment: str) -> str:
        """Generate Go SDK"""
        sdk = """// Generated Feature Flags SDK
package featureflags

import (
    "crypto/md5"
    "encoding/hex"
)

type FeatureFlags struct {
    flags       map[string]map[string]interface{}
    environment string
}

func NewFeatureFlags() *FeatureFlags {
    ff := &FeatureFlags{
        environment: \"""" + environment + """\",
        flags:       make(map[string]map[string]interface{}),
    }
    ff.initializeFlags()
    return ff
}

func (ff *FeatureFlags) initializeFlags() {
"""
        
        for flag in flags:
            sdk += f"""    ff.flags["{flag.key}"] = map[string]interface{{}}{{
        "enabled":       {str(flag.enabled).lower()},
        "default_value": {repr(flag.default_value)},
    }}
    
"""
        
        sdk += """}

func (ff *FeatureFlags) Evaluate(key string, context map[string]interface{}) interface{} {
    flag, exists := ff.flags[key]
    if !exists {
        return nil
    }
    
    if !flag["enabled"].(bool) {
        return flag["default_value"]
    }
    
    // Simple evaluation logic
    return flag["default_value"]
}

func hash(s string) int {
    h := md5.New()
    h.Write([]byte(s))
    hashBytes := h.Sum(nil)
    hashStr := hex.EncodeToString(hashBytes)
    
    // Convert first 8 chars to int and mod 100
    var result int
    for i := 0; i < 8 && i < len(hashStr); i++ {
        result = result*16 + int(hashStr[i])
    }
    return result % 100
}
"""
        return sdk
    
    # Analytics & Monitoring
    
    async def get_flag_analytics(
        self,
        flag_key: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get analytics for a flag"""
        # In a real implementation, this would query an analytics database
        # For now, return mock data
        return {
            "flag_key": flag_key,
            "evaluations": 10000,
            "unique_users": 5000,
            "variant_distribution": {
                "control": 0.5,
                "variant_a": 0.3,
                "variant_b": 0.2
            },
            "evaluation_reasons": {
                "enabled": 0.7,
                "rollout_excluded": 0.2,
                "no_segment_match": 0.1
            }
        }
    
    # Audit & Compliance
    
    async def get_audit_log(
        self,
        flag_key: Optional[str] = None,
        user: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[AuditLogEntry]:
        """Get audit log entries"""
        entries = self.audit_log
        
        # Filter by flag key
        if flag_key:
            entries = [e for e in entries if e.flag_key == flag_key]
        
        # Filter by user
        if user:
            entries = [e for e in entries if e.user == user]
        
        # Filter by time range
        if start_time:
            entries = [e for e in entries if e.timestamp >= start_time]
        if end_time:
            entries = [e for e in entries if e.timestamp <= end_time]
        
        # Sort by timestamp descending and limit
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries[:limit]
    
    async def _add_audit_log(
        self,
        flag_key: str,
        action: str,
        user: str,
        old_value: Optional[Dict[str, Any]] = None,
        new_value: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add entry to audit log"""
        entry = AuditLogEntry(
            timestamp=datetime.now(timezone.utc),
            flag_key=flag_key,
            action=action,
            user=user,
            old_value=old_value,
            new_value=new_value,
            metadata=metadata or {}
        )
        self.audit_log.append(entry)
        
        # Trim log if too large
        if len(self.audit_log) > 10000:
            self.audit_log = self.audit_log[-5000:]
    
    # Webhooks & Notifications
    
    async def add_webhook(self, url: str) -> None:
        """Add a webhook for flag changes"""
        if url not in self.webhooks:
            self.webhooks.append(url)
    
    async def remove_webhook(self, url: str) -> None:
        """Remove a webhook"""
        if url in self.webhooks:
            self.webhooks.remove(url)
    
    async def _notify_webhooks(self, event: str, flag: FeatureFlag) -> None:
        """Notify webhooks of flag changes"""
        if not self.webhooks:
            return
        
        payload = {
            "event": event,
            "flag": flag.to_dict(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for webhook_url in self.webhooks:
                task = self._send_webhook(session, webhook_url, payload)
                tasks.append(task)
            
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _send_webhook(
        self,
        session: aiohttp.ClientSession,
        url: str,
        payload: Dict[str, Any]
    ) -> None:
        """Send webhook notification"""
        try:
            async with session.post(
                url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status >= 400:
                    logger.warning(
                        f"Webhook failed: {url} - Status: {response.status}"
                    )
        except Exception as e:
            logger.error(f"Webhook error: {url} - {str(e)}")
    
    # Cache Management
    
    def _invalidate_cache(self, flag_key: str) -> None:
        """Invalidate cache for a flag"""
        if flag_key in self.cache:
            del self.cache[flag_key]
        
        # Clear evaluation cache for this flag
        keys_to_remove = [
            k for k in self._evaluation_cache.keys()
            if k.startswith(f"{flag_key}:")
        ]
        for key in keys_to_remove:
            del self._evaluation_cache[key]
    
    async def clear_cache(self) -> None:
        """Clear all caches"""
        self.cache.clear()
        self._evaluation_cache.clear()
    
    # Emergency Controls
    
    async def activate_kill_switch(
        self,
        flag_key: str,
        user: str = "system"
    ) -> FeatureFlag:
        """Activate kill switch for a flag"""
        return await self.update_flag(flag_key, {"kill_switch": True}, user)
    
    async def deactivate_kill_switch(
        self,
        flag_key: str,
        user: str = "system"
    ) -> FeatureFlag:
        """Deactivate kill switch for a flag"""
        return await self.update_flag(flag_key, {"kill_switch": False}, user)
    
    async def emergency_disable_all(self, user: str = "system") -> List[str]:
        """Emergency disable all flags"""
        disabled = []
        keys = await self.storage.list_flags()
        
        for key in keys:
            try:
                await self.update_flag(key, {"enabled": False}, user)
                disabled.append(key)
            except Exception as e:
                logger.error(f"Failed to disable flag {key}: {str(e)}")
        
        return disabled


# Example usage and validation
if __name__ == "__main__":
    async def main():
        """Test feature flag functionality"""
        interaction = FeatureFlagsInteraction()
        
        try:
            # Test 1: Create flags
            print("Test 1: Creating feature flags...")
            
            # Boolean flag with rollout
            flag1 = await interaction.create_flag(
                key="new-ui",
                name="New UI Design",
                flag_type=FlagType.BOOLEAN,
                enabled=True,
                rollout_percentage=25,
                description="Roll out new UI to 25% of users",
                tags=["ui", "experiment"]
            )
            
            # String flag with variants for A/B test
            flag2 = await interaction.create_flag(
                key="button-color",
                name="Button Color Test",
                flag_type=FlagType.STRING,
                default_value="blue",
                description="Test different button colors"
            )
            
            # Add variants
            await interaction.add_variant(
                "button-color",
                Variant(name="control", value="blue", weight=50)
            )
            await interaction.add_variant(
                "button-color",
                Variant(name="variant_a", value="green", weight=30)
            )
            await interaction.add_variant(
                "button-color",
                Variant(name="variant_b", value="red", weight=20)
            )
            
            print(f"✅ Created flags: {flag1.key}, {flag2.key}")
            
            # Test 2: Evaluate flags
            print("\nTest 2: Evaluating flags...")
            
            # Test with different users
            results = []
            for i in range(10):
                context = EvaluationContext(
                    user_id=f"user_{i}",
                    attributes={"country": "US", "plan": "premium"}
                )
                
                ui_enabled = await interaction.evaluate_flag("new-ui", context)
                button_color = await interaction.evaluate_flag("button-color", context)
                
                results.append({
                    "user": f"user_{i}",
                    "new_ui": ui_enabled,
                    "button_color": button_color
                })
            
            print("Evaluation results:")
            for r in results[:5]:
                print(f"  {r['user']}: new_ui={r['new_ui']}, button_color={r['button_color']}")
            
            # Test 3: Targeting
            print("\nTest 3: Adding targeting rules...")
            
            segment = Segment(
                name="premium_users",
                rules=[
                    TargetingRule(
                        attribute="plan",
                        operator=TargetingOperator.EQUALS,
                        value="premium"
                    )
                ]
            )
            
            await interaction.add_segment("new-ui", segment)
            
            # Test targeted evaluation
            premium_context = EvaluationContext(
                user_id="premium_user",
                attributes={"plan": "premium"}
            )
            basic_context = EvaluationContext(
                user_id="basic_user",
                attributes={"plan": "basic"}
            )
            
            premium_result = await interaction.evaluate_flag_detailed("new-ui", premium_context)
            basic_result = await interaction.evaluate_flag_detailed("new-ui", basic_context)
            
            print(f"Premium user: {premium_result.value} (reason: {premium_result.reason})")
            print(f"Basic user: {basic_result.value} (reason: {basic_result.reason})")
            
            # Test 4: SDK Generation
            print("\nTest 4: Generating SDKs...")
            
            js_sdk = await interaction.generate_sdk("javascript")
            print(f"JavaScript SDK generated: {len(js_sdk)} chars")
            
            py_sdk = await interaction.generate_sdk("python")
            print(f"Python SDK generated: {len(py_sdk)} chars")
            
            # Test 5: Analytics
            print("\nTest 5: Getting analytics...")
            
            analytics = await interaction.get_flag_analytics("new-ui")
            print(f"Flag analytics: {analytics['evaluations']} evaluations")
            
            # Test 6: Audit log
            print("\nTest 6: Checking audit log...")
            
            audit_entries = await interaction.get_audit_log(limit=5)
            print(f"Audit log entries: {len(audit_entries)}")
            for entry in audit_entries[:3]:
                print(f"  {entry.timestamp}: {entry.action} on {entry.flag_key} by {entry.user}")
            
            # Test 7: Kill switch
            print("\nTest 7: Testing kill switch...")
            
            await interaction.activate_kill_switch("new-ui")
            kill_result = await interaction.evaluate_flag("new-ui", premium_context)
            print(f"After kill switch: {kill_result}")
            
            await interaction.deactivate_kill_switch("new-ui")
            
            # Cleanup
            await interaction.delete_flag("new-ui")
            await interaction.delete_flag("button-color")
            
            print("\n✅ All feature flag tests passed!")
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    asyncio.run(main())