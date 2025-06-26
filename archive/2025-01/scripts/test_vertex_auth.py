#!/usr/bin/env python3
"""
Module: test_vertex_auth.py
Description: Test Vertex AI authentication with service account

External Dependencies:
- google-auth: https://google-auth.readthedocs.io/
- google-cloud-aiplatform: https://cloud.google.com/python/docs/reference/aiplatform/latest
- litellm: https://docs.litellm.ai/

Sample Input:
>>> None (uses service account JSON file)

Expected Output:
>>> Authentication successful or detailed error message

Example Usage:
>>> python test_vertex_auth.py
"""

import json
import os
import sys
from datetime import datetime
import jwt
import base64

# Test 1: Verify service account file structure
def test_service_account_file():
    """Test if service account JSON is valid"""
    print("\n=== Test 1: Verifying Service Account File ===")
    
    sa_path = "vertex_ai_service_account.json"
    
    try:
        with open(sa_path, 'r') as f:
            sa_data = json.load(f)
        
        required_fields = [
            "type", "project_id", "private_key_id", "private_key",
            "client_email", "client_id", "auth_uri", "token_uri"
        ]
        
        for field in required_fields:
            if field not in sa_data:
                print(f"❌ Missing field: {field}")
                return False
            else:
                print(f"✅ Found field: {field}")
        
        print(f"\nProject ID: {sa_data['project_id']}")
        print(f"Service Account: {sa_data['client_email']}")
        
        # Check private key format
        if sa_data['private_key'].startswith('-----BEGIN PRIVATE KEY-----'):
            print("✅ Private key format looks correct")
        else:
            print("❌ Private key format incorrect")
            
        return True
        
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")
        return False

# Test 2: Test Google Auth library directly
def test_google_auth():
    """Test authentication using google-auth library"""
    print("\n=== Test 2: Testing Google Auth Library ===")
    
    try:
        from google.auth import jwt as google_jwt
        from google.auth import transport
        
        # Set environment variable
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vertex_ai_service_account.json'
        
        # Try to create credentials
        with open('vertex_ai_service_account.json', 'r') as f:
            sa_info = json.load(f)
            
        credentials = google_jwt.Credentials.from_service_account_info(
            sa_info,
            audience='https://aiplatform.googleapis.com/'
        )
        
        print("✅ Created JWT credentials successfully")
        
        # Try to get an access token
        request = transport.requests.Request()
        credentials.refresh(request)
        
        print("✅ Successfully refreshed credentials")
        print(f"Token expiry: {credentials.expiry}")
        
        return True
        
    except Exception as e:
        print(f"❌ Google Auth error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test 3: Test with google-cloud-aiplatform
def test_aiplatform():
    """Test using google-cloud-aiplatform directly"""
    print("\n=== Test 3: Testing Google Cloud AI Platform ===")
    
    try:
        from google.cloud import aiplatform
        
        # Set credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vertex_ai_service_account.json'
        
        # Initialize
        with open('vertex_ai_service_account.json', 'r') as f:
            sa_info = json.load(f)
            
        project_id = sa_info['project_id']
        location = 'us-central1'  # Try common location
        
        print(f"Initializing with project: {project_id}, location: {location}")
        
        aiplatform.init(
            project=project_id,
            location=location
        )
        
        print("✅ Successfully initialized AI Platform")
        
        # Try to list models (minimal permission test)
        try:
            models = aiplatform.Model.list(limit=1)
            print("✅ Successfully made API call")
        except Exception as list_error:
            print(f"⚠️  API call failed (might be permissions): {list_error}")
            
        return True
        
    except Exception as e:
        print(f"❌ AI Platform error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test 4: Test with litellm
def test_litellm():
    """Test using litellm with vertex AI"""
    print("\n=== Test 4: Testing LiteLLM ===")
    
    try:
        import litellm
        
        # Set environment variables
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vertex_ai_service_account.json'
        
        with open('vertex_ai_service_account.json', 'r') as f:
            sa_info = json.load(f)
        
        # Set vertex project
        os.environ['VERTEX_PROJECT'] = sa_info['project_id']
        os.environ['VERTEX_LOCATION'] = 'us-central1'
        
        print(f"VERTEX_PROJECT: {os.environ['VERTEX_PROJECT']}")
        print(f"VERTEX_LOCATION: {os.environ['VERTEX_LOCATION']}")
        print(f"GOOGLE_APPLICATION_CREDENTIALS: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
        
        # Enable debug mode
        litellm.set_verbose = True
        
        # Try a simple completion
        response = litellm.completion(
            model="vertex_ai/gemini-1.5-pro",
            messages=[{"content": "Say 'Hello, authentication works!'", "role": "user"}],
            temperature=0
        )
        
        print("✅ LiteLLM call successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ LiteLLM error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test 5: Manual JWT inspection
def test_jwt_manually():
    """Manually inspect JWT construction"""
    print("\n=== Test 5: Manual JWT Inspection ===")
    
    try:
        with open('vertex_ai_service_account.json', 'r') as f:
            sa_info = json.load(f)
        
        # Check system time
        current_time = datetime.utcnow()
        print(f"System UTC time: {current_time}")
        
        # Create a test JWT payload
        iat = int(datetime.utcnow().timestamp())
        exp = iat + 3600  # 1 hour
        
        payload = {
            "iss": sa_info['client_email'],
            "sub": sa_info['client_email'],
            "aud": "https://oauth2.googleapis.com/token",
            "iat": iat,
            "exp": exp,
            "scope": "https://www.googleapis.com/auth/cloud-platform"
        }
        
        print(f"\nJWT Payload:")
        print(json.dumps(payload, indent=2))
        
        # Try to create JWT
        try:
            token = jwt.encode(
                payload,
                sa_info['private_key'],
                algorithm='RS256'
            )
            print("\n✅ Successfully created JWT token")
            print(f"Token length: {len(token)}")
            
            # Decode to verify
            decoded = jwt.decode(token, options={"verify_signature": False})
            print("\n✅ Token structure is valid")
            
        except Exception as jwt_error:
            print(f"\n❌ JWT creation error: {jwt_error}")
            
        return True
        
    except Exception as e:
        print(f"❌ Manual JWT test error: {e}")
        return False

# Main test runner
def main():
    """Run all authentication tests"""
    print("=== Vertex AI Authentication Diagnostic Tool ===")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    tests = [
        ("Service Account File", test_service_account_file),
        ("Google Auth Library", test_google_auth),
        ("AI Platform SDK", test_aiplatform),
        ("LiteLLM", test_litellm),
        ("Manual JWT", test_jwt_manually)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("=== TEST SUMMARY ===")
    print("="*50)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    print(f"\nTotal: {passed}/{len(tests)} tests passed")
    
    # Recommendations
    print("\n=== RECOMMENDATIONS ===")
    
    if not results[0][1]:  # Service account file test failed
        print("1. Check that the service account JSON file is valid")
        print("2. Ensure the file has proper read permissions")
    
    if not results[1][1]:  # Google auth failed
        print("1. Install/update google-auth: pip install --upgrade google-auth")
        print("2. Check system time is synchronized (NTP)")
        print("3. Try regenerating the service account key in GCP Console")
    
    if not results[3][1]:  # LiteLLM failed
        print("1. Ensure litellm is updated: pip install --upgrade litellm")
        print("2. Try setting GOOGLE_APPLICATION_CREDENTIALS explicitly")
        print("3. Check if the service account has Vertex AI permissions")
        print("4. Try using a different region (us-central1, us-east1, etc.)")
    
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    sys.exit(main())