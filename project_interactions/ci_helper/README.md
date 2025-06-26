# CI Helper

A comprehensive CI/CD orchestration system that provides multi-platform pipeline management, deployment automation, and quality gates.

## Features

### Pipeline Orchestration
- **Multi-Platform Support**: GitHub Actions, Jenkins, GitLab CI, CircleCI, Azure DevOps
- **Dynamic Pipeline Generation**: Create pipelines programmatically
- **Parallel Job Execution**: Run jobs concurrently within stages
- **Dependency Resolution**: Handle job dependencies automatically
- **Stage-Based Execution**: Organize jobs into sequential stages

### Deployment Automation
- **Multiple Strategies**:
  - Blue-Green: Zero-downtime deployments with instant rollback
  - Canary: Gradual rollout with metrics monitoring
  - Rolling: Update instances in batches
  - Recreate: Simple stop-and-start deployment
- **Environment Management**: Deploy to dev, staging, production
- **Rollback Orchestration**: Quick rollback to previous versions
- **Custom Configuration**: Environment-specific settings

### Quality Gates
- **Metrics-Based Gates**: Code coverage, test pass rate, security vulnerabilities
- **Blocking vs Non-Blocking**: Control pipeline flow based on criticality
- **Flexible Operators**: gt, lt, eq, gte, lte comparisons
- **Custom Thresholds**: Set per-pipeline quality standards

### Additional Features
- **Secret Management**: Encrypted storage for sensitive data
- **Artifact Management**: Track and manage build artifacts
- **Notification System**: Multi-channel notifications
- **Pipeline Metrics**: Success rates, durations, failure analysis
- **Configuration Generation**: Export to platform-specific formats

## Usage

```python
from ci_helper_interaction import CIHelperInteraction

# Initialize the CI helper
ci_helper = CIHelperInteraction()

# Create a pipeline
pipeline_config = {
    "name": "My Application Pipeline",
    "stages": ["build", "test", "deploy"],
    "jobs": {
        "build": {
            "compile": {
                "commands": ["npm install", "npm run build"],
                "artifacts": ["dist/*"]
            }
        },
        "test": {
            "unit": {
                "commands": ["npm test"],
                "parallel": True
            },
            "integration": {
                "commands": ["npm run test:integration"],
                "parallel": True
            }
        },
        "deploy": {
            "production": {
                "commands": ["npm run deploy"],
                "dependencies": ["unit", "integration"]
            }
        }
    }
}

pipeline = ci_helper.create_pipeline("github_actions", pipeline_config)

# Add quality gates
ci_helper.add_quality_gate(pipeline["id"], {
    "name": "Code Coverage",
    "metric": "code_coverage",
    "threshold": 80.0,
    "operator": "gte",
    "blocking": True
})

# Execute the pipeline
execution = ci_helper.execute_pipeline(pipeline["id"])

# Deploy with blue-green strategy
deployment = ci_helper.deploy(
    pipeline["id"],
    environment="production",
    strategy="blue_green"
)

# Rollback if needed
if deployment["status"] == "failed":
    rollback = ci_helper.rollback(deployment["id"])
```

## Pipeline Configuration

### GitHub Actions Example
```yaml
name: My Application Pipeline
on: ["push", "pull_request"]
jobs:
  compile:
    runs-on: ubuntu-latest
    steps:
      - run: npm install
      - run: npm run build
```

### Jenkins Example
```groovy
pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
    }
}
```

### GitLab CI Example
```yaml
stages:
  - build
  - test
  - deploy

compile:
  stage: build
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/*
```

## Deployment Strategies

### Blue-Green
- Maintains two identical production environments
- Switches traffic instantly between blue and green
- Provides immediate rollback capability
- Zero downtime deployment

### Canary
- Gradually rolls out changes to a subset of users
- Monitors metrics during rollout
- Automatically promotes or rolls back based on success criteria
- Minimizes risk for production deployments

### Rolling
- Updates instances in configurable batches
- Maintains service availability during deployment
- Configurable pause between batches
- Suitable for large-scale deployments

### Recreate
- Simplest deployment strategy
- Stops all instances, then starts new version
- Brief downtime during deployment
- Suitable for non-critical applications

## Quality Gates

Define quality standards that must be met:

```python
# Code coverage must be at least 80%
ci_helper.add_quality_gate(pipeline_id, {
    "name": "Code Coverage",
    "metric": "code_coverage",
    "threshold": 80.0,
    "operator": "gte",
    "blocking": True
})

# Build time should be under 10 minutes
ci_helper.add_quality_gate(pipeline_id, {
    "name": "Build Time",
    "metric": "build_time",
    "threshold": 600,
    "operator": "lt",
    "blocking": False
})
```

## Secret Management

Securely store and retrieve sensitive data:

```python
# Add a secret
ci_helper.manage_secrets("add", "API_KEY", "your-secret-key")

# Retrieve a secret
secret = ci_helper.manage_secrets("get", "API_KEY")

# Delete a secret
ci_helper.manage_secrets("delete", "API_KEY")
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_pipeline_orchestration.py -v

# Run with coverage
pytest --cov=ci_helper tests/
```

## Integration

The CI Helper can be integrated with other project interactions:

- **Container Orchestrator**: Deploy containerized applications
- **Service Mesh Manager**: Configure service mesh during deployments
- **Monitoring Systems**: Track deployment metrics
- **Log Analyzer**: Analyze logs during pipeline execution
- **Test Reporter**: Generate comprehensive test reports