#!/usr/bin/env python3
"""Extract all 67 scenarios from the markdown file."""

import re
from pathlib import Path

def extract_scenarios():
    """Extract all scenarios from the bug hunter document."""
    doc_path = Path('/home/graham/workspace/shared_claude_docs/project_interactions/GRANGER_BUG_HUNTER_SCENARIOS_COMPLETE.md')
    content = doc_path.read_text()
    
    scenarios = []
    current_scenario = None
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Match scenario headers
        if line.startswith('## Scenario '):
            # Save previous scenario
            if current_scenario:
                scenarios.append(current_scenario)
            
            # Extract scenario number and name
            match = re.match(r'## Scenario (\d+): (.+)', line)
            if match:
                scenario_num = int(match.group(1))
                scenario_name = match.group(2)
                
                current_scenario = {
                    'number': scenario_num,
                    'name': scenario_name,
                    'modules': [],
                    'bug_target': '',
                    'expected_result': '',
                    'level': None
                }
        
        # Extract fields
        elif current_scenario:
            if line.startswith('**Modules**:'):
                modules_str = line.replace('**Modules**:', '').strip()
                current_scenario['modules'] = [m.strip() for m in modules_str.split(',')]
            
            elif line.startswith('**Bug Target**:'):
                current_scenario['bug_target'] = line.replace('**Bug Target**:', '').strip()
            
            elif line.startswith('**Expected Result**:'):
                # Capture multi-line expected result
                expected_lines = []
                j = i + 1
                while j < len(lines) and not lines[j].startswith('##') and not lines[j].startswith('**'):
                    if lines[j].strip().startswith('-'):
                        expected_lines.append(lines[j].strip())
                    j += 1
                current_scenario['expected_result'] = '\n'.join(expected_lines)
        
        # Detect level
        if line.startswith('# Level 0:'):
            level = 0
        elif line.startswith('# Level 1:'):
            level = 1
        elif line.startswith('# Level 2:'):
            level = 2
        elif line.startswith('# Level 3:'):
            level = 3
        elif line.startswith('# Level 4:'):
            level = 4
        elif line.startswith('# Bug Hunter Unique'):
            level = 5
    
    # Don't forget the last scenario
    if current_scenario:
        scenarios.append(current_scenario)
    
    # Assign levels
    current_level = 0
    for scenario in scenarios:
        if scenario['number'] <= 10:
            scenario['level'] = 0
        elif scenario['number'] <= 20:
            scenario['level'] = 1
        elif scenario['number'] <= 30:
            scenario['level'] = 2
        elif scenario['number'] <= 42:
            scenario['level'] = 3
        else:
            scenario['level'] = 5  # Bug hunter unique
    
    return scenarios

# Extract and save
scenarios = extract_scenarios()
print(f"Extracted {len(scenarios)} scenarios")

# Save as Python module
with open('all_scenarios.py', 'w') as f:
    f.write('"""All 67 Bug Hunter Scenarios."""\n\n')
    f.write('SCENARIOS = [\n')
    for s in scenarios:
        f.write('    {\n')
        f.write(f'        "number": {s["number"]},\n')
        f.write(f'        "name": {repr(s["name"])},\n')
        f.write(f'        "modules": {s["modules"]},\n')
        f.write(f'        "bug_target": {repr(s["bug_target"])},\n')
        f.write(f'        "expected_result": {repr(s["expected_result"])},\n')
        f.write(f'        "level": {s["level"]}\n')
        f.write('    },\n')
    f.write(']\n')

print(f"Saved to all_scenarios.py")

# Show summary
levels = {}
for s in scenarios:
    level = s['level']
    if level not in levels:
        levels[level] = []
    levels[level].append(s['number'])

print("\nScenarios by level:")
for level in sorted(levels.keys()):
    print(f"  Level {level}: {len(levels[level])} scenarios ({levels[level][0]}-{levels[level][-1]})")