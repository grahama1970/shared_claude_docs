#!/bin/bash
# Alternative setup script using venv instead of uv

set -e

echo "Setting up Shared Claude Documentation System with venv..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install package in development mode
echo "Installing package and dependencies..."
pip install -e .

# Install development dependencies
echo "Installing development dependencies..."
pip install -e ".[dev]"

# Create .env from template if it doesn't exist
if [ ! -f .env ]; then
    echo "Note: .env file already exists"
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
