#!/bin/bash

echo "Installing cleanup utility dependencies..."

# Install ripgrep if not already installed
if ! command -v rg &> /dev/null; then
    echo "Installing ripgrep..."
    curl -LO https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb
    sudo dpkg -i ripgrep_13.0.0_amd64.deb
    rm ripgrep_13.0.0_amd64.deb
else
    echo "ripgrep already installed"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Dependencies installed successfully!"
