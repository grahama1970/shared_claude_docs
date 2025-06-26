# Implementation Priority Plan

Based on bug hunting results (26 bugs found across 9 modules), here's the prioritized implementation plan:

## 🔴 Priority 1: System Breaking Issues (Week 1)

### 1. Fix SPARTA Syntax Error
**File**: `/home/graham/workspace/experiments/sparta/src/sparta/core/__init__.py`
```python
# Fix missing closing quotes in docstring
"""Core business logic for SPARTA module."""
```

### 2. Implement Rate Limiting Across All Modules
**Implementation**: Copy `granger_common` to each project
```bash
# For each project:
cp -r /home/graham/workspace/shared_claude_docs/granger_common /home/graham/workspace/experiments/sparta/src/
cp -r /home/graham/workspace/shared_claude_docs/granger_common /home/graham/workspace/experiments/youtube_transcripts/src/
# ... etc
```

**Code Changes**:
- SPARTA: Add `rate_limiter = get_rate_limiter("nvd")` 
- YouTube: Add `rate_limiter = get_rate_limiter("youtube")`
- All external API calls: Wrap with `rate_limiter.acquire()`

### 3. Fix Schema Breaking Changes
**Implementation**: Use `granger_common.schema_manager`
```python
# In Module Communicator
from granger_common import schema_manager

# Ensure all messages are compatible
compatible_msg = schema_manager.ensure_compatibility(
    sender_message, 
    receiver_version="2.0"
)
```

## 🟡 Priority 2: Data Loss/Corruption (Week 2)

### 4. Marker Memory Management
**Implementation**: Use `SmartPDFHandler` with 1GB threshold
```python
from granger_common import SmartPDFHandler

handler = SmartPDFHandler(memory_threshold_mb=1000)
result = handler.process_pdf(pdf_path)
```

### 5. Unsloth Training Robustness
**Issues to fix**:
- Add JSON validation before training
- Implement checkpoint recovery
- Fix memory leak in data loading

```python
# Add validation
def validate_training_data(jsonl_path):
    with open(jsonl_path) as f:
        for line_num, line in enumerate(f, 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at line {line_num}: {e}")

# Add checkpoint recovery
def resume_training(checkpoint_path):
    if checkpoint_path.exists():
        state = torch.load(checkpoint_path)
        model.load_state_dict(state['model'])
        optimizer.load_state_dict(state['optimizer'])
        start_epoch = state['epoch']
        logger.info(f"Resumed from epoch {start_epoch}")
```

### 6. YouTube Long Video Handling
**Implementation**: Chunk processing for videos > 2 hours
```python
def fetch_long_video_transcript(video_id, duration_seconds):
    if duration_seconds > 7200:  # 2 hours
        # Process in 1-hour chunks
        chunks = []
        for start in range(0, duration_seconds, 3600):
            chunk = fetch_transcript_chunk(video_id, start, min(start+3600, duration_seconds))
            chunks.extend(chunk)
        return chunks
    else:
        return fetch_transcript(video_id)
```

## 🟢 Priority 3: Quality Improvements (Week 3)

### 7. Improve Error Messages
**Template for all modules**:
```python
class DetailedError(Exception):
    ERROR_CODES = {
        "PDF_ENCRYPTED": "The PDF is password protected",
        "NO_CAPTIONS": "This video does not have captions available",
        "CVE_NOT_FOUND": "CVE ID not found in NVD database",
        "CHECKPOINT_CORRUPT": "Training checkpoint is corrupted"
    }
    
    def __init__(self, code, details=None):
        self.code = code
        self.message = self.ERROR_CODES.get(code, "Unknown error")
        self.details = details
        super().__init__(f"{code}: {self.message}" + (f" - {details}" if details else ""))
```

### 8. Add Missing Metrics
**Unsloth GPU memory tracking**:
```python
import torch

def log_gpu_memory():
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            memory_used = torch.cuda.memory_allocated(i) / 1024**3
            memory_total = torch.cuda.get_device_properties(i).total_memory / 1024**3
            logger.info(f"GPU {i}: {memory_used:.1f}/{memory_total:.1f} GB")
```

## Implementation Checklist

### Week 1 (Critical)
- [ ] Fix SPARTA syntax error
- [ ] Deploy rate limiting to all modules
- [ ] Test schema compatibility between all module pairs
- [ ] Verify Module Communicator routing with new schemas

### Week 2 (Data Integrity)  
- [ ] Deploy SmartPDFHandler to Marker
- [ ] Fix Unsloth memory leak
- [ ] Implement checkpoint recovery
- [ ] Add YouTube chunked processing

### Week 3 (Quality)
- [ ] Standardize error messages across all modules
- [ ] Add GPU memory metrics to Unsloth
- [ ] Improve OCR quality checks in Marker
- [ ] Add caption quality indicators to YouTube

## Testing Requirements

After each implementation:
1. Run module-specific bug hunter test
2. Run integration test with dependent modules
3. Verify with `granger-verify --project <name> --test`
4. Check logs for proper rate limiting

## Success Metrics

- **Week 1**: All modules can communicate, no syntax errors, rate limiting active
- **Week 2**: Can process 2GB PDFs, training can resume, 8-hour videos work
- **Week 3**: Clear error messages, all metrics tracked, quality indicators present

---

Total Implementation Time: 3 weeks
Developer Resources: 1-2 developers
Testing Time: 20% of development time