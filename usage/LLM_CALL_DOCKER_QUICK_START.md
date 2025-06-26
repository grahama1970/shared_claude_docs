# LLM Call Docker Quick Start

> Get up and running with llm_call Docker in under 5 minutes

## 🚀 1-Minute Setup

```bash
# Clone and start
git clone https://github.com/yourusername/llm_call.git
cd llm_call
docker compose up -d

# Authenticate Claude (one-time)
./docker/claude-proxy/authenticate.sh

# Test it works
curl http://localhost:8001/health
```

## 🔥 Quick Examples

### Basic Chat
```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "Say hello!"}]
  }'
```

### Python Client
```python
import requests

def ask_llm(prompt: str, model: str = "claude-3-5-sonnet-20241022"):
    response = requests.post(
        "http://localhost:8001/v1/chat/completions",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()['choices'][0]['message']['content']

# Use it
answer = ask_llm("What is Docker?")
print(answer)
```

### With JSON Validation
```python
# Get structured output
response = requests.post(
    "http://localhost:8001/v1/chat/completions",
    json={
        "model": "claude-3-5-sonnet-20241022",
        "messages": [{
            "role": "user",
            "content": "List 3 benefits of Docker as JSON"
        }],
        "validation": {
            "strategy": "json_validation",
            "schema": {
                "type": "object",
                "properties": {
                    "benefits": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 3
                    }
                },
                "required": ["benefits"]
            }
        }
    }
)

data = response.json()
benefits = data['choices'][0]['message']['content']
# This is guaranteed to be valid JSON matching the schema
```

## 🎯 Common Use Cases

### 1. Code Generation
```python
code = ask_llm("""
Write a Python function that connects to Redis 
and implements a simple cache decorator
""")
```

### 2. Data Extraction
```python
extracted = ask_llm(f"""
Extract the key facts from this text as JSON:

{document_text}

Return format: {{"facts": ["fact1", "fact2", ...]}}
""")
```

### 3. Multi-Model Fallback
```python
models = ["claude-3-5-sonnet-20241022", "gpt-4", "gemini-pro"]

for model in models:
    try:
        result = ask_llm(prompt, model=model)
        print(f"Success with {model}")
        break
    except Exception as e:
        print(f"Failed with {model}: {e}")
        continue
```

## 🔌 Environment Variables

Create `.env` file:
```bash
# Optional API keys for fallback models
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
ANTHROPIC_API_KEY=...  # Not needed if using Claude Docker

# Service configuration
LOG_LEVEL=INFO
ENABLE_CACHE=true
```

## 🛠️ Useful Commands

```bash
# View logs
docker compose logs -f llm-call-api

# Restart services
docker compose restart

# Check Claude auth status
curl http://localhost:3010/health | jq .

# Stop everything
docker compose down

# Remove volumes (careful!)
docker compose down -v
```

## 🎨 Advanced Features

### Custom System Prompts
```python
response = ask_llm(
    "Explain quantum computing",
    system="You are a physics professor explaining to a 5-year-old"
)
```

### Streaming (if implemented)
```python
import sseclient

response = requests.post(
    "http://localhost:8001/v1/chat/completions",
    json={
        "model": "claude-3-5-sonnet-20241022",
        "messages": messages,
        "stream": True
    },
    stream=True
)

for event in sseclient.SSEClient(response).events():
    print(json.loads(event.data)['choices'][0]['delta']['content'], end='')
```

## 🚨 Troubleshooting

**Can't connect?**
```bash
docker compose ps  # Check services are running
lsof -i :8001     # Check port is free
```

**Authentication issues?**
```bash
./docker/claude-proxy/authenticate.sh  # Re-authenticate
docker compose logs claude-proxy       # Check logs
```

**Model errors?**
- Check API keys in `.env`
- Verify model names are correct
- Try a different model

## 📚 Next Steps

- [Full Integration Guide](../docs/03_modules/integration/LLM_CALL_DOCKER_INTEGRATION_GUIDE.md)
- [Docker Authentication Details](../docs/04_implementation/tutorials/LLM_CALL_DOCKER_AUTHENTICATION.md)
- [API Reference](../docs/02_api_reference/llm_call_api.md)