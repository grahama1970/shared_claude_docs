#!/usr/bin/env python3
"""
Module: bug_hunter_automation_batch.py
Description: Automated batch execution of bug hunter tasks

External Dependencies:
- asyncio: Built-in async support
- subprocess: Built-in process management
"""

import asyncio
import subprocess
import json
from pathlib import Path
import time

class BugHunterBatchRunner:
    """Run multiple bug hunter tasks in batch."""
    
    def __init__(self):
        self.results = []
        self.report_dir = Path("bug_hunter_reports")
        self.report_dir.mkdir(exist_ok=True)
        
    async def run_task(self, task_number: int, task_script: str) -> dict:
        """Run a single bug hunter task."""
        print(f"\n{'='*60}")
        print(f"🚀 Starting Task #{task_number:03d}: {task_script}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            # Run the task script
            result = subprocess.run(
                ["python", task_script],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            duration = time.time() - start_time
            
            # Parse JSON report if it exists
            report_path = self.report_dir / f"task_{task_number:03d}_*_report.json"
            report_files = list(self.report_dir.glob(f"task_{task_number:03d}_*_report.json"))
            
            if report_files:
                with open(report_files[0]) as f:
                    report_data = json.load(f)
                    bugs_found = report_data.get('bugs_found', 0)
            else:
                bugs_found = 0
            
            return {
                "task": task_number,
                "script": task_script,
                "status": "success" if result.returncode == 0 else "failed",
                "duration": duration,
                "bugs_found": bugs_found,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "task": task_number,
                "script": task_script,
                "status": "timeout",
                "duration": 300,
                "bugs_found": 0,
                "error": "Task timed out after 5 minutes"
            }
        except Exception as e:
            return {
                "task": task_number,
                "script": task_script,
                "status": "error",
                "duration": time.time() - start_time,
                "bugs_found": 0,
                "error": str(e)
            }
    
    async def run_batch(self, start_task: int, end_task: int):
        """Run a batch of tasks."""
        tasks = []
        
        # Define task ranges
        task_definitions = {
            # Level 1: Two Module Integration (Tasks 12-26)
            14: "task_014_arangodb_unsloth.py",
            15: "task_015_youtube_marker.py",
            16: "task_016_arxiv_arangodb.py",
            17: "task_017_llm_module_comm.py",
            18: "task_018_hub_reporter.py",
            19: "task_019_sparta_arangodb.py",
            20: "task_020_marker_unsloth.py",
            21: "task_021_youtube_arangodb.py",
            22: "task_022_arxiv_marker.py",
            23: "task_023_llm_hub.py",
            24: "task_024_reporter_hub.py",
            25: "task_025_module_comm_all.py",
            26: "task_026_rl_optimization.py",
        }
        
        # Run tasks in the specified range
        for task_num in range(start_task, end_task + 1):
            if task_num in task_definitions:
                script_name = task_definitions[task_num]
                result = await self.run_task(task_num, script_name)
                self.results.append(result)
                
                # Small delay between tasks
                await asyncio.sleep(1)
        
        return self.results
    
    def generate_batch_report(self):
        """Generate summary report for the batch."""
        total_bugs = sum(r.get('bugs_found', 0) for r in self.results)
        successful = sum(1 for r in self.results if r['status'] == 'success')
        failed = sum(1 for r in self.results if r['status'] != 'success')
        
        report = f"""# Bug Hunter Batch Report

## Summary
- Tasks Run: {len(self.results)}
- Successful: {successful}
- Failed: {failed}
- Total Bugs Found: {total_bugs}

## Task Results
"""
        
        for result in self.results:
            status_emoji = "✅" if result['status'] == 'success' else "❌"
            report += f"\n### Task #{result['task']:03d}: {result['script']}\n"
            report += f"- Status: {status_emoji} {result['status']}\n"
            report += f"- Duration: {result['duration']:.2f}s\n"
            report += f"- Bugs Found: {result['bugs_found']}\n"
            
            if result.get('error'):
                report += f"- Error: {result['error']}\n"
        
        report += f"\n---\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Save report
        report_path = self.report_dir / f"batch_report_{time.strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report)
        
        print(f"\n📄 Batch report saved to: {report_path}")
        
        return report


async def main():
    """Main function."""
    runner = BugHunterBatchRunner()
    
    # Get task range from user or use defaults
    print("🐛 Bug Hunter Batch Automation")
    print("Enter task range (default: 14-26 for remaining Level 1 tasks)")
    
    try:
        start = int(input("Start task [14]: ") or "14")
        end = int(input("End task [26]: ") or "26")
    except ValueError:
        start, end = 14, 26
    
    print(f"\n🚀 Running tasks {start} to {end}...")
    
    # Create placeholder scripts for tasks that don't exist yet
    for task_num in range(start, end + 1):
        script_name = f"task_{task_num:03d}_placeholder.py"
        if not Path(script_name).exists():
            # We'll need to create these scripts
            pass
    
    # Run the batch
    results = await runner.run_batch(start, end)
    
    # Generate report
    runner.generate_batch_report()
    
    print(f"\n✅ Batch complete! Found {sum(r.get('bugs_found', 0) for r in results)} bugs total.")


if __name__ == "__main__":
    asyncio.run(main())