#!/usr/bin/env python3
"""
Module: setup_arangodb_test_database.py
Description: Set up ArangoDB test database with credentials from .env file

External Dependencies:
- python-arango: https://docs.python-arango.com/
- python-dotenv: https://pypi.org/project/python-dotenv/

Example Usage:
>>> python setup_arangodb_test_database.py
"""

import os
import sys
from pathlib import Path
from arango import ArangoClient
from arango.exceptions import DatabaseCreateError, DatabaseDeleteError
from dotenv import load_dotenv


def setup_test_database():
    """Set up ArangoDB test database using .env credentials."""
    print("🔧 Setting up ArangoDB Test Database")
    print("=" * 60)
    
    # Load environment variables
    env_path = Path("/home/graham/workspace/shared_claude_docs/.env")
    if not env_path.exists():
        print("❌ .env file not found!")
        return False
        
    load_dotenv(env_path)
    
    # Get credentials from environment
    arango_host = os.getenv("ARANGO_HOST", "localhost")
    arango_port = os.getenv("ARANGO_PORT", "8529")
    arango_user = os.getenv("ARANGO_USER", "root")
    arango_password = os.getenv("ARANGO_PASSWORD", "openSesame")
    
    # Use the test database name from .env
    test_db_name = os.getenv("ARANGO_TEST_DB_NAME", "youtube_transcripts_test")
    
    print(f"\n📌 Connection Details:")
    print(f"  Host: {arango_host}:{arango_port}")
    print(f"  User: {arango_user}")
    print(f"  Test DB: {test_db_name}")
    
    try:
        # Connect to ArangoDB
        client = ArangoClient(hosts=f"http://{arango_host}:{arango_port}")
        
        # Connect to system database
        sys_db = client.db('_system', username=arango_user, password=arango_password)
        
        # Check if test database exists and delete it
        if sys_db.has_database(test_db_name):
            print(f"\n⚠️  Test database '{test_db_name}' already exists. Dropping it...")
            sys_db.delete_database(test_db_name)
            print("  ✓ Dropped existing test database")
        
        # Create fresh test database
        print(f"\n📦 Creating test database '{test_db_name}'...")
        sys_db.create_database(test_db_name)
        print("  ✓ Test database created")
        
        # Connect to test database
        test_db = client.db(test_db_name, username=arango_user, password=arango_password)
        
        # Create some standard collections for testing
        print("\n📁 Creating test collections:")
        
        # Create vertex collections
        vertex_collections = ["documents", "test_collection"]
        for collection in vertex_collections:
            if not test_db.has_collection(collection):
                test_db.create_collection(collection)
                print(f"  ✓ Created vertex collection: {collection}")
        
        # Create edge collection
        if not test_db.has_collection("edges"):
            test_db.create_collection("edges", edge=True)
            print("  ✓ Created edge collection: edges")
        
        # Create a test graph
        if not test_db.has_graph("test_graph"):
            test_db.create_graph(
                "test_graph",
                edge_definitions=[{
                    "edge_collection": "edges",
                    "from_vertex_collections": ["documents"],
                    "to_vertex_collections": ["documents"]
                }]
            )
            print("  ✓ Created test graph: test_graph")
        
        print("\n✅ Test database setup complete!")
        print(f"   Database '{test_db_name}' is ready for testing")
        
        # Export credentials for tests to use
        print("\n📝 Exporting test credentials...")
        with open("/tmp/arangodb_test_creds.env", "w") as f:
            f.write(f"ARANGO_HOST=http://{arango_host}:{arango_port}\\n")
            f.write(f"ARANGO_USER={arango_user}\\n")
            f.write(f"ARANGO_PASSWORD={arango_password}\\n")
            f.write(f"ARANGO_TEST_DB={test_db_name}\\n")
        print("  ✓ Test credentials exported to /tmp/arangodb_test_creds.env")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error setting up test database: {e}")
        return False


def cleanup_test_database():
    """Clean up test database after tests."""
    print("\n🧹 Cleaning up test database...")
    
    # Load environment variables
    env_path = Path("/home/graham/workspace/shared_claude_docs/.env")
    load_dotenv(env_path)
    
    arango_host = os.getenv("ARANGO_HOST", "localhost")
    arango_port = os.getenv("ARANGO_PORT", "8529")
    arango_user = os.getenv("ARANGO_USER", "root")
    arango_password = os.getenv("ARANGO_PASSWORD", "openSesame")
    test_db_name = os.getenv("ARANGO_TEST_DB_NAME", "youtube_transcripts_test")
    
    try:
        client = ArangoClient(hosts=f"http://{arango_host}:{arango_port}")
        sys_db = client.db('_system', username=arango_user, password=arango_password)
        
        if sys_db.has_database(test_db_name):
            sys_db.delete_database(test_db_name)
            print(f"  ✓ Deleted test database '{test_db_name}'")
        else:
            print(f"  ℹ️  Test database '{test_db_name}' not found")
            
    except Exception as e:
        print(f"  ❌ Error cleaning up: {e}")


if __name__ == "__main__":
    # Setup test database
    success = setup_test_database()
    
    if success and len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        # If --cleanup flag is passed, also clean up
        cleanup_test_database()
    
    sys.exit(0 if success else 1)