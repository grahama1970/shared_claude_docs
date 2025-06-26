"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test conflict resolution and operational transformation

Tests the system's ability to handle concurrent edits and resolve conflicts.
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
    OperationalTransform,
    resolve_conflicts
)


@pytest.fixture
async def engine():
    """Create test engine instance"""
    engine = CollaborationEngine(storage_dir="./test_conflict_data")
    yield engine
    # Cleanup
    import shutil
    if Path("./test_conflict_data").exists():
        shutil.rmtree("./test_conflict_data")


@pytest.fixture
async def session_with_document(engine):
    """Create session with initial document content"""
    session = await engine.create_session("conflict_doc", "user1", "Alice")
    
    # Add initial content
    op = Operation(
        id="init",
        type=OperationType.INSERT,
        user_id="user1",
        timestamp=time.time(),
        version=0,
        data={"position": 0, "text": "The quick brown fox jumps over the lazy dog."}
    )
    await engine.apply_operation(session.id, op)
    
    # Add second user
    await engine.join_session(session.id, "user2", "Bob")
    
    return session


class TestConflictResolution:
    """Test conflict resolution mechanisms"""
    
    @pytest.mark.asyncio
    async def test_insert_insert_transform(self, engine):
        """Test transformation of concurrent inserts"""
        # Create two concurrent insert operations
        op1 = Operation(
            id="op1",
            type=OperationType.INSERT,
            user_id="user1",
            timestamp=100.0,
            version=1,
            data={"position": 5, "text": "AAA"}
        )
        
        op2 = Operation(
            id="op2",
            type=OperationType.INSERT,
            user_id="user2",
            timestamp=100.1,
            version=1,
            data={"position": 5, "text": "BBB"}
        )
        
        # Transform operations
        op1_prime, op2_prime = OperationalTransform.transform(op1, op2)
        
        # First operation should remain at position 5
        assert op1_prime.data["position"] == 5
        # Second operation should be shifted by length of first
        assert op2_prime.data["position"] == 8  # 5 + len("AAA")
    
    @pytest.mark.asyncio
    async def test_delete_delete_transform(self, engine):
        """Test transformation of concurrent deletes"""
        # Non-overlapping deletes
        op1 = Operation(
            id="op1",
            type=OperationType.DELETE,
            user_id="user1",
            timestamp=100.0,
            version=1,
            data={"start": 0, "end": 5}
        )
        
        op2 = Operation(
            id="op2",
            type=OperationType.DELETE,
            user_id="user2",
            timestamp=100.1,
            version=1,
            data={"start": 10, "end": 15}
        )
        
        op1_prime, op2_prime = OperationalTransform.transform(op1, op2)
        
        # First delete should remain unchanged
        assert op1_prime.data["start"] == 0
        assert op1_prime.data["end"] == 5
        
        # Second delete should be shifted
        assert op2_prime.data["start"] == 5  # 10 - 5
        assert op2_prime.data["end"] == 10   # 15 - 5
    
    @pytest.mark.asyncio
    async def test_concurrent_edits_same_position(self, engine, session_with_document):
        """Test handling of edits at the same position"""
        session = session_with_document
        base_version = engine.documents[session.document_id].version
        
        # Two users try to insert at the same position
        op1 = Operation(
            id="same_pos_1",
            type=OperationType.INSERT,
            user_id="user1",
            timestamp=time.time(),
            version=base_version,
            data={"position": 4, "text": " very"}
        )
        
        op2 = Operation(
            id="same_pos_2",
            type=OperationType.INSERT,
            user_id="user2",
            timestamp=time.time() + 0.001,
            version=base_version,
            data={"position": 4, "text": " really"}
        )
        
        # Apply both operations
        await engine.apply_operation(session.id, op1)
        await engine.apply_operation(session.id, op2)
        
        # Both insertions should be present
        doc = engine.documents[session.document_id]
        assert " very" in doc.content
        assert " really" in doc.content
        
        # They should be in timestamp order
        assert doc.content.index(" very") < doc.content.index(" really")
    
    @pytest.mark.asyncio
    async def test_overlapping_deletes(self, engine, session_with_document):
        """Test handling of overlapping delete operations"""
        session = session_with_document
        
        # Set up some content
        initial_content = engine.documents[session.document_id].content
        
        # Create overlapping deletes
        op1 = Operation(
            id="overlap_del_1",
            type=OperationType.DELETE,
            user_id="user1",
            timestamp=time.time(),
            version=engine.documents[session.document_id].version,
            data={"start": 4, "end": 15}  # "quick brown"
        )
        
        op2 = Operation(
            id="overlap_del_2",
            type=OperationType.DELETE,
            user_id="user2",
            timestamp=time.time() + 0.001,
            version=engine.documents[session.document_id].version,
            data={"start": 10, "end": 20}  # "brown fox j"
        )
        
        # Apply first delete
        await engine.apply_operation(session.id, op1)
        
        # Apply second delete - should be transformed
        await engine.apply_operation(session.id, op2)
        
        # Check that overlapping content is handled correctly
        doc = engine.documents[session.document_id]
        assert "quick" not in doc.content
        assert "brown" not in doc.content
    
    @pytest.mark.asyncio
    async def test_merge_conflicts_api(self, engine, session_with_document):
        """Test the merge conflicts API"""
        session = session_with_document
        base_version = engine.documents[session.document_id].version
        
        # Simulate some server-side changes
        server_op = Operation(
            id="server_op",
            type=OperationType.INSERT,
            user_id="user1",
            timestamp=time.time(),
            version=base_version,
            data={"position": 0, "text": "SERVER: "}
        )
        await engine.apply_operation(session.id, server_op)
        
        # Client sends changes based on old version
        client_changes = [
            {
                "type": "insert",
                "user_id": "user2",
                "data": {"position": 0, "text": "CLIENT: "}
            },
            {
                "type": "delete",
                "user_id": "user2",
                "data": {"start": 10, "end": 15}
            }
        ]
        
        # Resolve conflicts
        result = await resolve_conflicts(engine, session.id, base_version, client_changes)
        
        assert result["success"] is True
        assert len(result["merged"]) > 0
        # First insert should conflict (same position)
        # Delete might be transformed
    
    @pytest.mark.asyncio
    async def test_complex_conflict_scenario(self, engine):
        """Test complex multi-user editing scenario"""
        # Create collaborative document
        session = await engine.create_session("complex_doc", "user1", "Alice")
        await engine.join_session(session.id, "user2", "Bob")
        await engine.join_session(session.id, "user3", "Charlie")
        
        # Initial content
        await engine.apply_operation(session.id, Operation(
            id="init",
            type=OperationType.INSERT,
            user_id="user1",
            timestamp=time.time(),
            version=0,
            data={"position": 0, "text": "The quick brown fox"}
        ))
        
        base_version = engine.documents[session.document_id].version
        
        # Simulate concurrent edits from all users
        operations = [
            # User 1: Insert at beginning
            Operation(
                id="u1_op1",
                type=OperationType.INSERT,
                user_id="user1",
                timestamp=time.time(),
                version=base_version,
                data={"position": 0, "text": "START: "}
            ),
            # User 2: Insert in middle
            Operation(
                id="u2_op1",
                type=OperationType.INSERT,
                user_id="user2",
                timestamp=time.time() + 0.001,
                version=base_version,
                data={"position": 10, "text": " very"}
            ),
            # User 3: Delete some text
            Operation(
                id="u3_op1",
                type=OperationType.DELETE,
                user_id="user3",
                timestamp=time.time() + 0.002,
                version=base_version,
                data={"start": 4, "end": 9}  # "quick"
            ),
            # User 1: Another insert
            Operation(
                id="u1_op2",
                type=OperationType.INSERT,
                user_id="user1",
                timestamp=time.time() + 0.003,
                version=base_version,
                data={"position": 19, "text": " jumps"}
            ),
        ]
        
        # Apply all operations
        for op in operations:
            await engine.apply_operation(session.id, op)
        
        # Verify document integrity
        doc = engine.documents[session.document_id]
        assert doc.content != ""  # Should have content
        assert doc.version > base_version  # Version should increase
        
        # Check that operations were transformed correctly
        assert "START:" in doc.content  # User 1's first insert
        # "quick" should be deleted by User 3
        assert "quick" not in doc.content or doc.content.count("quick") < operations[0].data["text"].count("quick")
    
    @pytest.mark.asyncio
    async def test_offline_conflict_resolution(self, engine, session_with_document):
        """Test resolving conflicts from offline edits"""
        session = session_with_document
        doc_version_before = engine.documents[session.document_id].version
        
        # Online user makes changes
        online_ops = []
        for i in range(3):
            op = Operation(
                id=f"online_{i}",
                type=OperationType.INSERT,
                user_id="user1",
                timestamp=time.time() + i,
                version=doc_version_before + i,
                data={"position": 0, "text": f"[Online{i}] "}
            )
            await engine.apply_operation(session.id, op)
            online_ops.append(op)
        
        # Offline user comes back with conflicting changes
        offline_changes = [
            {
                "type": "insert",
                "data": {"position": 0, "text": "[Offline1] "},
                "version": doc_version_before
            },
            {
                "type": "insert",
                "data": {"position": 10, "text": "[Offline2] "},
                "version": doc_version_before + 1
            }
        ]
        
        # Resolve conflicts
        result = await resolve_conflicts(
            engine,
            session.id,
            doc_version_before,
            offline_changes
        )
        
        assert result["success"] is True
        
        # Apply merged changes
        for merged_op in result["merged"]:
            op = Operation(
                id=merged_op["id"],
                type=OperationType(merged_op["type"]),
                user_id="user2",
                timestamp=merged_op["timestamp"],
                version=merged_op["version"],
                data=merged_op["data"]
            )
            await engine.apply_operation(session.id, op)
        
        # Verify both online and offline changes are present
        doc = engine.documents[session.document_id]
        assert "[Online" in doc.content
        assert "[Offline" in doc.content
    
    @pytest.mark.asyncio
    async def test_performance_under_conflicts(self, engine):
        """Test system performance with many conflicts"""
        session = await engine.create_session("perf_doc", "user1", "Alice")
        
        # Create many concurrent users
        for i in range(10):
            await engine.join_session(session.id, f"user{i+2}", f"User{i+2}")
        
        # Generate many concurrent operations
        start_time = time.time()
        tasks = []
        
        for i in range(100):
            op = Operation(
                id=f"perf_{i}",
                type=OperationType.INSERT if i % 2 == 0 else OperationType.DELETE,
                user_id=f"user{(i % 10) + 1}",
                timestamp=time.time() + (i * 0.0001),
                version=0,  # All based on version 0 - maximum conflicts
                data={
                    "position": i % 20, "text": f"X{i}"
                } if i % 2 == 0 else {
                    "start": i % 10, "end": (i % 10) + 1
                }
            )
            tasks.append(engine.apply_operation(session.id, op))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        # Count successful operations
        successful = sum(1 for r in results if r is True)
        
        print(f"Processed {successful}/{len(tasks)} operations with conflicts in {end_time - start_time:.3f}s")
        
        # At least some operations should succeed
        assert successful > 0
        
        # Should complete in reasonable time even with conflicts
        assert end_time - start_time < 10.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])