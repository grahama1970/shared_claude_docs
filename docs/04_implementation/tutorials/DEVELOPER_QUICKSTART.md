# GRANGER Developer Quickstart Guide

Get up and running with GRANGER in under 10 minutes!

## 🚀 What is GRANGER?

GRANGER (Graph-Reinforced Autonomous Network for General Enterprise Research) is an AI-powered research platform that integrates:
- **SPARTA**: Cybersecurity vulnerability data
- **ArXiv**: Academic research papers  
- **Marker**: PDF to Markdown conversion
- **ArangoDB**: Knowledge graph storage
- **Claude**: AI-powered processing

## 📋 Prerequisites

- Python 3.10+
- ArangoDB running locally (docker recommended)
- 4GB RAM minimum
- Internet connection for API access

## 🔧 Quick Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/shared_claude_docs.git
cd shared_claude_docs

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
export ARANGO_HOST='http://localhost:8529'
export ARANGO_USER='root'
export ARANGO_PASSWORD='openSesame'

# Optional API keys
export NASA_API_KEY='your-key'  # For SPARTA NASA data
```

## 🏃 5-Minute Test Drive

### 1. Test ArXiv Integration (100% Working)
```python
from project_interactions.arxiv_handlers.real_arxiv_handlers import ArxivSearchHandler

# Search for papers
handler = ArxivSearchHandler()
result = handler.handle({
    "query": "quantum computing",
    "max_results": 3
})

print(f"Found {len(result['data']['papers'])} papers!")
```

### 2. Test the Optimized Pipeline
```bash
cd project_interactions/performance_optimization
python performance_optimization_task.py

# Expected output:
# Pipeline completed in <10s (was 34.67s)
# Cache hit rate: 98%
```

### 3. Run Full Integration Test
```bash
cd project_interactions/level_3_tests
python test_full_granger_pipeline.py

# Shows which modules are working
```

## 💡 Common Integration Patterns

### Basic Pipeline
```python
# 1. Search papers
papers = arxiv.handle({"query": "buffer overflow"})

# 2. Download PDFs (parallel)
pdfs = downloader.download_papers_parallel(paper_ids)

# 3. Convert to Markdown (with fallback)
for pdf in pdfs:
    markdown = marker.handle({"pdf_path": pdf})
    
# 4. Store in ArangoDB
arango.handle({
    "operation": "create",
    "collection": "papers",
    "data": {"content": markdown}
})
```

### Error-Resilient Pattern
```python
from project_interactions.performance_optimization.module_specific_optimizations import (
    ErrorRecoveryOptimizations as ERO
)

@ERO.intelligent_retry(max_attempts=3)
@ERO.circuit_breaker(failure_threshold=5)
def safe_operation():
    # Your code - automatically retries and circuit breaks
    return handler.handle(params)
```

## 🔍 Module Status Quick Reference

| Module | Working | Try This First |
|--------|---------|----------------|
| ArXiv | ✅ 100% | `arxiv.handle({"query": "AI"})` |
| SPARTA | ⚠️ 40% | CVE search only |
| ArangoDB | ⚠️ 33% | Basic CRUD works |
| Marker | ⚠️ Fallback | PDF conversion with fallbacks |

## 🐛 Known Issues & Quick Fixes

### ArangoDB Connection Error
```python
# Error: Invalid URL 'localhost'
# Fix is automatic, but ensure:
export ARANGO_HOST='http://localhost:8529'
```

### Marker Import Error
```python
# Error: No module named 'pdftext'
# Fix: Automatic fallback to PyPDF2
# No action needed - it works!
```

### Rate Limiting
```python
# APIs may rate limit
# Fix: Built-in adaptive rate limiter
# Just retry if you see 429 errors
```

## 📊 Performance Tips

### 1. Use Caching
```python
# Searches are cached automatically
# 98% hit rate on repeated queries
```

### 2. Batch Operations
```python
# Instead of:
for doc in documents:
    arango.create(doc)  # Slow

# Do:
arango.batch_create(documents)  # 40x faster
```

### 3. Parallel Processing
```python
# Built-in parallel support
results = handler.download_papers_parallel(ids, max_workers=5)
```

## 🧪 Testing Your Integration

### Run Specific Test Levels
```bash
# Level 0: Single modules
cd project_interactions/sparta_tests
python test_sparta_handlers.py

# Level 1: Two-module pipelines  
cd project_interactions/level_1_tests
python test_arxiv_marker_pipeline.py

# Level 2: Three modules
cd project_interactions/level_2_tests
python test_arxiv_marker_arangodb.py

# Level 3: Full pipeline
cd project_interactions/level_3_tests
python test_full_granger_pipeline.py
```

### Generate Performance Report
```bash
cd project_interactions/performance_optimization
python benchmark_performance.py
# Creates: performance_benchmark_report.md
```

## 📚 Essential Documentation

1. **Integration Patterns**: `docs/integration_patterns/MODULE_INTEGRATION_COOKBOOK.md`
2. **Visual Architecture**: `docs/visual_diagrams/GRANGER_ARCHITECTURE_DIAGRAMS.md`
3. **Error Handling**: `docs/integration_patterns/ERROR_HANDLING_STRATEGIES.md`
4. **Phase 2 Progress**: `docs/tasks/GRANGER_PHASE2_PROGRESS_87_PERCENT.md`

## 🎯 Next Steps

### For Module Development
1. Follow the handler pattern
2. Test with real APIs (no mocks)
3. Add error recovery
4. Benchmark performance

### For Integration Work
1. Start with working modules (ArXiv)
2. Use established patterns
3. Add caching and parallelization
4. Document any new issues

### For Testing
1. Use progressive levels (0→1→2→3)
2. Validate with timing (>0.1s = real)
3. Track all failures
4. Generate reports

## 🆘 Troubleshooting

### Nothing Works?
```bash
# Check ArangoDB is running
curl http://localhost:8529/_api/version

# Verify environment
python -c "import os; print(os.getenv('ARANGO_HOST'))"

# Test simplest operation
cd project_interactions/arxiv_handlers
python -c "from real_arxiv_handlers import *; print('OK')"
```

### Slow Performance?
- Check cache is working (98% hit rate expected)
- Use parallel operations where available
- Batch database operations

### Integration Failures?
- Check `docs/integration_patterns/ERROR_HANDLING_STRATEGIES.md`
- Most issues have known fixes
- Use fallback patterns

## 🎉 Success Checklist

- [ ] ArXiv search returns papers
- [ ] Performance test shows <10s pipeline
- [ ] At least 2 modules working together
- [ ] Cache hit rate >90%
- [ ] No hardcoded credentials

## 📞 Getting Help

1. Check error handling docs for known issues
2. Review integration patterns for examples
3. Look at visual diagrams for architecture
4. Run benchmark to identify bottlenecks

---

**Welcome to GRANGER!** You're now ready to build powerful research integrations with battle-tested patterns and optimized performance.

*Remember: This is Phase 2 - we've already discovered and fixed 19+ integration bugs, so you're starting with a solid foundation!*