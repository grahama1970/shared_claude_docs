#!/usr/bin/env python3
"""Hunt for real bugs in Granger modules"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

class GrangerBugHunter:
    def __init__(self):
        self.bugs_found = []
        self.modules_tested = set()
        
    def hunt_module_bugs(self, module_name, module_path):
        """Hunt for bugs in a specific module"""
        bugs = []
        self.modules_tested.add(module_name)
        
        print(f"\n🔍 Hunting bugs in {module_name}...")
        
        # Check for syntax errors in __init__.py files
        init_files = list(module_path.rglob("__init__.py"))
        for init_file in init_files:
            try:
                with open(init_file, 'r') as f:
                    content = f.read()
                # Check for module docstring in wrong place
                if "Module:" in content and not content.strip().startswith('"""'):
                    bugs.append({
                        "module": module_name,
                        "file": str(init_file),
                        "bug": "Module docstring not at start of file",
                        "severity": "HIGH"
                    })
            except Exception as e:
                pass
        
        # Test imports
        sys.path.insert(0, str(module_path / "src"))
        try:
            module = __import__(module_name)
            print(f"  ✅ Import successful: {module_name}")
        except SyntaxError as e:
            bugs.append({
                "module": module_name,
                "bug": f"Syntax error: {e}",
                "severity": "CRITICAL",
                "file": str(e.filename) if e.filename else "unknown"
            })
        except ImportError as e:
            bugs.append({
                "module": module_name,
                "bug": f"Import error: {e}",
                "severity": "HIGH"
            })
        
        return bugs
    
    def hunt_all_bugs(self):
        """Hunt for bugs across all modules"""
        print("🎯 GRANGER BUG HUNTER")
        print("="*60)
        
        modules_base = Path("/home/graham/workspace/experiments")
        modules = ["sparta", "arangodb", "marker", "youtube_transcripts"]
        
        for module_name in modules:
            module_path = modules_base / module_name
            if module_path.exists():
                bugs = self.hunt_module_bugs(module_name, module_path)
                self.bugs_found.extend(bugs)
            else:
                print(f"  ❌ Module not found: {module_name}")
        
        # Generate report
        print("\n" + "="*60)
        print(f"🐛 Total Bugs Found: {len(self.bugs_found)}")
        print(f"📦 Modules Tested: {len(self.modules_tested)}")
        
        if self.bugs_found:
            print("\n🚨 BUGS FOUND:")
            for bug in self.bugs_found:
                print(f"  - {bug['module']}: {bug['bug']} [{bug['severity']}]")
                if 'file' in bug:
                    print(f"    File: {bug['file']}")
        
        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "bugs_found": len(self.bugs_found),
            "modules_tested": len(self.modules_tested),
            "bugs": self.bugs_found
        }
        
        report_path = Path("bug_hunt_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Report saved to: {report_path}")
        
        return len(self.bugs_found)

if __name__ == "__main__":
    hunter = GrangerBugHunter()
    bugs = hunter.hunt_all_bugs()
    exit(1 if bugs > 0 else 0)