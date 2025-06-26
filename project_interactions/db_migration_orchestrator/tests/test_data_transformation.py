"""
Module: test_data_transformation.py
Purpose: Test data transformation and migration capabilities

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest test_data_transformation.py -v
... All tests pass
"""

import asyncio
import json
import sys
from pathlib import Path
import pytest
from datetime import datetime
from typing import Dict, List, Any

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
async def test_simple_data_migration(orchestrator):
    """Test simple data migration"""
    migration = orchestrator.create_migration(
        "migrate_user_data",
        DatabaseType.POSTGRESQL
    )
    
    # Add data migration operation
    op = orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="UPDATE users SET status = 'active' WHERE last_login > NOW() - INTERVAL '30 days'",
        rollback_sql="UPDATE users SET status = 'inactive' WHERE status = 'active'",
        affects_rows=1000
    )
    
    assert op.affects_rows == 1000
    assert op.estimated_time > 0
    
    result = await orchestrator.execute_migration(migration)
    assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_batch_data_transformation(orchestrator):
    """Test batch data transformation"""
    migration = orchestrator.create_migration(
        "batch_transform",
        DatabaseType.POSTGRESQL
    )
    
    # Add multiple batch operations
    batch_size = 5000
    total_rows = 50000
    
    for i in range(0, total_rows, batch_size):
        orchestrator.add_operation(
            migration,
            MigrationType.DATA,
            sql=f"""
                UPDATE users 
                SET email = LOWER(email) 
                WHERE id >= {i} AND id < {i + batch_size}
            """,
            rollback_sql=f"""
                UPDATE users 
                SET email = UPPER(email) 
                WHERE id >= {i} AND id < {i + batch_size}
            """,
            affects_rows=batch_size
        )
    
    assert len(migration.operations) == 10
    
    # Test impact analysis
    impact = await orchestrator.analyze_migration_impact(migration)
    assert impact["affected_rows"] == total_rows
    assert impact["operations"] == 10


@pytest.mark.asyncio
async def test_data_type_conversion(orchestrator):
    """Test data type conversion migration"""
    migration = orchestrator.create_migration(
        "convert_data_types",
        DatabaseType.POSTGRESQL
    )
    
    # Step 1: Add new column
    orchestrator.add_operation(
        migration,
        MigrationType.SCHEMA,
        sql="ALTER TABLE products ADD COLUMN price_decimal DECIMAL(10,2)",
        rollback_sql="ALTER TABLE products DROP COLUMN price_decimal"
    )
    
    # Step 2: Convert data
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="UPDATE products SET price_decimal = CAST(price_string AS DECIMAL(10,2))",
        rollback_sql="UPDATE products SET price_decimal = NULL",
        affects_rows=10000
    )
    
    # Step 3: Drop old column
    orchestrator.add_operation(
        migration,
        MigrationType.SCHEMA,
        sql="ALTER TABLE products DROP COLUMN price_string",
        rollback_sql="ALTER TABLE products ADD COLUMN price_string VARCHAR(20)"
    )
    
    result = await orchestrator.execute_migration(migration)
    assert result["status"] == "completed"
    assert result["operations"] == 3


@pytest.mark.asyncio
async def test_mongodb_data_transformation(orchestrator):
    """Test MongoDB data transformation"""
    migration = orchestrator.create_migration(
        "mongodb_transform",
        DatabaseType.MONGODB
    )
    
    # Add data transformation for MongoDB
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        script="""
            db.users.updateMany(
                {},
                [{
                    $set: {
                        fullName: { $concat: ["$firstName", " ", "$lastName"] },
                        updatedAt: new Date()
                    }
                }]
            )
        """,
        rollback_script="""
            db.users.updateMany(
                {},
                { $unset: { fullName: "", updatedAt: "" } }
            )
        """,
        affects_rows=5000
    )
    
    # Add aggregation pipeline operation
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        script="""
            db.orders.aggregate([
                { $group: { _id: "$userId", totalSpent: { $sum: "$amount" } } },
                { $out: "user_spending_summary" }
            ])
        """,
        rollback_script="db.user_spending_summary.drop()",
        affects_rows=10000
    )
    
    result = await orchestrator.execute_migration(migration)
    assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_data_validation_during_migration(orchestrator):
    """Test data validation during migration"""
    migration = orchestrator.create_migration(
        "validated_migration",
        DatabaseType.POSTGRESQL
    )
    
    # Add operation with validation
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="""
            UPDATE users 
            SET email = LOWER(email) 
            WHERE email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        """,
        rollback_sql="UPDATE users SET email = UPPER(email)",
        affects_rows=8000
    )
    
    # Add validation check
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="""
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM users WHERE email NOT LIKE '%@%') THEN
                    RAISE EXCEPTION 'Invalid emails found after migration';
                END IF;
            END $$;
        """,
        affects_rows=0
    )
    
    result = await orchestrator.execute_migration(migration)
    assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_cross_table_data_migration(orchestrator):
    """Test migration involving multiple tables"""
    migration = orchestrator.create_migration(
        "cross_table_migration",
        DatabaseType.POSTGRESQL
    )
    
    # Denormalize data for performance
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="""
            UPDATE orders o
            SET customer_name = u.name,
                customer_email = u.email
            FROM users u
            WHERE o.user_id = u.id
        """,
        rollback_sql="""
            UPDATE orders
            SET customer_name = NULL,
                customer_email = NULL
        """,
        affects_rows=20000
    )
    
    # Create summary table
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="""
            INSERT INTO order_summary (user_id, total_orders, total_amount, last_order_date)
            SELECT 
                user_id,
                COUNT(*) as total_orders,
                SUM(amount) as total_amount,
                MAX(order_date) as last_order_date
            FROM orders
            GROUP BY user_id
        """,
        rollback_sql="TRUNCATE TABLE order_summary",
        affects_rows=5000
    )
    
    result = await orchestrator.execute_migration(migration)
    assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_json_data_transformation(orchestrator):
    """Test JSON data transformation"""
    migration = orchestrator.create_migration(
        "json_transform",
        DatabaseType.POSTGRESQL
    )
    
    # Transform JSON data
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="""
            UPDATE products
            SET attributes = jsonb_set(
                attributes,
                '{normalized}',
                'true'::jsonb
            )
            WHERE attributes IS NOT NULL
        """,
        rollback_sql="""
            UPDATE products
            SET attributes = attributes - 'normalized'
            WHERE attributes IS NOT NULL
        """,
        affects_rows=15000
    )
    
    # Extract JSON fields to columns
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="""
            UPDATE products
            SET 
                brand = attributes->>'brand',
                category = attributes->>'category'
            WHERE attributes IS NOT NULL
        """,
        rollback_sql="""
            UPDATE products
            SET brand = NULL, category = NULL
        """,
        affects_rows=15000
    )
    
    result = await orchestrator.execute_migration(migration)
    assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_data_migration_with_progress(orchestrator):
    """Test data migration with progress tracking"""
    migration = orchestrator.create_migration(
        "progress_tracked",
        DatabaseType.POSTGRESQL
    )
    
    progress_updates = []
    
    def track_progress(result):
        progress_updates.append({
            "completed": result.operations_completed,
            "total": result.operations_total
        })
    
    # Add multiple operations
    for i in range(5):
        orchestrator.add_operation(
            migration,
            MigrationType.DATA,
            sql=f"UPDATE table_{i} SET processed = true",
            rollback_sql=f"UPDATE table_{i} SET processed = false",
            affects_rows=1000 * (i + 1)
        )
    
    result = await orchestrator.execute_migration(
        migration,
        progress_callback=track_progress
    )
    
    assert result["status"] == "completed"
    assert len(progress_updates) >= 5
    assert progress_updates[-1]["completed"] == 5


@pytest.mark.asyncio
async def test_conditional_data_migration(orchestrator):
    """Test conditional data migration"""
    migration = orchestrator.create_migration(
        "conditional_migration",
        DatabaseType.POSTGRESQL
    )
    
    # Migrate based on conditions
    orchestrator.add_operation(
        migration,
        MigrationType.DATA,
        sql="""
            WITH eligible_users AS (
                SELECT id FROM users 
                WHERE created_at < '2024-01-01' 
                AND status = 'active'
            )
            UPDATE users u
            SET loyalty_tier = 'gold'
            FROM eligible_users e
            WHERE u.id = e.id
        """,
        rollback_sql="""
            UPDATE users 
            SET loyalty_tier = 'standard' 
            WHERE loyalty_tier = 'gold'
        """,
        affects_rows=3000
    )
    
    result = await orchestrator.execute_migration(migration)
    assert result["status"] == "completed"


def run_all_tests():
    """Run all data transformation tests"""
    test_results = []
    
    async def run_tests():
        orchestrator = DatabaseMigrationOrchestrator()
        
        tests = [
            ("Simple Data Migration", test_simple_data_migration),
            ("Batch Transformation", test_batch_data_transformation),
            ("Data Type Conversion", test_data_type_conversion),
            ("MongoDB Transformation", test_mongodb_data_transformation),
            ("Data Validation", test_data_validation_during_migration),
            ("Cross Table Migration", test_cross_table_data_migration),
            ("JSON Transformation", test_json_data_transformation),
            ("Progress Tracking", test_data_migration_with_progress),
            ("Conditional Migration", test_conditional_data_migration)
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
    
    print("\n✅ All data transformation tests passed!")
    exit(0)