"""
Tests for feature flag management functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Expected Usage:
>>> pytest test_flag_management.py -v
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
from datetime import datetime, timezone
from pathlib import Path
import shutil
from typing import List

from feature_flags_interaction import (
    FeatureFlagsInteraction,
    FeatureFlag,
    FlagType,
    RolloutConfig,
    RolloutStrategy,
    Variant
)


@pytest.fixture
async def interaction():
    """Create test interaction with temporary storage"""
    test_path = Path("./test_feature_flags_data")
    if test_path.exists():
        shutil.rmtree(test_path)
    
    interaction = FeatureFlagsInteraction(storage_path=test_path)
    yield interaction
    
    # Cleanup
    if test_path.exists():
        shutil.rmtree(test_path)


@pytest.mark.asyncio
async def test_create_flag(interaction):
    """Test creating a feature flag"""
    flag = await interaction.create_flag(
        key="test-flag",
        name="Test Flag",
        flag_type=FlagType.BOOLEAN,
        enabled=True,
        description="Test description",
        tags=["test", "demo"]
    )
    
    assert flag.key == "test-flag"
    assert flag.name == "Test Flag"
    assert flag.flag_type == FlagType.BOOLEAN
    assert flag.enabled is True
    assert flag.description == "Test description"
    assert "test" in flag.tags
    assert "demo" in flag.tags


@pytest.mark.asyncio
async def test_create_flag_with_rollout(interaction):
    """Test creating flag with rollout percentage"""
    flag = await interaction.create_flag(
        key="rollout-flag",
        name="Rollout Flag",
        rollout_percentage=25.5
    )
    
    assert flag.rollout is not None
    assert flag.rollout.strategy == RolloutStrategy.PERCENTAGE
    assert flag.rollout.percentage == 25.5


@pytest.mark.asyncio
async def test_create_duplicate_flag(interaction):
    """Test creating duplicate flag fails"""
    await interaction.create_flag(
        key="duplicate",
        name="First Flag"
    )
    
    with pytest.raises(ValueError, match="already exists"):
        await interaction.create_flag(
            key="duplicate",
            name="Second Flag"
        )


@pytest.mark.asyncio
async def test_update_flag(interaction):
    """Test updating a flag"""
    flag = await interaction.create_flag(
        key="update-test",
        name="Original Name",
        enabled=True
    )
    
    updated = await interaction.update_flag(
        "update-test",
        {
            "name": "Updated Name",
            "enabled": False,
            "description": "New description"
        }
    )
    
    assert updated.name == "Updated Name"
    assert updated.enabled is False
    assert updated.description == "New description"
    assert updated.updated_at > flag.created_at


@pytest.mark.asyncio
async def test_update_nonexistent_flag(interaction):
    """Test updating non-existent flag fails"""
    with pytest.raises(ValueError, match="not found"):
        await interaction.update_flag("missing", {"enabled": False})


@pytest.mark.asyncio
async def test_delete_flag(interaction):
    """Test deleting a flag"""
    await interaction.create_flag(
        key="delete-test",
        name="To Delete"
    )
    
    await interaction.delete_flag("delete-test")
    
    # Verify flag is gone
    flag = await interaction.get_flag("delete-test")
    assert flag is None


@pytest.mark.asyncio
async def test_delete_nonexistent_flag(interaction):
    """Test deleting non-existent flag fails"""
    with pytest.raises(ValueError, match="not found"):
        await interaction.delete_flag("missing")


@pytest.mark.asyncio
async def test_get_flag(interaction):
    """Test retrieving a flag"""
    created = await interaction.create_flag(
        key="get-test",
        name="Get Test",
        flag_type=FlagType.STRING,
        default_value="hello"
    )
    
    retrieved = await interaction.get_flag("get-test")
    
    assert retrieved is not None
    assert retrieved.key == created.key
    assert retrieved.name == created.name
    assert retrieved.flag_type == created.flag_type
    assert retrieved.default_value == created.default_value


@pytest.mark.asyncio
async def test_get_nonexistent_flag(interaction):
    """Test retrieving non-existent flag returns None"""
    flag = await interaction.get_flag("missing")
    assert flag is None


@pytest.mark.asyncio
async def test_list_flags(interaction):
    """Test listing all flags"""
    # Create test flags
    await interaction.create_flag("flag1", "Flag 1", tags=["production"])
    await interaction.create_flag("flag2", "Flag 2", tags=["test"])
    await interaction.create_flag("flag3", "Flag 3", tags=["production", "test"])
    
    # List all flags
    all_flags = await interaction.list_flags()
    assert len(all_flags) == 3
    
    # List by tag
    prod_flags = await interaction.list_flags(tags=["production"])
    assert len(prod_flags) == 2
    
    test_flags = await interaction.list_flags(tags=["test"])
    assert len(test_flags) == 2


@pytest.mark.asyncio
async def test_flag_caching(interaction):
    """Test flag caching mechanism"""
    # Create flag
    await interaction.create_flag("cache-test", "Cache Test")
    
    # First get should load from storage
    flag1 = await interaction.get_flag("cache-test")
    assert flag1 is not None
    
    # Second get should use cache
    flag2 = await interaction.get_flag("cache-test")
    assert flag2 is not None
    assert flag1.created_at == flag2.created_at
    
    # Update should invalidate cache
    await interaction.update_flag("cache-test", {"name": "Updated"})
    
    # Next get should reflect update
    flag3 = await interaction.get_flag("cache-test")
    assert flag3.name == "Updated"


@pytest.mark.asyncio
async def test_add_variant(interaction):
    """Test adding variants for A/B testing"""
    flag = await interaction.create_flag(
        key="ab-test",
        name="A/B Test",
        flag_type=FlagType.STRING,
        default_value="control"
    )
    
    # Add variants
    await interaction.add_variant(
        "ab-test",
        Variant(name="variant_a", value="red", weight=30)
    )
    await interaction.add_variant(
        "ab-test",
        Variant(name="variant_b", value="blue", weight=20)
    )
    
    updated = await interaction.get_flag("ab-test")
    assert len(updated.variants) == 2
    assert updated.variants[0].name == "variant_a"
    assert updated.variants[0].value == "red"
    assert updated.variants[1].name == "variant_b"
    assert updated.variants[1].value == "blue"


@pytest.mark.asyncio
async def test_kill_switch(interaction):
    """Test emergency kill switch"""
    flag = await interaction.create_flag(
        key="kill-test",
        name="Kill Switch Test",
        enabled=True
    )
    
    # Activate kill switch
    updated = await interaction.activate_kill_switch("kill-test")
    assert updated.kill_switch is True
    
    # Deactivate kill switch
    updated = await interaction.deactivate_kill_switch("kill-test")
    assert updated.kill_switch is False


@pytest.mark.asyncio
async def test_emergency_disable_all(interaction):
    """Test emergency disable all flags"""
    # Create multiple flags
    await interaction.create_flag("emergency1", "Emergency 1", enabled=True)
    await interaction.create_flag("emergency2", "Emergency 2", enabled=True)
    await interaction.create_flag("emergency3", "Emergency 3", enabled=True)
    
    # Emergency disable
    disabled = await interaction.emergency_disable_all()
    assert len(disabled) == 3
    
    # Verify all are disabled
    for key in disabled:
        flag = await interaction.get_flag(key)
        assert flag.enabled is False


@pytest.mark.asyncio
async def test_audit_log(interaction):
    """Test audit logging"""
    # Create and modify flag
    await interaction.create_flag("audit-test", "Audit Test", user="test_user")
    await interaction.update_flag("audit-test", {"enabled": False}, user="admin")
    await interaction.delete_flag("audit-test", user="admin")
    
    # Get audit log
    entries = await interaction.get_audit_log()
    assert len(entries) >= 3
    
    # Check latest entry (delete)
    latest = entries[0]
    assert latest.flag_key == "audit-test"
    assert latest.action == "delete"
    assert latest.user == "admin"
    
    # Filter by flag
    flag_entries = await interaction.get_audit_log(flag_key="audit-test")
    assert all(e.flag_key == "audit-test" for e in flag_entries)
    
    # Filter by user
    user_entries = await interaction.get_audit_log(user="admin")
    assert all(e.user == "admin" for e in user_entries)


@pytest.mark.asyncio
async def test_webhook_management(interaction):
    """Test webhook management"""
    webhook_url = "https://example.com/webhook"
    
    # Add webhook
    await interaction.add_webhook(webhook_url)
    assert webhook_url in interaction.webhooks
    
    # Add duplicate (should not duplicate)
    await interaction.add_webhook(webhook_url)
    assert interaction.webhooks.count(webhook_url) == 1
    
    # Remove webhook
    await interaction.remove_webhook(webhook_url)
    assert webhook_url not in interaction.webhooks


@pytest.mark.asyncio
async def test_clear_cache(interaction):
    """Test clearing all caches"""
    # Create and access flags to populate cache
    await interaction.create_flag("cache1", "Cache 1")
    await interaction.create_flag("cache2", "Cache 2")
    
    await interaction.get_flag("cache1")
    await interaction.get_flag("cache2")
    
    # Verify cache is populated
    assert len(interaction.cache) == 2
    
    # Clear cache
    await interaction.clear_cache()
    
    # Verify cache is empty
    assert len(interaction.cache) == 0
    assert len(interaction._evaluation_cache) == 0


# Validation
if __name__ == "__main__":
    async def validate():
        """Run validation tests"""
        print("Running flag management validation...")
        
        interaction = FeatureFlagsInteraction(
            storage_path=Path("./validation_feature_flags")
        )
        
        try:
            # Create various flag types
            bool_flag = await interaction.create_flag(
                "validation-bool",
                "Boolean Flag",
                FlagType.BOOLEAN,
                enabled=True
            )
            print(f"✅ Created boolean flag: {bool_flag.key}")
            
            string_flag = await interaction.create_flag(
                "validation-string",
                "String Flag",
                FlagType.STRING,
                default_value="default"
            )
            print(f"✅ Created string flag: {string_flag.key}")
            
            # Update flag
            updated = await interaction.update_flag(
                "validation-bool",
                {"description": "Updated description"}
            )
            print(f"✅ Updated flag: {updated.description}")
            
            # List flags
            flags = await interaction.list_flags()
            print(f"✅ Listed {len(flags)} flags")
            
            # Cleanup
            await interaction.delete_flag("validation-bool")
            await interaction.delete_flag("validation-string")
            print("✅ Cleaned up test flags")
            
            # Cleanup storage
            if interaction.storage_path.exists():
                shutil.rmtree(interaction.storage_path)
            
            print("\n✅ Flag management validation passed!")
            
        except Exception as e:
            print(f"\n❌ Validation failed: {str(e)}")
            raise
    
    asyncio.run(validate())