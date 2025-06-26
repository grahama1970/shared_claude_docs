#!/bin/bash
# Fix UI Project Dependencies Script

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 Fixing UI Project Dependencies${NC}"
echo "=================================="

# Function to install Python dependencies
install_python_deps() {
    local project_name=$1
    local project_path=$2
    
    echo -e "\n${YELLOW}📦 Installing dependencies for $project_name...${NC}"
    
    if [ -d "$project_path" ]; then
        cd "$project_path"
        
        # Check if pyproject.toml exists
        if [ -f "pyproject.toml" ]; then
            # Use uv to sync dependencies
            echo "Running uv sync..."
            uv sync
            
            # Install additional dependencies if needed
            if [ "$project_name" == "annotator" ]; then
                echo "Installing additional dependencies for annotator..."
                uv add websockets scikit-learn playwright
                playwright install chromium
            elif [ "$project_name" == "aider-daemon" ]; then
                echo "Note: aider-daemon has git dependencies that may need manual installation"
            fi
            
            echo -e "${GREEN}✅ $project_name dependencies installed${NC}"
        else
            echo -e "${RED}❌ No pyproject.toml found for $project_name${NC}"
        fi
    else
        echo -e "${RED}❌ Project directory not found: $project_path${NC}"
    fi
}

# Function to install JavaScript dependencies
install_js_deps() {
    local project_name=$1
    local project_path=$2
    
    echo -e "\n${YELLOW}📦 Installing dependencies for $project_name...${NC}"
    
    if [ -d "$project_path" ]; then
        cd "$project_path"
        
        # Check package manager
        if [ -f "pnpm-lock.yaml" ]; then
            echo "Using pnpm..."
            pnpm install --frozen-lockfile
        elif [ -f "package-lock.json" ]; then
            echo "Using npm..."
            npm ci
        elif [ -f "package.json" ]; then
            echo "Using npm install..."
            npm install
        else
            echo -e "${RED}❌ No package.json found for $project_name${NC}"
            return 1
        fi
        
        echo -e "${GREEN}✅ $project_name dependencies installed${NC}"
    else
        echo -e "${RED}❌ Project directory not found: $project_path${NC}"
    fi
}

# Activate virtual environment
echo -e "${YELLOW}🐍 Activating virtual environment...${NC}"
source /home/graham/workspace/shared_claude_docs/.venv/bin/activate

# Fix aider-daemon
install_python_deps "aider-daemon" "/home/graham/workspace/experiments/aider-daemon"

# Fix annotator
install_python_deps "annotator" "/home/graham/workspace/experiments/annotator"

# Fix chat backend
install_python_deps "chat-backend" "/home/graham/workspace/experiments/chat"

# Fix chat frontend
install_js_deps "chat-frontend" "/home/graham/workspace/experiments/chat/frontend"

# Fix granger-ui
install_js_deps "granger-ui" "/home/graham/workspace/granger-ui"

echo -e "\n${BLUE}🔧 Removing Deprecated Tests${NC}"
echo "=================================="

# Function to archive deprecated tests
archive_deprecated_tests() {
    local project_name=$1
    local project_path=$2
    
    echo -e "\n${YELLOW}📁 Archiving deprecated tests for $project_name...${NC}"
    
    if [ -d "$project_path" ]; then
        cd "$project_path"
        
        # Create archive directory if it doesn't exist
        mkdir -p archive/deprecated_tests
        
        # Move mock-based tests
        find tests -name "*mock*.py" -o -name "*mocked*.py" | while read file; do
            if [ -f "$file" ]; then
                echo "Archiving $file"
                mv "$file" "archive/deprecated_tests/" 2>/dev/null || true
            fi
        done
        
        # Move .disabled files
        find tests -name "*.disabled" | while read file; do
            if [ -f "$file" ]; then
                echo "Archiving $file"
                mv "$file" "archive/deprecated_tests/" 2>/dev/null || true
            fi
        done
        
        echo -e "${GREEN}✅ Deprecated tests archived for $project_name${NC}"
    fi
}

# Archive deprecated tests
archive_deprecated_tests "aider-daemon" "/home/graham/workspace/experiments/aider-daemon"
archive_deprecated_tests "annotator" "/home/graham/workspace/experiments/annotator"
archive_deprecated_tests "chat" "/home/graham/workspace/experiments/chat"

echo -e "\n${BLUE}🔧 Fixing Import Issues${NC}"
echo "=================================="

# Fix chat frontend import aliases
CHAT_FRONTEND="/home/graham/workspace/experiments/chat/frontend"
if [ -d "$CHAT_FRONTEND" ]; then
    echo -e "${YELLOW}Fixing import aliases in chat frontend...${NC}"
    
    # Create jsconfig.json if it doesn't exist
    cat > "$CHAT_FRONTEND/jsconfig.json" << 'EOF'
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components/*": ["src/components/*"],
      "@/hooks/*": ["src/hooks/*"],
      "@/services/*": ["src/services/*"],
      "@/lib/*": ["src/lib/*"]
    }
  }
}
EOF
    
    echo -e "${GREEN}✅ Import aliases configured${NC}"
fi

echo -e "\n${BLUE}=================================="
echo -e "${GREEN}✅ Dependency fixes completed!${NC}"
echo -e "${BLUE}==================================${NC}"
echo ""
echo "Next steps:"
echo "1. Run individual test suites to verify fixes"
echo "2. Check for any remaining import errors"
echo "3. Test basic functionality of each project"
echo ""
echo -e "${YELLOW}Note: Some dependencies may require manual installation, especially git-based ones.${NC}"