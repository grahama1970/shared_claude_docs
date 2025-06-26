# Task #47: Microservices Dependency Mapper

A Level 2 (Parallel Processing) implementation of a microservices dependency mapping and visualization system.

## Features

### Service Discovery Integration
- **Consul** service registry support
- **Kubernetes** service discovery
- Automatic service metadata extraction
- Version information tracking

### Dependency Analysis
- **Runtime dependency detection** from actual traffic patterns
- **Static code analysis** for compile-time dependencies
- **Database dependency tracking** (PostgreSQL, MySQL, MongoDB, Redis)
- **Message queue topology** (RabbitMQ, Kafka, SQS)
- **External API dependencies** with endpoint mapping

### Visualization & Export
- **DOT format** export for Graphviz visualization
- **JSON export** for D3.js interactive graphs
- Node coloring based on health status
- Edge styling by dependency type
- Support for circular dependency highlighting

### Advanced Features
- **Circular dependency detection** using graph algorithms
- **Service health correlation** and impact analysis
- **Version compatibility checking** between services
- **Service mesh integration** support
- **Parallel processing** for scalable analysis

## Usage

```python
import asyncio
from microservices_mapper_interaction import MicroservicesMapper

async def main():
    mapper = MicroservicesMapper()
    
    # Map dependencies from Consul
    result = await mapper.map_dependencies("http://localhost:8500")
    
    print(f"Found {result['services']} services")
    print(f"Mapped {result['dependencies']} dependencies")
    print(f"Circular dependencies: {result['circular']}")
    
    # Export visualizations
    mapper.export_to_dot(Path("./output"))
    mapper.export_to_json(Path("./output"))

asyncio.run(main())
```

## Dependency Types

- **API**: HTTP/REST service calls
- **Database**: Direct database connections
- **Queue**: Message queue dependencies
- **External**: Third-party API dependencies

## Test Coverage

- Service discovery from multiple sources
- Dependency analysis accuracy
- Visualization export formats
- Circular dependency detection
- Health impact propagation

## Integration Points

This mapper can integrate with:
- Service registries (Consul, Etcd, Kubernetes)
- APM tools for runtime analysis
- Service mesh sidecars (Istio, Linkerd)
- CI/CD pipelines for version tracking
- Monitoring systems for health correlation