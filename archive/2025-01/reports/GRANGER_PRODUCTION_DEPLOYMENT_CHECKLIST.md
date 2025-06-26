# GRANGER PRODUCTION DEPLOYMENT CHECKLIST

> **Comprehensive checklist for deploying the Granger ecosystem to production**  
> Last Updated: January 2025

---

## 📋 Overview

This checklist ensures safe, reliable deployment of the Granger ecosystem to production environments. Follow each section in order and verify all checks pass before proceeding.

---

## 1. Pre-Deployment Verification

### Code Quality Checks
```bash
# Run all tests across the ecosystem
cd /home/graham/workspace/shared_claude_docs
./scripts/run_all_granger_tests.py

# Verify no mock usage in production code
./scripts/scan_for_mock_usage.py

# Check for hardcoded credentials
rg -i "(api_key|password|secret|token)\s*=\s*['\"]" --type py

# Verify all modules have proper error handling
rg "except\s+Exception\s*:" --type py
```

### Documentation Verification
- [ ] All API endpoints documented
- [ ] Integration guides updated
- [ ] CHANGELOG.md reflects all changes
- [ ] Security considerations documented
- [ ] Rollback procedures documented

### Version Control
```bash
# Ensure clean working directory
git status

# Tag the release
git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin v1.0.0

# Create release branch
git checkout -b release/v1.0.0
```

---

## 2. Infrastructure Requirements

### Minimum System Requirements
```yaml
# Production Environment Requirements
CPU: 16+ cores
RAM: 32GB minimum (64GB recommended)
Storage: 500GB SSD (1TB recommended)
Network: 1Gbps dedicated
OS: Ubuntu 22.04 LTS or RHEL 8+
```

### Service Dependencies
```bash
# Verify all required services
systemctl status postgresql    # Database
systemctl status redis        # Cache
systemctl status nginx        # Reverse proxy
systemctl status docker       # Container runtime

# Check ArangoDB cluster
curl -X GET http://localhost:8529/_api/cluster/health

# Verify message queue
rabbitmqctl status
```

### Environment Configuration
```bash
# Production environment file template
cat > .env.production << EOF
# Core Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Service URLs
GRANGER_HUB_URL=https://hub.granger.prod
ARANGODB_URL=https://db.granger.prod:8529
LLM_CALL_URL=https://llm.granger.prod
TEST_REPORTER_URL=https://test.granger.prod

# Security
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -hex 32)

# Resource Limits
MAX_WORKERS=8
MAX_MEMORY_MB=8192
REQUEST_TIMEOUT=30
EOF
```

---

## 3. Security Checks

### Authentication & Authorization
```bash
# Verify all endpoints require authentication
grep -r "@requires_auth" --include="*.py" | wc -l

# Check for exposed admin endpoints
rg "admin|debug" --type py | grep -i "route\|endpoint"

# Validate JWT implementation
python -c "
from jose import jwt
token = jwt.encode({'sub': 'test'}, 'secret', algorithm='HS256')
print('JWT implementation: OK')
"
```

### Network Security
```bash
# Firewall configuration
sudo ufw status verbose

# Required firewall rules
sudo ufw allow 22/tcp     # SSH (restricted IPs)
sudo ufw allow 443/tcp    # HTTPS
sudo ufw allow 8529/tcp   # ArangoDB (internal only)
sudo ufw allow 5672/tcp   # RabbitMQ (internal only)
```

### SSL/TLS Configuration
```bash
# Generate SSL certificates
certbot certonly --standalone -d granger.prod

# Verify SSL configuration
openssl s_client -connect granger.prod:443 -servername granger.prod

# Check certificate expiry
echo | openssl s_client -connect granger.prod:443 2>/dev/null | openssl x509 -noout -dates
```

### Security Scanning
```bash
# Run security audit
pip-audit --desc

# Check for known vulnerabilities
safety check --json

# OWASP dependency check
dependency-check --project Granger --scan . --format JSON
```

---

## 4. Module Health Verification

### Core Module Health Checks
```bash
# Hub health check
curl -X GET https://hub.granger.prod/health

# RL Commons health check
curl -X GET https://rl.granger.prod/health

# World Model health check
curl -X GET https://world.granger.prod/health

# Test Reporter health check
curl -X GET https://test.granger.prod/health
```

### Module Readiness Script
```python
#!/usr/bin/env python3
# verify_module_health.py

import requests
import sys
from typing import Dict, List

MODULES = {
    "Granger Hub": "https://hub.granger.prod/health",
    "RL Commons": "https://rl.granger.prod/health",
    "World Model": "https://world.granger.prod/health",
    "Test Reporter": "https://test.granger.prod/health",
    "SPARTA": "https://sparta.granger.prod/health",
    "Marker": "https://marker.granger.prod/health",
    "ArangoDB": "https://db.granger.prod:8529/_api/version",
    "LLM Call": "https://llm.granger.prod/health",
    "Unsloth": "https://unsloth.granger.prod/health"
}

def check_health() -> bool:
    all_healthy = True
    
    for name, url in MODULES.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: Healthy")
            else:
                print(f"❌ {name}: Unhealthy (Status: {response.status_code})")
                all_healthy = False
        except Exception as e:
            print(f"❌ {name}: Failed ({str(e)})")
            all_healthy = False
    
    return all_healthy

if __name__ == "__main__":
    if not check_health():
        sys.exit(1)
```

---

## 5. Integration Test Requirements

### Pre-Production Integration Tests
```bash
# Run full integration test suite
cd /home/graham/workspace/shared_claude_docs
pytest tests/integration/ -v --tb=short

# Test pipeline flow
python tests/integration/test_full_pipeline.py

# Load testing
locust -f tests/load/locustfile.py --host=https://granger.prod
```

### Critical Path Testing
```python
#!/usr/bin/env python3
# test_critical_paths.py

import asyncio
from typing import Dict, Any

async def test_research_pipeline():
    """Test SPARTA → Marker → ArangoDB → Unsloth flow"""
    # Test implementation
    pass

async def test_rl_optimization():
    """Test RL Commons integration with modules"""
    # Test implementation
    pass

async def test_module_communication():
    """Test inter-module messaging via Hub"""
    # Test implementation
    pass

async def test_failover():
    """Test system behavior during module failures"""
    # Test implementation
    pass

async def run_all_tests():
    tests = [
        test_research_pipeline(),
        test_rl_optimization(),
        test_module_communication(),
        test_failover()
    ]
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ Test {i+1} failed: {result}")
            return False
    
    print("✅ All critical path tests passed")
    return True

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
```

---

## 6. Monitoring Setup

### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'granger-hub'
    static_configs:
      - targets: ['hub.granger.prod:9090']
  
  - job_name: 'granger-modules'
    static_configs:
      - targets: 
        - 'rl.granger.prod:9090'
        - 'world.granger.prod:9090'
        - 'test.granger.prod:9090'
        - 'sparta.granger.prod:9090'
        - 'marker.granger.prod:9090'
```

### Grafana Dashboards
```bash
# Import Granger dashboards
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @dashboards/granger-overview.json

# Set up alerts
curl -X POST http://admin:admin@localhost:3000/api/alert-notifications \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Granger Alerts",
    "type": "email",
    "settings": {
      "addresses": "ops@granger.ai"
    }
  }'
```

### Logging Configuration
```bash
# Centralized logging with ELK
cat > /etc/filebeat/filebeat.yml << EOF
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/granger/*.log
  fields:
    service: granger
    environment: production

output.elasticsearch:
  hosts: ["elasticsearch.granger.prod:9200"]
EOF

# Start Filebeat
systemctl restart filebeat
```

### Health Check Monitoring
```python
#!/usr/bin/env python3
# monitor_health.py

import time
import requests
from datetime import datetime
from loguru import logger

def monitor_endpoints():
    """Continuous health monitoring"""
    while True:
        timestamp = datetime.now().isoformat()
        
        for module, url in MODULES.items():
            try:
                response = requests.get(url, timeout=5)
                latency = response.elapsed.total_seconds()
                
                if response.status_code == 200:
                    logger.info(f"{module} healthy - latency: {latency:.3f}s")
                else:
                    logger.error(f"{module} unhealthy - status: {response.status_code}")
                    # Send alert
                    send_alert(module, response.status_code)
                    
            except Exception as e:
                logger.error(f"{module} failed: {str(e)}")
                send_alert(module, str(e))
        
        time.sleep(30)  # Check every 30 seconds

def send_alert(module: str, error: str):
    """Send alert to ops team"""
    # Implementation for alerts (email, Slack, PagerDuty, etc.)
    pass
```

---

## 7. Rollback Procedures

### Automated Rollback Script
```bash
#!/bin/bash
# rollback.sh

PREVIOUS_VERSION=$1

if [ -z "$PREVIOUS_VERSION" ]; then
    echo "Usage: ./rollback.sh <previous-version>"
    exit 1
fi

echo "🔄 Starting rollback to version $PREVIOUS_VERSION"

# Stop current services
docker-compose down

# Checkout previous version
git checkout "v$PREVIOUS_VERSION"

# Restore database backup
pg_restore -d granger_prod /backups/granger_${PREVIOUS_VERSION}.sql

# Rebuild and start services
docker-compose build
docker-compose up -d

# Verify services
sleep 30
python verify_module_health.py

if [ $? -eq 0 ]; then
    echo "✅ Rollback successful"
else
    echo "❌ Rollback failed - manual intervention required"
    exit 1
fi
```

### Manual Rollback Steps
1. **Stop all services**
   ```bash
   systemctl stop granger-*
   docker-compose down
   ```

2. **Restore database**
   ```bash
   # PostgreSQL
   pg_restore -d granger_prod /backups/granger_backup.sql
   
   # ArangoDB
   arangorestore --server.endpoint tcp://localhost:8529 \
     --input-directory /backups/arangodb/
   ```

3. **Restore code**
   ```bash
   git checkout v1.0.0  # Previous stable version
   ```

4. **Restart services**
   ```bash
   docker-compose up -d
   systemctl start granger-*
   ```

---

## 8. Post-Deployment Validation

### Smoke Tests
```bash
# Quick validation of core functionality
python scripts/smoke_tests.py

# Verify API endpoints
curl -X GET https://api.granger.prod/v1/status

# Check database connectivity
psql -h db.granger.prod -U granger -c "SELECT version();"

# Verify message queue
rabbitmqctl list_queues
```

### Performance Validation
```python
#!/usr/bin/env python3
# validate_performance.py

import time
import statistics
from typing import List

def measure_latency(endpoint: str, iterations: int = 100) -> Dict[str, float]:
    """Measure endpoint latency"""
    latencies = []
    
    for _ in range(iterations):
        start = time.time()
        response = requests.get(endpoint)
        latency = time.time() - start
        latencies.append(latency)
    
    return {
        "mean": statistics.mean(latencies),
        "median": statistics.median(latencies),
        "p95": sorted(latencies)[int(0.95 * len(latencies))],
        "p99": sorted(latencies)[int(0.99 * len(latencies))]
    }

# Performance thresholds
THRESHOLDS = {
    "mean": 0.1,      # 100ms
    "p95": 0.5,       # 500ms
    "p99": 1.0        # 1 second
}

def validate_performance():
    """Validate all endpoints meet performance criteria"""
    all_passed = True
    
    for module, url in MODULES.items():
        metrics = measure_latency(url)
        
        for metric, value in metrics.items():
            if metric in THRESHOLDS and value > THRESHOLDS[metric]:
                print(f"❌ {module} {metric}: {value:.3f}s (threshold: {THRESHOLDS[metric]}s)")
                all_passed = False
            else:
                print(f"✅ {module} {metric}: {value:.3f}s")
    
    return all_passed
```

### User Acceptance Testing
- [ ] UI responsiveness verified
- [ ] API response times acceptable
- [ ] Error messages user-friendly
- [ ] Documentation accessible
- [ ] Support channels operational

---

## 📊 Deployment Sign-Off

### Pre-Deployment Checklist
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Infrastructure ready
- [ ] Monitoring configured
- [ ] Rollback plan tested
- [ ] Team notified

### Deployment Execution
- [ ] Services deployed in order
- [ ] Health checks passing
- [ ] Integration tests successful
- [ ] Performance validated
- [ ] Monitoring active

### Post-Deployment
- [ ] Smoke tests passed
- [ ] User acceptance verified
- [ ] Documentation updated
- [ ] Team debriefed
- [ ] Lessons learned documented

---

## 🚨 Emergency Contacts

- **On-Call Engineer**: +1-XXX-XXX-XXXX
- **DevOps Lead**: devops@granger.ai
- **Security Team**: security@granger.ai
- **Escalation**: escalation@granger.ai

---

## 📝 Notes

- Always deploy during maintenance windows
- Keep rollback scripts tested and ready
- Monitor for 24 hours post-deployment
- Document any deviations from this checklist
- Update this checklist based on lessons learned

---

*Last verified: January 2025*