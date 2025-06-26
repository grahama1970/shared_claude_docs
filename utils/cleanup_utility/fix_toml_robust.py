#!/usr/bin/env python3
"""
Robust TOML syntax fixer
Handles various quote issues in pyproject.toml files
"""

import os
import sys
import re
from pathlib import Path
import json
import shutil
from datetime import datetime

class RobustTOMLFixer:
    """Fix various TOML syntax errors"""
    
    def __init__(self, config_file='cleanup_config_localhost.json'):
        config_path = Path(__file__).parent / config_file
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.fixed_count = 0
        self.backup_dir = Path(__file__).parent / 'toml_backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def fix_toml_content(self, content: str) -> str:
        """Apply multiple fixes to TOML content"""
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            original_line = line
            
            # Skip comments and empty lines
            if line.strip().startswith('#') or not line.strip():
                fixed_lines.append(line)
                continue
            
            # Fix 1: Remove trailing quotes after closing brackets
            # Example: authors = [{ name = "..." }]" -> authors = [{ name = "..." }]
            line = re.sub(r'(\])\s*"(\s*(?:#.*)?$)', r'\1\2', line)
            
            # Fix 2: Remove trailing quotes after section headers
            # Example: [tool.pytest]" -> [tool.pytest]
            line = re.sub(r'^(\s*\[[^\]]+\])\s*"(\s*(?:#.*)?$)', r'\1\2', line)
            
            # Fix 3: Fix unclosed quotes in dependencies with brackets
            # Example: "package[extra]" -> "package[extra]"
            if '=' in line and '[' in line and ']' in line:
                # Check if we have a dependency line
                if re.search(r'=\s*["\'].*\[.*\]', line):
                    # Count quotes before and after the bracket
                    before_bracket = line[:line.index('[')]
                    after_bracket = line[line.index(']'):]
                    
                    # If odd number of quotes total, likely missing closing quote
                    if line.count('"') % 2 != 0 or line.count("'") % 2 != 0:
                        # Add closing quote if missing
                        if '"' in line and not re.search(r'\]"', line):
                            line = re.sub(r'(\[[^\]]+\])(?=\s*(?:,|$))', r'\1"', line)
            
            # Fix 4: Remove double quotes at end of strings
            # Example: "dependency>=1.0.0"" -> "dependency>=1.0.0"
            line = re.sub(r'""(\s*(?:,|]|}|$))', r'"\1', line)
            line = re.sub(r"''(\s*(?:,|]|}|$))", r"'\1", line)
            
            # Fix 5: Fix section headers that are improperly quoted
            # Example: "[tool.poetry]" -> [tool.poetry]
            line = re.sub(r'^"(\[.*\])"$', r'\1', line)
            
            # Fix 6: Ensure arrays/lists are properly closed
            # If line starts an array but doesn't close it, and next line doesn't continue it
            if '[' in line and ']' not in line and '=' in line:
                # Check if this looks like a single-line array that's missing closing ]
                if i + 1 < len(lines) and not lines[i + 1].strip().startswith('"'):
                    if line.rstrip().endswith(','):
                        line = line.rstrip()[:-1] + '],'
                    else:
                        line = line + ']'
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def validate_and_fix_toml(self, toml_path: Path) -> tuple[bool, str]:
        """Validate TOML and return (is_valid, error_message)"""
        try:
            import toml
            with open(toml_path, 'r') as f:
                content = f.read()
            
            # Try to parse
            try:
                toml.loads(content)
                return True, ""
            except toml.TomlDecodeError as e:
                # Apply fixes
                fixed_content = self.fix_toml_content(content)
                
                # Try to parse again
                try:
                    toml.loads(fixed_content)
                    # Save the fixed content
                    with open(toml_path, 'w') as f:
                        f.write(fixed_content)
                    return True, "Fixed"
                except toml.TomlDecodeError as e2:
                    return False, str(e2)
                    
        except Exception as e:
            return False, str(e)
    
    def fix_project_toml(self, project_path: Path) -> bool:
        """Fix TOML file for a single project"""
        project_name = project_path.name
        toml_path = project_path / 'pyproject.toml'
        
        if not toml_path.exists():
            print(f"  ⚠️  No pyproject.toml found in {project_name}")
            return False
        
        try:
            # Create backup
            backup_path = self.backup_dir / f"{project_name}_pyproject.toml.bak"
            shutil.copy2(toml_path, backup_path)
            
            # Check and fix
            is_valid, message = self.validate_and_fix_toml(toml_path)
            
            if is_valid:
                if message == "Fixed":
                    print(f"  ✅ Fixed {project_name}/pyproject.toml")
                    self.fixed_count += 1
                else:
                    print(f"  ✓ {project_name}/pyproject.toml is already valid")
                return True
            else:
                # Restore backup
                shutil.copy2(backup_path, toml_path)
                print(f"  ❌ Could not fix {project_name}: {message[:80]}")
                
                # Show the problematic line if possible
                if "line" in message:
                    try:
                        line_match = re.search(r'line (\d+)', message)
                        if line_match:
                            line_num = int(line_match.group(1))
                            with open(toml_path, 'r') as f:
                                lines = f.readlines()
                            if 0 < line_num <= len(lines):
                                print(f"     Line {line_num}: {lines[line_num-1].strip()}")
                    except:
                        pass
                
                return False
                
        except Exception as e:
            print(f"  ❌ Error processing {project_name}: {e}")
            return False
    
    def run(self):
        """Fix TOML files in all projects"""
        print("🔧 Robust TOML Syntax Fixer")
        print(f"📁 Backups will be saved to: {self.backup_dir}")
        print("")
        
        # Ensure toml package is available
        try:
            import toml
        except ImportError:
            print("Installing toml package...")
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'toml'])
            import toml
        
        success_count = 0
        failed_projects = []
        
        for project_path in self.config['projects']:
            project_path = Path(project_path)
            project_name = project_path.name
            
            print(f"\n🔍 Processing {project_name}...")
            
            if self.fix_project_toml(project_path):
                success_count += 1
            else:
                failed_projects.append(project_name)
        
        print(f"\n\n{'='*60}")
        print("📊 TOML FIX SUMMARY")
        print(f"{'='*60}")
        print(f"Total projects: {len(self.config['projects'])}")
        print(f"Successfully processed: {success_count}")
        print(f"Files fixed: {self.fixed_count}")
        print(f"Failed to fix: {len(failed_projects)}")
        
        if failed_projects:
            print(f"\n❌ Failed projects:")
            for proj in failed_projects:
                print(f"  - {proj}")
            print("\nThese projects may need manual intervention.")
        
        if self.fixed_count > 0:
            print(f"\n✅ Fixed {self.fixed_count} TOML files!")
            print("You can now run the test suite or cleanup utilities.")
        
        print(f"\n📁 All backups saved to: {self.backup_dir}")
        
        return 0 if len(failed_projects) == 0 else 1

def main():
    """Run the robust TOML fixer"""
    try:
        fixer = RobustTOMLFixer()
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