#!/bin/bash

# Manual TOML fixes for remaining projects
# Run this to see the specific issues and suggested fixes

echo "🔧 Manual TOML Fix Guide"
echo "========================"
echo ""
echo "The following projects need manual TOML fixes:"
echo ""

# Function to show TOML issue
show_issue() {
    local project=$1
    local issue=$2
    local line=$3
    local fix=$4
    
    echo "📁 $project"
    echo "   Issue: $issue"
    echo "   Line: $line" 
    echo "   Fix: $fix"
    echo ""
}

# List issues and fixes
show_issue "arangodb" \
    "Invalid character ',' in key name at line 11" \
    '"python-dotenv>=1.0.0",' \
    'Remove trailing comma or check for missing closing bracket'

show_issue "claude_max_proxy" \
    "Unbalanced quotes at line 29" \
    '"uvicorn[standard]"' \
    'Check if line needs closing quote or has extra quote'

show_issue "arxiv-mcp-server" \
    "Key group not on a line by itself at line 14" \
    '[[project.authors]]]' \
    'Should be [[project.authors]] (remove extra bracket)'

show_issue "claude-test-reporter" \
    "Invalid character 'n' in key name at line 13" \
    '{ name = "Your Name", email = "your.email@example.com" }' \
    'Check for syntax errors in author definition'

show_issue "unsloth_wip" \
    "Key name without value at line 14" \
    ']"' \
    'Remove the extra quote after closing bracket'

show_issue "mcp-screenshot" \
    "Unbalanced quotes at line 12" \
    '"typer[all]"' \
    'Check for missing or extra quotes'

echo "To fix each project:"
echo "1. cd /path/to/project"
echo "2. cp pyproject.toml pyproject.toml.bak"
echo "3. Edit pyproject.toml with the suggested fix"
echo "4. Validate with: python -c \"import toml; toml.load(open('pyproject.toml'))\""
echo ""
echo "Example vim commands:"
echo "  :set number      # Show line numbers"
echo "  :14              # Go to line 14"
echo "  :%s/]]/]/g       # Replace ]] with ]"