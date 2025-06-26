#!/bin/bash

# Install Dependencies for Claude Module Interactions

set -e

echo "🚀 Installing Claude Module Interactions Dependencies"
echo "=================================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install core dependencies
echo "Installing core dependencies..."
pip install aiohttp asyncio networkx matplotlib jsonschema

# Install visualization dependencies
echo "Installing visualization dependencies..."
pip install plotly pandas seaborn

# Install testing dependencies
echo "Installing testing dependencies..."
pip install pytest pytest-asyncio pytest-cov

# Install optional dependencies for enhanced features
echo "Installing optional dependencies..."
pip install pyyaml python-dotenv rich tqdm

# Create necessary directories
echo "Creating directory structure..."
mkdir -p discovery
mkdir -p orchestrator
mkdir -p scenarios
mkdir -p protocols
mkdir -p visualizations
mkdir -p reports
mkdir -p tests

# Create __init__.py files
touch discovery/__init__.py
touch orchestrator/__init__.py
touch scenarios/__init__.py
touch protocols/__init__.py
touch tests/__init__.py

echo ""
echo "✅ Installation complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To start the discovery service, run:"
echo "  ./start_discovery_service.sh"