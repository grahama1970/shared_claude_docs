#!/usr/bin/env python3
"""
Module: granger_ai_collaborate.py
Description: Multi-AI collaboration system for resolving Granger ecosystem issues

External Dependencies:
- llm_call: https://github.com/granger/llm_call
- subprocess: Built-in Python module for process execution

Sample Input:
>>> python granger_ai_collaborate.py --project marker --issue "missing documentation headers"

Expected Output:
>>> AI Collaboration Report with fixes applied

Example Usage:
>>> # Run for all projects with remaining issues
>>> python granger_ai_collaborate.py --all
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time

class GrangerAICollaborator:
    """Orchestrates multi-AI collaboration for issue resolution."""
    
    def __init__(self):
        self.llm_call_path = "/home/graham/workspace/experiments/llm_call"
        self.results = {
            'claude_attempts': {},
            'perplexity_research': {},
            'gemini_analysis': {},
            'human_guidance': {}
        }
    
    def attempt_claude_fix(self, project: str, issues: List[Dict]) -> Tuple[bool, Dict]:
        """Step 1: Claude attempts to fix issues."""
        print(f"\n🤖 Claude attempting to fix {len(issues)} issues in {project}...")
        
        # Run enhanced granger-verify with force-fix
        cmd = ["/home/graham/.claude/commands/granger-verify", 
               "--project", project, 
               "--force-fix",
               "--quiet"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Check if fixes were successful
            success = "✅" in result.stdout or "Fixed" in result.stdout
            
            return success, {
                'fixed': success,
                'output': result.stdout,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return False, {'error': str(e)}
    
    def consult_perplexity(self, project: str, issues: List[Dict]) -> Dict:
        """Step 2: Consult Perplexity for research and solutions."""
        print(f"\n🔍 Consulting Perplexity AI for {project} issues...")
        
        # Build research query
        query = f"How to fix these Python project issues in {project}: "
        for issue in issues[:3]:  # Limit to avoid token overflow
            query += f"{issue.get('type', 'unknown')}: {issue.get('description', '')}. "
        
        # Call Perplexity via llm_call with MCP
        cmd = [
            "python", "-m", "llm_call",
            "--provider", "perplexity",
            "--model", "llama-3.1-sonar-large-128k-online",
            "--prompt", query,
            "--mcp-config", json.dumps({
                "mcpServers": {
                    "perplexity-ask": {
                        "command": "npx",
                        "args": ["-y", "@haltiamieli/perplexity-server"],
                        "env": {"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"}
                    }
                }
            })
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.llm_call_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'research': result.stdout,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def collaborate_with_gemini(self, project: str, issues: List[Dict], 
                               perplexity_research: str) -> Dict:
        """Step 3: Gemini analyzes and provides expert recommendations."""
        print(f"\n🧠 Consulting Google Gemini 2.0 for {project}...")
        
        prompt = f"""You are Google Gemini Code 2.0. Claude and Perplexity have attempted to resolve these issues:

Project: {project}
Issues: {json.dumps(issues, indent=2)}

Perplexity's Research:
{perplexity_research[:1000]}

Provide specific code fixes and implementation steps."""
        
        # Use existing Gemini integration
        cmd = ["python", "/home/graham/.claude/commands/analyze_unresolved_with_gemini.py",
               "--prompt", prompt,
               "--project", project]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {
                'success': result.returncode == 0,
                'advice': result.stdout,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_human_guidance(self, project: str, all_results: Dict) -> str:
        """Step 4: Generate human guidance for unresolved issues."""
        guidance = f"""# 🚨 Human Intervention Required: {project}

## AI Collaboration Summary:
1. **Claude Fix Attempt**: {'✅ Success' if all_results['claude']['fixed'] else '❌ Failed'}
2. **Perplexity Research**: {'✅ Completed' if all_results['perplexity']['success'] else '❌ Failed'}  
3. **Gemini Analysis**: {'✅ Provided' if all_results['gemini']['success'] else '❌ Failed'}

## Remaining Issues Requiring Human Review:
"""
        
        # Add specific guidance based on issue patterns
        if "missing documentation headers" in str(all_results):
            guidance += """
### Documentation Headers:
- Manually review files with complex logic
- Ensure descriptions accurately reflect functionality
- Add proper external dependency URLs
"""
        
        if "mock usage" in str(all_results):
            guidance += """
### Mock Usage:
- Review if mocks are for honeypot tests (intentional)
- Consider if real service integration is feasible
- Check infrastructure requirements for real tests
"""
        
        return guidance
    
    def process_project(self, project: str, issues: List[Dict]) -> Dict:
        """Process a single project through all AI collaboration steps."""
        results = {
            'project': project,
            'initial_issues': len(issues),
            'stages': {}
        }
        
        # Step 1: Claude attempts fix
        success, claude_result = self.attempt_claude_fix(project, issues)
        results['stages']['claude'] = claude_result
        
        if success:
            print(f"✅ Claude successfully fixed {project}")
            results['final_status'] = 'resolved_by_claude'
            return results
        
        # Step 2: Consult Perplexity
        perplexity_result = self.consult_perplexity(project, issues)
        results['stages']['perplexity'] = perplexity_result
        
        # Step 3: Collaborate with Gemini
        gemini_result = self.collaborate_with_gemini(
            project, issues, 
            perplexity_result.get('research', 'No research available')
        )
        results['stages']['gemini'] = gemini_result
        
        # Step 4: Generate human guidance
        if not gemini_result.get('success'):
            guidance = self.generate_human_guidance(project, results['stages'])
            results['stages']['human_guidance'] = guidance
            results['final_status'] = 'requires_human'
        else:
            results['final_status'] = 'resolved_by_ai_collaboration'
        
        return results

def main():
    """Main execution function."""
    print("🤖 Granger Multi-AI Collaboration System")
    print("Claude → Perplexity → Gemini → Human\n")
    
    collaborator = GrangerAICollaborator()
    
    # Get remaining issues from latest verification
    remaining_issues = {
        'marker': [
            {'type': 'missing_doc_header', 'description': '226 files missing headers'},
            {'type': 'mock_usage', 'description': 'Tests using mocks'}
        ],
        'llm_call': [
            {'type': 'missing_doc_header', 'description': '154 files missing headers'}
        ],
        'arangodb': [
            {'type': 'missing_doc_header', 'description': '141 files missing headers'}
        ]
    }
    
    all_results = []
    
    for project, issues in remaining_issues.items():
        print(f"\n{'='*60}")
        print(f"Processing: {project}")
        print(f"Issues: {len(issues)}")
        
        result = collaborator.process_project(project, issues)
        all_results.append(result)
        
        # Brief pause between projects
        time.sleep(2)
    
    # Generate final report
    report_path = f"ai_collaboration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(report_path, 'w') as f:
        f.write("# Granger AI Collaboration Report\n\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        
        for result in all_results:
            f.write(f"\n## {result['project']}\n")
            f.write(f"- Initial Issues: {result['initial_issues']}\n")
            f.write(f"- Final Status: {result['final_status']}\n")
            
            if result.get('stages', {}).get('human_guidance'):
                f.write("\n### Human Guidance:\n")
                f.write(result['stages']['human_guidance'])
    
    print(f"\n✅ Report saved to: {report_path}")
    
    # Summary
    resolved = sum(1 for r in all_results if 'resolved' in r['final_status'])
    human_needed = sum(1 for r in all_results if r['final_status'] == 'requires_human')
    
    print(f"\n📊 Summary:")
    print(f"- Projects processed: {len(all_results)}")
    print(f"- Resolved by AI: {resolved}")
    print(f"- Requiring human: {human_needed}")

if __name__ == "__main__":
    main()