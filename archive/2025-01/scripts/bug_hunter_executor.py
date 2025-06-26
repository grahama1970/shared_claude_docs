#!/usr/bin/env python3
"""
Module: bug_hunter_executor.py
Description: Execute all 67 Granger Bug Hunter scenarios and find real bugs

External Dependencies:
- httpx: https://www.python-httpx.org/
- aiofiles: https://github.com/Tinche/aiofiles

Sample Input:
>>> scenario = {"name": "SPARTA CVE Search", "modules": ["sparta"], "expected": "CVE data"}

Expected Output:
>>> result = {"scenario": "SPARTA CVE Search", "status": "FAIL", "bugs": ["No retry on timeout"]}

Example Usage:
>>> python bug_hunter_executor.py
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import httpx
import sys

class BugHunterExecutor:
    """Execute bug hunting scenarios against real Granger modules."""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        
        # Module endpoints (adjust as needed)
        self.endpoints = {
            'sparta': 'http://localhost:8080',
            'arxiv-mcp-server': 'http://localhost:8081',
            'arangodb': 'http://localhost:8529',
            'youtube_transcripts': 'http://localhost:8082',
            'marker': 'http://localhost:8083',
            'llm_call': 'http://localhost:8001',
            'gitget': 'http://localhost:8084',
            'world_model': 'http://localhost:8085',
            'rl_commons': 'http://localhost:8086',
            'claude-test-reporter': 'http://localhost:8002',
            'granger_hub': 'http://localhost:8000',
            'unsloth': 'http://localhost:8087',
        }
        
    async def execute_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single scenario and return results."""
        print(f"\n🔍 Executing: {scenario['name']}")
        print(f"   Modules: {', '.join(scenario['modules'])}")
        
        result = {
            'scenario': scenario['name'],
            'modules': scenario['modules'],
            'expected': scenario['expected_result'],
            'actual': None,
            'status': 'PENDING',
            'bugs': [],
            'evidence': {},
            'duration': 0
        }
        
        start = time.time()
        
        try:
            # Execute based on scenario type
            if scenario['name'] == 'SPARTA CVE Search':
                result['actual'] = await self.test_sparta_cve_search()
            elif scenario['name'] == 'ArXiv Paper Search':
                result['actual'] = await self.test_arxiv_search()
            elif scenario['name'] == 'ArangoDB Storage Operations':
                result['actual'] = await self.test_arangodb_operations()
            # Add more scenario implementations...
            else:
                result['actual'] = f"Scenario {scenario['name']} not yet implemented"
                result['status'] = 'SKIP'
                
        except Exception as e:
            result['actual'] = f"Error: {str(e)}"
            result['status'] = 'ERROR'
            result['bugs'].append(f"Unhandled exception: {type(e).__name__}")
            result['evidence']['error'] = str(e)
        
        result['duration'] = time.time() - start
        
        # Grade the result
        result['status'] = self.grade_result(scenario, result)
        
        return result
    
    async def test_sparta_cve_search(self) -> str:
        """Test SPARTA CVE search functionality."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test 1: Valid CVE search
            try:
                response = await client.get(f"{self.endpoints['sparta']}/api/cve/CVE-2021-44228")
                if response.status_code == 200:
                    data = response.json()
                    # Check expected fields
                    if not all(k in data for k in ['id', 'description', 'severity']):
                        return "Missing required fields in CVE response"
                    return f"Success: {data}"
                else:
                    return f"Failed with status {response.status_code}"
            except httpx.ConnectError:
                return "Connection failed - is SPARTA running?"
            except Exception as e:
                return f"Unexpected error: {e}"
    
    async def test_arxiv_search(self) -> str:
        """Test ArXiv paper search."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                # Test special characters
                response = await client.get(
                    f"{self.endpoints['arxiv-mcp-server']}/search",
                    params={"q": "Müller quantum"}
                )
                if response.status_code == 200:
                    data = response.json()
                    if 'papers' not in data:
                        return "Missing 'papers' field in response"
                    # Check for proper Unicode handling
                    return f"Found {len(data['papers'])} papers"
                else:
                    return f"Failed with status {response.status_code}"
            except httpx.ConnectError:
                return "Connection failed - is ArXiv MCP server running?"
            except Exception as e:
                return f"Unexpected error: {e}"
    
    async def test_arangodb_operations(self) -> str:
        """Test ArangoDB CRUD operations."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                # Test insert
                doc = {"test": "data", "timestamp": datetime.now().isoformat()}
                response = await client.post(
                    f"{self.endpoints['arangodb']}/_api/document/test_collection",
                    json=doc
                )
                if response.status_code in [201, 202]:
                    result = response.json()
                    if '_id' not in result:
                        return "Insert didn't return document ID"
                    return f"Insert successful: {result['_id']}"
                else:
                    return f"Insert failed with status {response.status_code}"
            except httpx.ConnectError:
                return "Connection failed - is ArangoDB running?"
            except Exception as e:
                return f"Unexpected error: {e}"
    
    def grade_result(self, scenario: Dict, result: Dict) -> str:
        """Grade the result against expected behavior."""
        actual = result['actual']
        expected = scenario['expected_result']
        
        # Simple grading logic (to be enhanced)
        if 'Error' in str(actual) or 'failed' in str(actual).lower():
            return 'FAIL'
        elif 'not yet implemented' in str(actual):
            return 'SKIP'
        elif 'Success' in str(actual) or 'successful' in str(actual).lower():
            return 'PASS'
        else:
            return 'WARN'
    
    async def run_all_scenarios(self):
        """Run all 67 scenarios."""
        # Load scenarios (simplified for now)
        scenarios = [
            {
                'name': 'SPARTA CVE Search',
                'modules': ['sparta'],
                'expected_result': 'Should return structured CVE data with fields: ID, description, severity'
            },
            {
                'name': 'ArXiv Paper Search',
                'modules': ['arxiv-mcp-server'],
                'expected_result': 'Returns list of papers with title, authors, abstract, PDF URL'
            },
            {
                'name': 'ArangoDB Storage Operations',
                'modules': ['arangodb'],
                'expected_result': 'Insert returns document ID'
            },
            # Add all 67 scenarios...
        ]
        
        print(f"🚀 Starting Bug Hunter Execution")
        print(f"📅 {datetime.now()}")
        print(f"🎯 Total scenarios: {len(scenarios)}")
        print("=" * 60)
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n[{i}/{len(scenarios)}] ", end='')
            result = await self.execute_scenario(scenario)
            self.results.append(result)
            
            # Show immediate feedback
            status_emoji = {
                'PASS': '✅',
                'FAIL': '❌',
                'WARN': '⚠️',
                'SKIP': '⏭️',
                'ERROR': '💥'
            }
            print(f" {status_emoji.get(result['status'], '❓')} {result['status']}")
            
            if result['bugs']:
                print(f"   🐛 Bugs found: {', '.join(result['bugs'])}")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive bug report."""
        report_time = datetime.now()
        duration = (report_time - self.start_time).total_seconds()
        
        # Calculate statistics
        stats = {
            'total': len(self.results),
            'executed': len([r for r in self.results if r['status'] != 'SKIP']),
            'passed': len([r for r in self.results if r['status'] == 'PASS']),
            'failed': len([r for r in self.results if r['status'] == 'FAIL']),
            'warnings': len([r for r in self.results if r['status'] == 'WARN']),
            'errors': len([r for r in self.results if r['status'] == 'ERROR']),
            'skipped': len([r for r in self.results if r['status'] == 'SKIP']),
        }
        
        # Find all bugs
        all_bugs = []
        critical_bugs = []
        
        for result in self.results:
            if result['bugs']:
                for bug in result['bugs']:
                    bug_entry = {
                        'scenario': result['scenario'],
                        'modules': result['modules'],
                        'bug': bug,
                        'evidence': result.get('evidence', {})
                    }
                    all_bugs.append(bug_entry)
                    
                    # Determine if critical
                    if any(term in bug.lower() for term in ['crash', 'data loss', 'security']):
                        critical_bugs.append(bug_entry)
        
        # Generate markdown report
        report = f"""# Bug Hunter Report - {report_time.strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Scenarios**: {stats['total']}
- **Executed**: {stats['executed']}
- **Passed**: {stats['passed']} ✅
- **Failed**: {stats['failed']} ❌
- **Warnings**: {stats['warnings']} ⚠️
- **Errors**: {stats['errors']} 💥
- **Skipped**: {stats['skipped']} ⏭️
- **Total Duration**: {duration:.2f} seconds
- **Bugs Found**: {len(all_bugs)} 🐛
- **Critical Bugs**: {len(critical_bugs)} 🚨

## Critical Findings
"""
        
        if critical_bugs:
            for i, bug in enumerate(critical_bugs, 1):
                report += f"\n### Critical Bug #{i}\n"
                report += f"- **Scenario**: {bug['scenario']}\n"
                report += f"- **Modules**: {', '.join(bug['modules'])}\n"
                report += f"- **Issue**: {bug['bug']}\n"
                if bug['evidence']:
                    report += f"- **Evidence**: `{bug['evidence']}`\n"
        else:
            report += "\nNo critical bugs found.\n"
        
        report += "\n## Detailed Results\n\n"
        report += "| # | Scenario | Modules | Status | Duration | Bugs |\n"
        report += "|---|----------|---------|--------|----------|------|\n"
        
        for i, result in enumerate(self.results, 1):
            status_display = {
                'PASS': '✅ PASS',
                'FAIL': '❌ FAIL',
                'WARN': '⚠️ WARN',
                'SKIP': '⏭️ SKIP',
                'ERROR': '💥 ERROR'
            }.get(result['status'], result['status'])
            
            bugs_str = ', '.join(result['bugs']) if result['bugs'] else '-'
            report += f"| {i} | {result['scenario']} | {', '.join(result['modules'])} | {status_display} | {result['duration']:.2f}s | {bugs_str} |\n"
        
        report += f"\n## Evidence\n\n"
        report += "### Failed Scenarios\n"
        
        for result in self.results:
            if result['status'] in ['FAIL', 'ERROR']:
                report += f"\n#### {result['scenario']}\n"
                report += f"- **Expected**: {result['expected']}\n"
                report += f"- **Actual**: {result['actual']}\n"
                if result.get('evidence'):
                    report += f"- **Evidence**: {json.dumps(result['evidence'], indent=2)}\n"
        
        # Save report
        report_path = Path('bug_hunter_report.md')
        report_path.write_text(report)
        print(f"\n📄 Report saved to: {report_path}")
        
        # Also save JSON for AI analysis
        json_path = Path('bug_hunter_results.json')
        json_path.write_text(json.dumps({
            'metadata': {
                'start_time': self.start_time.isoformat(),
                'end_time': report_time.isoformat(),
                'duration': duration,
                'stats': stats
            },
            'results': self.results,
            'bugs': all_bugs,
            'critical_bugs': critical_bugs
        }, indent=2))
        print(f"📊 JSON results saved to: {json_path}")

async def main():
    """Main entry point."""
    executor = BugHunterExecutor()
    await executor.run_all_scenarios()

if __name__ == "__main__":
    asyncio.run(main())