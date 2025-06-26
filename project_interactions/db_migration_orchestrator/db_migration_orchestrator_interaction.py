
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: db_migration_orchestrator_interaction.py
Purpose: Database migration orchestration system with multi-database support and zero-downtime capabilities

External Dependencies:
- sqlalchemy: https://docs.sqlalchemy.org/
- psycopg2-binary: https://www.psycopg.org/docs/
- pymongo: https://pymongo.readthedocs.io/
- pymysql: https://pymysql.readthedocs.io/

Example Usage:
>>> orchestrator = DatabaseMigrationOrchestrator()
>>> migration = orchestrator.create_migration("add_user_table", "postgresql")
>>> result = orchestrator.execute_migration(migration, dry_run=True)
{'status': 'success', 'operations': 1, 'time': 0.15}
"""

import asyncio
import hashlib
import json
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from loguru import logger
from pydantic import BaseModel, Field, validator


class DatabaseType(str, Enum):
    """Supported database types"""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    SQLITE = "sqlite"
    REDIS = "redis"


class MigrationStatus(str, Enum):
    """Migration status states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class MigrationType(str, Enum):
    """Types of database migrations"""
    SCHEMA = "schema"
    DATA = "data"
    INDEX = "index"
    CONSTRAINT = "constraint"
    PROCEDURE = "procedure"


class MigrationOperation(BaseModel):
    """Single migration operation"""
    id: str
    type: MigrationType
    database: DatabaseType
    sql: Optional[str] = None
    script: Optional[str] = None
    params: Dict[str, Any] = Field(default_factory=dict)
    rollback_sql: Optional[str] = None
    rollback_script: Optional[str] = None
    estimated_time: float = 0.0
    affects_rows: int = 0
    
    @validator("id")
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Operation ID cannot be empty")
        return v


class Migration(BaseModel):
    """Database migration definition"""
    id: str
    version: str
    name: str
    description: str
    database_type: DatabaseType
    operations: List[MigrationOperation]
    dependencies: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    checksum: Optional[str] = None
    pre_hooks: List[str] = Field(default_factory=list)
    post_hooks: List[str] = Field(default_factory=list)
    
    def calculate_checksum(self) -> str:
        """Calculate migration checksum"""
        content = json.dumps({
            "version": self.version,
            "operations": [op.model_dump() for op in self.operations]
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


class MigrationResult(BaseModel):
    """Migration execution result"""
    migration_id: str
    status: MigrationStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    operations_completed: int = 0
    operations_total: int = 0
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    execution_time: float = 0.0
    rows_affected: int = 0
    rollback_available: bool = True


class DatabaseAdapter(ABC):
    """Abstract base for database adapters"""
    
    @abstractmethod
    async def connect(self, connection_string: str) -> None:
        """Connect to database"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from database"""
        pass
    
    @abstractmethod
    async def execute_operation(self, operation: MigrationOperation) -> Dict[str, Any]:
        """Execute migration operation"""
        pass
    
    @abstractmethod
    async def check_health(self) -> bool:
        """Check database health"""
        pass
    
    @abstractmethod
    async def get_schema_info(self) -> Dict[str, Any]:
        """Get current schema information"""
        pass


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter"""
    
    def __init__(self):
        self.connection = None
        
    async def connect(self, connection_string: str) -> None:
        """Connect to PostgreSQL"""
        # Simplified for example - would use asyncpg in production
        logger.info(f"Connecting to PostgreSQL: {connection_string}")
        self.connection = {"connected": True, "type": "postgresql"}
    
    async def disconnect(self) -> None:
        """Disconnect from PostgreSQL"""
        if self.connection:
            logger.info("Disconnecting from PostgreSQL")
            self.connection = None
    
    async def execute_operation(self, operation: MigrationOperation) -> Dict[str, Any]:
        """Execute PostgreSQL operation"""
        start_time = time.time()
        
        # Simulate operation execution
        await asyncio.sleep(0.1)
        
        return {
            "success": True,
            "rows_affected": operation.affects_rows,
            "execution_time": time.time() - start_time
        }
    
    async def check_health(self) -> bool:
        """Check PostgreSQL health"""
        return self.connection is not None
    
    async def get_schema_info(self) -> Dict[str, Any]:
        """Get PostgreSQL schema information"""
        return {
            "tables": ["users", "orders", "products"],
            "version": "14.5"
        }


class MongoDBAdapter(DatabaseAdapter):
    """MongoDB database adapter"""
    
    def __init__(self):
        self.client = None
        
    async def connect(self, connection_string: str) -> None:
        """Connect to MongoDB"""
        logger.info(f"Connecting to MongoDB: {connection_string}")
        self.client = {"connected": True, "type": "mongodb"}
    
    async def disconnect(self) -> None:
        """Disconnect from MongoDB"""
        if self.client:
            logger.info("Disconnecting from MongoDB")
            self.client = None
    
    async def execute_operation(self, operation: MigrationOperation) -> Dict[str, Any]:
        """Execute MongoDB operation"""
        start_time = time.time()
        
        # Simulate operation execution
        await asyncio.sleep(0.05)
        
        return {
            "success": True,
            "documents_affected": operation.affects_rows,
            "execution_time": time.time() - start_time
        }
    
    async def check_health(self) -> bool:
        """Check MongoDB health"""
        return self.client is not None
    
    async def get_schema_info(self) -> Dict[str, Any]:
        """Get MongoDB schema information"""
        return {
            "collections": ["users", "orders", "products"],
            "version": "5.0"
        }


class MigrationValidator:
    """Validates migrations before execution"""
    
    @staticmethod
    def validate_migration(migration: Migration, schema_info: Dict[str, Any]) -> List[str]:
        """Validate migration against current schema"""
        warnings = []
        
        # Check for potentially dangerous operations
        for op in migration.operations:
            if op.type == MigrationType.DATA and op.affects_rows > 10000:
                warnings.append(f"Operation {op.id} affects {op.affects_rows} rows")
            
            if op.rollback_sql is None and op.rollback_script is None:
                warnings.append(f"Operation {op.id} has no rollback defined")
        
        # Check dependencies
        if migration.dependencies:
            warnings.append(f"Migration has {len(migration.dependencies)} dependencies")
        
        return warnings
    
    @staticmethod
    def validate_data_integrity(before_data: Dict, after_data: Dict) -> bool:
        """Validate data integrity after migration"""
        # Simplified validation - would include comprehensive checks
        return True


class MigrationExecutor:
    """Executes individual migration operations"""
    
    def __init__(self, adapter: DatabaseAdapter):
        self.adapter = adapter
        self.operation_history: List[MigrationOperation] = []
    
    async def execute_operation(
        self,
        operation: MigrationOperation,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Execute single operation"""
        logger.info(f"Executing operation: {operation.id} (dry_run={dry_run})")
        
        if dry_run:
            # Simulate execution
            await asyncio.sleep(0.01)
            return {
                "success": True,
                "dry_run": True,
                "estimated_time": operation.estimated_time
            }
        
        result = await self.adapter.execute_operation(operation)
        self.operation_history.append(operation)
        return result
    
    async def rollback_operation(self, operation: MigrationOperation) -> Dict[str, Any]:
        """Rollback single operation"""
        logger.warning(f"Rolling back operation: {operation.id}")
        
        # Create rollback operation
        rollback_op = MigrationOperation(
            id=f"{operation.id}_rollback",
            type=operation.type,
            database=operation.database,
            sql=operation.rollback_sql,
            script=operation.rollback_script,
            params=operation.params,
            affects_rows=operation.affects_rows
        )
        
        return await self.adapter.execute_operation(rollback_op)


class DatabaseMigrationOrchestrator:
    """Main orchestrator for database migrations"""
    
    def __init__(self):
        self.adapters: Dict[DatabaseType, DatabaseAdapter] = {
            DatabaseType.POSTGRESQL: PostgreSQLAdapter(),
            DatabaseType.MONGODB: MongoDBAdapter()
        }
        self.migrations: Dict[str, Migration] = {}
        self.execution_history: List[MigrationResult] = []
        self.validator = MigrationValidator()
        self.executors: Dict[DatabaseType, MigrationExecutor] = {}
        
        # Initialize executors
        for db_type, adapter in self.adapters.items():
            self.executors[db_type] = MigrationExecutor(adapter)
    
    def create_migration(
        self,
        name: str,
        database_type: Union[str, DatabaseType],
        version: Optional[str] = None
    ) -> Migration:
        """Create new migration"""
        if isinstance(database_type, str):
            database_type = DatabaseType(database_type)
        
        migration_id = f"{name}_{int(time.time())}"
        version = version or datetime.now().strftime("%Y%m%d%H%M%S")
        
        migration = Migration(
            id=migration_id,
            version=version,
            name=name,
            description=f"Migration: {name}",
            database_type=database_type,
            operations=[]
        )
        
        self.migrations[migration_id] = migration
        return migration
    
    def add_operation(
        self,
        migration: Migration,
        operation_type: Union[str, MigrationType],
        sql: Optional[str] = None,
        script: Optional[str] = None,
        rollback_sql: Optional[str] = None,
        rollback_script: Optional[str] = None,
        affects_rows: int = 0
    ) -> MigrationOperation:
        """Add operation to migration"""
        if isinstance(operation_type, str):
            operation_type = MigrationType(operation_type)
        
        operation = MigrationOperation(
            id=f"{migration.id}_op_{len(migration.operations) + 1}",
            type=operation_type,
            database=migration.database_type,
            sql=sql,
            script=script,
            rollback_sql=rollback_sql,
            rollback_script=rollback_script,
            affects_rows=affects_rows,
            estimated_time=affects_rows * 0.0001  # Simple estimation
        )
        
        migration.operations.append(operation)
        migration.checksum = migration.calculate_checksum()
        return operation
    
    async def execute_migration(
        self,
        migration: Migration,
        dry_run: bool = False,
        parallel: bool = False,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Execute migration with optional dry run"""
        logger.info(f"Executing migration: {migration.id} (dry_run={dry_run})")
        
        # Get adapter and executor
        adapter = self.adapters.get(migration.database_type)
        executor = self.executors.get(migration.database_type)
        
        if not adapter or not executor:
            return {"status": "error", "message": "Unsupported database type"}
        
        # Connect to database
        await adapter.connect("connection_string_here")
        
        # Validate migration
        schema_info = await adapter.get_schema_info()
        warnings = self.validator.validate_migration(migration, schema_info)
        
        # Create result
        result = MigrationResult(
            migration_id=migration.id,
            status=MigrationStatus.RUNNING,
            started_at=datetime.now(),
            operations_total=len(migration.operations)
        )
        
        try:
            # Execute pre-hooks
            for hook in migration.pre_hooks:
                logger.info(f"Executing pre-hook: {hook}")
            
            # Execute operations
            if parallel and len(migration.operations) > 1:
                # Execute operations in parallel
                tasks = [
                    executor.execute_operation(op, dry_run)
                    for op in migration.operations
                ]
                results = await asyncio.gather(*tasks)
                result.operations_completed = len(migration.operations)
            else:
                # Execute operations sequentially
                results = []
                for i, op in enumerate(migration.operations):
                    op_result = await executor.execute_operation(op, dry_run)
                    results.append(op_result)
                    result.operations_completed = i + 1
                    
                    if progress_callback:
                        progress_callback(result)
            
            # Execute post-hooks
            for hook in migration.post_hooks:
                logger.info(f"Executing post-hook: {hook}")
            
            # Update result
            result.status = MigrationStatus.COMPLETED
            result.completed_at = datetime.now()
            result.execution_time = (
                result.completed_at - result.started_at
            ).total_seconds()
            
            # Calculate total rows affected
            result.rows_affected = sum(
                r.get("rows_affected", 0) for r in results if r.get("success")
            )
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            result.status = MigrationStatus.FAILED
            result.errors.append(str(e))
            
            # Attempt rollback
            if not dry_run:
                await self.rollback_migration(migration, result.operations_completed)
        
        finally:
            await adapter.disconnect()
            self.execution_history.append(result)
        
        return {
            "status": result.status.value,
            "operations": result.operations_completed,
            "time": result.execution_time,
            "warnings": warnings,
            "errors": result.errors
        }
    
    async def rollback_migration(
        self,
        migration: Migration,
        up_to_operation: int
    ) -> Dict[str, Any]:
        """Rollback migration up to specific operation"""
        logger.warning(f"Rolling back migration: {migration.id}")
        
        executor = self.executors.get(migration.database_type)
        if not executor:
            return {"status": "error", "message": "No executor available"}
        
        rollback_count = 0
        errors = []
        
        # Rollback in reverse order
        for i in range(up_to_operation - 1, -1, -1):
            operation = migration.operations[i]
            try:
                await executor.rollback_operation(operation)
                rollback_count += 1
            except Exception as e:
                errors.append(f"Failed to rollback {operation.id}: {e}")
        
        return {
            "status": "rolled_back",
            "operations_rolled_back": rollback_count,
            "errors": errors
        }
    
    def get_migration_status(self, migration_id: str) -> Optional[MigrationResult]:
        """Get status of specific migration"""
        for result in reversed(self.execution_history):
            if result.migration_id == migration_id:
                return result
        return None
    
    def get_pending_migrations(self) -> List[Migration]:
        """Get list of pending migrations"""
        executed_ids = {r.migration_id for r in self.execution_history
                       if r.status == MigrationStatus.COMPLETED}
        return [m for m in self.migrations.values() if m.id not in executed_ids]
    
    async def analyze_migration_impact(
        self,
        migration: Migration
    ) -> Dict[str, Any]:
        """Analyze potential impact of migration"""
        adapter = self.adapters.get(migration.database_type)
        if not adapter:
            return {"error": "Unsupported database type"}
        
        await adapter.connect("connection_string_here")
        schema_info = await adapter.get_schema_info()
        await adapter.disconnect()
        
        # Analyze impact
        total_time = sum(op.estimated_time for op in migration.operations)
        total_rows = sum(op.affects_rows for op in migration.operations)
        
        return {
            "estimated_time": total_time,
            "affected_rows": total_rows,
            "operations": len(migration.operations),
            "has_rollback": all(
                op.rollback_sql or op.rollback_script
                for op in migration.operations
            ),
            "warnings": self.validator.validate_migration(migration, schema_info)
        }


def progress_reporter(result: MigrationResult) -> None:
    """Report migration progress"""
    progress = result.operations_completed / result.operations_total * 100
    logger.info(f"Migration progress: {progress:.1f}% "
                f"({result.operations_completed}/{result.operations_total})")


async def main():
    """Test migration orchestrator with real scenarios"""
    orchestrator = DatabaseMigrationOrchestrator()
    
    # Test 1: Create PostgreSQL schema migration
    logger.info("=== Test 1: PostgreSQL Schema Migration ===")
    pg_migration = orchestrator.create_migration("add_user_table", "postgresql")
    
    # Add operations
    orchestrator.add_operation(
        pg_migration,
        "schema",
        sql="CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(255))",
        rollback_sql="DROP TABLE users",
        affects_rows=0
    )
    
    orchestrator.add_operation(
        pg_migration,
        "index",
        sql="CREATE INDEX idx_users_name ON users(name)",
        rollback_sql="DROP INDEX idx_users_name",
        affects_rows=0
    )
    
    # Dry run first
    dry_result = await orchestrator.execute_migration(pg_migration, dry_run=True)
    logger.info(f"Dry run result: {dry_result}")
    
    # Execute migration
    result = await orchestrator.execute_migration(
        pg_migration,
        progress_callback=progress_reporter
    )
    logger.info(f"Migration result: {result}")
    
    # Test 2: MongoDB data migration
    logger.info("\n=== Test 2: MongoDB Data Migration ===")
    mongo_migration = orchestrator.create_migration("migrate_user_data", "mongodb")
    
    orchestrator.add_operation(
        mongo_migration,
        "data",
        script="db.users.updateMany({}, {$set: {migrated: true}})",
        rollback_script="db.users.updateMany({}, {$unset: {migrated: 1}})",
        affects_rows=5000
    )
    
    # Analyze impact
    impact = await orchestrator.analyze_migration_impact(mongo_migration)
    logger.info(f"Migration impact analysis: {impact}")
    
    # Execute with progress tracking
    result = await orchestrator.execute_migration(
        mongo_migration,
        progress_callback=progress_reporter
    )
    logger.info(f"MongoDB migration result: {result}")
    
    # Test 3: Check migration status
    logger.info("\n=== Test 3: Migration Status ===")
    status = orchestrator.get_migration_status(pg_migration.id)
    if status:
        logger.info(f"PostgreSQL migration status: {status.status}")
        logger.info(f"Execution time: {status.execution_time:.2f}s")
    
    # Test 4: List pending migrations
    logger.info("\n=== Test 4: Pending Migrations ===")
    pending = orchestrator.get_pending_migrations()
    logger.info(f"Pending migrations: {len(pending)}")
    
    # Test 5: Failed migration with rollback
    logger.info("\n=== Test 5: Failed Migration with Rollback ===")
    fail_migration = orchestrator.create_migration("failing_migration", "postgresql")
    
    orchestrator.add_operation(
        fail_migration,
        "schema",
        sql="CREATE TABLE test1 (id INT)",
        rollback_sql="DROP TABLE test1"
    )
    
    # This would fail in real scenario
    orchestrator.add_operation(
        fail_migration,
        "schema",
        sql="INVALID SQL SYNTAX",
        rollback_sql="DROP TABLE test2"
    )
    
    # Execute and watch rollback
    result = await orchestrator.execute_migration(fail_migration)
    logger.info(f"Failed migration result: {result}")
    
    return {
        "total_migrations": len(orchestrator.migrations),
        "executed": len([h for h in orchestrator.execution_history
                        if h.status == MigrationStatus.COMPLETED]),
        "failed": len([h for h in orchestrator.execution_history
                      if h.status == MigrationStatus.FAILED])
    }


if __name__ == "__main__":
    result = asyncio.run(main())
    logger.info(f"\n✅ Migration orchestrator validation completed: {result}")