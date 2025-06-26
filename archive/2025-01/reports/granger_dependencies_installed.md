# Granger Ecosystem Dependencies Installation Report

## Date: 2025-06-09

### Successfully Installed Dependencies

The following PyPI dependencies were missing and have been successfully installed:

1. **backoff==2.2.1** - Retry decorator for functions
2. **grep-ast==0.9.0** - AST-based code search tool
   - Also installed: tree-sitter==0.24.0 and related packages
3. **mss==10.0.0** - Cross-platform screenshot module
4. **prompt-toolkit==3.0.51** - Library for building powerful interactive command lines
   - Also installed: wcwidth==0.2.13
5. **pymupdf==1.26.0** - Python bindings for MuPDF (PDF processing)
6. **pypandoc==1.15** - Wrapper for pandoc document converter
7. **pyperclip==1.9.0** - Cross-platform clipboard functions
8. **sounddevice==0.5.2** - Audio playback and recording
   - Also installed: cffi==1.17.1, pycparser==2.22
9. **soundfile==0.13.1** - Audio file I/O
10. **pytube==15.0.0** - YouTube video downloader
11. **configargparse==1.7.1** - Configuration file and command line argument parser
12. **fastmcp==2.7.1** - Fast Model Context Protocol implementation
    - Also installed: authlib==1.6.0, cryptography==45.0.3, openapi-pydantic==0.5.1

### Already Installed Dependencies

The following dependencies were already present in the environment:
- beautifulsoup4==4.13.4
- gitpython==3.1.44
- mkdocs==1.6.1
- mkdocs-material==9.6.14
- mkdocs-mermaid2-plugin==1.2.1
- Pillow==11.2.1
- pymdown-extensions==10.15
- PyYAML==6.0.2

### Notes on pyproject.toml Errors

Multiple projects have syntax errors in their pyproject.toml files that need to be fixed:
- granger_hub
- rl_commons
- world_model
- claude_test_reporter
- shared_docs
- llm_call
- arangodb
- sparta
- marker
- youtube_transcripts
- unsloth
- darpa_crawl
- chat
- annotator
- aider_daemon
- arxiv_mcp
- mcp_screenshot
- gitget

These errors appear to be related to Python syntax issues in the toml files, particularly:
- "unmatched ')'" errors
- "unknown extension ?)" errors

### Installation Method

All dependencies were installed using `uv pip install` as the `uv add` command had issues with the fine_tuning package build.

### Next Steps

1. The pyproject.toml syntax errors in various projects should be investigated and fixed
2. The fine_tuning package appears to have build issues that need resolution
3. Consider updating the global pyproject.toml to include these common dependencies