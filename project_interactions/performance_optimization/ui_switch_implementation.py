#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
GRANGER UI Switching Implementation - Simple & Fast

This module provides the core implementation for seamless switching between
GRANGER's three interfaces: Chat, Annotator, and Terminal.

External Dependencies:
- fastapi: https://fastapi.tiangolo.com/
- websockets: https://websockets.readthedocs.io/
- pyjwt: https://pyjwt.readthedocs.io/

Example Usage:
    >>> from ui_switch_implementation import UISwitcher
    >>> switcher = UISwitcher()
    >>> switcher.switch_to_interface('annotator', context={'doc_id': 'xyz789'})
    'granger://switch/annotator?doc=xyz789&session=abc123'
"""

import asyncio
import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Any
from pathlib import Path
import jwt
import aiofiles
from loguru import logger


class Interface(Enum):
    """Available GRANGER interfaces"""
    CHAT = "chat"
    ANNOTATOR = "annotator"
    TERMINAL = "terminal"


@dataclass
class SwitchContext:
    """Context preserved during interface switches"""
    current_interface: Interface
    session_id: str
    auth_token: str
    state_data: Dict[str, Any]
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class UISwitcher:
    """Main controller for UI switching operations"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".granger" / "ui_config.json"
        self.current_context: Optional[SwitchContext] = None
        self._switch_history = []
        self._performance_metrics = {
            "total_switches": 0,
            "average_switch_time": 0,
            "fastest_switch": float('inf'),
            "slowest_switch": 0
        }
        
    async def initialize(self):
        """Initialize the UI switcher with saved state"""
        if self.config_path.exists():
            async with aiofiles.open(self.config_path, 'r') as f:
                config_data = json.loads(await f.read())
                logger.info(f"Loaded UI config from {self.config_path}")
                
                # Restore last context
                if "last_context" in config_data:
                    self.current_context = SwitchContext(**config_data["last_context"])
    
    async def switch_to_interface(
        self, 
        target: str, 
        context: Optional[Dict[str, Any]] = None,
        preserve_state: bool = True
    ) -> str:
        """
        Switch to target interface with optional context
        
        Args:
            target: Interface to switch to ('chat', 'annotator', 'terminal')
            context: Additional context to pass to target interface
            preserve_state: Whether to save current state before switching
            
        Returns:
            Deep link URL for the switch
        """
        start_time = time.time()
        
        # Validate target
        try:
            target_interface = Interface(target.lower())
        except ValueError:
            raise ValueError(f"Invalid interface: {target}. Must be one of: {[i.value for i in Interface]}")
        
        # Save current state if requested
        if preserve_state and self.current_context:
            await self._save_current_state()
        
        # Generate session ID if needed
        session_id = self.current_context.session_id if self.current_context else self._generate_session_id()
        
        # Build deep link
        deep_link = self._build_deep_link(target_interface, session_id, context)
        
        # Update context
        self.current_context = SwitchContext(
            current_interface=target_interface,
            session_id=session_id,
            auth_token=await self._get_auth_token(),
            state_data=context or {}
        )
        
        # Record metrics
        switch_time = time.time() - start_time
        await self._record_switch_metrics(switch_time)
        
        # Log the switch
        logger.info(f"Switched to {target} in {switch_time:.3f}s - {deep_link}")
        
        return deep_link
    
    async def get_switch_suggestions(self, current_activity: Dict[str, Any]) -> list:
        """
        Get intelligent suggestions for which interface to switch to
        based on current activity
        """
        suggestions = []
        
        # Analyze current activity
        if "pdf_file" in current_activity or "document" in current_activity:
            suggestions.append({
                "interface": Interface.ANNOTATOR,
                "reason": "PDF document detected - annotator recommended",
                "confidence": 0.9
            })
        
        if "command" in current_activity or "terminal_output" in current_activity:
            suggestions.append({
                "interface": Interface.TERMINAL,
                "reason": "Command execution detected - terminal recommended",
                "confidence": 0.85
            })
        
        if "conversation" in current_activity or "question" in current_activity:
            suggestions.append({
                "interface": Interface.CHAT,
                "reason": "Conversational context - chat recommended",
                "confidence": 0.8
            })
        
        return sorted(suggestions, key=lambda x: x["confidence"], reverse=True)
    
    async def quick_switch_cycle(self):
        """Cycle through interfaces in order (Chat → Annotator → Terminal → Chat)"""
        current = self.current_context.current_interface if self.current_context else Interface.CHAT
        
        # Define cycle order
        cycle_order = [Interface.CHAT, Interface.ANNOTATOR, Interface.TERMINAL]
        current_index = cycle_order.index(current)
        next_index = (current_index + 1) % len(cycle_order)
        
        return await self.switch_to_interface(cycle_order[next_index].value)
    
    def _build_deep_link(
        self, 
        interface: Interface, 
        session_id: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build deep link URL for interface switching"""
        base_url = f"granger://switch/{interface.value}"
        params = [f"session={session_id}"]
        
        if context:
            # Add context-specific parameters
            if interface == Interface.ANNOTATOR and "doc_id" in context:
                params.append(f"doc={context['doc_id']}")
                if "page" in context:
                    params.append(f"page={context['page']}")
            
            elif interface == Interface.TERMINAL and "workspace" in context:
                params.append(f"workspace={context['workspace']}")
                if "command" in context:
                    params.append(f"cmd={context['command']}")
            
            elif interface == Interface.CHAT and "conversation_id" in context:
                params.append(f"conv={context['conversation_id']}")
        
        return f"{base_url}?{'&'.join(params)}"
    
    async def _save_current_state(self):
        """Save current interface state to disk"""
        if not self.current_context:
            return
        
        state_data = {
            "last_context": {
                "current_interface": self.current_context.current_interface.value,
                "session_id": self.current_context.session_id,
                "auth_token": self.current_context.auth_token,
                "state_data": self.current_context.state_data,
                "timestamp": self.current_context.timestamp
            },
            "switch_history": self._switch_history[-10:],  # Keep last 10 switches
            "metrics": self._performance_metrics
        }
        
        # Ensure directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(self.config_path, 'w') as f:
            await f.write(json.dumps(state_data, indent=2))
    
    async def _get_auth_token(self) -> str:
        """Get or generate JWT auth token"""
        if self.current_context and self.current_context.auth_token:
            return self.current_context.auth_token
        
        # Generate new token (simplified for demo)
        payload = {
            "sub": "granger_user",
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600  # 1 hour expiry
        }
        
        # In production, use proper secret key management
        secret_key = "granger_secret_key_change_in_production"
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        
        return token
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    async def _record_switch_metrics(self, switch_time: float):
        """Record performance metrics for the switch"""
        metrics = self._performance_metrics
        
        # Update metrics
        metrics["total_switches"] += 1
        
        # Update average
        if metrics["total_switches"] == 1:
            metrics["average_switch_time"] = switch_time
        else:
            total_time = metrics["average_switch_time"] * (metrics["total_switches"] - 1)
            metrics["average_switch_time"] = (total_time + switch_time) / metrics["total_switches"]
        
        # Update extremes
        metrics["fastest_switch"] = min(metrics["fastest_switch"], switch_time)
        metrics["slowest_switch"] = max(metrics["slowest_switch"], switch_time)
        
        # Add to history
        self._switch_history.append({
            "timestamp": time.time(),
            "duration": switch_time,
            "target": self.current_context.current_interface.value if self.current_context else None
        })
        
        # Log if switch was slow
        if switch_time > 1.5:
            logger.warning(f"Slow switch detected: {switch_time:.3f}s (target: <1.5s)")


class QuickSwitchBar:
    """UI component for the persistent switch bar"""
    
    def __init__(self, switcher: UISwitcher):
        self.switcher = switcher
        self.shortcuts = {
            "ctrl+alt+1": Interface.CHAT,
            "ctrl+alt+2": Interface.ANNOTATOR,
            "ctrl+alt+3": Interface.TERMINAL,
            "ctrl+tab": "cycle"
        }
    
    def render_html(self) -> str:
        """Render the switch bar as HTML"""
        current = self.switcher.current_context.current_interface.value if self.switcher.current_context else "none"
        session = self.switcher.current_context.session_id if self.switcher.current_context else "no-session"
        
        return f"""
        <div class="granger-switch-bar">
            <button class="switch-btn {'active' if current == 'chat' else ''}" onclick="switchTo('chat')">
                📱 Chat
            </button>
            <button class="switch-btn {'active' if current == 'annotator' else ''}" onclick="switchTo('annotator')">
                📝 Annotator
            </button>
            <button class="switch-btn {'active' if current == 'terminal' else ''}" onclick="switchTo('terminal')">
                ⌨️ Terminal
            </button>
            <span class="current-info">Current: {current.title()} | Session: {session}</span>
        </div>
        """
    
    async def handle_shortcut(self, key_combo: str) -> Optional[str]:
        """Handle keyboard shortcut for switching"""
        if key_combo not in self.shortcuts:
            return None
        
        action = self.shortcuts[key_combo]
        
        if action == "cycle":
            return await self.switcher.quick_switch_cycle()
        else:
            return await self.switcher.switch_to_interface(action.value)


# Example usage and validation
if __name__ == "__main__":
    async def main():
        # Initialize switcher
        switcher = UISwitcher()
        await switcher.initialize()
        
        # Test 1: Basic switch to annotator
        print("Test 1: Switching to annotator...")
        link = await switcher.switch_to_interface(
            "annotator", 
            context={"doc_id": "test123", "page": 5}
        )
        assert "granger://switch/annotator" in link
        assert "doc=test123" in link
        assert "page=5" in link
        print(f"✅ Generated link: {link}")
        
        # Test 2: Quick cycle through interfaces
        print("\nTest 2: Cycling through interfaces...")
        for i in range(4):  # Should go: annotator → terminal → chat → annotator
            link = await switcher.quick_switch_cycle()
            print(f"  Cycle {i+1}: {link}")
        
        # Test 3: Context suggestions
        print("\nTest 3: Getting switch suggestions...")
        suggestions = await switcher.get_switch_suggestions({
            "pdf_file": "document.pdf",
            "current_page": 10
        })
        assert len(suggestions) > 0
        assert suggestions[0]["interface"] == Interface.ANNOTATOR
        print(f"✅ Top suggestion: {suggestions[0]['reason']}")
        
        # Test 4: Performance check
        print("\nTest 4: Performance metrics...")
        metrics = switcher._performance_metrics
        print(f"  Total switches: {metrics['total_switches']}")
        print(f"  Average time: {metrics['average_switch_time']:.3f}s")
        print(f"  Fastest: {metrics['fastest_switch']:.3f}s")
        print(f"  Slowest: {metrics['slowest_switch']:.3f}s")
        
        # Verify performance requirement
        assert metrics['average_switch_time'] < 1.5, "Average switch time exceeds 1.5s target"
        print("✅ Performance meets <1.5s requirement")
        
        # Test 5: Switch bar rendering
        print("\nTest 5: Switch bar rendering...")
        switch_bar = QuickSwitchBar(switcher)
        html = switch_bar.render_html()
        assert "granger-switch-bar" in html
        assert "📱 Chat" in html
        assert "📝 Annotator" in html
        assert "⌨️ Terminal" in html
        print("✅ Switch bar HTML generated successfully")
        
        print("\n🎉 All tests passed! UI switching is ready for GRANGER.")
    
    # Run the validation
    asyncio.run(main())