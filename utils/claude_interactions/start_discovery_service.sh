#!/bin/bash

# Start the Module Discovery Service

set -e

echo "🔍 Starting Module Discovery Service"
echo "==================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running installation..."
    ./install_dependencies.sh
fi

# Activate virtual environment
source .venv/bin/activate

# Start the discovery service
echo ""
echo "Starting discovery service on http://localhost:8888"
echo ""
echo "Available endpoints:"
echo "  GET  /modules                       - List all modules"
echo "  GET  /modules/{name}                - Get module details"
echo "  POST /modules                       - Register new module"
echo "  GET  /capabilities                  - List all capabilities"
echo "  GET  /capabilities/{name}/providers - Get capability providers"
echo "  GET  /discover/{module}/compatible  - Find compatible modules"
echo "  GET  /chain/{start}/{end}          - Find capability chains"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

# Run the discovery service
python discovery/module_registry.py