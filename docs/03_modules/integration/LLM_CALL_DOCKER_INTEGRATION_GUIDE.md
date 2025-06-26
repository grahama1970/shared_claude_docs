# LLM Call Docker Integration Guide

> How other GRANGER components can integrate with the llm_call Docker container

## 🚀 Quick Start for Other Projects

### 1. Using the Docker API Endpoint

The llm_call Docker container exposes a REST API on port 8001 that other projects can use:

```python
import requests

# Example: Call Claude through the Docker API
response = requests.post(
    "http://localhost:8001/v1/chat/completions",
    json={
        "model": "claude-3-5-sonnet-20241022",
        "messages": [
            {"role": "user", "content": "Your prompt here"}
        ]
    }
)

result = response.json()
print(result['choices'][0]['message']['content'])
```

### 2. Available Models

The Docker container supports multiple models through unified API:

- **Claude Models** (via proxy on port 3010):
  - `claude-3-5-sonnet-20241022` (Claude Max)
  - `claude-3-opus-20240229` (Claude Opus)
  
- **Other Models** (via API keys):
  - OpenAI GPT models
  - Google Gemini models
  - Local Ollama models (if GPU profile enabled)

### 3. Docker Compose Integration

Add llm_call to your project's docker-compose.yml:

```yaml
services:
  your-service:
    # Your service configuration
    depends_on:
      - llm-call-api
    environment:
      - LLM_CALL_URL=http://llm-call-api:8001
    networks:
      - llm-call-network

networks:
  llm-call-network:
    external: true
    name: llm-call-network
```

## 📡 API Endpoints

### Main API Service (Port 8001)

#### Chat Completions
```http
POST http://localhost:8001/v1/chat/completions
Content-Type: application/json

{
  "model": "claude-3-5-sonnet-20241022",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

#### Health Check
```http
GET http://localhost:8001/health
```

#### Validation Options
```http
POST http://localhost:8001/v1/chat/completions
{
  "model": "claude-3-5-sonnet-20241022",
  "messages": [...],
  "validation": {
    "strategy": "json_validation",
    "schema": {...}
  }
}
```

### Claude Proxy Service (Port 3010)

#### Direct Claude Access
```http
POST http://localhost:3010/v1/chat/completions
```

#### Health & Auth Status
```http
GET http://localhost:3010/health
```

## 🔧 Environment Variables

Set these in your project to connect to llm_call:

```bash
# Required
LLM_CALL_API_URL=http://localhost:8001

# Optional (if not using Docker networking)
CLAUDE_PROXY_URL=http://localhost:3010

# For direct API access (bypass Docker)
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
GOOGLE_API_KEY=your-key
```

## 🐍 Python Client Example

```python
from typing import List, Dict, Optional
import requests
import json

class LLMCallClient:
    """Client for interacting with llm_call Docker container."""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        validation: Optional[Dict] = None
    ) -> Dict:
        """Send chat completion request to llm_call."""
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        if validation:
            payload["validation"] = validation
        
        response = self.session.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    def health_check(self) -> Dict:
        """Check if llm_call service is healthy."""
        response = self.session.get(f"{self.base_url}/health")
        return response.json()

# Usage example
client = LLMCallClient()

# Check health
health = client.health_check()
print(f"LLM Call Status: {health['status']}")

# Send a request
result = client.chat_completion(
    messages=[{"role": "user", "content": "Explain Docker networking"}],
    model="claude-3-5-sonnet-20241022"
)

print(result['choices'][0]['message']['content'])
```

## 🎯 Integration Patterns

### 1. Retry with Fallback Models

```python
models = [
    "claude-3-5-sonnet-20241022",  # Try Claude first
    "gpt-4",                        # Fallback to GPT-4
    "gemini-pro"                    # Final fallback
]

for model in models:
    try:
        result = client.chat_completion(messages, model=model)
        break
    except requests.HTTPError as e:
        if e.response.status_code == 503:  # Service unavailable
            continue
        raise
```

### 2. Structured Output with Validation

```python
# Request JSON output with schema validation
result = client.chat_completion(
    messages=[{
        "role": "user", 
        "content": "List 3 Docker best practices as JSON"
    }],
    validation={
        "strategy": "json_validation",
        "schema": {
            "type": "object",
            "properties": {
                "practices": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 3
                }
            },
            "required": ["practices"]
        }
    }
)
```

### 3. Streaming Responses

```python
# For streaming (if implemented)
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

client = sseclient.SSEClient(response)
for event in client.events():
    data = json.loads(event.data)
    print(data['choices'][0]['delta']['content'], end='')
```

## 🐳 Docker Network Communication

### Internal Service Names

When running inside Docker network, use these hostnames:

- `llm-call-api:8001` - Main API service
- `llm-call-claude-proxy:3010` - Claude proxy service
- `llm-call-redis:6379` - Redis cache

### Example Docker Integration

```dockerfile
# Your service Dockerfile
FROM python:3.11-slim

# Install dependencies
RUN pip install requests

# Your app code
COPY . /app
WORKDIR /app

# Set llm_call URL
ENV LLM_CALL_URL=http://llm-call-api:8001

CMD ["python", "your_app.py"]
```

## 🔐 Authentication

### For Claude Max/Opus

The Claude proxy requires OAuth authentication (one-time setup):

```bash
# From host machine
./docker/claude-proxy/authenticate.sh
```

### For API-based Models

Set environment variables in your docker-compose.yml:

```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - GOOGLE_API_KEY=${GOOGLE_API_KEY}
```

## 📊 Monitoring & Debugging

### Check Service Status

```bash
# All services
docker compose ps

# Logs
docker compose logs llm-call-api
docker compose logs llm-call-claude-proxy

# Health endpoints
curl http://localhost:8001/health
curl http://localhost:3010/health
```

### Debug Connection Issues

```python
import socket

def check_llm_call_connection():
    """Debug connectivity to llm_call services."""
    
    services = [
        ("localhost", 8001, "API"),
        ("localhost", 3010, "Claude Proxy"),
        ("llm-call-api", 8001, "Docker API"),
        ("llm-call-claude-proxy", 3010, "Docker Proxy")
    ]
    
    for host, port, name in services:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✅ {name} ({host}:{port}) - Connected")
            else:
                print(f"❌ {name} ({host}:{port}) - Failed")
        except Exception as e:
            print(f"❌ {name} ({host}:{port}) - Error: {e}")
```

## 🚀 Advanced Features

### 1. Custom Validation Strategies

llm_call supports 16 built-in validators:

- `json_validation` - Schema-based JSON validation
- `length_validation` - Response length constraints
- `format_validation` - Regex pattern matching
- `keyword_validation` - Required/forbidden keywords
- `semantic_validation` - Meaning preservation
- And more...

### 2. Multi-Model Routing

The router automatically selects the best model based on:
- Availability
- Cost optimization
- Performance metrics
- Request requirements

### 3. Caching with Redis

Responses are automatically cached. Control with headers:

```python
# Bypass cache
headers = {"X-No-Cache": "true"}
response = requests.post(url, json=payload, headers=headers)
```

## 📝 Example: GRANGER Module Integration

```python
# Example: ArXiv module using llm_call for paper summarization
class ArXivWithLLM:
    def __init__(self):
        self.llm_client = LLMCallClient()
    
    def summarize_paper(self, paper_text: str) -> str:
        """Use llm_call to summarize research paper."""
        
        result = self.llm_client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at summarizing academic papers."
                },
                {
                    "role": "user",
                    "content": f"Summarize this paper in 3 paragraphs:\n\n{paper_text[:4000]}"
                }
            ],
            model="claude-3-5-sonnet-20241022",
            max_tokens=500
        )
        
        return result['choices'][0]['message']['content']
```

## 🆘 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure Docker containers are running: `docker compose ps`
   - Check port availability: `lsof -i :8001`

2. **Authentication Error**
   - For Claude: Run `./docker/claude-proxy/authenticate.sh`
   - For APIs: Check environment variables

3. **Model Not Available**
   - Check health endpoint for available models
   - Ensure proper authentication for premium models

### Support

- Check logs: `docker compose logs -f`
- Health status: `curl http://localhost:8001/health`
- Integration examples: `/shared_claude_docs/docs/05_examples/`

---

For more details, see:
- [LLM Call Main Documentation](../spokes/005_Describe_llm_call.md)
- [Docker Authentication Guide](../../04_implementation/tutorials/LLM_CALL_DOCKER_AUTHENTICATION.md)
- [API Reference](../../02_api_reference/llm_call_api.md)