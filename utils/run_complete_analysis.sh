#!/bin/bash

# Run Complete Analysis with Claude Interactions
# This script runs all analysis tools and generates comprehensive reports

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🎯 Complete Big Picture Analysis & Testing Suite${NC}"
echo "================================================"
echo ""
echo "This comprehensive analysis includes:"
echo "  1. Basic project analysis"
echo "  2. Enhanced security & metrics analysis"
echo "  3. Claude interaction test generation"
echo "  4. Multi-module orchestration scenarios"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Create all necessary directories
echo -e "${YELLOW}Setting up directories...${NC}"
mkdir -p docs/big_picture/claude_interaction_tests
mkdir -p docs/big_picture/reports
mkdir -p docs/big_picture/visualizations

# Step 1: Run basic analysis
echo -e "\n${BLUE}Step 1: Running basic analysis...${NC}"
python3 utils/big_picture_analyzer.py

# Step 2: Run enhanced analysis with security and metrics
echo -e "\n${BLUE}Step 2: Running enhanced analysis...${NC}"
# Check and install dependencies if needed
if ! command -v radon &> /dev/null; then
    echo "Installing analysis tools..."
    pip install radon bandit pip-audit safety
fi
python3 utils/enhanced_big_picture_analyzer.py

# Step 3: Generate Claude interaction scenarios
echo -e "\n${BLUE}Step 3: Generating Claude interaction scenarios...${NC}"
cd docs/big_picture
python3 ../../utils/claude_interaction_orchestrator.py --complexity random --output claude_interaction_tests
cd ../..

# Step 4: Generate summary report
echo -e "\n${BLUE}Step 4: Generating comprehensive summary...${NC}"

python3 -c "
import json
from datetime import datetime
from pathlib import Path

# Gather all reports
basic_analyses = list(Path('docs/big_picture').glob('*_Describe_*.md'))
interaction_tests = list(Path('docs/big_picture/claude_interaction_tests').glob('*.py'))

summary = {
    'timestamp': datetime.now().isoformat(),
    'analyses': {
        'basic': len([f for f in basic_analyses if 'ENHANCED' not in f.name]),
        'enhanced': len([f for f in basic_analyses if 'ENHANCED' in f.name]),
        'interaction_tests': len(interaction_tests)
    },
    'projects_analyzed': len(basic_analyses) // 2,  # Divided by 2 for basic + enhanced
    'health_scores': {},
    'security_issues': {},
    'test_scenarios': []
}

# Extract health scores from enhanced analyses
for analysis_file in basic_analyses:
    if analysis_file.exists():
        content = analysis_file.read_text()
        # Extract project name
        project = analysis_file.stem.split('_')[-1]
        
        # Extract health score
        import re
        health_match = re.search(r'Overall Health Score: (\d+)/100', content)
        if health_match:
            summary['health_scores'][project] = int(health_match.group(1))
        
        # Check for security issues
        if 'vulnerabilities found' in content:
            vuln_match = re.search(r'Found (\d+) vulnerabilities', content)
            if vuln_match:
                summary['security_issues'][project] = int(vuln_match.group(1))

# List test scenarios
for test_file in interaction_tests[:5]:  # First 5
    summary['test_scenarios'].append(test_file.name)

# Save summary
summary_file = Path('docs/big_picture/ANALYSIS_SUMMARY.json')
with open(summary_file, 'w') as f:
    json.dump(summary, f, indent=2)

print(f'📊 Summary saved to: {summary_file}')

# Generate markdown summary
md_summary = f'''# Big Picture Analysis Summary

Generated: {summary['timestamp']}

## Analysis Results

- **Projects Analyzed**: {summary['projects_analyzed']}
- **Basic Analyses**: {summary['analyses']['basic']}
- **Enhanced Analyses**: {summary['analyses']['enhanced']}
- **Interaction Tests Generated**: {summary['analyses']['interaction_tests']}

## Health Scores

| Project | Score | Status |
|---------|-------|--------|
'''

for project, score in sorted(summary['health_scores'].items(), key=lambda x: x[1], reverse=True):
    emoji = '🟢' if score >= 90 else '🟡' if score >= 70 else '🟠' if score >= 50 else '🔴'
    md_summary += f'| {project} | {score}/100 | {emoji} |\n'

if summary['security_issues']:
    md_summary += '''

## Security Issues Found

| Project | Vulnerabilities |
|---------|----------------|
'''
    for project, count in sorted(summary['security_issues'].items(), key=lambda x: x[1], reverse=True):
        md_summary += f'| {project} | {count} |\n'

md_summary += '''

## Generated Test Scenarios

'''
for scenario in summary['test_scenarios']:
    md_summary += f'- {scenario}\n'

md_summary += '''

## Next Steps

1. Address security vulnerabilities in affected projects
2. Improve health scores for projects below 70
3. Run generated interaction tests
4. Review and update documentation based on findings
'''

summary_md = Path('docs/big_picture/ANALYSIS_SUMMARY.md')
with open(summary_md, 'w') as f:
    f.write(md_summary)

print(f'📄 Markdown summary saved to: {summary_md}')
"

# Step 5: Generate interactive dashboard
echo -e "\n${BLUE}Step 5: Generating interactive dashboard...${NC}"
python3 utils/interaction_dashboard.py

# Display summary
echo -e "\n${GREEN}✅ Complete analysis finished!${NC}"
echo ""
echo "📁 Results available in:"
echo "  - Basic analyses: docs/big_picture/00*_Describe_*.md"
echo "  - Enhanced analyses: docs/big_picture/00*_Describe_*.md (with metrics)"
echo "  - Interaction tests: docs/big_picture/claude_interaction_tests/"
echo "  - Summary report: docs/big_picture/ANALYSIS_SUMMARY.md"
echo "  - Interactive dashboard: docs/big_picture/interaction_dashboard.html"
echo ""
echo "🌐 To view the dashboard:"
echo "  open docs/big_picture/interaction_dashboard.html"
echo ""
echo "🧪 To run interaction tests:"
echo "  cd docs/big_picture/claude_interaction_tests"
echo "  ./run_suite_*.sh"
echo ""
echo "🔄 For continuous testing:"
echo "  python3 utils/claude_interaction_orchestrator.py --continuous --interval 30"