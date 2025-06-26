# Test Reporter Integration for Interaction Testing

## Overview

This document outlines how to integrate interaction testing metrics into the claude-test-reporter engine.

## New Metrics to Track

### 1. Interaction Test Categories
```python
class InteractionMetrics:
    """Metrics for module interaction testing"""
    
    def __init__(self):
        self.metrics = {
            "isolation_tests": 0,        # Level 0
            "binary_interactions": 0,    # Level 1
            "pipeline_tests": 0,         # Level 2
            "ecosystem_tests": 0,        # Level 3
            "ui_interaction_tests": 0,   # Level 4
            
            "total_modules": 0,
            "connected_modules": 0,
            "isolated_modules": 0,
            "skeleton_modules": 0,
            
            "interaction_failures": [],
            "communication_latency": {},
            "message_format_compliance": {},
        }
```

### 2. Interaction Matrix Data
```python
# Track which modules successfully communicate
interaction_matrix = {
    "sparta": {
        "marker": {"success": True, "latency": 0.15, "tests": 10},
        "arangodb": {"success": False, "error": "Connection refused", "tests": 5},
        "hub": {"success": True, "latency": 0.05, "tests": 20}
    },
    # ... for each module
}
```

### 3. Skeleton Detection Results
```python
skeleton_detection = {
    "module_name": {
        "implementation_ratio": 0.25,
        "skeleton_indicators": 45,
        "working_functions": 3,
        "is_skeleton": True,
        "interaction_capable": False
    }
}
```

## Report Template Extensions

### 1. Add Interaction Summary Card
```html
<div class="summary-card interaction-health">
    <h3>Interaction Health</h3>
    <div class="metric-row">
        <span>Connected Modules:</span>
        <span class="metric-value">{connected}/{total}</span>
    </div>
    <div class="metric-row">
        <span>Interaction Success Rate:</span>
        <span class="metric-value">{success_rate}%</span>
    </div>
    <div class="metric-row warning">
        <span>Skeleton Projects:</span>
        <span class="metric-value">{skeleton_count}</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {connectivity_percentage}%"></div>
    </div>
</div>
```

### 2. Interaction Matrix Visualization
```html
<div class="interaction-matrix">
    <h3>Module Communication Matrix</h3>
    <table class="matrix-table">
        <tr>
            <th></th>
            <!-- Column headers for each module -->
        </tr>
        <!-- Row for each module showing connections -->
        <tr>
            <td>ModuleA</td>
            <td class="success">✓</td>
            <td class="failure">✗</td>
            <td class="not-tested">?</td>
        </tr>
    </table>
</div>
```

### 3. Test Level Distribution
```javascript
// Add to report JavaScript
const interactionLevels = {
    labels: ['Level 0', 'Level 1', 'Level 2', 'Level 3', 'Level 4'],
    datasets: [{
        label: 'Tests by Level',
        data: [isolationTests, binaryTests, pipelineTests, ecosystemTests, uiTests],
        backgroundColor: ['#gray', '#blue', '#green', '#yellow', '#purple']
    }]
};
```

## CLI Integration

### New Commands
```bash
# Generate interaction-focused report
claude-test-reporter generate --interaction-focus

# Show interaction matrix
claude-test-reporter interaction-matrix --project granger

# Check skeleton modules
claude-test-reporter skeleton-check --threshold 0.3

# Module health dashboard
claude-test-reporter module-health --show-disconnected
```

### Enhanced Output
```
=== Granger Ecosystem Test Report ===
Total Tests: 1,234
Passed: 1,100 (89.1%)
Failed: 134 (10.9%)

=== Interaction Testing Summary ===
Module Connectivity: 15/20 (75%)
Skeleton Modules: 3 (world_model, unsloth, chat)
Interaction Test Coverage:
  - Level 0 (Isolation): 20/20 ✓
  - Level 1 (Binary): 12/20 ⚠️
  - Level 2 (Pipeline): 8/20 ⚠️
  - Level 3 (Ecosystem): 3/20 ❌
  - Level 4 (UI): 0/3 ❌

Critical Issues:
- world_model: 23% implementation (skeleton)
- arangodb ↔ rl_commons: Connection failures
- marker: No hub integration

Recommendations:
1. Implement skeleton modules before testing
2. Fix arangodb connection issues
3. Add missing Level 2+ tests
```

## Integration with MultiProjectDashboard

### Add Interaction Overview Section
```python
def generate_interaction_overview(self, projects: List[Project]) -> str:
    """Generate interaction testing overview for dashboard"""
    
    html = """
    <section class="interaction-overview">
        <h2>Ecosystem Connectivity</h2>
        <div class="connectivity-grid">
    """
    
    for project in projects:
        connectivity = self.calculate_connectivity(project)
        status_class = "connected" if connectivity > 0.7 else "isolated"
        
        html += f"""
        <div class="project-connectivity {status_class}">
            <h4>{project.name}</h4>
            <div class="connections">
                Connects to: {', '.join(project.connections)}
            </div>
            <div class="interaction-stats">
                Binary Tests: {project.binary_tests}
                Pipeline Tests: {project.pipeline_tests}
            </div>
        </div>
        """
    
    html += "</div></section>"
    return html
```

## Adapter for Interaction Tests

Create `interaction_test_adapter.py`:

```python
class InteractionTestAdapter(BaseAdapter):
    """Adapter for processing interaction test results"""
    
    def parse_test_result(self, raw_result: Dict) -> TestResult:
        """Parse interaction test results"""
        
        result = TestResult(
            name=raw_result['name'],
            status=raw_result['status'],
            duration=raw_result['duration']
        )
        
        # Add interaction-specific metadata
        if 'interaction_level' in raw_result:
            result.metadata['level'] = raw_result['interaction_level']
            
        if 'modules_involved' in raw_result:
            result.metadata['modules'] = raw_result['modules_involved']
            
        if 'communication_type' in raw_result:
            result.metadata['comm_type'] = raw_result['communication_type']
            
        return result
    
    def categorize_test(self, test: TestResult) -> str:
        """Categorize test by interaction level"""
        
        if 'level' in test.metadata:
            return f"Level {test.metadata['level']}"
        
        # Infer from test name
        if 'interaction' in test.name.lower():
            if 'binary' in test.name:
                return "Level 1"
            elif 'pipeline' in test.name:
                return "Level 2"
            elif 'ecosystem' in test.name:
                return "Level 3"
                
        return "Level 0"
```

## Configuration Extension

Add to `config.yaml`:

```yaml
reporting:
  interaction_testing:
    enabled: true
    minimum_connectivity: 0.7
    skeleton_threshold: 0.3
    required_levels:
      - 0  # Isolation
      - 1  # Binary
      - 2  # Pipeline
    visualization:
      show_matrix: true
      show_flow_diagram: true
      highlight_isolated: true
  
  alerts:
    skeleton_module_found:
      severity: critical
      message: "Module {name} is {ratio}% skeleton - implement before testing"
    
    module_isolated:
      severity: warning
      message: "Module {name} has no verified connections"
    
    interaction_test_missing:
      severity: warning
      message: "Module {name} missing Level {level} interaction tests"
```

## Usage in Test Suites

```python
# In your test files
from claude_test_reporter import TestReporter, InteractionMetrics

reporter = TestReporter()
interaction_metrics = InteractionMetrics()

# After running interaction tests
interaction_metrics.record_interaction(
    source="sparta",
    target="marker", 
    success=True,
    latency=0.15,
    test_level=1
)

# Generate enhanced report
reporter.generate_report(
    include_interactions=True,
    interaction_metrics=interaction_metrics
)
```

## Dashboard Integration

The Multi-Project Dashboard should show:

1. **Connectivity Heatmap** - Visual matrix of module connections
2. **Skeleton Alert Banner** - Warning when skeleton modules detected
3. **Test Level Progress** - How many modules have each level completed
4. **Integration Health Score** - Overall ecosystem connectivity percentage
5. **Critical Path Status** - Health of main pipelines (SPARTA→Marker→ArangoDB)

This integration ensures the Test Reporter becomes the single source of truth for both individual test results AND ecosystem-wide interaction health.