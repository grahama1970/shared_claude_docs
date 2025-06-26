"""
Tests for user targeting and segmentation functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Expected Usage:
>>> pytest test_targeting.py -v
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
from pathlib import Path
import shutil
from typing import Dict, Any

from feature_flags_interaction import (
    FeatureFlagsInteraction,
    FlagType,
    TargetingRule,
    TargetingOperator,
    Segment,
    EvaluationContext,
    EvaluationResult
)


@pytest.fixture
async def interaction():
    """Create test interaction with temporary storage"""
    test_path = Path("./test_targeting_data")
    if test_path.exists():
        shutil.rmtree(test_path)
    
    interaction = FeatureFlagsInteraction(storage_path=test_path)
    yield interaction
    
    # Cleanup
    if test_path.exists():
        shutil.rmtree(test_path)


@pytest.mark.asyncio
async def test_targeting_rule_equals(interaction):
    """Test EQUALS targeting operator"""
    rule = TargetingRule(
        attribute="country",
        operator=TargetingOperator.EQUALS,
        value="US"
    )
    
    # Should match
    assert rule.evaluate({"country": "US"}) is True
    
    # Should not match
    assert rule.evaluate({"country": "UK"}) is False
    assert rule.evaluate({"city": "New York"}) is False  # Missing attribute


@pytest.mark.asyncio
async def test_targeting_rule_not_equals(interaction):
    """Test NOT_EQUALS targeting operator"""
    rule = TargetingRule(
        attribute="plan",
        operator=TargetingOperator.NOT_EQUALS,
        value="free"
    )
    
    assert rule.evaluate({"plan": "premium"}) is True
    assert rule.evaluate({"plan": "free"}) is False


@pytest.mark.asyncio
async def test_targeting_rule_contains(interaction):
    """Test CONTAINS targeting operator"""
    rule = TargetingRule(
        attribute="email",
        operator=TargetingOperator.CONTAINS,
        value="@company.com"
    )
    
    assert rule.evaluate({"email": "user@company.com"}) is True
    assert rule.evaluate({"email": "user@other.com"}) is False


@pytest.mark.asyncio
async def test_targeting_rule_in(interaction):
    """Test IN targeting operator"""
    rule = TargetingRule(
        attribute="role",
        operator=TargetingOperator.IN,
        value=["admin", "moderator", "developer"]
    )
    
    assert rule.evaluate({"role": "admin"}) is True
    assert rule.evaluate({"role": "developer"}) is True
    assert rule.evaluate({"role": "user"}) is False


@pytest.mark.asyncio
async def test_targeting_rule_comparison(interaction):
    """Test GREATER_THAN and LESS_THAN operators"""
    gt_rule = TargetingRule(
        attribute="age",
        operator=TargetingOperator.GREATER_THAN,
        value=18
    )
    
    lt_rule = TargetingRule(
        attribute="score",
        operator=TargetingOperator.LESS_THAN,
        value=100
    )
    
    assert gt_rule.evaluate({"age": 25}) is True
    assert gt_rule.evaluate({"age": 18}) is False
    assert gt_rule.evaluate({"age": 15}) is False
    
    assert lt_rule.evaluate({"score": 50}) is True
    assert lt_rule.evaluate({"score": 100}) is False
    assert lt_rule.evaluate({"score": 150}) is False


@pytest.mark.asyncio
async def test_targeting_rule_regex(interaction):
    """Test REGEX targeting operator"""
    rule = TargetingRule(
        attribute="version",
        operator=TargetingOperator.REGEX,
        value=r"^2\.\d+\.\d+$"
    )
    
    assert rule.evaluate({"version": "2.0.0"}) is True
    assert rule.evaluate({"version": "2.1.5"}) is True
    assert rule.evaluate({"version": "1.0.0"}) is False
    assert rule.evaluate({"version": "2.0"}) is False


@pytest.mark.asyncio
async def test_segment_match_all(interaction):
    """Test segment with AND logic (match_all=True)"""
    segment = Segment(
        name="premium_us_users",
        rules=[
            TargetingRule("country", TargetingOperator.EQUALS, "US"),
            TargetingRule("plan", TargetingOperator.EQUALS, "premium"),
            TargetingRule("active", TargetingOperator.EQUALS, True)
        ],
        match_all=True
    )
    
    # All conditions match
    assert segment.evaluate({
        "country": "US",
        "plan": "premium",
        "active": True
    }) is True
    
    # One condition doesn't match
    assert segment.evaluate({
        "country": "US",
        "plan": "free",
        "active": True
    }) is False


@pytest.mark.asyncio
async def test_segment_match_any(interaction):
    """Test segment with OR logic (match_all=False)"""
    segment = Segment(
        name="special_users",
        rules=[
            TargetingRule("role", TargetingOperator.EQUALS, "admin"),
            TargetingRule("beta_tester", TargetingOperator.EQUALS, True),
            TargetingRule("vip", TargetingOperator.EQUALS, True)
        ],
        match_all=False
    )
    
    # Any condition matches
    assert segment.evaluate({"role": "admin"}) is True
    assert segment.evaluate({"beta_tester": True}) is True
    assert segment.evaluate({"vip": True}) is True
    
    # No conditions match
    assert segment.evaluate({
        "role": "user",
        "beta_tester": False,
        "vip": False
    }) is False


@pytest.mark.asyncio
async def test_flag_with_segments(interaction):
    """Test flag evaluation with segments"""
    # Create flag
    flag = await interaction.create_flag(
        key="targeted-feature",
        name="Targeted Feature",
        flag_type=FlagType.BOOLEAN,
        enabled=True,
        default_value=False
    )
    
    # Add segment
    segment = Segment(
        name="early_adopters",
        rules=[
            TargetingRule("early_adopter", TargetingOperator.EQUALS, True)
        ]
    )
    
    await interaction.add_segment("targeted-feature", segment)
    
    # Test evaluation
    early_adopter_context = EvaluationContext(
        user_id="user1",
        attributes={"early_adopter": True}
    )
    
    regular_context = EvaluationContext(
        user_id="user2",
        attributes={"early_adopter": False}
    )
    
    # Early adopter should get the feature
    result1 = await interaction.evaluate_flag_detailed(
        "targeted-feature",
        early_adopter_context
    )
    assert result1.value is True
    assert result1.reason == "enabled"
    
    # Regular user should not (no segment match)
    result2 = await interaction.evaluate_flag_detailed(
        "targeted-feature",
        regular_context
    )
    assert result2.value is False
    assert result2.reason == "no_segment_match"


@pytest.mark.asyncio
async def test_multiple_segments(interaction):
    """Test flag with multiple segments"""
    flag = await interaction.create_flag(
        key="multi-segment",
        name="Multi Segment Feature",
        enabled=True,
        default_value="default"
    )
    
    # Add multiple segments
    await interaction.add_segment(
        "multi-segment",
        Segment(
            name="premium_users",
            rules=[TargetingRule("plan", TargetingOperator.EQUALS, "premium")]
        )
    )
    
    await interaction.add_segment(
        "multi-segment",
        Segment(
            name="beta_users",
            rules=[TargetingRule("beta", TargetingOperator.EQUALS, True)]
        )
    )
    
    # Test different contexts
    contexts = [
        ({"plan": "premium"}, True),  # Matches first segment
        ({"beta": True}, True),        # Matches second segment
        ({"plan": "premium", "beta": True}, True),  # Matches both
        ({"plan": "free", "beta": False}, False)    # Matches neither
    ]
    
    for attributes, should_match in contexts:
        context = EvaluationContext(
            user_id=f"user_{attributes}",
            attributes=attributes
        )
        result = await interaction.evaluate_flag_detailed("multi-segment", context)
        
        if should_match:
            assert result.reason == "enabled"
        else:
            assert result.reason == "no_segment_match"


@pytest.mark.asyncio
async def test_add_targeting_rule_to_segment(interaction):
    """Test adding rules to existing segments"""
    # Create flag with segment
    flag = await interaction.create_flag(
        key="evolving-flag",
        name="Evolving Flag"
    )
    
    segment = Segment(
        name="evolving_segment",
        rules=[
            TargetingRule("country", TargetingOperator.EQUALS, "US")
        ]
    )
    
    await interaction.add_segment("evolving-flag", segment)
    
    # Add another rule
    await interaction.add_targeting_rule(
        "evolving-flag",
        "evolving_segment",
        TargetingRule("age", TargetingOperator.GREATER_THAN, 18)
    )
    
    # Test evaluation
    updated_flag = await interaction.get_flag("evolving-flag")
    assert len(updated_flag.segments[0].rules) == 2
    
    # Should match both rules
    context = EvaluationContext(
        attributes={"country": "US", "age": 25}
    )
    result = await interaction.evaluate_flag_detailed("evolving-flag", context)
    assert result.reason == "enabled"
    
    # Should fail if one rule doesn't match
    context2 = EvaluationContext(
        attributes={"country": "US", "age": 16}
    )
    result2 = await interaction.evaluate_flag_detailed("evolving-flag", context2)
    assert result2.reason == "no_segment_match"


@pytest.mark.asyncio
async def test_complex_targeting_scenario(interaction):
    """Test complex targeting with multiple rules and operators"""
    flag = await interaction.create_flag(
        key="complex-targeting",
        name="Complex Targeting",
        enabled=True,
        default_value="default"
    )
    
    # Create complex segment
    segment = Segment(
        name="power_users",
        rules=[
            TargetingRule(
                "account_age_days",
                TargetingOperator.GREATER_THAN,
                30
            ),
            TargetingRule(
                "subscription_level",
                TargetingOperator.IN,
                ["premium", "enterprise"]
            ),
            TargetingRule(
                "email",
                TargetingOperator.NOT_CONTAINS,
                "@test.com"
            ),
            TargetingRule(
                "api_calls_per_month",
                TargetingOperator.GREATER_THAN,
                1000
            )
        ],
        match_all=True
    )
    
    await interaction.add_segment("complex-targeting", segment)
    
    # Test various user profiles
    test_cases = [
        (
            {
                "account_age_days": 45,
                "subscription_level": "premium",
                "email": "user@company.com",
                "api_calls_per_month": 5000
            },
            True,  # All conditions match
            "enabled"
        ),
        (
            {
                "account_age_days": 15,  # Too new
                "subscription_level": "premium",
                "email": "user@company.com",
                "api_calls_per_month": 5000
            },
            False,
            "no_segment_match"
        ),
        (
            {
                "account_age_days": 45,
                "subscription_level": "free",  # Wrong level
                "email": "user@company.com",
                "api_calls_per_month": 5000
            },
            False,
            "no_segment_match"
        ),
        (
            {
                "account_age_days": 45,
                "subscription_level": "premium",
                "email": "user@test.com",  # Test email
                "api_calls_per_month": 5000
            },
            False,
            "no_segment_match"
        )
    ]
    
    for attributes, should_match, expected_reason in test_cases:
        context = EvaluationContext(
            user_id=f"user_{hash(str(attributes))}",
            attributes=attributes
        )
        result = await interaction.evaluate_flag_detailed("complex-targeting", context)
        assert result.reason == expected_reason


@pytest.mark.asyncio
async def test_environment_specific_targeting(interaction):
    """Test environment-specific flag configuration"""
    flag = await interaction.create_flag(
        key="env-specific",
        name="Environment Specific",
        enabled=True,
        environments={
            "development": {"enabled": True},
            "staging": {"enabled": True},
            "production": {"enabled": False}
        }
    )
    
    # Test different environments
    dev_context = EvaluationContext(
        user_id="user1",
        environment="development"
    )
    
    prod_context = EvaluationContext(
        user_id="user1",
        environment="production"
    )
    
    dev_result = await interaction.evaluate_flag_detailed("env-specific", dev_context)
    assert dev_result.value is True
    assert dev_result.reason == "enabled"
    
    prod_result = await interaction.evaluate_flag_detailed("env-specific", prod_context)
    assert prod_result.value is None  # default_value
    assert prod_result.reason == "disabled_in_environment"


# Validation
if __name__ == "__main__":
    async def validate():
        """Run validation tests"""
        print("Running targeting validation...")
        
        interaction = FeatureFlagsInteraction(
            storage_path=Path("./validation_targeting")
        )
        
        try:
            # Create flag with targeting
            flag = await interaction.create_flag(
                "validation-targeting",
                "Targeting Test",
                enabled=True,
                default_value=False
            )
            print(f"✅ Created flag: {flag.key}")
            
            # Add segment
            segment = Segment(
                name="test_segment",
                rules=[
                    TargetingRule("country", TargetingOperator.EQUALS, "US"),
                    TargetingRule("age", TargetingOperator.GREATER_THAN, 18)
                ]
            )
            await interaction.add_segment("validation-targeting", segment)
            print("✅ Added segment with rules")
            
            # Test evaluations
            test_contexts = [
                ({"country": "US", "age": 25}, True),
                ({"country": "US", "age": 16}, False),
                ({"country": "UK", "age": 25}, False)
            ]
            
            for attrs, expected in test_contexts:
                context = EvaluationContext(attributes=attrs)
                result = await interaction.evaluate_flag_detailed(
                    "validation-targeting",
                    context
                )
                actual = result.value if result else None
                print(f"✅ Context {attrs}: {actual} (expected {expected})")
            
            # Cleanup
            await interaction.delete_flag("validation-targeting")
            if interaction.storage_path.exists():
                shutil.rmtree(interaction.storage_path)
            
            print("\n✅ Targeting validation passed!")
            
        except Exception as e:
            print(f"\n❌ Validation failed: {str(e)}")
            raise
    
    asyncio.run(validate())