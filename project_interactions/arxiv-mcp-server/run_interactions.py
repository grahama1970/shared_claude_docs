#!/usr/bin/env python

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Run all ArXiv MCP Server interactions

This script runs all Level 0 and Level 1 interactions for the ArXiv MCP Server
and generates a comprehensive report.

Usage:
    python run_interactions.py [--level LEVEL]
    
    --level: Run only specific level (0, 1, or all)
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.append(str(Path(__file__).parent))

from interaction_framework import InteractionRunner

# Import Level 0 interactions
from level_0.search_interactions import (
    BasicSearchInteraction,
    AdvancedSearchInteraction,
    SemanticSearchInteraction,
    AuthorSearchInteraction
)
from level_0.evidence_interactions import (
    FindSupportingEvidenceInteraction,
    FindContradictingEvidenceInteraction,
    HypothesisTestingInteraction,
    CitationMiningInteraction
)
from level_0.batch_interactions import (
    BatchDownloadInteraction,
    DailyDigestInteraction,
    ReadingListInteraction,
    CollectionManagementInteraction,
    BulkExportInteraction
)


def run_level_0_interactions(runner):
    """Run all Level 0 interactions"""
    print("\n" + "="*60)
    print("LEVEL 0 INTERACTIONS - Single Module Tests")
    print("="*60)
    
    # Search interactions
    print("\n### Search Functionality ###")
    search_interactions = [
        BasicSearchInteraction(),
        AdvancedSearchInteraction(),
        SemanticSearchInteraction(),
        AuthorSearchInteraction()
    ]
    
    for interaction in search_interactions:
        runner.run_interaction(interaction)
        
    # Evidence mining interactions
    print("\n### Evidence Mining ###")
    evidence_interactions = [
        FindSupportingEvidenceInteraction(),
        FindContradictingEvidenceInteraction(),
        HypothesisTestingInteraction(),
        CitationMiningInteraction()
    ]
    
    for interaction in evidence_interactions:
        runner.run_interaction(interaction)
        
    # Batch operations
    print("\n### Batch Operations ###")
    batch_interactions = [
        BatchDownloadInteraction(),
        DailyDigestInteraction(),
        ReadingListInteraction(),
        CollectionManagementInteraction(),
        BulkExportInteraction()
    ]
    
    for interaction in batch_interactions:
        runner.run_interaction(interaction)


def run_level_1_interactions(runner):
    """Run all Level 1 interactions (when implemented)"""
    print("\n" + "="*60)
    print("LEVEL 1 INTERACTIONS - Two Module Pipelines")
    print("="*60)
    
    print("\nLevel 1 interactions not yet implemented.")
    print("These will include:")
    print("- ArXiv → Marker (search and convert)")
    print("- ArXiv → ArangoDB (search and store)")
    print("- ArXiv → SPARTA (search and analyze)")


def generate_summary_report(runner, level):
    """Generate and save summary report"""
    report = runner.generate_report()
    
    # Add metadata
    report["metadata"] = {
        "project": "ArXiv MCP Server",
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform
        }
    }
    
    # Save JSON report
    report_path = Path(f"arxiv_interaction_report_{level}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"\nReport saved to: {report_path}")
    
    # Generate markdown summary
    md_content = f"""# ArXiv MCP Server Interaction Report

**Date:** {report['metadata']['timestamp']}  
**Level:** {level}  
**Project:** {report['metadata']['project']}

## Summary

- **Total Interactions:** {report['summary']['total']}
- **Passed:** {report['summary']['passed']}
- **Failed:** {report['summary']['failed']}
- **Success Rate:** {report['summary']['success_rate']:.1f}%

## Results by Level

"""
    
    for level_name, stats in report.get("by_level", {}).items():
        md_content += f"### {level_name}\n"
        md_content += f"- Total: {stats['total']}\n"
        md_content += f"- Passed: {stats['passed']}\n"
        md_content += f"- Failed: {stats['failed']}\n\n"
        
    # Add failed interactions details
    failed_interactions = [r for r in report["results"] if not r["success"]]
    if failed_interactions:
        md_content += "## Failed Interactions\n\n"
        for result in failed_interactions:
            md_content += f"### {result['interaction_name']}\n"
            md_content += f"- Error: {result.get('error', 'Unknown error')}\n"
            md_content += f"- Duration: {result['duration']:.2f}s\n\n"
            
    md_path = report_path.with_suffix(".md")
    with open(md_path, "w") as f:
        f.write(md_content)
        
    print(f"Markdown summary saved to: {md_path}")
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Run ArXiv MCP Server interactions")
    parser.add_argument("--level", choices=["0", "1", "all"], default="all",
                       help="Interaction level to run")
    args = parser.parse_args()
    
    # Initialize runner
    runner = InteractionRunner("ArXiv MCP Server")
    
    # Run requested levels
    if args.level in ["0", "all"]:
        run_level_0_interactions(runner)
        
    if args.level in ["1", "all"]:
        run_level_1_interactions(runner)
        
    # Generate report
    report = generate_summary_report(runner, args.level)
    
    # Exit with appropriate code
    failed = report["summary"]["failed"]
    if failed > 0:
        print(f"\n❌ {failed} interactions failed!")
        sys.exit(1)
    else:
        print(f"\n✅ All {report['summary']['total']} interactions passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()