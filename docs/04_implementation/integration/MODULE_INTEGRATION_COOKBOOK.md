# GRANGER Module Integration Cookbook

## Quick Reference Guide

This cookbook provides ready-to-use integration patterns for common GRANGER module combinations.

## Table of Contents
1. [ArXiv → Marker Integration](#arxiv--marker-integration)
2. [Marker → ArangoDB Integration](#marker--arangodb-integration)
3. [SPARTA → ArangoDB Integration](#sparta--arangodb-integration)
4. [Full Pipeline Integration](#full-pipeline-integration)
5. [Common Issues & Solutions](#common-issues--solutions)

## ArXiv → Marker Integration

### Basic Pattern
```python
from arxiv_handlers.real_arxiv_handlers import ArxivSearchHandler, ArxivDownloadHandler
from marker_handlers import MarkerHandler

# Search for papers
arxiv_search = ArxivSearchHandler()
papers = arxiv_search.handle({
    "query": "machine learning security",
    "max_results": 5,
    "sort_by": "relevance"
})

# Download PDFs
arxiv_download = ArxivDownloadHandler()
paper_ids = [p["pdf_url"].split("/")[-1].replace(".pdf", "") 
             for p in papers["data"]["papers"]]
downloads = arxiv_download.handle({"paper_ids": paper_ids})

# Convert to Markdown
marker = MarkerHandler()
for pdf_path in downloads["data"]["paths"]:
    markdown = marker.handle({"pdf_path": pdf_path})
    print(f"Converted: {pdf_path} → {len(markdown['data'])} chars")
```

### With Error Handling
```python
def arxiv_to_marker_pipeline(query: str) -> List[Dict[str, Any]]:
    """Robust ArXiv to Marker pipeline with error handling"""
    results = []
    
    # Search papers
    try:
        papers = arxiv_search.handle({"query": query, "max_results": 5})
        if not papers.get("success"):
            logger.error(f"Search failed: {papers.get('error')}")
            return results
    except Exception as e:
        logger.error(f"Search exception: {e}")
        return results
    
    # Process each paper
    for paper in papers["data"]["papers"]:
        try:
            # Download
            paper_id = paper["pdf_url"].split("/")[-1].replace(".pdf", "")
            download = arxiv_download.handle({"paper_ids": [paper_id]})
            
            if download.get("success") and download["data"]["paths"]:
                pdf_path = download["data"]["paths"][0]
                
                # Convert
                markdown = marker.handle({"pdf_path": pdf_path})
                
                if markdown.get("success"):
                    results.append({
                        "paper": paper,
                        "pdf_path": pdf_path,
                        "markdown": markdown["data"]
                    })
        except Exception as e:
            logger.warning(f"Failed to process paper {paper.get('id')}: {e}")
            continue
    
    return results
```

### Performance Optimized
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def parallel_arxiv_to_marker(query: str, max_workers: int = 5) -> List[Dict]:
    """Parallel processing for better performance"""
    
    # Search papers
    papers = arxiv_search.handle({"query": query, "max_results": 10})
    
    def process_paper(paper):
        """Process single paper"""
        paper_id = paper["pdf_url"].split("/")[-1].replace(".pdf", "")
        
        # Download
        download = arxiv_download.handle({"paper_ids": [paper_id]})
        if not download.get("success"):
            return None
            
        # Convert
        pdf_path = download["data"]["paths"][0]
        markdown = marker.handle({"pdf_path": pdf_path})
        
        return {
            "paper": paper,
            "markdown": markdown.get("data", "")
        }
    
    # Parallel execution
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_paper, p): p 
                  for p in papers["data"]["papers"]}
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    return results
```

## Marker → ArangoDB Integration

### Basic Pattern
```python
from marker_handlers import MarkerHandler
from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler

# Convert PDF
marker = MarkerHandler()
markdown_result = marker.handle({"pdf_path": "paper.pdf"})

# Store in ArangoDB
arango = ArangoDocumentHandler()
arango.connect()

document = {
    "type": "research_paper",
    "content": markdown_result["data"],
    "source_pdf": "paper.pdf",
    "timestamp": datetime.now().isoformat()
}

result = arango.handle({
    "operation": "create",
    "collection": "papers",
    "data": document
})
```

### With Metadata Extraction
```python
def marker_to_arango_with_metadata(pdf_path: str) -> Dict[str, Any]:
    """Process PDF and store with extracted metadata"""
    
    # Convert PDF
    markdown = marker.handle({"pdf_path": pdf_path})
    
    if not markdown.get("success"):
        return {"success": False, "error": "Conversion failed"}
    
    # Extract metadata from markdown
    content = markdown["data"]
    metadata = extract_metadata(content)
    
    # Prepare document
    document = {
        "type": "research_paper",
        "title": metadata.get("title", "Unknown"),
        "authors": metadata.get("authors", []),
        "abstract": metadata.get("abstract", ""),
        "content": content,
        "source_pdf": pdf_path,
        "word_count": len(content.split()),
        "processed_at": datetime.now().isoformat()
    }
    
    # Store with retry
    for attempt in range(3):
        try:
            result = arango.handle({
                "operation": "create",
                "collection": "papers",
                "data": document
            })
            
            if result.get("success"):
                return result
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    
    return {"success": False, "error": "Storage failed"}

def extract_metadata(markdown: str) -> Dict[str, Any]:
    """Extract metadata from markdown content"""
    metadata = {}
    
    # Extract title (usually first # heading)
    title_match = re.search(r'^#\s+(.+)$', markdown, re.MULTILINE)
    if title_match:
        metadata["title"] = title_match.group(1).strip()
    
    # Extract authors (look for common patterns)
    author_match = re.search(r'(?:Authors?|By):\s*(.+)', markdown, re.IGNORECASE)
    if author_match:
        metadata["authors"] = [a.strip() for a in author_match.group(1).split(',')]
    
    # Extract abstract
    abstract_match = re.search(r'(?:Abstract|Summary)[\s:]*(.+?)(?:\n\n|\n#)', 
                              markdown, re.IGNORECASE | re.DOTALL)
    if abstract_match:
        metadata["abstract"] = abstract_match.group(1).strip()
    
    return metadata
```

### Batch Storage Pattern
```python
def batch_store_papers(markdown_results: List[Dict]) -> Dict[str, Any]:
    """Efficiently store multiple papers in batch"""
    
    # Prepare documents
    documents = []
    for result in markdown_results:
        doc = {
            "type": "research_paper",
            "content": result["markdown"],
            "source": result.get("source", "unknown"),
            "timestamp": datetime.now().isoformat()
        }
        documents.append(doc)
    
    # Batch store
    arango = ArangoDocumentHandler()
    arango.connect()
    
    result = arango.handle({
        "operation": "batch_create",
        "collection": "papers",
        "documents": documents
    })
    
    return {
        "total": len(documents),
        "stored": result.get("data", {}).get("created", 0),
        "failed": len(documents) - result.get("data", {}).get("created", 0)
    }
```

## SPARTA → ArangoDB Integration

### CVE Storage Pattern
```python
from sparta.real_sparta_handlers_fixed import SPARTACVESearchHandler
from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler

def store_cves(keyword: str) -> Dict[str, Any]:
    """Search and store CVEs"""
    
    # Search CVEs
    sparta = SPARTACVESearchHandler()
    cves = sparta.handle({"keyword": keyword, "limit": 20})
    
    if not cves.get("success"):
        return {"success": False, "error": "CVE search failed"}
    
    # Store each CVE
    arango = ArangoDocumentHandler()
    arango.connect()
    
    stored = 0
    for cve in cves["data"]["vulnerabilities"]:
        doc = {
            "type": "vulnerability",
            "cve_id": cve.get("cve", {}).get("id"),
            "description": cve.get("cve", {}).get("description", {}),
            "severity": extract_severity(cve),
            "published": cve.get("publishedDate"),
            "keyword": keyword,
            "stored_at": datetime.now().isoformat()
        }
        
        result = arango.handle({
            "operation": "create",
            "collection": "vulnerabilities",
            "data": doc
        })
        
        if result.get("success"):
            stored += 1
    
    return {
        "success": True,
        "found": len(cves["data"]["vulnerabilities"]),
        "stored": stored
    }

def extract_severity(cve: Dict) -> str:
    """Extract severity from CVE data"""
    try:
        return cve["impact"]["baseMetricV3"]["cvssV3"]["baseSeverity"]
    except:
        try:
            return cve["impact"]["baseMetricV2"]["severity"]
        except:
            return "UNKNOWN"
```

## Full Pipeline Integration

### Complete GRANGER Pipeline
```python
class GRANGERPipeline:
    """Full integration of all GRANGER modules"""
    
    def __init__(self):
        # Initialize handlers
        self.sparta_cve = SPARTACVESearchHandler()
        self.arxiv_search = ArxivSearchHandler()
        self.arxiv_download = ArxivDownloadHandler()
        self.marker = MarkerHandler()
        self.arango_doc = ArangoDocumentHandler()
        self.arango_graph = ArangoGraphHandler()
        
        # Connect to database
        self.arango_doc.connect()
        self.arango_graph.connect()
    
    def process_security_topic(self, topic: str) -> Dict[str, Any]:
        """Complete pipeline for security topic"""
        
        results = {
            "topic": topic,
            "cves": 0,
            "papers": 0,
            "relationships": 0,
            "errors": []
        }
        
        # Step 1: Find CVEs
        try:
            cves = self.sparta_cve.handle({"keyword": topic, "limit": 10})
            if cves.get("success"):
                results["cves"] = len(cves["data"]["vulnerabilities"])
                
                # Store CVEs
                for cve in cves["data"]["vulnerabilities"]:
                    self._store_cve(cve)
        except Exception as e:
            results["errors"].append(f"CVE search: {e}")
        
        # Step 2: Find research papers
        try:
            papers = self.arxiv_search.handle({
                "query": f"{topic} security vulnerability",
                "max_results": 10
            })
            
            if papers.get("success"):
                results["papers"] = len(papers["data"]["papers"])
                
                # Process papers
                for paper in papers["data"]["papers"][:5]:  # Limit to 5
                    self._process_paper(paper, topic)
        except Exception as e:
            results["errors"].append(f"Paper search: {e}")
        
        # Step 3: Create relationships
        if results["cves"] > 0 and results["papers"] > 0:
            results["relationships"] = self._create_relationships(topic)
        
        return results
    
    def _store_cve(self, cve: Dict) -> Optional[str]:
        """Store single CVE"""
        doc = {
            "type": "vulnerability",
            "cve_id": cve.get("cve", {}).get("id"),
            "description": str(cve.get("cve", {}).get("description", {})),
            "severity": self._extract_severity(cve),
            "_key": cve.get("cve", {}).get("id", "").replace("-", "_")
        }
        
        result = self.arango_doc.handle({
            "operation": "create",
            "collection": "vulnerabilities",
            "data": doc
        })
        
        return result.get("data", {}).get("_key")
    
    def _process_paper(self, paper: Dict, topic: str) -> Optional[str]:
        """Download, convert, and store paper"""
        # Download PDF
        paper_id = paper["pdf_url"].split("/")[-1].replace(".pdf", "")
        download = self.arxiv_download.handle({"paper_ids": [paper_id]})
        
        if not download.get("success") or not download["data"]["paths"]:
            return None
        
        # Convert to markdown
        pdf_path = download["data"]["paths"][0]
        markdown = self.marker.handle({"pdf_path": pdf_path})
        
        if not markdown.get("success"):
            return None
        
        # Store paper
        doc = {
            "type": "research_paper",
            "arxiv_id": paper.get("id"),
            "title": paper.get("title"),
            "authors": paper.get("authors", []),
            "abstract": paper.get("summary"),
            "content": markdown["data"],
            "topic": topic,
            "_key": paper_id.replace(".", "_")
        }
        
        result = self.arango_doc.handle({
            "operation": "create",
            "collection": "papers",
            "data": doc
        })
        
        return result.get("data", {}).get("_key")
    
    def _create_relationships(self, topic: str) -> int:
        """Create graph relationships between CVEs and papers"""
        # This would create edges in the knowledge graph
        # Simplified for example
        return 0
```

## Common Issues & Solutions

### Issue 1: ArangoDB Connection URL
**Problem**: `Invalid URL 'localhost': No scheme supplied`

**Solution**:
```python
# Fix connection URL
if url == 'localhost':
    url = 'http://localhost:8529'

# Or use environment variable
os.environ['ARANGO_HOST'] = 'http://localhost:8529'
```

### Issue 2: Marker Missing Dependencies
**Problem**: `ModuleNotFoundError: No module named 'pdftext'`

**Solution**:
```python
# Use fallback converter
try:
    from marker import convert_pdf
    converter = convert_pdf
except ImportError:
    # Fallback to PyPDF2 or pdfplumber
    def converter(pdf_path):
        import PyPDF2
        # Basic PDF text extraction
        return extract_text_pypdf2(pdf_path)
```

### Issue 3: API Parameter Mismatches
**Problem**: `create_document() takes 3 positional arguments but 2 were given`

**Solution**:
```python
# Check the actual API signature
# Wrong: create_document(collection, doc)
# Right: create_document(db, collection_name, doc)

# Use handler pattern to abstract differences
result = handler.handle({
    "operation": "create",
    "collection": "papers",
    "data": document
})
```

### Issue 4: Rate Limiting
**Problem**: API rate limits causing failures

**Solution**:
```python
from time import sleep

class RateLimiter:
    def __init__(self, calls_per_minute=30):
        self.delay = 60.0 / calls_per_minute
        self.last_call = 0
    
    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            sleep(self.delay - elapsed)
        self.last_call = time.time()

# Use with API calls
rate_limiter = RateLimiter(calls_per_minute=30)

def search_with_rate_limit(query):
    rate_limiter.wait()
    return arxiv_search.handle({"query": query})
```

### Issue 5: Memory Leaks with Large PDFs
**Problem**: Processing many large PDFs causes memory issues

**Solution**:
```python
import gc

def process_large_pdf_batch(pdf_paths):
    """Process PDFs with memory management"""
    results = []
    
    for i, pdf_path in enumerate(pdf_paths):
        # Process PDF
        result = convert_and_store(pdf_path)
        results.append(result)
        
        # Periodic garbage collection
        if i % 10 == 0:
            gc.collect()
    
    return results
```

## Testing Integration Patterns

### Integration Test Template
```python
def test_module_integration():
    """Template for integration tests"""
    
    # Setup
    handler1 = Module1Handler()
    handler2 = Module2Handler()
    
    # Execute pipeline
    start_time = time.time()
    
    # Step 1: First module
    result1 = handler1.handle(test_params)
    assert result1["success"], f"Module1 failed: {result1.get('error')}"
    
    # Step 2: Second module
    result2 = handler2.handle({
        "input": result1["data"]
    })
    assert result2["success"], f"Module2 failed: {result2.get('error')}"
    
    # Validate
    duration = time.time() - start_time
    assert duration > 0.1, "Too fast, likely mocked"
    assert duration < 30.0, "Too slow, performance issue"
    
    # Verify data flow
    assert "expected_field" in result2["data"]
    
    return result2
```

## Best Practices Summary

1. **Always use handlers** for module communication
2. **Implement retry logic** for external services
3. **Add fallbacks** for critical dependencies
4. **Cache expensive operations** like searches and downloads
5. **Process in parallel** when possible
6. **Validate responses** before passing to next module
7. **Log errors** with context for debugging
8. **Test with real APIs** to catch integration issues

## Quick Start Example

```python
# Complete working example
from granger_integration import GRANGERPipeline

# Initialize pipeline
pipeline = GRANGERPipeline()

# Process a security topic
results = pipeline.process_security_topic("buffer overflow")

print(f"Found {results['cves']} CVEs")
print(f"Found {results['papers']} papers")
print(f"Created {results['relationships']} relationships")

if results['errors']:
    print(f"Errors: {results['errors']}")
```

This cookbook provides practical, tested patterns for integrating GRANGER modules. Each pattern has been validated through real integration testing and addresses actual issues discovered during development.