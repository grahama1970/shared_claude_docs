#!/usr/bin/env python3
"""
Fix TOML syntax errors in pyproject.toml files
Focuses on fixing unbalanced quotes which is the most common issue
"""

import os
import sys
import re
from pathlib import Path
import json
import shutil
from datetime import datetime

class TOMLFixer:
    """Fix common TOML syntax errors"""
    
    def __init__(self, config_file='cleanup_config_localhost.json'):
        config_path = Path(__file__).parent / config_file
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.fixed_count = 0
        self.backup_dir = Path(__file__).parent / 'toml_backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def fix_unbalanced_quotes(self, content: str) -> str:
        """Fix unbalanced quotes in TOML content"""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Skip comments and empty lines
            if line.strip().startswith('#') or not line.strip():
                fixed_lines.append(line)
                continue
            
            # Fix lines that end with quotes inside brackets without closing quote
            # Example: "package[extra]" -> "package[extra]"
            if re.search(r'"[^"]+\[[^\]]+\](?!")(?=\s*,|\s*$)', line):
                line = re.sub(r'"([^"]+\[[^\]]+\])(?!")(?=\s*,|\s*$)', r'"\1"', line)
            
            # Fix lines with extra quotes at the end
            # Example: "dependency>=1.0.0"" -> "dependency>=1.0.0"
            if line.count('"') % 2 != 0 and line.rstrip().endswith('"'):
                # Check if it's likely an extra quote
                if re.search(r'"\s*$', line) and re.search(r'=\s*"[^"]+""$', line):
                    line = line.rstrip()[:-1]
            
            # Fix section headers with trailing quotes
            # Example: [tool.pytest]" -> [tool.pytest]
            if re.match(r'^\s*\[[^\]]+\]"?\s*$', line):
                line = re.sub(r'"\s*$', '', line)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_project_toml(self, project_path: Path) -> bool:
        """Fix TOML file for a single project"""
        project_name = project_path.name
        toml_path = project_path / 'pyproject.toml'
        
        if not toml_path.exists():
            print(f"  ⚠️  No pyproject.toml found in {project_name}")
            return False
        
        try:
            # Read current content
            with open(toml_path, 'r') as f:
                original_content = f.read()
            
            # Create backup
            backup_path = self.backup_dir / f"{project_name}_pyproject.toml.bak"
            shutil.copy2(toml_path, backup_path)
            
            # Fix content
            fixed_content = self.fix_unbalanced_quotes(original_content)
            
            # Only write if changed
            if fixed_content != original_content:
                with open(toml_path, 'w') as f:
                    f.write(fixed_content)
                
                # Verify it's now valid TOML
                try:
                    import toml
                    with open(toml_path, 'r') as f:
                        toml.load(f)
                    print(f"  ✅ Fixed {project_name}/pyproject.toml")
                    self.fixed_count += 1
                    return True
                except Exception as e:
                    # Restore backup if still invalid
                    shutil.copy2(backup_path, toml_path)
                    print(f"  ❌ Failed to fix {project_name}: {str(e)[:80]}")
                    return False
            else:
                print(f"  ✓ {project_name}/pyproject.toml is already valid")
                return True
                
        except Exception as e:
            print(f"  ❌ Error processing {project_name}: {e}")
            return False
    
    def run(self):
        """Fix TOML files in all projects"""
        print("🔧 Fixing TOML syntax errors in all projects")
        print(f"📁 Backups will be saved to: {self.backup_dir}")
        print("")
        
        # First, ensure toml package is available
        try:
            import toml
        except ImportError:
            print("Installing toml package...")
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'toml'])
            import toml
        
        success_count = 0
        
        for project_path in self.config['projects']:
            project_path = Path(project_path)
            project_name = project_path.name
            
            print(f"\n🔍 Checking {project_name}...")
            
            if self.fix_project_toml(project_path):
                success_count += 1
        
        print(f"\n\n{'='*60}")
        print("📊 TOML FIX SUMMARY")
        print(f"{'='*60}")
        print(f"Total projects: {len(self.config['projects'])}")
        print(f"Successfully processed: {success_count}")
        print(f"Files fixed: {self.fixed_count}")
        print(f"Backups saved to: {self.backup_dir}")
        
        if self.fixed_count > 0:
            print("\n✅ TOML syntax errors have been fixed!")
            print("You can now run the test suite or cleanup utilities.")
        
        return 0 if success_count == len(self.config['projects']) else 1

def main():
    """Fix TOML syntax errors"""
    try:
        fixer = TOMLFixer()
        sys.exit(fixer.run())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()