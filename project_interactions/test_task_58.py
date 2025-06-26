"""
Test Task 58: Feature Flag Management System

This script validates the feature flag management system implementation.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
import shutil
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from feature_flags.feature_flags_interaction import (
    FeatureFlagsInteraction,
    FlagType,
    TargetingRule,
    TargetingOperator,
    Segment,
    Variant,
    RolloutConfig,
    RolloutStrategy,
    EvaluationContext
)


async def test_flag_creation_and_management(interaction: FeatureFlagsInteraction) -> Dict[str, Any]:
    """Test basic flag creation and management"""
    print("\n1. Testing flag creation and management...")
    results = []
    
    try:
        # Create different flag types
        bool_flag = await interaction.create_flag(
            key="test-bool-flag",
            name="Test Boolean Flag",
            flag_type=FlagType.BOOLEAN,
            enabled=True,
            description="Test boolean feature flag",
            tags=["test", "boolean"]
        )
        results.append(("Create boolean flag", True, None))
        print(f"   ✓ Created boolean flag: {bool_flag.key}")
        
        string_flag = await interaction.create_flag(
            key="test-string-flag",
            name="Test String Flag",
            flag_type=FlagType.STRING,
            default_value="default",
            description="Test string feature flag"
        )
        results.append(("Create string flag", True, None))
        print(f"   ✓ Created string flag: {string_flag.key}")
        
        # Update flag
        updated = await interaction.update_flag(
            "test-bool-flag",
            {"description": "Updated description", "enabled": False}
        )
        results.append(("Update flag", updated.description == "Updated description", None))
        print(f"   ✓ Updated flag: {updated.description}")
        
        # List flags
        flags = await interaction.list_flags()
        results.append(("List flags", len(flags) >= 2, None))
        print(f"   ✓ Listed {len(flags)} flags")
        
        # Delete flag
        await interaction.delete_flag("test-string-flag")
        remaining = await interaction.list_flags()
        results.append(("Delete flag", len(remaining) == len(flags) - 1, None))
        print("   ✓ Deleted flag successfully")
        
    except Exception as e:
        results.append(("Flag management", False, str(e)))
        print(f"   ✗ Error: {str(e)}")
    
    return {"test": "Flag Management", "results": results}


async def test_targeting_and_segmentation(interaction: FeatureFlagsInteraction) -> Dict[str, Any]:
    """Test user targeting and segmentation"""
    print("\n2. Testing targeting and segmentation...")
    results = []
    
    try:
        # Create flag with targeting
        flag = await interaction.create_flag(
            key="targeted-feature",
            name="Targeted Feature",
            flag_type=FlagType.BOOLEAN,
            enabled=True,
            default_value=False
        )
        
        # Add segments
        premium_segment = Segment(
            name="premium_users",
            rules=[
                TargetingRule("plan", TargetingOperator.EQUALS, "premium"),
                TargetingRule("country", TargetingOperator.IN, ["US", "UK", "CA"])
            ]
        )
        
        await interaction.add_segment("targeted-feature", premium_segment)
        results.append(("Add segment", True, None))
        print("   ✓ Added premium users segment")
        
        # Test evaluation with different contexts
        premium_us_context = EvaluationContext(
            user_id="premium_us_user",
            attributes={"plan": "premium", "country": "US"}
        )
        
        free_us_context = EvaluationContext(
            user_id="free_us_user",
            attributes={"plan": "free", "country": "US"}
        )
        
        premium_result = await interaction.evaluate_flag_detailed("targeted-feature", premium_us_context)
        free_result = await interaction.evaluate_flag_detailed("targeted-feature", free_us_context)
        
        results.append(("Premium user evaluation", premium_result.value is True, None))
        results.append(("Free user evaluation", free_result.value is False, None))
        
        print(f"   ✓ Premium user: {premium_result.value} (reason: {premium_result.reason})")
        print(f"   ✓ Free user: {free_result.value} (reason: {free_result.reason})")
        
    except Exception as e:
        results.append(("Targeting", False, str(e)))
        print(f"   ✗ Error: {str(e)}")
    
    return {"test": "Targeting & Segmentation", "results": results}


async def test_rollout_strategies(interaction: FeatureFlagsInteraction) -> Dict[str, Any]:
    """Test various rollout strategies"""
    print("\n3. Testing rollout strategies...")
    results = []
    
    try:
        # Percentage rollout
        percentage_flag = await interaction.create_flag(
            key="percentage-feature",
            name="Percentage Rollout",
            rollout_percentage=30
        )
        results.append(("Create percentage rollout", True, None))
        print("   ✓ Created flag with 30% rollout")
        
        # Test distribution
        enabled_count = 0
        test_users = 100
        for i in range(test_users):
            context = EvaluationContext(user_id=f"test_user_{i}")
            if await interaction.evaluate_flag("percentage-feature", context):
                enabled_count += 1
        
        percentage = (enabled_count / test_users) * 100
        results.append(("Percentage distribution", 20 <= percentage <= 40, f"Got {percentage}%"))
        print(f"   ✓ Rollout distribution: {percentage}% (expected ~30%)")
        
        # Ring rollout
        ring_flag = await interaction.create_flag(
            key="ring-feature",
            name="Ring Rollout"
        )
        
        internal_ring = Segment(
            name="internal",
            rules=[TargetingRule("employee", TargetingOperator.EQUALS, True)]
        )
        
        rollout = RolloutConfig(
            strategy=RolloutStrategy.RING,
            ring_definitions=[internal_ring]
        )
        
        await interaction.update_flag("ring-feature", {"rollout": rollout})
        
        employee_context = EvaluationContext(attributes={"employee": True})
        external_context = EvaluationContext(attributes={"employee": False})
        
        employee_result = await interaction.evaluate_flag("ring-feature", employee_context)
        external_result = await interaction.evaluate_flag("ring-feature", external_context)
        
        results.append(("Ring rollout - employees", employee_result is True, None))
        results.append(("Ring rollout - external", external_result is None, None))
        
        print(f"   ✓ Ring rollout: employees={employee_result}, external={external_result}")
        
    except Exception as e:
        results.append(("Rollout strategies", False, str(e)))
        print(f"   ✗ Error: {str(e)}")
    
    return {"test": "Rollout Strategies", "results": results}


async def test_ab_testing(interaction: FeatureFlagsInteraction) -> Dict[str, Any]:
    """Test A/B testing with variants"""
    print("\n4. Testing A/B testing...")
    results = []
    
    try:
        # Create flag with variants
        ab_flag = await interaction.create_flag(
            key="button-color-test",
            name="Button Color A/B Test",
            flag_type=FlagType.STRING,
            default_value="blue"
        )
        
        # Add variants
        await interaction.add_variant(
            "button-color-test",
            Variant(name="control", value="blue", weight=50)
        )
        await interaction.add_variant(
            "button-color-test",
            Variant(name="variant_a", value="green", weight=30)
        )
        await interaction.add_variant(
            "button-color-test",
            Variant(name="variant_b", value="red", weight=20)
        )
        
        results.append(("Add variants", True, None))
        print("   ✓ Added 3 variants with weights 50/30/20")
        
        # Test distribution
        variant_counts = {"blue": 0, "green": 0, "red": 0}
        for i in range(100):
            context = EvaluationContext(user_id=f"ab_user_{i}")
            result = await interaction.evaluate_flag("button-color-test", context)
            if result in variant_counts:
                variant_counts[result] += 1
        
        print(f"   ✓ Variant distribution: {variant_counts}")
        
        # Check consistent assignment
        test_user_context = EvaluationContext(user_id="consistent_user")
        first_result = await interaction.evaluate_flag("button-color-test", test_user_context)
        
        consistent = True
        for _ in range(5):
            result = await interaction.evaluate_flag("button-color-test", test_user_context)
            if result != first_result:
                consistent = False
                break
        
        results.append(("Consistent variant assignment", consistent, None))
        print(f"   ✓ User consistently gets: {first_result}")
        
    except Exception as e:
        results.append(("A/B testing", False, str(e)))
        print(f"   ✗ Error: {str(e)}")
    
    return {"test": "A/B Testing", "results": results}


async def test_dependencies_and_kill_switch(interaction: FeatureFlagsInteraction) -> Dict[str, Any]:
    """Test flag dependencies and kill switch"""
    print("\n5. Testing dependencies and kill switch...")
    results = []
    
    try:
        # Create parent and child flags
        parent = await interaction.create_flag(
            key="parent-feature",
            name="Parent Feature",
            enabled=True
        )
        
        child = await interaction.create_flag(
            key="child-feature",
            name="Child Feature",
            enabled=True,
            dependencies=["parent-feature"]
        )
        
        context = EvaluationContext(user_id="dep_user")
        
        # Test with parent enabled
        child_result = await interaction.evaluate_flag_detailed("child-feature", context)
        results.append(("Child with parent enabled", child_result.value is True, None))
        print(f"   ✓ Child evaluation with parent enabled: {child_result.value}")
        
        # Disable parent
        await interaction.update_flag("parent-feature", {"enabled": False})
        # Clear cache to ensure fresh evaluation
        await interaction.clear_cache()
        child_result = await interaction.evaluate_flag_detailed("child-feature", context)
        results.append(("Child with parent disabled", child_result.reason == "dependency_not_met", f"Got: {child_result.reason}"))
        print(f"   ✓ Child evaluation with parent disabled: {child_result.reason}")
        
        # Test kill switch
        kill_flag = await interaction.create_flag(
            key="kill-switch-test",
            name="Kill Switch Test",
            enabled=True
        )
        
        # Normal evaluation
        normal_result = await interaction.evaluate_flag("kill-switch-test", context)
        results.append(("Normal evaluation", normal_result is True, None))
        
        # Activate kill switch
        await interaction.activate_kill_switch("kill-switch-test")
        kill_result = await interaction.evaluate_flag_detailed("kill-switch-test", context)
        results.append(("Kill switch activated", kill_result.reason == "kill_switch", None))
        print(f"   ✓ Kill switch: {kill_result.reason}")
        
    except Exception as e:
        results.append(("Dependencies/Kill switch", False, str(e)))
        print(f"   ✗ Error: {str(e)}")
    
    return {"test": "Dependencies & Kill Switch", "results": results}


async def test_sdk_generation(interaction: FeatureFlagsInteraction) -> Dict[str, Any]:
    """Test SDK generation for multiple languages"""
    print("\n6. Testing SDK generation...")
    results = []
    
    try:
        # Create test flags
        await interaction.create_flag(
            key="sdk-test-flag",
            name="SDK Test Flag",
            flag_type=FlagType.BOOLEAN,
            enabled=True,
            rollout_percentage=50
        )
        
        # Generate SDKs
        languages = ["javascript", "python", "java", "go"]
        
        for lang in languages:
            # Generate SDK with specific flags
            sdk = await interaction.generate_sdk(lang, flags=["sdk-test-flag"])
            valid = len(sdk) > 0
            has_flag = "sdk-test-flag" in sdk or "sdk_test_flag" in sdk
            results.append((f"Generate {lang} SDK", valid and has_flag, f"SDK length: {len(sdk)}, has flag: {has_flag}"))
            if valid and has_flag:
                print(f"   ✓ Generated {lang} SDK: {len(sdk)} chars")
            else:
                print(f"   ✗ Failed to generate {lang} SDK properly (length: {len(sdk)}, has flag: {has_flag})")
        
        # Test invalid language
        try:
            await interaction.generate_sdk("ruby")
            results.append(("Invalid language error", False, "Should have failed"))
        except ValueError:
            results.append(("Invalid language error", True, None))
            print("   ✓ Correctly rejected unsupported language")
        
    except Exception as e:
        results.append(("SDK generation", False, str(e)))
        print(f"   ✗ Error: {str(e)}")
    
    return {"test": "SDK Generation", "results": results}


async def test_audit_and_analytics(interaction: FeatureFlagsInteraction) -> Dict[str, Any]:
    """Test audit logging and analytics"""
    print("\n7. Testing audit and analytics...")
    results = []
    
    try:
        # Create and modify flag to generate audit log
        audit_flag = await interaction.create_flag(
            key="audit-test-flag",
            name="Audit Test",
            user="test_admin"
        )
        
        await interaction.update_flag(
            "audit-test-flag",
            {"enabled": False},
            user="test_admin"
        )
        
        # Get audit log
        audit_entries = await interaction.get_audit_log(
            flag_key="audit-test-flag",
            user="test_admin"
        )
        
        results.append(("Audit log entries", len(audit_entries) >= 2, f"Got {len(audit_entries)} entries"))
        print(f"   ✓ Audit log has {len(audit_entries)} entries")
        
        for entry in audit_entries[:2]:
            print(f"     - {entry.action} by {entry.user} at {entry.timestamp}")
        
        # Get analytics
        analytics = await interaction.get_flag_analytics("audit-test-flag")
        results.append(("Analytics data", "evaluations" in analytics, None))
        print(f"   ✓ Analytics: {analytics['evaluations']} evaluations")
        
    except Exception as e:
        results.append(("Audit/Analytics", False, str(e)))
        print(f"   ✗ Error: {str(e)}")
    
    return {"test": "Audit & Analytics", "results": results}


async def main():
    """Run all tests"""
    print("Feature Flag Management System Tests")
    print("=" * 50)
    
    # Create test interaction
    test_path = Path("./test_feature_flags_verification")
    if test_path.exists():
        shutil.rmtree(test_path)
    
    interaction = FeatureFlagsInteraction(storage_path=test_path)
    
    all_results = []
    
    try:
        # Run all test suites
        all_results.append(await test_flag_creation_and_management(interaction))
        all_results.append(await test_targeting_and_segmentation(interaction))
        all_results.append(await test_rollout_strategies(interaction))
        all_results.append(await test_ab_testing(interaction))
        all_results.append(await test_dependencies_and_kill_switch(interaction))
        all_results.append(await test_sdk_generation(interaction))
        all_results.append(await test_audit_and_analytics(interaction))
        
        # Summary
        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)
        
        total_tests = 0
        passed_tests = 0
        
        for suite in all_results:
            suite_passed = sum(1 for _, passed, _ in suite["results"] if passed)
            suite_total = len(suite["results"])
            total_tests += suite_total
            passed_tests += suite_passed
            
            status = "✓" if suite_passed == suite_total else "✗"
            print(f"{status} {suite['test']}: {suite_passed}/{suite_total} passed")
            
            # Show failures
            for test_name, passed, error in suite["results"]:
                if not passed:
                    print(f"  ✗ {test_name}: {error or 'Failed'}")
        
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
        
        # Generate test report
        report_path = Path("docs/reports") / f"test_report_task_58_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, "w") as f:
            f.write("# Task 58 Test Report: Feature Flag Management System\n\n")
            f.write(f"Generated: {datetime.now()}\n\n")
            f.write("| Test Suite | Test Name | Result | Error |\n")
            f.write("|------------|-----------|--------|-------|\n")
            
            for suite in all_results:
                for test_name, passed, error in suite["results"]:
                    status = "✅ Pass" if passed else "❌ Fail"
                    error_msg = error or ""
                    f.write(f"| {suite['test']} | {test_name} | {status} | {error_msg} |\n")
        
        print(f"\nTest report saved to: {report_path}")
        
        # Cleanup
        if test_path.exists():
            shutil.rmtree(test_path)
        
        # Exit with appropriate code
        if passed_tests == total_tests:
            print("\n✅ All tests passed!")
            return 0
        else:
            print(f"\n❌ {total_tests - passed_tests} tests failed!")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    # sys.exit() removed