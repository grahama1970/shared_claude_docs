#!/usr/bin/env python3
"""
Module: test_marker_arangodb_integration.py
Description: Real integration test for Marker -> ArangoDB document processing

External Dependencies:
- None
"""

import sys
import asyncio
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path("/home/graham/workspace/experiments/marker/src")))
sys.path.insert(0, str(Path("/home/graham/workspace/experiments/arangodb/src")))

async def test_marker_to_arangodb():
    """Test document processing and storage"""
    print("\n🧪 Testing Marker -> ArangoDB Integration...")
    
    try:
        # Import modules
        from marker.integrations.marker_module import MarkerModule
        from arangodb.handlers import ArangoDBModule
        
        # Initialize
        marker = MarkerModule()
        arangodb = ArangoDBModule()
        
        # Step 1: Process a document
        print("  📄 Processing document...")
        doc_request = {
            "action": "process_pdf",
            "data": {"file_path": "/tmp/test.pdf"}
        }
        
        doc_result = await marker.process(doc_request)
        
        if not doc_result.get("success"):
            print(f"  ❌ Document processing failed: {doc_result.get('error')}")
            return False
        
        processed_data = doc_result.get("data", {})
        print(f"  ✅ Processed {processed_data.get('pages', 0)} pages")
        
        # Step 2: Store processed document
        print("  💾 Storing processed document...")
        doc_id = await arangodb.store({
            "type": "processed_document",
            "source": "marker",
            "data": processed_data,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"  ✅ Stored with ID: {doc_id}")
        
        # Step 3: Verify storage
        retrieved = await arangodb.get(doc_id)
        if retrieved:
            print("  ✅ Document retrieval verified!")
            return True
        else:
            print("  ❌ Document retrieval failed!")
            return False
            
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        return False

from datetime import datetime

if __name__ == "__main__":
    result = asyncio.run(test_marker_to_arangodb())
    exit(0 if result else 1)
