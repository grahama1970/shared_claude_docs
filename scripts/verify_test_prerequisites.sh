#!/bin/bash
# Granger Test Prerequisites Checker
# Verifies all requirements are met before running tests

set -euo pipefail

echo "🔍 Granger Test Prerequisites Check"
echo "=================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if all checks pass
ALL_PASSED=true

# Function to check command exists
check_command() {
    local cmd=$1
    local install_hint=$2
    
    if command -v "$cmd" &> /dev/null; then
        echo -e "${GREEN}✅ $cmd installed${NC}"
        return 0
    else
        echo -e "${RED}❌ $cmd not found${NC}"
        echo "   Install: $install_hint"
        ALL_PASSED=false
        return 1
    fi
}

# Function to check Python package
check_python_package() {
    local package=$1
    
    if python -c "import $package" 2>/dev/null; then
        echo -e "${GREEN}✅ Python package '$package' installed${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Python package '$package' not found${NC}"
        echo "   Install: uv add $package"
        return 1
    fi
}

# Function to check service
check_service() {
    local name=$1
    local port=$2
    local url=$3
    
    if lsof -i:$port | grep -q LISTEN; then
        echo -e "${GREEN}✅ $name running on port $port${NC}"
        
        # Try to hit health endpoint if URL provided
        if [ -n "$url" ]; then
            if curl -s -f "$url" > /dev/null 2>&1; then
                echo -e "${GREEN}   Health check passed${NC}"
            else
                echo -e "${YELLOW}   Health check failed (service may still be starting)${NC}"
            fi
        fi
        return 0
    else
        echo -e "${YELLOW}⚠️  $name not running on port $port${NC}"
        echo "   Some tests may fail without this service"
        return 1
    fi
}

# Function to check disk space
check_disk_space() {
    local path=$1
    local min_gb=$2
    
    local available_gb=$(df -BG "$path" | tail -1 | awk '{print $4}' | sed 's/G//')
    
    if [ "$available_gb" -ge "$min_gb" ]; then
        echo -e "${GREEN}✅ Disk space: ${available_gb}GB available in $path${NC}"
        return 0
    else
        echo -e "${RED}❌ Insufficient disk space: ${available_gb}GB available (need ${min_gb}GB)${NC}"
        ALL_PASSED=false
        return 1
    fi
}

echo -e "\n1. System Requirements"
echo "----------------------"

# Check required commands
check_command "git" "sudo apt install git"
check_command "tmux" "sudo apt install tmux"
check_command "python3" "sudo apt install python3"
check_command "uv" "curl -LsSf https://astral.sh/uv/install.sh | sh"
check_command "lsof" "sudo apt install lsof"
check_command "curl" "sudo apt install curl"
check_command "jq" "sudo apt install jq"

echo -e "\n2. Python Environment"
echo "--------------------"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
    echo -e "${GREEN}✅ Python version: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python version: $PYTHON_VERSION (need 3.9+)${NC}"
    ALL_PASSED=false
fi

# Check virtual environment
if [ -n "${VIRTUAL_ENV:-}" ]; then
    echo -e "${GREEN}✅ Virtual environment active: $VIRTUAL_ENV${NC}"
else
    echo -e "${YELLOW}⚠️  No virtual environment active${NC}"
    echo "   Activate with: source .venv/bin/activate"
fi

# Check key Python packages
check_python_package "pytest"
check_python_package "asyncio"
check_python_package "yaml"

echo -e "\n3. Granger Services"
echo "------------------"

# Check core services
check_service "Granger Hub" 8000 "http://localhost:8000/health"
check_service "ArangoDB" 8529 "http://localhost:8529/_api/version"
check_service "Test Reporter" 8002 "http://localhost:8002/status"

echo -e "\n4. System Resources"
echo "------------------"

# Check disk space
check_disk_space "/tmp" 5
check_disk_space "$HOME" 10

# Check memory
TOTAL_MEM=$(free -g | awk '/^Mem:/{print $2}')
AVAIL_MEM=$(free -g | awk '/^Mem:/{print $7}')

if [ "$AVAIL_MEM" -ge 4 ]; then
    echo -e "${GREEN}✅ Memory: ${AVAIL_MEM}GB available of ${TOTAL_MEM}GB total${NC}"
else
    echo -e "${YELLOW}⚠️  Low memory: ${AVAIL_MEM}GB available (recommend 4GB+)${NC}"
fi

echo -e "\n5. Git Configuration"
echo "-------------------"

# Check git user config
GIT_USER=$(git config --global user.name || echo "")
GIT_EMAIL=$(git config --global user.email || echo "")

if [ -n "$GIT_USER" ] && [ -n "$GIT_EMAIL" ]; then
    echo -e "${GREEN}✅ Git configured: $GIT_USER <$GIT_EMAIL>${NC}"
else
    echo -e "${YELLOW}⚠️  Git user not configured${NC}"
    echo "   Configure with:"
    echo "   git config --global user.name 'Your Name'"
    echo "   git config --global user.email 'your.email@example.com'"
fi

# Check for uncommitted changes
cd /home/graham/workspace/shared_claude_docs
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${GREEN}✅ No uncommitted changes${NC}"
else
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    echo "   Consider committing before testing"
fi

echo -e "\n6. Test Configuration"
echo "--------------------"

# Check for test config file
if [ -f "granger_test_tasks.yaml" ] || [ -f "docs/ideas/granger_test_tasks.yaml" ]; then
    echo -e "${GREEN}✅ Test configuration file found${NC}"
else
    echo -e "${RED}❌ Test configuration file not found${NC}"
    echo "   Expected: granger_test_tasks.yaml"
    ALL_PASSED=false
fi

# Check for orchestrator script
if [ -f "scripts/granger_test_orchestrator.py" ]; then
    echo -e "${GREEN}✅ Test orchestrator script found${NC}"
else
    echo -e "${RED}❌ Test orchestrator script not found${NC}"
    ALL_PASSED=false
fi

echo -e "\n=================================="

if $ALL_PASSED; then
    echo -e "${GREEN}✅ All prerequisites met! Ready to run tests.${NC}"
    exit 0
else
    echo -e "${RED}❌ Some prerequisites are missing. Please fix the issues above.${NC}"
    echo -e "\nFor optional services (marked with ⚠️), tests may still run but could fail."
    exit 1
fi