# API Documentation Generator

An intelligent API documentation generation system with multi-framework support, code example generation, and OpenAPI/Swagger specification creation.

## Features

- **Multi-Framework Support**: Extract API endpoints from FastAPI, Flask, and Django REST Framework
- **OpenAPI/Swagger Generation**: Create OpenAPI 3.0.3 compliant specifications
- **Code Example Generation**: Automatically generate examples in Python, JavaScript, and cURL
- **Markdown Documentation**: Beautiful, readable documentation in Markdown format
- **HTML Documentation**: Styled HTML output with syntax highlighting
- **Postman Collection Export**: Convert API specs to Postman collections
- **Documentation Updates**: Track changes and update documentation incrementally
- **SDK Generation Hints**: Guidance for generating client SDKs

## Installation

```bash
uv add pydantic jinja2 openapi-spec-validator markdown
```

## Usage

### Basic Documentation Generation

```python
from api_doc_generator_interaction import (
    APIDocGeneratorInteraction,
    DocumentationConfig
)

# Configure documentation
config = DocumentationConfig(
    title="My API",
    version="1.0.0",
    description="My awesome API",
    base_url="https://api.example.com"
)

# Create generator
generator = APIDocGeneratorInteraction(config)

# Generate documentation from FastAPI app
docs = generator.generate_documentation(
    "path/to/app.py",
    framework="fastapi",
    output_formats=["openapi", "markdown", "html"]
)

# Access generated documentation
print(docs["openapi"])  # OpenAPI specification
print(docs["markdown"])  # Markdown documentation
print(docs["html"])     # HTML documentation
```

### Extracting from Different Frameworks

```python
# FastAPI
fastapi_docs = generator.generate_documentation(
    "app.py",
    framework="fastapi"
)

# Flask
flask_docs = generator.generate_documentation(
    "app.py",
    framework="flask"
)

# Django
django_docs = generator.generate_documentation(
    "urls.py",
    framework="django"
)
```

### Generating Code Examples

```python
from api_doc_generator_interaction import ExampleGenerator, APIEndpoint

# Create example generator
example_gen = ExampleGenerator(base_url="https://api.example.com")

# Define endpoint
endpoint = APIEndpoint(
    path="/users",
    method="POST",
    summary="Create user",
    request_body={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"}
                    }
                }
            }
        }
    },
    security=[{"bearerAuth": []}]
)

# Generate examples
examples = example_gen.generate_examples(endpoint)
print(examples["python"])      # Python example
print(examples["javascript"])  # JavaScript example
print(examples["curl"])        # cURL example
```

### Updating Documentation

```python
# Load existing OpenAPI spec
with open("openapi.json") as f:
    existing_spec = json.load(f)

# Update documentation
result = generator.update_documentation(
    "app.py",
    existing_spec,
    framework="fastapi"
)

print(f"Found {result['change_count']} changes")
print(result["changes"])  # List of changes
print(result["openapi"])  # Updated specification
```

### Exporting to Postman

```python
# Generate documentation with Postman export
docs = generator.generate_documentation(
    "app.py",
    framework="fastapi",
    output_formats=["openapi", "postman"]
)

# Save Postman collection
with open("postman_collection.json", "w") as f:
    json.dump(docs["postman"], f, indent=2)
```

### SDK Generation Hints

```python
# Get SDK generation hints
sdk_hints = generator.generate_sdk_hints(docs["openapi"], "python")
print(sdk_hints)

# Outputs installation and usage instructions for:
# - Python: openapi-python-client
# - TypeScript: openapi-typescript-codegen
# - Go: oapi-codegen
```

## Configuration Options

```python
config = DocumentationConfig(
    title="My API",
    version="1.0.0",
    description="API description",
    base_url="https://api.example.com",
    contact={
        "name": "API Support",
        "email": "support@example.com",
        "url": "https://example.com/support"
    },
    license={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {"url": "https://api.example.com", "description": "Production"},
        {"url": "https://staging-api.example.com", "description": "Staging"}
    ],
    security_schemes={
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
)
```

## Output Formats

### OpenAPI Specification
- Complete OpenAPI 3.0.3 specification
- Includes paths, schemas, security definitions
- Validated for compliance

### Markdown Documentation
- Human-readable documentation
- Includes endpoint descriptions
- Code examples for each endpoint
- Authentication instructions
- Error code reference

### HTML Documentation
- Styled HTML with syntax highlighting
- Responsive design
- Color-coded HTTP methods
- Collapsible sections

### Postman Collection
- Ready-to-import collection
- Pre-configured requests
- Environment variables support
- Authentication setup

## Advanced Features

### Custom Authentication Documentation
The generator automatically detects and documents authentication schemes:
- Bearer token authentication
- API key authentication
- OAuth2 flows

### Automatic Tag Generation
Tags are automatically extracted from endpoint paths for better organization.

### Parameter Detection
- Path parameters from URL patterns
- Query parameters from function arguments
- Request body schemas from type hints

### Response Documentation
- Automatic detection of response models
- Multiple response codes support
- Content type handling

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run the verification script:

```bash
python test_task_52.py
```

## Integration Example

```python
# Complete example with all features
from pathlib import Path
from api_doc_generator_interaction import (
    APIDocGeneratorInteraction,
    DocumentationConfig
)

# Setup configuration
config = DocumentationConfig(
    title="E-Commerce API",
    version="2.0.0",
    description="Complete e-commerce platform API",
    base_url="https://api.shop.com",
    contact={"name": "API Team", "email": "api@shop.com"},
    license={"name": "Commercial", "url": "https://shop.com/license"}
)

# Initialize generator
generator = APIDocGeneratorInteraction(config)

# Generate all documentation formats
docs = generator.generate_documentation(
    Path("src/api/main.py"),
    framework="fastapi",
    output_formats=["openapi", "markdown", "html", "postman"]
)

# Save outputs
Path("docs/openapi.json").write_text(json.dumps(docs["openapi"], indent=2))
Path("docs/api.md").write_text(docs["markdown"])
Path("docs/api.html").write_text(docs["html"])
Path("docs/postman.json").write_text(json.dumps(docs["postman"], indent=2))

# Generate SDK hints
for lang in ["python", "typescript", "go"]:
    hints = generator.generate_sdk_hints(docs["openapi"], lang)
    Path(f"docs/sdk_{lang}.md").write_text(hints)

print(f"✅ Generated documentation for {len(docs['endpoints'])} endpoints")
```

## Requirements

- Python 3.9+
- pydantic
- jinja2
- openapi-spec-validator
- markdown

## Contributing

1. Follow the project coding standards
2. Add tests for new features
3. Update documentation
4. Run the test suite before submitting