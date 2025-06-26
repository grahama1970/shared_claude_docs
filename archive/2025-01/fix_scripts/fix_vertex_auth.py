#!/usr/bin/env python3
"""
Module: fix_vertex_auth.py
Description: Fix Vertex AI authentication issues with multiple approaches

External Dependencies:
- google-auth: https://google-auth.readthedocs.io/
- google-cloud-aiplatform: https://cloud.google.com/python/docs/reference/aiplatform/latest
- litellm: https://docs.litellm.ai/

Sample Input:
>>> None (uses environment and service account)

Expected Output:
>>> Working authentication configuration

Example Usage:
>>> python fix_vertex_auth.py
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def fix_method_1_env_vars():
    """Method 1: Set all required environment variables"""
    print("\n=== Method 1: Environment Variables ===")
    
    sa_path = Path("vertex_ai_service_account.json").absolute()
    
    with open(sa_path, 'r') as f:
        sa_info = json.load(f)
    
    # Set all possible environment variables
    env_vars = {
        'GOOGLE_APPLICATION_CREDENTIALS': str(sa_path),
        'VERTEX_PROJECT': sa_info['project_id'],
        'VERTEX_LOCATION': 'us-central1',
        'GCP_PROJECT': sa_info['project_id'],
        'GOOGLE_CLOUD_PROJECT': sa_info['project_id'],
        'GCLOUD_PROJECT': sa_info['project_id']
    }
    
    print("Setting environment variables:")
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"  {key}={value}")
    
    # Test with litellm
    try:
        import litellm
        response = litellm.completion(
            model="vertex_ai/gemini-1.5-pro",
            messages=[{"content": "Say 'Hello'", "role": "user"}],
            temperature=0,
            max_tokens=10
        )
        print("✅ Method 1 SUCCESS: Environment variables work!")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
        return False

def fix_method_2_gcloud_auth():
    """Method 2: Use gcloud auth with service account"""
    print("\n=== Method 2: gcloud Auth ===")
    
    sa_path = Path("vertex_ai_service_account.json").absolute()
    
    with open(sa_path, 'r') as f:
        sa_info = json.load(f)
    
    try:
        # Activate service account
        cmd = [
            'gcloud', 'auth', 'activate-service-account',
            sa_info['client_email'],
            f'--key-file={sa_path}',
            f'--project={sa_info["project_id"]}'
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Service account activated successfully")
            
            # Set application default credentials
            cmd2 = ['gcloud', 'auth', 'application-default', 'login', '--impersonate-service-account', sa_info['client_email']]
            print(f"Running: {' '.join(cmd2)}")
            
            # Note: This might require interactive login
            print("⚠️  This method may require interactive authentication")
            
            return True
        else:
            print(f"❌ gcloud activation failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ gcloud CLI not found. Install with: https://cloud.google.com/sdk/docs/install")
        return False
    except Exception as e:
        print(f"❌ Method 2 failed: {e}")
        return False

def fix_method_3_oauth2_client():
    """Method 3: Use google-auth-oauthlib for OAuth2"""
    print("\n=== Method 3: Direct OAuth2 Client ===")
    
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
        
        sa_path = Path("vertex_ai_service_account.json").absolute()
        
        # Create credentials with specific scopes
        credentials = service_account.Credentials.from_service_account_file(
            str(sa_path),
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # Refresh the token
        request = Request()
        credentials.refresh(request)
        
        print("✅ OAuth2 credentials created and refreshed")
        print(f"Token valid: {credentials.valid}")
        print(f"Token expiry: {credentials.expiry}")
        
        # Save credentials for use
        os.environ['GOOGLE_OAUTH_ACCESS_TOKEN'] = credentials.token
        
        return True
        
    except Exception as e:
        print(f"❌ Method 3 failed: {e}")
        return False

def fix_method_4_litellm_direct():
    """Method 4: Configure litellm directly with credentials"""
    print("\n=== Method 4: Direct LiteLLM Configuration ===")
    
    try:
        import litellm
        from google.oauth2 import service_account
        
        sa_path = Path("vertex_ai_service_account.json").absolute()
        
        with open(sa_path, 'r') as f:
            sa_info = json.load(f)
        
        # Create credentials
        credentials = service_account.Credentials.from_service_account_file(
            str(sa_path),
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # Configure litellm
        litellm.vertex_project = sa_info['project_id']
        litellm.vertex_location = "us-central1"
        
        # Try with custom auth
        response = litellm.completion(
            model="vertex_ai/gemini-1.5-pro",
            messages=[{"content": "Say 'Hello'", "role": "user"}],
            temperature=0,
            max_tokens=10,
            vertex_credentials=credentials  # Pass credentials directly
        )
        
        print("✅ Method 4 SUCCESS: Direct credentials work!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Method 4 failed: {e}")
        return False

def fix_method_5_adc_setup():
    """Method 5: Set up Application Default Credentials"""
    print("\n=== Method 5: Application Default Credentials ===")
    
    sa_path = Path("vertex_ai_service_account.json").absolute()
    
    # Set up ADC
    adc_path = Path.home() / '.config' / 'gcloud' / 'application_default_credentials.json'
    adc_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Copy service account to ADC location
        import shutil
        shutil.copy2(sa_path, adc_path)
        print(f"✅ Copied service account to: {adc_path}")
        
        # Also set the environment variable
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(sa_path)
        
        # Test
        import litellm
        response = litellm.completion(
            model="vertex_ai/gemini-1.5-pro",
            messages=[{"content": "Say 'Hello'", "role": "user"}],
            temperature=0,
            max_tokens=10
        )
        
        print("✅ Method 5 SUCCESS: ADC setup works!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Method 5 failed: {e}")
        return False

def create_working_example():
    """Create a working example script"""
    print("\n=== Creating Working Example ===")
    
    example_code = '''#!/usr/bin/env python3
"""Working Vertex AI example with authentication fix"""

import os
import json
from pathlib import Path

# Set up authentication
sa_path = Path("vertex_ai_service_account.json").absolute()

with open(sa_path, 'r') as f:
    sa_info = json.load(f)

# Set all required environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(sa_path)
os.environ['VERTEX_PROJECT'] = sa_info['project_id']
os.environ['VERTEX_LOCATION'] = 'us-central1'

# Import litellm after setting env vars
import litellm

# Optional: Enable debug logging
# litellm.set_verbose = True

def test_gemini():
    """Test Gemini model"""
    try:
        response = litellm.completion(
            model="vertex_ai/gemini-1.5-pro",
            messages=[
                {"content": "What is 2+2? Reply with just the number.", "role": "user"}
            ],
            temperature=0,
            max_tokens=10
        )
        
        print(f"Success! Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        
        # Try alternative authentication
        try:
            from google.oauth2 import service_account
            
            credentials = service_account.Credentials.from_service_account_file(
                str(sa_path),
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            
            # Try again with explicit credentials
            response = litellm.completion(
                model="vertex_ai/gemini-1.5-pro",
                messages=[
                    {"content": "What is 2+2? Reply with just the number.", "role": "user"}
                ],
                temperature=0,
                max_tokens=10,
                vertex_credentials=credentials
            )
            
            print(f"Success with explicit credentials! Response: {response.choices[0].message.content}")
            return True
            
        except Exception as e2:
            print(f"Alternative auth also failed: {e2}")
            return False

if __name__ == "__main__":
    print(f"Project ID: {sa_info['project_id']}")
    print(f"Service Account: {sa_info['client_email']}")
    print(f"Testing Vertex AI connection...")
    
    if test_gemini():
        print("\\n✅ Vertex AI authentication is working!")
    else:
        print("\\n❌ Authentication still failing. Try:")
        print("1. Regenerate service account key in GCP Console")
        print("2. Check service account has Vertex AI User role")
        print("3. Try a different region (us-east1, europe-west4)")
'''
    
    with open('vertex_ai_working_example.py', 'w') as f:
        f.write(example_code)
    
    print("✅ Created vertex_ai_working_example.py")

def main():
    """Try all authentication fix methods"""
    print("=== Vertex AI Authentication Fix Tool ===\n")
    
    # Check if service account exists
    sa_path = Path("vertex_ai_service_account.json")
    if not sa_path.exists():
        print("❌ Service account file not found: vertex_ai_service_account.json")
        return 1
    
    # Try each method
    methods = [
        ("Environment Variables", fix_method_1_env_vars),
        ("gcloud Auth", fix_method_2_gcloud_auth),
        ("OAuth2 Client", fix_method_3_oauth2_client),
        ("Direct LiteLLM Config", fix_method_4_litellm_direct),
        ("Application Default Credentials", fix_method_5_adc_setup)
    ]
    
    success = False
    for method_name, method_func in methods:
        try:
            if method_func():
                success = True
                break
        except Exception as e:
            print(f"Method {method_name} exception: {e}")
    
    # Create working example
    create_working_example()
    
    # Final recommendations
    print("\n=== FINAL RECOMMENDATIONS ===")
    
    if success:
        print("✅ Authentication is now working!")
        print("\nTo use in your code:")
        print("1. Set environment variables before importing litellm")
        print("2. See vertex_ai_working_example.py for a complete example")
    else:
        print("❌ All automatic fixes failed. Manual steps required:")
        print("\n1. Go to GCP Console: https://console.cloud.google.com")
        print("2. Navigate to IAM & Admin > Service Accounts")
        print("3. Find your service account: 145786706699-compute@developer.gserviceaccount.com")
        print("4. Create a new key (Actions > Manage keys > Add key > Create new key)")
        print("5. Download the new JSON key and replace vertex_ai_service_account.json")
        print("\n6. Ensure the service account has these roles:")
        print("   - Vertex AI User")
        print("   - Service Account Token Creator")
        print("\n7. Enable these APIs in your project:")
        print("   - Vertex AI API")
        print("   - Cloud Resource Manager API")
        print("\n8. Try a different region if us-central1 doesn't work:")
        print("   - us-east1")
        print("   - europe-west4")
        print("   - asia-northeast1")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())