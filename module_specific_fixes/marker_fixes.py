#!/usr/bin/env python3
"""
Module: marker_fixes.py
Description: Marker-specific bug fixes implementation

External Dependencies:
- granger_common: Our standardized components
"""

from pathlib import Path
import re

def apply_marker_fixes():
    """Apply all Marker-specific fixes."""
    print("\n📄 Applying Marker fixes...")
    
    # 1. Fix memory management for large PDFs
    memory_management_code = '''
from granger_common import SmartPDFHandler

# Initialize with 1GB threshold for 256GB RAM workstation
pdf_handler = SmartPDFHandler(memory_threshold_mb=1000)

async def process_pdf(file_path: str) -> dict:
    """Process PDF with smart memory management."""
    try:
        # Use SmartPDFHandler for automatic memory management
        result = await pdf_handler.process_pdf(file_path)
        
        # If processing failed due to size, it will use streaming
        if result.get("streamed", False):
            logger.info(f"Large PDF processed using streaming: {file_path}")
        
        return result
    except Exception as e:
        logger.error(f"PDF processing failed: {e}")
        raise
'''
    
    # 2. Fix transaction integrity for ArangoDB storage
    transaction_code = '''
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from granger_common import SchemaManager

@asynccontextmanager
async def atomic_transaction(db_connection) -> AsyncGenerator[Any, None]:
    """Ensure atomic transactions with proper rollback."""
    transaction = None
    try:
        # Begin transaction
        transaction = await db_connection.begin_transaction(
            read=["documents", "embeddings"],
            write=["documents", "embeddings", "processing_queue"]
        )
        
        yield transaction
        
        # Commit on success
        await transaction.commit()
        logger.info("Transaction committed successfully")
        
    except Exception as e:
        # Rollback on error
        if transaction:
            await transaction.abort()
        logger.error(f"Transaction failed, rolled back: {e}")
        raise
    finally:
        # Ensure cleanup
        if transaction and hasattr(transaction, 'status') and transaction.status == 'running':
            await transaction.abort()

async def store_document_with_integrity(doc_data: dict, embeddings: list):
    """Store document and embeddings atomically."""
    async with atomic_transaction(db) as txn:
        # Both operations succeed or both fail
        doc_id = await txn.insert_document(doc_data)
        await txn.insert_embeddings(doc_id, embeddings)
        return doc_id
'''
    
    # 3. Add schema versioning for document storage
    schema_versioning_code = '''
from granger_common import SchemaManager, SchemaVersion

# Initialize schema manager
schema_manager = SchemaManager()

# Define document schema versions
DOCUMENT_SCHEMA_V1 = {
    "version": "1.0",
    "fields": {
        "content": "string",
        "metadata": "object",
        "embeddings": "array"
    }
}

DOCUMENT_SCHEMA_V2 = {
    "version": "2.0", 
    "fields": {
        "content": "string",
        "metadata": "object",
        "embeddings": "array",
        "processing_info": "object",
        "quality_score": "number"
    }
}

# Register schemas
schema_manager.register_schema("document", SchemaVersion(1, 0), DOCUMENT_SCHEMA_V1)
schema_manager.register_schema("document", SchemaVersion(2, 0), DOCUMENT_SCHEMA_V2)

# Migration function
def migrate_v1_to_v2(doc: dict) -> dict:
    """Migrate document from v1 to v2."""
    doc["processing_info"] = {
        "processor": "marker",
        "timestamp": datetime.now().isoformat()
    }
    doc["quality_score"] = calculate_quality_score(doc)
    return doc

schema_manager.register_migration(
    "document",
    SchemaVersion(1, 0),
    SchemaVersion(2, 0),
    migrate_v1_to_v2
)
'''
    
    # 4. Fix path validation
    path_validation_code = '''
def validate_pdf_path(file_path: str) -> Path:
    """Validate PDF file path for security."""
    path = Path(file_path).resolve()
    
    # Allowed directories for PDF processing
    allowed_dirs = [
        Path("/home/graham/workspace/experiments/marker/data"),
        Path("/tmp/marker_processing"),
        Path.home() / ".marker" / "cache"
    ]
    
    # Check for path traversal
    if ".." in str(file_path):
        raise ValueError(f"Path traversal detected: {file_path}")
    
    # Ensure within allowed directories
    allowed_paths = [d.resolve() for d in allowed_dirs]
    if not any(path.is_relative_to(allowed) for allowed in allowed_paths):
        raise ValueError(f"Path outside allowed directories: {file_path}")
    
    # Ensure it's a PDF
    if path.suffix.lower() not in ['.pdf', '.PDF']:
        raise ValueError(f"Not a PDF file: {file_path}")
    
    return path
'''
    
    print("✅ Marker fixes defined - ready for implementation")
    
    # Create implementation guide
    implementation_guide = '''
# Marker Module Fix Implementation Guide

## 1. Memory Management (CRITICAL)
Location: src/marker/pdf_processor.py
- Import SmartPDFHandler from granger_common
- Replace direct PDF loading with SmartPDFHandler
- Set 1GB threshold for streaming large files
- Add memory monitoring logs

## 2. Transaction Integrity (HIGH)
Location: src/marker/arangodb_storage.py
- Add atomic_transaction context manager
- Wrap all multi-step operations
- Ensure proper rollback on failures
- Log transaction status

## 3. Schema Versioning (MEDIUM)
Location: src/marker/storage/schema.py
- Import SchemaManager from granger_common
- Define document schemas for each version
- Register migration functions
- Version all stored documents

## 4. Path Validation (HIGH)
Location: src/marker/pdf_processor.py
- Add validate_pdf_path function
- Call before any file operations
- Define allowed directories explicitly
- Check file extensions

## 5. Error Context (MEDIUM)
Location: All Marker modules
- Add document_id context to operations
- Include PDF metadata in error logs
- Track processing stages

## Testing
1. Memory test: Process 2GB PDF file
2. Transaction test: Simulate failure during storage
3. Schema test: Migrate v1 documents to v2
4. Path test: Try "../../../etc/passwd.pdf"
5. Load test: Process 100 PDFs concurrently
'''
    
    # Save implementation guide
    guide_path = Path("/home/graham/workspace/shared_claude_docs/module_specific_fixes/marker_implementation_guide.md")
    guide_path.parent.mkdir(exist_ok=True)
    guide_path.write_text(implementation_guide)
    print(f"📝 Implementation guide saved to: {guide_path}")


if __name__ == "__main__":
    apply_marker_fixes()