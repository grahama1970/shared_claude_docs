# GRANGER Error Handling Strategies

## Overview
This document captures error handling strategies discovered through real integration testing of the GRANGER system. Each strategy addresses specific failure modes observed during Phase 2 testing.

## Error Categories

### 1. Connection Errors
**Observed**: ArangoDB connection failures due to URL format issues

**Strategy**: URL Validation and Correction
```python
def safe_connect(url: str) -> ArangoClient:
    """Connect with URL validation and correction"""
    # Common fixes
    if url == 'localhost':
        url = 'http://localhost:8529'
    elif url.startswith('localhost:'):
        url = f'http://{url}'
    elif not url.startswith(('http://', 'https://')):
        url = f'http://{url}'
    
    try:
        client = ArangoClient(hosts=url)
        # Test connection
        sys_db = client.db('_system')
        sys_db.properties()  # Will fail if not connected
        return client
    except Exception as e:
        # Try alternative URLs
        alternatives = [
            'http://localhost:8529',
            'http://127.0.0.1:8529',
            'http://arangodb:8529'  # Docker service name
        ]
        
        for alt_url in alternatives:
            try:
                client = ArangoClient(hosts=alt_url)
                sys_db = client.db('_system')
                sys_db.properties()
                logger.info(f"Connected using alternative URL: {alt_url}")
                return client
            except:
                continue
        
        raise ConnectionError(f"Failed to connect to ArangoDB: {e}")
```

### 2. Missing Dependencies
**Observed**: Marker module fails due to missing 'pdftext' dependency

**Strategy**: Graceful Degradation Chain
```python
class PDFConverterChain:
    """Chain of responsibility for PDF conversion"""
    
    def __init__(self):
        self.converters = []
        self._setup_converters()
    
    def _setup_converters(self):
        """Setup available converters in priority order"""
        # Try marker first
        try:
            from marker import convert_pdf
            self.converters.append(('marker', convert_pdf))
        except ImportError:
            logger.warning("Marker not available")
        
        # Try PyPDF2
        try:
            import PyPDF2
            self.converters.append(('pypdf2', self._pypdf2_convert))
        except ImportError:
            logger.warning("PyPDF2 not available")
        
        # Try pdfplumber
        try:
            import pdfplumber
            self.converters.append(('pdfplumber', self._pdfplumber_convert))
        except ImportError:
            logger.warning("pdfplumber not available")
        
        # Always have basic fallback
        self.converters.append(('basic', self._basic_convert))
    
    def convert(self, pdf_path: str) -> Dict[str, Any]:
        """Convert PDF using first available converter"""
        for name, converter in self.converters:
            try:
                result = converter(pdf_path)
                return {
                    "success": True,
                    "data": result,
                    "converter": name
                }
            except Exception as e:
                logger.warning(f"{name} converter failed: {e}")
                continue
        
        return {
            "success": False,
            "error": "All converters failed",
            "attempted": [name for name, _ in self.converters]
        }
```

### 3. API Rate Limiting
**Observed**: NASA API returns 403, NVD has rate limits

**Strategy**: Adaptive Rate Limiting with Backoff
```python
class AdaptiveRateLimiter:
    """Automatically adjusts rate based on API responses"""
    
    def __init__(self, initial_delay=0.1):
        self.delay = initial_delay
        self.last_call = 0
        self.consecutive_errors = 0
        self.max_delay = 60.0
    
    def wait(self):
        """Wait with adaptive delay"""
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_call = time.time()
    
    def success(self):
        """Called on successful API response"""
        self.consecutive_errors = 0
        # Gradually reduce delay
        self.delay = max(0.1, self.delay * 0.9)
    
    def rate_limited(self):
        """Called on rate limit error"""
        self.consecutive_errors += 1
        # Exponential backoff
        self.delay = min(self.max_delay, self.delay * 2)
        logger.warning(f"Rate limited, increasing delay to {self.delay}s")
    
    def request_with_limiting(self, func, *args, **kwargs):
        """Execute request with rate limiting"""
        self.wait()
        
        try:
            result = func(*args, **kwargs)
            
            # Check for rate limit indicators
            if isinstance(result, dict):
                if result.get('status_code') == 429:
                    self.rate_limited()
                    raise RateLimitError()
                elif result.get('status_code') == 403:
                    # Might be rate limit disguised as forbidden
                    self.rate_limited()
                    raise RateLimitError()
            
            self.success()
            return result
            
        except RateLimitError:
            # Wait extra time before re-raising
            time.sleep(self.delay)
            raise
```

### 4. Parameter Mismatches
**Observed**: Function signatures don't match expected parameters

**Strategy**: Parameter Adaptation Layer
```python
class ParameterAdapter:
    """Adapts parameters to match actual function signatures"""
    
    def __init__(self):
        self.adaptations = {
            'create_document': self._adapt_create_document,
            'search': self._adapt_search,
            'ensure_graph': self._adapt_ensure_graph
        }
    
    def adapt(self, operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt parameters for specific operation"""
        if operation in self.adaptations:
            return self.adaptations[operation](params)
        return params
    
    def _adapt_create_document(self, params: Dict) -> Dict:
        """Fix create_document parameters"""
        adapted = params.copy()
        
        # Handle different parameter names
        if 'collection' in params and 'collection_name' not in params:
            adapted['collection_name'] = params.pop('collection')
        
        if 'data' in params and 'document' not in params:
            adapted['document'] = params.pop('data')
        
        return adapted
    
    def _adapt_search(self, params: Dict) -> Dict:
        """Fix search parameters"""
        adapted = params.copy()
        
        # Remove unsupported parameters
        if 'collection_name' in params:
            # Store for potential use in query
            collection = params.pop('collection_name')
            adapted['_collection_hint'] = collection
        
        return adapted
```

### 5. Transient Failures
**Observed**: Temporary network issues, service unavailability

**Strategy**: Circuit Breaker with Health Checks
```python
class SmartCircuitBreaker:
    """Circuit breaker with active health checking"""
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
            else:
                raise CircuitOpenError(f"Circuit open until {self._reset_time()}")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if we should try to close circuit"""
        return (self.last_failure and 
                time.time() - self.last_failure > self.recovery_timeout)
    
    def _on_success(self):
        """Handle successful call"""
        if self.state == 'HALF_OPEN':
            logger.info("Circuit breaker reset to CLOSED")
            self.state = 'CLOSED'
        self.failures = 0
    
    def _on_failure(self):
        """Handle failed call"""
        self.failures += 1
        self.last_failure = time.time()
        
        if self.failures >= self.failure_threshold:
            logger.warning(f"Circuit breaker OPEN after {self.failures} failures")
            self.state = 'OPEN'
        elif self.state == 'HALF_OPEN':
            logger.warning("Circuit breaker remains OPEN after half-open test")
            self.state = 'OPEN'
    
    async def health_check(self, check_func):
        """Actively check service health"""
        if self.state == 'OPEN' and self._should_attempt_reset():
            try:
                await check_func()
                logger.info("Health check passed, closing circuit")
                self.state = 'CLOSED'
                self.failures = 0
            except:
                logger.info("Health check failed, circuit remains open")
                self.last_failure = time.time()
```

### 6. Data Validation Errors
**Observed**: Invalid data formats cause downstream failures

**Strategy**: Defensive Data Validation
```python
class DataValidator:
    """Validate and sanitize data between modules"""
    
    @staticmethod
    def validate_arxiv_paper(paper: Dict) -> Dict:
        """Validate and fix ArXiv paper data"""
        validated = {}
        
        # Required fields with defaults
        validated['id'] = paper.get('id', 'unknown')
        validated['title'] = paper.get('title', 'Untitled')
        validated['authors'] = paper.get('authors', [])
        
        # Ensure authors is a list
        if isinstance(validated['authors'], str):
            validated['authors'] = [validated['authors']]
        
        # Clean and validate PDF URL
        pdf_url = paper.get('pdf_url', '')
        if pdf_url and pdf_url.startswith('http'):
            validated['pdf_url'] = pdf_url
        else:
            # Try to construct from ID
            validated['pdf_url'] = f"https://arxiv.org/pdf/{validated['id']}.pdf"
        
        # Validate summary
        validated['summary'] = paper.get('summary', '')
        if len(validated['summary']) > 10000:
            validated['summary'] = validated['summary'][:10000] + '...'
        
        return validated
    
    @staticmethod
    def validate_cve(cve: Dict) -> Dict:
        """Validate and fix CVE data"""
        validated = {}
        
        # Extract CVE ID
        cve_data = cve.get('cve', {})
        validated['id'] = cve_data.get('id', 'CVE-UNKNOWN')
        
        # Safe description extraction
        desc_data = cve_data.get('description', {})
        desc_list = desc_data.get('description_data', [])
        if desc_list and isinstance(desc_list, list):
            validated['description'] = desc_list[0].get('value', 'No description')
        else:
            validated['description'] = str(desc_data)[:1000]
        
        # Safe severity extraction
        try:
            validated['severity'] = (cve.get('impact', {})
                                       .get('baseMetricV3', {})
                                       .get('cvssV3', {})
                                       .get('baseSeverity', 'UNKNOWN'))
        except:
            validated['severity'] = 'UNKNOWN'
        
        return validated
```

### 7. Cascading Failures
**Observed**: One module failure causes entire pipeline to fail

**Strategy**: Bulkhead Pattern with Partial Results
```python
class BulkheadPipeline:
    """Isolate failures to prevent cascading"""
    
    def __init__(self):
        self.results = {
            'successful': [],
            'failed': [],
            'partial': []
        }
    
    async def process_with_bulkheads(self, items: List[Any], 
                                   processors: List[callable]) -> Dict:
        """Process items through pipeline with failure isolation"""
        
        for item in items:
            item_result = {
                'item': item,
                'stages': {},
                'status': 'success'
            }
            
            for processor in processors:
                stage_name = processor.__name__
                
                try:
                    # Process with timeout
                    result = await asyncio.wait_for(
                        processor(item_result.get('last_output', item)),
                        timeout=30.0
                    )
                    
                    item_result['stages'][stage_name] = 'success'
                    item_result['last_output'] = result
                    
                except asyncio.TimeoutError:
                    logger.error(f"Timeout in {stage_name} for item {item}")
                    item_result['stages'][stage_name] = 'timeout'
                    item_result['status'] = 'partial'
                    break
                    
                except Exception as e:
                    logger.error(f"Error in {stage_name}: {e}")
                    item_result['stages'][stage_name] = f'error: {str(e)}'
                    item_result['status'] = 'partial'
                    break
            
            # Categorize result
            if item_result['status'] == 'success':
                self.results['successful'].append(item_result)
            elif any(v == 'success' for v in item_result['stages'].values()):
                self.results['partial'].append(item_result)
            else:
                self.results['failed'].append(item_result)
        
        return self.results
```

## Error Recovery Patterns

### 1. Retry with Jitter
```python
def retry_with_jitter(max_attempts=3, base_delay=1.0, max_delay=60.0):
    """Retry with exponential backoff and jitter"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    
                    # Exponential backoff with jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)
                    
                    logger.info(f"Retry {attempt + 1}/{max_attempts} after {delay + jitter:.2f}s")
                    await asyncio.sleep(delay + jitter)
            
        return wrapper
    return decorator
```

### 2. Fallback Chain
```python
class FallbackChain:
    """Execute fallback strategies in sequence"""
    
    def __init__(self, strategies: List[Tuple[str, callable]]):
        self.strategies = strategies
    
    async def execute(self, *args, **kwargs):
        """Try each strategy until one succeeds"""
        errors = []
        
        for name, strategy in self.strategies:
            try:
                logger.info(f"Trying strategy: {name}")
                result = await strategy(*args, **kwargs)
                logger.info(f"Strategy {name} succeeded")
                return result
            except Exception as e:
                logger.warning(f"Strategy {name} failed: {e}")
                errors.append((name, str(e)))
        
        # All strategies failed
        error_summary = "; ".join(f"{name}: {error}" for name, error in errors)
        raise Exception(f"All strategies failed: {error_summary}")
```

### 3. Compensation Actions
```python
class CompensatingTransaction:
    """Undo operations on failure"""
    
    def __init__(self):
        self.operations = []
    
    def add_operation(self, do_func, undo_func, *args, **kwargs):
        """Add operation with compensation"""
        self.operations.append({
            'do': do_func,
            'undo': undo_func,
            'args': args,
            'kwargs': kwargs,
            'result': None
        })
    
    async def execute(self):
        """Execute operations with automatic rollback on failure"""
        completed = []
        
        try:
            for op in self.operations:
                result = await op['do'](*op['args'], **op['kwargs'])
                op['result'] = result
                completed.append(op)
            
            return [op['result'] for op in self.operations]
            
        except Exception as e:
            # Rollback completed operations
            logger.error(f"Operation failed, rolling back: {e}")
            
            for op in reversed(completed):
                try:
                    await op['undo'](op['result'])
                    logger.info(f"Rolled back {op['do'].__name__}")
                except Exception as undo_error:
                    logger.error(f"Rollback failed: {undo_error}")
            
            raise
```

## Monitoring and Alerting

### Error Metrics Collection
```python
class ErrorMetrics:
    """Collect and analyze error patterns"""
    
    def __init__(self):
        self.errors = defaultdict(list)
        self.window_size = 300  # 5 minutes
    
    def record_error(self, error_type: str, details: Dict):
        """Record error occurrence"""
        self.errors[error_type].append({
            'timestamp': time.time(),
            'details': details
        })
        
        # Clean old errors
        cutoff = time.time() - self.window_size
        self.errors[error_type] = [
            e for e in self.errors[error_type] 
            if e['timestamp'] > cutoff
        ]
    
    def get_error_rate(self, error_type: str) -> float:
        """Get error rate per minute"""
        count = len(self.errors[error_type])
        return count / (self.window_size / 60)
    
    def should_alert(self, error_type: str, threshold: float = 10.0) -> bool:
        """Check if error rate exceeds threshold"""
        return self.get_error_rate(error_type) > threshold
```

## Best Practices

1. **Log Everything**: Include context in error messages
2. **Fail Fast**: Validate inputs early
3. **Timeout Everything**: Prevent indefinite hangs
4. **Monitor Patterns**: Track error rates and patterns
5. **Document Failures**: Keep error documentation updated
6. **Test Error Paths**: Explicitly test error handling
7. **Graceful Degradation**: Provide partial results when possible

## Conclusion

These error handling strategies were discovered through real integration testing of the GRANGER system. They provide robust patterns for handling the various failure modes observed in distributed module architectures. The key insight is that errors are inevitable in distributed systems, but with proper handling strategies, the system can remain resilient and provide value even when components fail.