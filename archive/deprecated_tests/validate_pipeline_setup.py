#!/usr/bin/env python3
"""
Module: validate_pipeline_setup.py
Purpose: Validate that all dependencies are available for pipeline testing

Example Usage:
>>> python validate_pipeline_setup.py
"""

import sys
from pathlib import Path


def check_imports():
    """Check all required imports are available"""
    print("Checking required imports...")
    
    failed = []
    
    # Check arxiv
    try:
        import arxiv
        print("✅ arxiv module available")
    except ImportError as e:
        print("❌ arxiv module missing")
        failed.append(("arxiv", str(e)))
    
    # Check requests
    try:
        import requests
        print("✅ requests module available")
    except ImportError as e:
        print("❌ requests module missing")
        failed.append(("requests", str(e)))
    
    # Check PyPDF2
    try:
        import PyPDF2
        print("✅ PyPDF2 module available")
    except ImportError as e:
        print("❌ PyPDF2 module missing")
        failed.append(("PyPDF2", str(e)))
    
    # Check interaction framework
    try:
        sys.path.append(str(Path(__file__).parent.parent.parent))
        sys.path.append(str(Path(__file__).parent.parent.parent.parent))
        from templates.interaction_framework import Level1Interaction, InteractionResult
        print("✅ Interaction framework available")
    except ImportError as e:
        print("❌ Interaction framework missing")
        failed.append(("interaction_framework", str(e)))
    
    return failed


def test_arxiv_connection():
    """Test basic ArXiv API connection"""
    print("\nTesting ArXiv API connection...")
    
    try:
        import arxiv
        
        # Search for a single paper
        search = arxiv.Search(
            query="test",
            max_results=1
        )
        
        papers = list(search.results())
        if papers:
            print(f"✅ ArXiv API working - found paper: {papers[0].title[:50]}...")
            return True
        else:
            print("❌ ArXiv API returned no results")
            return False
            
    except Exception as e:
        print(f"❌ ArXiv API error: {e}")
        return False


def main():
    """Run all validation checks"""
    print("=" * 60)
    print("ArXiv → Marker Pipeline Setup Validation")
    print("=" * 60)
    
    # Check imports
    failed_imports = check_imports()
    
    if failed_imports:
        print("\n⚠️  Missing dependencies detected!")
        print("Please install missing modules:")
        print("  pip install -r ../requirements.txt")
        for module, error in failed_imports:
            print(f"  - {module}: {error}")
        return 1
    
    # Test ArXiv
    if not test_arxiv_connection():
        print("\n⚠️  ArXiv API test failed!")
        print("This could be a temporary network issue.")
        return 1
    
    # Check pipeline test exists
    print("\nChecking pipeline test file...")
    test_file = Path(__file__).parent / "test_arxiv_marker_pipeline.py"
    if test_file.exists():
        print(f"✅ Pipeline test file exists: {test_file.name}")
    else:
        print(f"❌ Pipeline test file missing: {test_file.name}")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ All checks passed! Ready to run pipeline tests.")
    print("=" * 60)
    print("\nTo run the pipeline test:")
    print("  python test_arxiv_marker_pipeline.py")
    print("\nTo run comprehensive tests:")
    print("  python run_pipeline_test.py")
    
    return 0


if __name__ == "__main__":
    exit(main())