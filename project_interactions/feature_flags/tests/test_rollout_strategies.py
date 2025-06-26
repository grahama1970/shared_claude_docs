"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Tests for rollout strategies and A/B testing functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Expected Usage:
>>> pytest test_rollout_strategies.py -v
All tests should pass
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from pathlib import Path
import shutil
from typing import Dict, List
from collections import Counter

from feature_flags_interaction import (
    FeatureFlagsInteraction,
    FlagType,
    RolloutConfig,
    RolloutStrategy,
    Variant,
    EvaluationContext,
    Segment,
    TargetingRule,
    TargetingOperator
)


@pytest.fixture
async def interaction():
    """Create test interaction with temporary storage"""
    test_path = Path("./test_rollout_data")
    if test_path.exists():
        shutil.rmtree(test_path)
    
    interaction = FeatureFlagsInteraction(storage_path=test_path)
    yield interaction
    
    # Cleanup
    if test_path.exists():
        shutil.rmtree(test_path)


@pytest.mark.asyncio
async def test_percentage_rollout(interaction):
    """Test percentage-based rollout"""
    flag = await interaction.create_flag(
        key="percentage-rollout",
        name="Percentage Rollout",
        rollout_percentage=30
    )
    
    # Test with many users to verify distribution
    enabled_count = 0
    total_users = 1000
    
    for i in range(total_users):
        context = EvaluationContext(user_id=f"user_{i}")
        result = await interaction.evaluate_flag("percentage-rollout", context)
        if result:
            enabled_count += 1
    
    # Should be approximately 30% (allowing for some variance)
    percentage = (enabled_count / total_users) * 100
    assert 25 <= percentage <= 35, f"Expected ~30%, got {percentage}%"


@pytest.mark.asyncio
async def test_gradual_rollout(interaction):
    """Test gradual rollout over time"""
    now = datetime.now(timezone.utc)
    
    # Create flag with gradual rollout
    flag = await interaction.create_flag(
        key="gradual-rollout",
        name="Gradual Rollout"
    )
    
    rollout = RolloutConfig(
        strategy=RolloutStrategy.GRADUAL,
        start_percentage=0,
        end_percentage=100,
        start_time=now - timedelta(hours=1),
        end_time=now + timedelta(hours=1)
    )
    
    await interaction.update_flag("gradual-rollout", {"rollout": rollout})
    
    # Test current percentage (should be ~50% since we're halfway)
    current_percentage = rollout.get_current_percentage()
    assert 45 <= current_percentage <= 55
    
    # Test with users
    enabled_count = 0
    for i in range(100):
        context = EvaluationContext(user_id=f"user_{i}")
        result = await interaction.evaluate_flag("gradual-rollout", context)
        if result:
            enabled_count += 1
    
    # Should be approximately 50%
    assert 40 <= enabled_count <= 60


@pytest.mark.asyncio
async def test_ring_rollout(interaction):
    """Test ring-based rollout"""
    flag = await interaction.create_flag(
        key="ring-rollout",
        name="Ring Rollout"
    )
    
    # Define rings
    internal_ring = Segment(
        name="internal",
        rules=[
            TargetingRule("employee", TargetingOperator.EQUALS, True)
        ]
    )
    
    beta_ring = Segment(
        name="beta",
        rules=[
            TargetingRule("beta_tester", TargetingOperator.EQUALS, True)
        ]
    )
    
    rollout = RolloutConfig(
        strategy=RolloutStrategy.RING,
        ring_definitions=[internal_ring, beta_ring]
    )
    
    await interaction.update_flag("ring-rollout", {"rollout": rollout})
    
    # Test different user types
    employee_context = EvaluationContext(
        attributes={"employee": True}
    )
    beta_context = EvaluationContext(
        attributes={"beta_tester": True}
    )
    regular_context = EvaluationContext(
        attributes={"employee": False, "beta_tester": False}
    )
    
    # Employees and beta testers should get it
    assert await interaction.evaluate_flag("ring-rollout", employee_context) is True
    assert await interaction.evaluate_flag("ring-rollout", beta_context) is True
    
    # Regular users should not
    assert await interaction.evaluate_flag("ring-rollout", regular_context) is None


@pytest.mark.asyncio
async def test_canary_rollout(interaction):
    """Test canary deployment strategy"""
    flag = await interaction.create_flag(
        key="canary-rollout",
        name="Canary Rollout"
    )
    
    rollout = RolloutConfig(
        strategy=RolloutStrategy.CANARY,
        percentage=10  # 10% canary
    )
    
    await interaction.update_flag("canary-rollout", {"rollout": rollout})
    
    # Test distribution
    enabled_count = 0
    for i in range(1000):
        context = EvaluationContext(user_id=f"canary_user_{i}")
        result = await interaction.evaluate_flag("canary-rollout", context)
        if result:
            enabled_count += 1
    
    # Should be approximately 10%
    percentage = (enabled_count / 1000) * 100
    assert 8 <= percentage <= 12


@pytest.mark.asyncio
async def test_ab_testing_variants(interaction):
    """Test A/B testing with multiple variants"""
    flag = await interaction.create_flag(
        key="ab-test",
        name="A/B Test",
        flag_type=FlagType.STRING,
        default_value="control"
    )
    
    # Add variants with weights
    await interaction.add_variant(
        "ab-test",
        Variant(name="control", value="blue", weight=50)
    )
    await interaction.add_variant(
        "ab-test",
        Variant(name="variant_a", value="green", weight=30)
    )
    await interaction.add_variant(
        "ab-test",
        Variant(name="variant_b", value="red", weight=20)
    )
    
    # Test distribution
    variant_counts = Counter()
    for i in range(1000):
        context = EvaluationContext(user_id=f"ab_user_{i}")
        result = await interaction.evaluate_flag_detailed("ab-test", context)
        variant_counts[result.value] += 1
    
    # Check distribution (allowing for variance)
    total = sum(variant_counts.values())
    blue_percentage = (variant_counts["blue"] / total) * 100
    green_percentage = (variant_counts["green"] / total) * 100
    red_percentage = (variant_counts["red"] / total) * 100
    
    assert 45 <= blue_percentage <= 55  # ~50%
    assert 25 <= green_percentage <= 35  # ~30%
    assert 15 <= red_percentage <= 25   # ~20%


@pytest.mark.asyncio
async def test_consistent_variant_assignment(interaction):
    """Test that users get consistent variant assignments"""
    flag = await interaction.create_flag(
        key="consistent-test",
        name="Consistent Test",
        flag_type=FlagType.STRING
    )
    
    await interaction.add_variant(
        "consistent-test",
        Variant(name="a", value="A", weight=50)
    )
    await interaction.add_variant(
        "consistent-test",
        Variant(name="b", value="B", weight=50)
    )
    
    # Same user should always get same variant
    user_id = "consistent_user_123"
    context = EvaluationContext(user_id=user_id)
    
    first_result = await interaction.evaluate_flag("consistent-test", context)
    
    # Check multiple times
    for _ in range(10):
        result = await interaction.evaluate_flag("consistent-test", context)
        assert result == first_result


@pytest.mark.asyncio
async def test_flag_dependencies(interaction):
    """Test flag dependency evaluation"""
    # Create parent flag
    parent = await interaction.create_flag(
        key="parent-flag",
        name="Parent Flag",
        enabled=True
    )
    
    # Create child flag with dependency
    child = await interaction.create_flag(
        key="child-flag",
        name="Child Flag",
        enabled=True,
        dependencies=["parent-flag"]
    )
    
    context = EvaluationContext(user_id="dep_user")
    
    # Both enabled, should work
    child_result = await interaction.evaluate_flag_detailed("child-flag", context)
    assert child_result.value is True
    assert child_result.reason == "enabled"
    
    # Disable parent
    await interaction.update_flag("parent-flag", {"enabled": False})
    
    # Child should now fail dependency check
    child_result = await interaction.evaluate_flag_detailed("child-flag", context)
    assert child_result.value is None
    assert child_result.reason == "dependency_not_met"
    assert child_result.metadata["dependency"] == "parent-flag"


@pytest.mark.asyncio
async def test_kill_switch_overrides_all(interaction):
    """Test that kill switch overrides all other logic"""
    flag = await interaction.create_flag(
        key="kill-switch-test",
        name="Kill Switch Test",
        enabled=True,
        rollout_percentage=100
    )
    
    # Add variants
    await interaction.add_variant(
        "kill-switch-test",
        Variant(name="always", value="enabled", weight=100)
    )
    
    context = EvaluationContext(user_id="kill_test_user")
    
    # Should be enabled normally
    result = await interaction.evaluate_flag("kill-switch-test", context)
    assert result == "enabled"
    
    # Activate kill switch
    await interaction.activate_kill_switch("kill-switch-test")
    
    # Should now return default value
    result = await interaction.evaluate_flag("kill-switch-test", context)
    assert result is None
    
    detailed = await interaction.evaluate_flag_detailed("kill-switch-test", context)
    assert detailed.reason == "kill_switch"


@pytest.mark.asyncio
async def test_evaluation_caching(interaction):
    """Test that evaluation results are cached"""
    flag = await interaction.create_flag(
        key="cache-test",
        name="Cache Test",
        rollout_percentage=50
    )
    
    context = EvaluationContext(
        user_id="cache_user",
        attributes={"country": "US"}
    )
    
    # First evaluation
    result1 = await interaction.evaluate_flag("cache-test", context)
    
    # Subsequent evaluations should be cached
    for _ in range(5):
        result = await interaction.evaluate_flag("cache-test", context)
        assert result == result1
    
    # Clear cache
    await interaction.clear_cache()
    
    # Should still get same result (consistent hashing)
    result_after_clear = await interaction.evaluate_flag("cache-test", context)
    assert result_after_clear == result1


@pytest.mark.asyncio
async def test_sdk_generation(interaction):
    """Test SDK generation for different languages"""
    # Create test flags
    await interaction.create_flag(
        key="sdk-bool",
        name="SDK Boolean",
        flag_type=FlagType.BOOLEAN,
        enabled=True
    )
    
    await interaction.create_flag(
        key="sdk-string",
        name="SDK String",
        flag_type=FlagType.STRING,
        default_value="default"
    )
    
    # Generate SDKs
    languages = ["javascript", "python", "java", "go"]
    
    for lang in languages:
        sdk = await interaction.generate_sdk(lang)
        assert len(sdk) > 0
        assert "sdk-bool" in sdk
        assert "sdk-string" in sdk
        
        # Language-specific checks
        if lang == "javascript":
            assert "class FeatureFlags" in sdk
            assert "evaluate(" in sdk
        elif lang == "python":
            assert "class FeatureFlags:" in sdk
            assert "def evaluate(" in sdk
        elif lang == "java":
            assert "public class FeatureFlags" in sdk
            assert "public Object evaluate" in sdk
        elif lang == "go":
            assert "type FeatureFlags struct" in sdk
            assert "func (ff *FeatureFlags) Evaluate" in sdk


@pytest.mark.asyncio
async def test_analytics_tracking(interaction):
    """Test analytics data collection"""
    flag = await interaction.create_flag(
        key="analytics-test",
        name="Analytics Test",
        rollout_percentage=50
    )
    
    # Simulate evaluations
    for i in range(100):
        context = EvaluationContext(user_id=f"analytics_user_{i}")
        await interaction.evaluate_flag("analytics-test", context)
    
    # Get analytics
    analytics = await interaction.get_flag_analytics("analytics-test")
    
    assert analytics["flag_key"] == "analytics-test"
    assert analytics["evaluations"] > 0
    assert analytics["unique_users"] > 0
    assert "variant_distribution" in analytics
    assert "evaluation_reasons" in analytics


@pytest.mark.asyncio
async def test_complex_rollout_scenario(interaction):
    """Test complex scenario with multiple features"""
    # Base feature flag
    base = await interaction.create_flag(
        key="new-checkout",
        name="New Checkout Flow",
        enabled=True,
        rollout_percentage=20
    )
    
    # A/B test within the new checkout
    await interaction.create_flag(
        key="checkout-button",
        name="Checkout Button Test",
        flag_type=FlagType.STRING,
        default_value="Buy Now",
        dependencies=["new-checkout"]
    )
    
    await interaction.add_variant(
        "checkout-button",
        Variant(name="control", value="Buy Now", weight=50)
    )
    await interaction.add_variant(
        "checkout-button",
        Variant(name="variant", value="Purchase", weight=50)
    )
    
    # Test various users
    results = []
    for i in range(100):
        context = EvaluationContext(
            user_id=f"complex_user_{i}",
            attributes={
                "country": "US" if i % 2 == 0 else "UK",
                "premium": i % 3 == 0
            }
        )
        
        checkout_enabled = await interaction.evaluate_flag("new-checkout", context)
        button_text = await interaction.evaluate_flag("checkout-button", context)
        
        results.append({
            "user": f"user_{i}",
            "checkout": checkout_enabled,
            "button": button_text
        })
    
    # Verify dependency logic
    for r in results:
        if not r["checkout"]:
            # If checkout is disabled, button should be default
            assert r["button"] == "Buy Now"
        else:
            # If checkout is enabled, button should be one of the variants
            assert r["button"] in ["Buy Now", "Purchase"]


# Validation
if __name__ == "__main__":
    async def validate():
        """Run validation tests"""
        print("Running rollout strategies validation...")
        
        interaction = FeatureFlagsInteraction(
            storage_path=Path("./validation_rollout")
        )
        
        try:
            # Test percentage rollout
            flag = await interaction.create_flag(
                "validation-rollout",
                "Rollout Test",
                rollout_percentage=40
            )
            print(f"✅ Created flag with 40% rollout")
            
            # Test distribution
            enabled = 0
            for i in range(100):
                ctx = EvaluationContext(user_id=f"val_user_{i}")
                if await interaction.evaluate_flag("validation-rollout", ctx):
                    enabled += 1
            
            print(f"✅ Rollout distribution: {enabled}% (expected ~40%)")
            
            # Test A/B variants
            ab_flag = await interaction.create_flag(
                "validation-ab",
                "A/B Test",
                flag_type=FlagType.STRING,
                default_value="control"
            )
            
            await interaction.add_variant(
                "validation-ab",
                Variant(name="a", value="A", weight=60)
            )
            await interaction.add_variant(
                "validation-ab",
                Variant(name="b", value="B", weight=40)
            )
            
            # Test variant distribution
            variant_counts = {"A": 0, "B": 0}
            for i in range(100):
                ctx = EvaluationContext(user_id=f"ab_user_{i}")
                result = await interaction.evaluate_flag("validation-ab", ctx)
                if result in variant_counts:
                    variant_counts[result] += 1
            
            print(f"✅ A/B distribution: A={variant_counts['A']}%, B={variant_counts['B']}%")
            
            # Test SDK generation
            js_sdk = await interaction.generate_sdk("javascript")
            print(f"✅ Generated JavaScript SDK: {len(js_sdk)} chars")
            
            # Cleanup
            await interaction.delete_flag("validation-rollout")
            await interaction.delete_flag("validation-ab")
            if interaction.storage_path.exists():
                shutil.rmtree(interaction.storage_path)
            
            print("\n✅ Rollout strategies validation passed!")
            
        except Exception as e:
            print(f"\n❌ Validation failed: {str(e)}")
            raise
    
    asyncio.run(validate())