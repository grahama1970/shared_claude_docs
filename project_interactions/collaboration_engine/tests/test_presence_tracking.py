"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test presence tracking and awareness features

Tests user presence, cursor tracking, selections, and activity monitoring.
"""

import pytest
import asyncio
import time
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from collaboration_engine_interaction import (
    CollaborationEngine,
    User,
    track_presence
)


@pytest.fixture
async def engine():
    """Create test engine instance"""
    engine = CollaborationEngine(storage_dir="./test_presence_data")
    yield engine
    # Cleanup
    import shutil
    if Path("./test_presence_data").exists():
        shutil.rmtree("./test_presence_data")


@pytest.fixture
async def multi_user_session(engine):
    """Create session with multiple active users"""
    session = await engine.create_session("presence_doc", "user1", "Alice")
    
    # Add more users
    users = [
        ("user2", "Bob"),
        ("user3", "Charlie"),
        ("user4", "Diana"),
        ("user5", "Eve")
    ]
    
    for user_id, name in users:
        await engine.join_session(session.id, user_id, name)
    
    return session


class TestPresenceTracking:
    """Test presence tracking features"""
    
    @pytest.mark.asyncio
    async def test_user_join_leave(self, engine):
        """Test user join and leave tracking"""
        # Create session
        session = await engine.create_session("test_doc", "user1", "Alice")
        assert len(session.users) == 1
        
        # User joins
        result = await engine.join_session(session.id, "user2", "Bob")
        assert result is not None
        assert len(session.users) == 2
        
        # Same user can't join twice
        result = await engine.join_session(session.id, "user2", "Bob")
        assert result is None
        
        # User leaves
        result = await engine.leave_session(session.id, "user2")
        assert result is True
        assert len(session.users) == 1
        
        # Can't leave if not in session
        result = await engine.leave_session(session.id, "user3")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_cursor_tracking(self, engine, multi_user_session):
        """Test cursor position tracking"""
        session = multi_user_session
        
        # Update cursor positions
        positions = [
            ("user1", 0),
            ("user2", 10),
            ("user3", 20),
            ("user4", 30),
            ("user5", 40)
        ]
        
        for user_id, pos in positions:
            result = await engine.update_cursor(session.id, user_id, pos)
            assert result is True
        
        # Verify cursor positions
        for user_id, expected_pos in positions:
            user = session.users[user_id]
            assert user.cursor_pos == expected_pos
    
    @pytest.mark.asyncio
    async def test_selection_tracking(self, engine, multi_user_session):
        """Test selection tracking"""
        session = multi_user_session
        
        # Update selections
        selections = [
            ("user1", 0, 10),
            ("user2", 5, 15),
            ("user3", 20, 25),
            ("user4", 30, 40),
        ]
        
        for user_id, start, end in selections:
            result = await engine.update_selection(session.id, user_id, start, end)
            assert result is True
        
        # Verify selections
        for user_id, expected_start, expected_end in selections:
            user = session.users[user_id]
            assert user.selection_start == expected_start
            assert user.selection_end == expected_end
    
    @pytest.mark.asyncio
    async def test_active_user_detection(self, engine, multi_user_session):
        """Test detection of active vs inactive users"""
        session = multi_user_session
        
        # All users should be active initially
        active_users = session.get_active_users()
        assert len(active_users) == 5
        
        # Simulate some users going inactive
        for user_id in ["user3", "user4"]:
            user = session.users[user_id]
            user.last_seen = time.time() - 60  # 60 seconds ago
        
        # Check active users
        active_users = session.get_active_users()
        assert len(active_users) == 3
        
        # Verify correct users are active
        active_ids = {u.id for u in active_users}
        assert "user1" in active_ids
        assert "user2" in active_ids
        assert "user5" in active_ids
        assert "user3" not in active_ids
        assert "user4" not in active_ids
    
    @pytest.mark.asyncio
    async def test_presence_api(self, engine, multi_user_session):
        """Test the presence tracking API"""
        session = multi_user_session
        
        # Set up some cursor positions and selections
        await engine.update_cursor(session.id, "user1", 10)
        await engine.update_selection(session.id, "user1", 0, 10)
        
        await engine.update_cursor(session.id, "user2", 25)
        await engine.update_selection(session.id, "user2", 20, 30)
        
        # Get presence data
        presence_data = await track_presence(engine, session.id)
        
        assert len(presence_data) == 5
        
        # Check user1 data
        user1_data = next(p for p in presence_data if p["user_id"] == "user1")
        assert user1_data["name"] == "Alice"
        assert user1_data["cursor_pos"] == 10
        assert user1_data["selection"]["start"] == 0
        assert user1_data["selection"]["end"] == 10
        assert user1_data["active"] is True
    
    @pytest.mark.asyncio
    async def test_user_colors(self, engine):
        """Test consistent user color generation"""
        # Colors should be consistent for same user ID
        color1 = engine._generate_user_color("test_user")
        color2 = engine._generate_user_color("test_user")
        assert color1 == color2
        
        # Different users should get different colors
        colors = set()
        for i in range(10):
            color = engine._generate_user_color(f"user_{i}")
            colors.add(color)
        
        # Should generate different colors for different users
        assert len(colors) == 10
        
        # Colors should be in HSL format
        for color in colors:
            assert color.startswith("hsl(")
            assert color.endswith(")")
    
    @pytest.mark.asyncio
    async def test_presence_with_permissions(self, engine):
        """Test presence tracking with user permissions"""
        session = await engine.create_session("perm_doc", "admin", "Admin")
        
        # Add users with different permissions
        user_read = User(
            id="reader",
            name="Reader",
            color=engine._generate_user_color("reader"),
            permissions={"read"}
        )
        session.add_user(user_read)
        
        user_write = User(
            id="writer",
            name="Writer",
            color=engine._generate_user_color("writer"),
            permissions={"read", "write"}
        )
        session.add_user(user_write)
        
        # Verify permissions are tracked
        assert "write" not in session.users["reader"].permissions
        assert "write" in session.users["writer"].permissions
    
    @pytest.mark.asyncio
    async def test_presence_updates_on_activity(self, engine, multi_user_session):
        """Test that user activity updates presence"""
        session = multi_user_session
        
        # Get initial last_seen time
        user = session.users["user1"]
        initial_time = user.last_seen
        
        # Wait a bit
        await asyncio.sleep(0.1)
        
        # User activity should update last_seen
        await engine.update_cursor(session.id, "user1", 50)
        
        # Verify last_seen was updated
        assert user.last_seen > initial_time
    
    @pytest.mark.asyncio
    async def test_session_cleanup(self, engine):
        """Test that empty sessions are cleaned up"""
        # Create session
        session = await engine.create_session("cleanup_doc", "user1", "Alice")
        session_id = session.id
        
        # Session should exist
        assert session_id in engine.sessions
        
        # Last user leaves
        await engine.leave_session(session_id, "user1")
        
        # Session should be cleaned up
        assert session_id not in engine.sessions
    
    @pytest.mark.asyncio
    async def test_concurrent_presence_updates(self, engine, multi_user_session):
        """Test handling of concurrent presence updates"""
        session = multi_user_session
        
        # Simulate rapid concurrent updates
        tasks = []
        
        for i in range(100):
            user_id = f"user{(i % 5) + 1}"
            if i % 3 == 0:
                # Cursor update
                tasks.append(engine.update_cursor(session.id, user_id, i))
            elif i % 3 == 1:
                # Selection update
                tasks.append(engine.update_selection(session.id, user_id, i, i + 10))
            else:
                # Mixed update
                tasks.append(engine.update_cursor(session.id, user_id, i))
                tasks.append(engine.update_selection(session.id, user_id, i - 5, i + 5))
        
        # Execute all updates concurrently
        results = await asyncio.gather(*tasks)
        
        # All updates should succeed
        assert all(results)
        
        # Verify final state is consistent
        presence_data = await track_presence(engine, session.id)
        assert len(presence_data) == 5
        
        # Each user should have valid data
        for user_data in presence_data:
            assert user_data["cursor_pos"] >= 0
            if user_data["selection"]:
                assert user_data["selection"]["start"] <= user_data["selection"]["end"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])