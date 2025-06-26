#!/bin/bash
# Setup script for shared-claude-docs

set -e

echo "Setting up Shared Claude Documentation System..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment with Python 3.10.11..."
uv venv --python=3.10.11 .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install package in development mode
echo "Installing package and dependencies..."
uv pip install -e .

# Install development dependencies
echo "Installing development dependencies..."
uv pip install -e ".[dev]"

# Create .env from template if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env 2>/dev/null || echo "Note: No .env.example found, using existing .env"
fi

# Initialize git repository if not already initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Shared Claude Documentation System"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your configuration"
echo "2. Run 'source .venv/bin/activate' to activate the environment"
echo "3. Run 'claude-docs --help' to see available commands"
echo "4. Run 'validate-projects' to check project compliance"
echo ""
