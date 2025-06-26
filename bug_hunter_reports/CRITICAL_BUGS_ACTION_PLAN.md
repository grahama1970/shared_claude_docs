# Critical Bugs Action Plan

## Priority 1: System Breaking Issues (Fix Immediately)

### 1. SPARTA Module Import Error
**Impact**: Complete module failure  
**Fix**: 
```python
# In /home/graham/workspace/experiments/sparta/src/sparta/core/__init__.py
# Fix the docstring syntax error (missing closing quotes)
```

### 2. ArXiv Deprecated API ✅ ALREADY FIXED
**Status**: Fixed across 15+ files  
**Verification**: Run `granger-verify --project arxiv_mcp --test`

### 3. No Rate Limiting on External APIs
**Impact**: Risk of API bans  
**Fix Locations**:
- SPARTA: Add rate limiting to NVD API calls
- ArXiv: ✅ Already added (3 requests/second)
- YouTube: Check and add if missing

**Implementation**:
```python
# Add to each external API client
rate_limiter = RateLimiter(
    calls_per_second=3,
    burst_size=10,
    retry_on_limit=True
)
```

## Priority 2: Data Loss/Corruption Issues

### 4. Marker Memory Usage for Large PDFs
**Impact**: OOM errors, system crashes  
**Fix**: Implement streaming PDF processing
```python
# Instead of loading entire PDF:
def process_pdf_streaming(pdf_path):
    with open(pdf_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            process_chunk(chunk)
```

### 5. Schema Breaking Changes in Module Communicator
**Impact**: Module communication failures  
**Fix**: Implement proper versioning
```python
SCHEMA_VERSIONS = {
    "1.0": ["id", "name", "data"],
    "1.1": ["id", "name", "data", "timestamp"],
    "2.0": ["id", "name", "payload", "metadata"]
}

def migrate_schema(data, from_version, to_version):
    # Implement migration logic
    pass
```

## Priority 3: User Experience Issues

### 6. Poor Error Messages
**Locations**:
- Marker: Encrypted PDF errors
- All modules: Generic error messages

**Fix Template**:
```python
class DetailedError(Exception):
    def __init__(self, message, suggestion=None, error_code=None):
        self.message = message
        self.suggestion = suggestion
        self.error_code = error_code
        super().__init__(self.format_message())
    
    def format_message(self):
        msg = f"Error {self.error_code}: {self.message}"
        if self.suggestion:
            msg += f"\nSuggestion: {self.suggestion}"
        return msg
```

### 7. Table Extraction Issues in Marker
**Impact**: Data loss from PDFs  
**Fix**: Use advanced table detection
- Consider using tabula-py or camelot for better table extraction
- Implement fallback strategies for complex tables

### 8. OCR Quality Issues
**Impact**: Unreadable text from scanned PDFs  
**Fix**:
```python
# Add pre-processing for low quality scans
def enhance_scan_quality(image):
    # Apply filters: denoise, sharpen, contrast adjustment
    # Use OpenCV or PIL for image enhancement
    pass
```

## Implementation Schedule

### Week 1: Critical Fixes
- [ ] Fix SPARTA import error (Day 1)
- [ ] Implement rate limiting for all external APIs (Day 2-3)
- [ ] Fix schema versioning in Module Communicator (Day 4-5)

### Week 2: Data Integrity
- [ ] Implement streaming PDF processing (Day 6-8)
- [ ] Improve error messages across all modules (Day 9-10)

### Week 3: Quality Improvements
- [ ] Fix table extraction in Marker (Day 11-13)
- [ ] Improve OCR preprocessing (Day 14-15)

## Testing Requirements

After each fix:
1. Run `granger-verify --project <project_name> --test`
2. Run specific bug hunter test to verify fix
3. Run integration tests with dependent modules
4. Update test suite to prevent regression

## Monitoring

Set up monitoring for:
- API rate limit violations
- Memory usage spikes
- Schema version mismatches
- Error message quality metrics

---

Generated: 2025-06-09
Estimated Completion: 3 weeks with 1 developer