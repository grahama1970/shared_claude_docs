"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test document synchronization capabilities

Tests real-time document sync, version tracking, and multi-user editing.
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
    Operation,
    OperationType,
    handle_document_sync
)


@pytest.fixture
async def engine():
    """Create test engine instance"""
    engine = CollaborationEngine(storage_dir="./test_collab_data")
    yield engine
    # Cleanup
    import shutil
    if Path("./test_collab_data").exists():
        shutil.rmtree("./test_collab_data")


@pytest.fixture
async def session_with_users(engine):
    """Create session with multiple users"""
    session = await engine.create_session("test_doc", "user1", "Alice")
    await engine.join_session(session.id, "user2", "Bob")
    await engine.join_session(session.id, "user3", "Charlie")
    return session


class TestDocumentSync:
    """Test document synchronization"""
    
    @pytest.mark.asyncio
    async def test_basic_sync(self, engine, session_with_users):
        """Test basic document synchronization"""
        session = session_with_users
        
        # Apply some operations
        op1 = Operation(
            id="op1",
            type=OperationType.INSERT,
            user_id="user1",
            timestamp=time.time(),
            version=0,
            data={"position": 0, "text": "Hello "}
        )
        
        result = await engine.apply_operation(session.id, op1)
        assert result is True
        
        # Get sync status
        sync_data = await handle_document_sync(engine, session.id)
        
        assert sync_data["document"]["content"] == "Hello "
        assert sync_data["document"]["version"] == 1
        assert len(sync_data["users"]) == 3
    
    @pytest.mark.asyncio
    async def test_concurrent_edits(self, engine, session_with_users):
        """Test handling of concurrent edits"""
        session = session_with_users
        
        # Simulate concurrent edits from different users
        operations = [
            Operation(
                id=f"op{i}",
                type=OperationType.INSERT,
                user_id=f"user{(i % 3) + 1}",
                timestamp=time.time() + i * 0.001,
                version=i,
                data={"position": i * 5, "text": f"Text{i} "}
            )
            for i in range(5)
        ]
        
        # Apply all operations
        for op in operations:
            await engine.apply_operation(session.id, op)
        
        # Check final state
        doc = engine.documents[session.document_id]
        assert doc.version == 5
        assert all(f"Text{i}" in doc.content for i in range(5))
    
    @pytest.mark.asyncio
    async def test_version_tracking(self, engine, session_with_users):
        """Test document version tracking"""
        session = session_with_users
        initial_version = engine.documents[session.document_id].version
        
        # Apply operations and track versions
        versions = [initial_version]
        
        for i in range(10):
            op = Operation(
                id=f"version_op_{i}",
                type=OperationType.INSERT,
                user_id="user1",
                timestamp=time.time(),
                version=versions[-1],
                data={"position": 0, "text": f"{i}"}
            )
            
            await engine.apply_operation(session.id, op)
            versions.append(engine.documents[session.document_id].version)
        
        # Verify versions are monotonically increasing
        for i in range(1, len(versions)):
            assert versions[i] == versions[i-1] + 1
    
    @pytest.mark.asyncio
    async def test_sync_with_offline_user(self, engine, session_with_users):
        """Test syncing when user comes back online"""
        session = session_with_users
        
        # User 1 makes changes while user 2 is "offline"
        online_ops = []
        for i in range(3):
            op = Operation(
                id=f"online_op_{i}",
                type=OperationType.INSERT,
                user_id="user1",
                timestamp=time.time(),
                version=i,
                data={"position": 0, "text": f"Online{i} "}
            )
            await engine.apply_operation(session.id, op)
            online_ops.append(op)
        
        # User 2 comes back with offline changes
        offline_changes = [
            {
                "type": "insert",
                "data": {"position": 0, "text": "Offline1 "},
                "timestamp": time.time() - 30,
                "version": 0
            },
            {
                "type": "insert",
                "data": {"position": 8, "text": "Offline2 "},
                "timestamp": time.time() - 20,
                "version": 1
            }
        ]
        
        # Sync offline operations
        synced = await engine.sync_offline_operations(session.id, "user2", offline_changes)
        
        assert len(synced) == 2
        
        # Verify both online and offline changes are present
        doc = engine.documents[session.document_id]
        assert "Online" in doc.content
        assert "Offline" in doc.content
    
    @pytest.mark.asyncio
    async def test_document_persistence(self, engine):
        """Test document persistence across sessions"""
        # Create and modify document
        session1 = await engine.create_session("persist_doc", "user1", "Alice")
        
        op = Operation(
            id="persist_op",
            type=OperationType.INSERT,
            user_id="user1",
            timestamp=time.time(),
            version=0,
            data={"position": 0, "text": "Persistent content"}
        )
        
        await engine.apply_operation(session1.id, op)
        doc_id = session1.document_id
        
        # Save document
        await engine._save_document(engine.documents[doc_id])
        
        # Load document
        loaded_doc = await engine._load_document(doc_id)
        
        assert loaded_doc is not None
        assert loaded_doc.content == "Persistent content"
        assert loaded_doc.version == 1
        assert len(loaded_doc.operations) == 1
    
    @pytest.mark.asyncio
    async def test_real_time_sync_performance(self, engine, session_with_users):
        """Test performance of real-time sync"""
        session = session_with_users
        
        start_time = time.time()
        operation_count = 100
        
        # Rapid fire operations
        tasks = []
        for i in range(operation_count):
            op = Operation(
                id=f"perf_op_{i}",
                type=OperationType.INSERT,
                user_id=f"user{(i % 3) + 1}",
                timestamp=time.time(),
                version=i,
                data={"position": 0, "text": f"{i}"}
            )
            tasks.append(engine.apply_operation(session.id, op))
        
        # Apply all operations concurrently
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # All operations should succeed
        assert all(results)
        
        # Should handle 100 operations in reasonable time
        assert duration < 5.0, f"Sync took too long: {duration}s"
        
        # Verify document integrity
        doc = engine.documents[session.document_id]
        assert doc.version == operation_count
        
        print(f"Synced {operation_count} operations in {duration:.3f}s ({operation_count/duration:.1f} ops/sec)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])