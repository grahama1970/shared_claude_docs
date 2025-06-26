"""
Module: test_schema_migration.py
Purpose: Test schema migration capabilities

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest test_schema_migration.py -v
... All tests pass
"""

import asyncio
import sys
from pathlib import Path
import pytest
from datetime import datetime
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_migration_orchestrator_interaction import (
    DatabaseMigrationOrchestrator,
    DatabaseType,
    MigrationType,
    MigrationStatus,
    Migration,
    MigrationOperation
)


@pytest.fixture
def orchestrator():
    """Create migration orchestrator fixture"""
    return DatabaseMigrationOrchestrator()


@pytest.mark.asyncio
async def test_create_schema_migration(orchestrator):
    """Test creating schema migration"""
    migration = orchestrator.create_migration(
        "create_users_table",
        DatabaseType.POSTGRESQL
    )
    
    assert migration.name == "create_users_table"
    assert migration.database_type == DatabaseType.POSTGRESQL
    assert len(migration.operations) == 0
    assert migration.id in orchestrator.migrations


@pytest.mark.asyncio
async def test_add_schema_operations(orchestrator):
    """Test adding schema operations to migration"""
    migration = orchestrator.create_migration(
        "update_schema",
        DatabaseType.POSTGRESQL
    )
    
    # Add CREATE TABLE operation
    op1 = orchestrator.add_operation(
        migration,
        MigrationType.SCHEMA,
        sql="CREATE TABLE products (id SERIAL PRIMARY KEY, name TEXT)",
        rollback_sql="DROP TABLE products"
    )
    
    # Add ALTER TABLE operation
    op2 = orchestrator.add_operation(
        migration,
        MigrationType.SCHEMA,
        sql="ALTER TABLE products ADD COLUMN price DECIMAL(10,2)",
        rollback_sql="ALTER TABLE products DROP COLUMN price"
    )
    
    assert len(migration.operations) == 2
    assert op1.type == MigrationType.SCHEMA
    assert op2.sql == "ALTER TABLE products ADD COLUMN price DECIMAL(10,2)"
    assert migration.checksum is not None


@pytest.mark.asyncio
async def test_execute_schema_migration_dry_run(orchestrator):
    """Test dry run of schema migration"""
    migration = orchestrator.create_migration(
        "test_dry_run",
        DatabaseType.POSTGRESQL
    )
    
    orchestrator.add_operation(
        migration,
        MigrationType.SCHEMA,
        sql="CREATE TABLE test (id INT)",
        rollback_sql="DROP TABLE test"
    )
    
    result = await orchestrator.execute_migration(migration, dry_run=True)
    
    assert result["status"] == "completed"
    assert result["operations"] == 1
    assert len(result["errors"]) == 0


@pytest.mark.asyncio
async def test_schema_migration_with_dependencies(orchestrator):
    """Test schema migration with dependencies"""
    # Create base migration
    base_migration = orchestrator.create_migration(
        "create_base_tables",
        DatabaseType.POSTGRESQL
    )
    
    orchestrator.add_operation(
        base_migration,
        MigrationType.SCHEMA,
        sql="CREATE TABLE categories (id SERIAL PRIMARY KEY, name TEXT)"
    )
    
    # Create dependent migration
    dependent_migration = orchestrator.create_migration(
        "create_dependent_tables",
        DatabaseType.POSTGRESQL
    )
    dependent_migration.dependencies.append(base_migration.id)
    
    orchestrator.add_operation(
        dependent_migration,
        MigrationType.SCHEMA,
        sql="CREATE TABLE items (id SERIAL PRIMARY KEY, category_id INT REFERENCES categories(id))"
    )
    
    assert len(dependent_migration.dependencies) == 1
    assert base_migration.id in dependent_migration.dependencies


@pytest.mark.asyncio
async def test_index_operations(orchestrator):
    """Test index creation operations"""
    migration = orchestrator.create_migration(
        "add_indexes",
        DatabaseType.POSTGRESQL
    )
    
    # Add multiple index operations
    orchestrator.add_operation(
        migration,
        MigrationType.INDEX,
        sql="CREATE INDEX idx_users_email ON users(email)",
        rollback_sql="DROP INDEX idx_users_email"
    )
    
    orchestrator.add_operation(
        migration,
        MigrationType.INDEX,
        sql="CREATE UNIQUE INDEX idx_users_username ON users(username)",
        rollback_sql="DROP INDEX idx_users_username"
    )
    
    result = await orchestrator.execute_migration(migration)
    
    assert result["status"] == "completed"
    assert result["operations"] == 2


@pytest.mark.asyncio
async def test_constraint_operations(orchestrator):
    """Test constraint operations"""
    migration = orchestrator.create_migration(
        "add_constraints",
        DatabaseType.POSTGRESQL
    )
    
    orchestrator.add_operation(
        migration,
        MigrationType.CONSTRAINT,
        sql="ALTER TABLE orders ADD CONSTRAINT check_amount CHECK (amount > 0)",
        rollback_sql="ALTER TABLE orders DROP CONSTRAINT check_amount"
    )
    
    orchestrator.add_operation(
        migration,
        MigrationType.CONSTRAINT,
        sql="ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email)",
        rollback_sql="ALTER TABLE users DROP CONSTRAINT unique_email"
    )
    
    impact = await orchestrator.analyze_migration_impact(migration)
    
    assert impact["operations"] == 2
    assert impact["has_rollback"] is True


@pytest.mark.asyncio
async def test_mongodb_schema_migration(orchestrator):
    """Test MongoDB schema-like operations"""
    migration = orchestrator.create_migration(
        "mongodb_indexes",
        DatabaseType.MONGODB
    )
    
    orchestrator.add_operation(
        migration,
        MigrationType.INDEX,
        script="db.users.createIndex({email: 1}, {unique: true})",
        rollback_script="db.users.dropIndex({email: 1})"
    )
    
    orchestrator.add_operation(
        migration,
        MigrationType.SCHEMA,
        script="db.createCollection('logs', {capped: true, size: 1000000})",
        rollback_script="db.logs.drop()"
    )
    
    result = await orchestrator.execute_migration(migration)
    
    assert result["status"] == "completed"
    assert result["operations"] == 2


@pytest.mark.asyncio
async def test_migration_checksum_validation(orchestrator):
    """Test migration checksum calculation"""
    migration1 = orchestrator.create_migration(
        "checksum_test",
        DatabaseType.POSTGRESQL
    )
    
    orchestrator.add_operation(
        migration1,
        MigrationType.SCHEMA,
        sql="CREATE TABLE test (id INT)"
    )
    
    checksum1 = migration1.checksum
    
    # Create identical migration
    migration2 = orchestrator.create_migration(
        "checksum_test",
        DatabaseType.POSTGRESQL
    )
    migration2.version = migration1.version
    
    orchestrator.add_operation(
        migration2,
        MigrationType.SCHEMA,
        sql="CREATE TABLE test (id INT)"
    )
    
    checksum2 = migration2.checksum
    
    assert checksum1 == checksum2


@pytest.mark.asyncio
async def test_parallel_schema_operations(orchestrator):
    """Test parallel execution of schema operations"""
    migration = orchestrator.create_migration(
        "parallel_schema",
        DatabaseType.POSTGRESQL
    )
    
    # Add independent operations that can run in parallel
    for i in range(5):
        orchestrator.add_operation(
            migration,
            MigrationType.SCHEMA,
            sql=f"CREATE TABLE table_{i} (id INT)",
            rollback_sql=f"DROP TABLE table_{i}"
        )
    
    result = await orchestrator.execute_migration(migration, parallel=True)
    
    assert result["status"] == "completed"
    assert result["operations"] == 5


def run_all_tests():
    """Run all schema migration tests"""
    test_results = []
    
    async def run_tests():
        orchestrator = DatabaseMigrationOrchestrator()
        
        tests = [
            ("Create Schema Migration", test_create_schema_migration),
            ("Add Schema Operations", test_add_schema_operations),
            ("Execute Dry Run", test_execute_schema_migration_dry_run),
            ("Schema Dependencies", test_schema_migration_with_dependencies),
            ("Index Operations", test_index_operations),
            ("Constraint Operations", test_constraint_operations),
            ("MongoDB Schema", test_mongodb_schema_migration),
            ("Checksum Validation", test_migration_checksum_validation),
            ("Parallel Operations", test_parallel_schema_operations)
        ]
        
        for name, test_func in tests:
            try:
                await test_func(orchestrator)
                test_results.append((name, "PASS", None))
                print(f"✅ {name}: PASS")
            except Exception as e:
                test_results.append((name, "FAIL", str(e)))
                print(f"❌ {name}: FAIL - {e}")
        
        return test_results
    
    return asyncio.run(run_tests())


if __name__ == "__main__":
    results = run_all_tests()
    
    passed = sum(1 for _, status, _ in results if status == "PASS")
    failed = sum(1 for _, status, _ in results if status == "FAIL")
    
    print(f"\n📊 Test Summary: {passed} passed, {failed} failed out of {len(results)} tests")
    
    if failed > 0:
        print("\nFailed tests:")
        for name, status, error in results:
            if status == "FAIL":
                print(f"  - {name}: {error}")
        exit(1)
    
    print("\n✅ All schema migration tests passed!")
    exit(0)