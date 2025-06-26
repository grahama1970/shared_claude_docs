#!/bin/bash
# Start all required Granger services for testing

echo "🚀 Starting Granger Ecosystem Services"
echo "======================================"

# Check if ArangoDB is running
if ! nc -z localhost 8529 2>/dev/null; then
    echo "📦 Starting ArangoDB on localhost:8529..."
    docker run -d --name arangodb-granger \
        -p 8529:8529 \
        -e ARANGO_NO_AUTH=1 \
        arangodb/arangodb:latest
    
    # Wait for ArangoDB to be ready
    echo "Waiting for ArangoDB to be ready..."
    for i in {1..30}; do
        if nc -z localhost 8529 2>/dev/null; then
            echo "✅ ArangoDB is ready!"
            break
        fi
        sleep 1
    done
else
    echo "✅ ArangoDB already running on localhost:8529"
fi

# Start GrangerHub
echo -e "\n📡 Starting GrangerHub on localhost:8000..."
cd /home/graham/workspace/experiments/granger_hub

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "❌ GrangerHub venv not found. Creating..."
    uv venv --python=3.10.11
    uv sync
fi

# Kill any existing process on port 8000
lsof -ti:8000 | xargs -r kill -9 2>/dev/null

# Start in background
source .venv/bin/activate
nohup python -m granger_hub.server > granger_hub.log 2>&1 &
GRANGER_PID=$!
deactivate

echo "GrangerHub started with PID: $GRANGER_PID"

# Wait for GrangerHub to be ready
echo "Waiting for GrangerHub to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ GrangerHub is ready!"
        break
    fi
    sleep 1
done

# Start other services as needed
echo -e "\n📊 Service Status:"
echo "===================="

# Check ArangoDB
if nc -z localhost 8529 2>/dev/null; then
    echo "✅ ArangoDB: Running on localhost:8529"
else
    echo "❌ ArangoDB: Not running"
fi

# Check GrangerHub
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ GrangerHub: Running on localhost:8000"
else
    echo "❌ GrangerHub: Not running"
fi

echo -e "\n💡 To stop services:"
echo "docker stop arangodb-granger"
echo "kill $GRANGER_PID"