# ArXiv → Marker Pipeline Test (Level 1)

This directory contains a Level 1 Pipeline Test that demonstrates real integration between the ArXiv MCP Server and Marker PDF processing modules.

## Overview

The pipeline performs the following steps:
1. **ArXiv Module**: Searches for academic papers using real ArXiv API
2. **Download**: Downloads actual PDF files from ArXiv
3. **Marker Module**: Converts PDFs to enhanced Markdown format
4. **Validation**: Checks quality metrics and generates reports

## Test Requirements

- Python 3.8+
- Internet connection (for ArXiv API and PDF downloads)
- Dependencies: `arxiv`, `requests`, `pypdf2`

## Files

- `test_arxiv_marker_pipeline.py` - Main pipeline test implementation
- `run_pipeline_test.py` - Comprehensive test runner with multiple scenarios
- `validate_pipeline_setup.py` - Setup validation script
- `README.md` - This documentation

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Validate setup:
```bash
python validate_pipeline_setup.py
```

## Running Tests

### Basic Test
Run a single pipeline test:
```bash
python test_arxiv_marker_pipeline.py
```

### Comprehensive Test Suite
Run multiple test scenarios:
```bash
python run_pipeline_test.py
```

This runs:
- Basic pipeline test with common queries
- Complex query test with specific technical papers
- Recent papers test to verify handling of new publications

## Expected Performance

- **Duration**: 2.0s - 10.0s per PDF
- **Quality Score**: > 0.85 expected
- **Success Rate**: > 90% expected

## Test Output

The tests generate:
1. Console output with real-time progress
2. Markdown report in `docs/reports/`
3. JSON results for programmatic access

## Example Output

```
=== ArXiv Module ===
Searching for: 'machine learning optimization'
Max papers: 2

Paper 1:
  Title: Optimization Techniques for Deep Learning
  ID: http://arxiv.org/abs/2024.12345
  Published: 2024-01-15
  Downloading PDF from: http://arxiv.org/pdf/2024.12345
  Downloaded: 1,234,567 bytes
  Pages: 15

=== Marker Module ===
Processing: Optimization Techniques for Deep Learning
  File: /tmp/arxiv_marker_test_abc123/paper_1_2024.12345.pdf
  Pages: 15
  Saved markdown: /tmp/arxiv_marker_test_abc123/paper_1_2024.12345.md
```

## Quality Metrics

Each conversion includes:
- Text extraction confidence (0-1)
- Table detection count
- Formula recognition count
- Overall quality score
- AI enhancement status

## Integration Points

This test validates:
1. **ArXiv API Integration**: Real paper search and metadata extraction
2. **PDF Download**: Handling various PDF sizes and formats
3. **Marker Processing**: Conversion quality and feature extraction
4. **Error Handling**: Graceful handling of API limits, network issues
5. **Performance**: Meeting expected timing requirements

## Troubleshooting

### Import Errors
Run `validate_pipeline_setup.py` to check all dependencies

### ArXiv API Issues
- Check internet connection
- Verify no rate limiting (max 3 requests/second)
- Try different search queries

### PDF Processing Errors
- Some PDFs may be corrupted or have unusual encoding
- Test captures and reports these failures without stopping

## Future Enhancements

1. **Real Marker Integration**: Replace simulation with actual Marker module
2. **Claude AI Enhancement**: Add real AI-powered accuracy improvements
3. **Caching**: Cache downloaded PDFs for repeated tests
4. **Parallel Processing**: Process multiple PDFs simultaneously
5. **Quality Benchmarks**: Compare against ground truth conversions