#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: setup_granger_services.py
Description: Initialize all required services for Granger integration

This script sets up:
1. ArangoDB database
2. YouTube transcripts SQLite database
3. Any other required services

External Dependencies:
- python-arango: https://docs.python-arango.com/
- youtube_transcripts: Local module

Example Usage:
>>> python setup_granger_services.py
"""

import sys
import time
from pathlib import Path

def setup_arangodb():
    """Initialize ArangoDB with required database"""
    print("🔧 Setting up ArangoDB...")
    
    try:
        from arango import ArangoClient
        
        # Connect to system database
        client = ArangoClient(hosts='http://localhost:8529')
        sys_db = client.db('_system', username='root', password='')
        
        # Create granger_test database if it doesn't exist
        if not sys_db.has_database('granger_test'):
            sys_db.create_database('granger_test')
            print("   ✅ Created 'granger_test' database")
        else:
            print("   ℹ️  'granger_test' database already exists")
            
        # Connect to granger_test and create collections
        db = client.db('granger_test', username='root', password='')
        
        collections = [
            'documents',
            'entities', 
            'relationships',
            'conversations',
            'memory_entries',
            'antipatterns'
        ]
        
        for collection in collections:
            if not db.has_collection(collection):
                db.create_collection(collection)
                print(f"   ✅ Created '{collection}' collection")
            else:
                print(f"   ℹ️  '{collection}' collection already exists")
                
        print("   ✅ ArangoDB setup complete")
        return True
        
    except Exception as e:
        print(f"   ❌ ArangoDB setup failed: {e}")
        print("   💡 Make sure ArangoDB is running on port 8529")
        return False


def setup_youtube_transcripts():
    """Initialize YouTube transcripts database"""
    print("\n📹 Setting up YouTube Transcripts database...")
    
    try:
        # Add YouTube transcripts path
        sys.path.insert(0, '/home/graham/workspace/experiments/youtube_transcripts/src')
        
        from youtube_transcripts.core.database import initialize_database
        
        # Initialize database
        initialize_database()
        
        print("   ✅ YouTube transcripts database initialized")
        return True
        
    except Exception as e:
        print(f"   ❌ YouTube transcripts setup failed: {e}")
        return False


def test_services():
    """Test that all services are working"""
    print("\n🧪 Testing services...")
    
    all_good = True
    
    # Test ArangoDB
    try:
        from arango import ArangoClient
        client = ArangoClient(hosts='http://localhost:8529')
        db = client.db('granger_test', username='root', password='')
        
        # Try a simple query
        result = list(db.aql.execute("RETURN 1"))
        assert result == [1]
        print("   ✅ ArangoDB connection working")
    except Exception as e:
        print(f"   ❌ ArangoDB test failed: {e}")
        all_good = False
    
    # Test YouTube DB
    try:
        import sqlite3
        from youtube_transcripts.config import DB_PATH
        
        # Check tables exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if 'transcripts' in tables:
            print("   ✅ YouTube transcripts database working")
        else:
            print("   ❌ YouTube transcripts table not found")
            all_good = False
            
    except Exception as e:
        print(f"   ❌ YouTube transcripts test failed: {e}")
        all_good = False
        
    return all_good


def main():
    """Main setup function"""
    print("🚀 Granger Services Setup")
    print("=" * 50)
    
    # Setup services
    arangodb_ok = setup_arangodb()
    youtube_ok = setup_youtube_transcripts()
    
    # Test everything
    if arangodb_ok and youtube_ok:
        tests_ok = test_services()
        
        if tests_ok:
            print("\n✅ All services set up successfully!")
            print("\nYou can now run integration tests.")
        else:
            print("\n⚠️  Some services are not working correctly")
            print("Please check the error messages above.")
    else:
        print("\n❌ Setup failed. Please fix the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()