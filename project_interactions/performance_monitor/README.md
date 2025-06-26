# Performance Monitor Interaction

**GRANGER Task #26**: Real-Time Performance Monitoring Dashboard (Level 2)

## Overview

This module implements a real-time performance monitoring system that tracks metrics across multiple GRANGER modules in parallel. It provides live insights into system performance, detects anomalies, and generates alerts for performance issues.

## Features

- **Multi-Module Monitoring**: Simultaneously monitors performance across multiple modules
- **Real-Time Metrics**: Tracks latency percentiles (p50, p95, p99), throughput, and error rates
- **Anomaly Detection**: Uses statistical analysis (z-score) to identify unusual patterns
- **Alert Generation**: Creates alerts when metrics exceed configured thresholds
- **Performance Bottleneck Detection**: Identifies slowest components in the system
- **Dashboard Data**: Provides structured data suitable for visualization

## Architecture

```
PerformanceMonitor
├── ModuleMetrics (per module)
│   ├── Latency tracking (deque)
│   ├── Throughput calculation
│   └── Error rate monitoring
├── AnomalyDetector
│   ├── Baseline statistics
│   └── Z-score calculation
└── Alert System
    ├── Threshold checking
    └── Severity levels (INFO/WARNING/CRITICAL)
```

## Usage

```python
import asyncio
from performance_monitor_interaction import PerformanceMonitor

# Create monitor instance
monitor = PerformanceMonitor()

# Monitor multiple modules
modules = ['api_gateway', 'database', 'cache', 'search_engine']
dashboard_data = await monitor.monitor_modules(modules, duration=30.0)

# Access metrics
for module_name, data in dashboard_data['modules'].items():
    metrics = data['metrics']
    print(f"{module_name}:")
    print(f"  Latency (p95): {metrics['latency_p95']:.3f}s")
    print(f"  Throughput: {metrics['requests_per_second']:.1f} req/s")
    print(f"  Error rate: {metrics['error_rate']:.1%}")

# Check alerts
for alert in dashboard_data['alerts']:
    print(f"[{alert['level']}] {alert['message']}")
```

## Metrics Collected

### Latency Metrics
- **latency_mean**: Average request latency
- **latency_p50**: 50th percentile (median) latency
- **latency_p95**: 95th percentile latency
- **latency_p99**: 99th percentile latency

### Throughput Metrics
- **requests_per_second**: Current request rate

### Reliability Metrics
- **error_rate**: Percentage of failed requests

## Alert Thresholds

Default thresholds that trigger alerts:

| Metric | Threshold | Alert Level |
|--------|-----------|-------------|
| latency_p95 | > 500ms | WARNING |
| latency_p99 | > 1000ms | WARNING |
| latency_p95 | > 1000ms | CRITICAL |
| error_rate | > 5% | WARNING |
| error_rate | > 10% | CRITICAL |
| requests_per_second | < 10 req/s | WARNING |

## Anomaly Detection

The system uses statistical anomaly detection:
- Maintains a rolling window of baseline values
- Calculates z-scores for new measurements
- Flags values with |z-score| > 3 as anomalous
- Generates WARNING alerts for |z-score| > 3
- Generates CRITICAL alerts for |z-score| > 4

## Dashboard Data Structure

```json
{
    "timestamp": 1234567890.123,
    "modules": {
        "module_name": {
            "metrics": {
                "latency_mean": 0.150,
                "latency_p50": 0.120,
                "latency_p95": 0.250,
                "latency_p99": 0.450,
                "error_rate": 0.02,
                "requests_per_second": 150.5
            },
            "last_update": 1234567890.123,
            "total_requests": 1500,
            "total_errors": 30
        }
    },
    "alerts": [
        {
            "timestamp": 1234567890.123,
            "module": "database",
            "metric": "latency_p95",
            "value": 0.650,
            "threshold": 0.500,
            "level": "warning",
            "message": "database: latency_p95 = 0.650 (threshold: 0.500)"
        }
    ],
    "summary": {
        "total_modules": 4,
        "active_alerts": 2,
        "warning_alerts": 5
    }
}
```

## Testing

Run the test suite:

```bash
python -m pytest project_interactions/performance-monitor/tests/
```

Or run the validation directly:

```bash
python project_interactions/performance-monitor/performance_monitor_interaction.py
```

## Integration with GRANGER

This performance monitor can be integrated with other GRANGER modules:

1. **SPARTA**: Monitor document processing throughput
2. **Marker**: Track PDF conversion latencies
3. **ArangoDB**: Monitor query performance and indexing speed
4. **Claude Max Proxy**: Track LLM request latencies and rate limits
5. **Module Communicator**: Monitor inter-module communication overhead

## Performance Considerations

- Uses `asyncio` for parallel monitoring without blocking
- Maintains bounded queues (deque) to limit memory usage
- Calculates statistics incrementally where possible
- Configurable monitoring duration and intervals

## Future Enhancements

- Export metrics to Prometheus/Grafana
- Machine learning-based anomaly detection
- Predictive alerting based on trends
- Distributed tracing integration
- Custom metric types and aggregations