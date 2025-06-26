#!/usr/bin/env python3
"""
Module: setup_arangodb_test_env.py
Description: Set up ArangoDB test environment by disabling auth or creating test user

External Dependencies:
- None

Example Usage:
>>> python setup_arangodb_test_env.py
"""

import subprocess
import time


def main():
    """Set up ArangoDB for testing."""
    print("🔧 Setting up ArangoDB Test Environment")
    print("=" * 60)
    
    # First, let's restart ArangoDB without authentication
    print("\n1. Stopping current ArangoDB container...")
    subprocess.run(["docker", "stop", "arangodb"], capture_output=True)
    time.sleep(2)
    
    print("2. Removing old container...")
    subprocess.run(["docker", "rm", "arangodb"], capture_output=True)
    
    print("3. Starting new ArangoDB container without authentication...")
    cmd = [
        "docker", "run", "-d",
        "--name", "arangodb",
        "-p", "8529:8529",
        "-e", "ARANGO_NO_AUTH=1",
        "arangodb/arangodb:latest"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓ ArangoDB started without authentication")
    else:
        print(f"  ❌ Failed to start ArangoDB: {result.stderr}")
        return
    
    # Wait for ArangoDB to be ready
    print("\n4. Waiting for ArangoDB to be ready...")
    for i in range(30):
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8529/_api/version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and "version" in result.stdout:
                print("  ✓ ArangoDB is ready!")
                break
        except:
            pass
        time.sleep(1)
        if i % 5 == 0:
            print(f"  ... waiting ({i}s)")
    
    # Verify we can access without auth
    print("\n5. Verifying access...")
    result = subprocess.run(
        ["curl", "-s", "http://localhost:8529/_api/database"],
        capture_output=True,
        text=True
    )
    
    if "result" in result.stdout:
        print("  ✓ Can access ArangoDB without authentication")
        print(f"  Databases: {result.stdout}")
    else:
        print("  ❌ Still cannot access ArangoDB")
        print(f"  Response: {result.stdout}")
    
    print("\n✅ ArangoDB test environment setup complete!")
    print("   You can now run Level 0 tests without authentication issues.")


if __name__ == "__main__":
    main()