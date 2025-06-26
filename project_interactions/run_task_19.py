#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""Run Task #19 implementation"""

import sys
sys.path.insert(0, "/home/graham/workspace/shared_claude_docs")

# Execute the module
exec(open("/home/graham/workspace/shared_claude_docs/project_interactions/contradiction_detection/contradiction_detection_interaction.py").read())

print("\n✅ Task #19 Module executed successfully")
print("   Contradiction detection across sources demonstrated")
print("\nProceeding to Task #20...")