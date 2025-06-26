#!/usr/bin/env python3
"""
UI Self-Improvement Scenario
Modules collaborate to analyze UIs, generate improvements, and test changes
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path
import difflib

class UISelfImprovementScenario:
    """
    A scenario where modules collaborate to:
    1. Screenshot a UI with mcp-screenshot
    2. Analyze accessibility and usability issues
    3. Generate code improvements with Sparta
    4. Test the changes with claude-test-reporter
    5. Document improvements with Marker
    6. Iterate until UI meets quality standards
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.improvement_history = []
        self.ui_metrics = {
            "accessibility_score": 0,
            "usability_score": 0,
            "performance_score": 0
        }
        self.code_versions = []
    
    async def run(self, target_url: str, component_path: str, max_iterations: int = 5):
        """Run the UI self-improvement scenario"""
        print(f"🎨 Starting UI Self-Improvement for: {target_url}")
        print("="*60)
        
        improvement_achieved = False
        
        for iteration in range(max_iterations):
            print(f"\n🔄 Iteration {iteration + 1}/{max_iterations}")
            print("-"*40)
            
            # Phase 1: Capture and Analyze Current UI
            ui_analysis = await self._capture_and_analyze_ui(target_url)
            
            # Phase 2: Check if improvements are needed
            needs_improvement, issues = self._evaluate_ui_quality(ui_analysis)
            
            if not needs_improvement:
                print("✅ UI meets quality standards!")
                improvement_achieved = True
                break
            
            # Phase 3: Generate Improvement Suggestions
            improvements = await self._generate_improvements(ui_analysis, issues)
            
            # Phase 4: Apply Code Changes
            code_changes = await self._apply_improvements(component_path, improvements)
            
            # Phase 5: Test Changes
            test_results = await self._test_changes(component_path)
            
            # Phase 6: Document Changes
            await self._document_changes(code_changes, test_results, ui_analysis)
            
            # Phase 7: Deploy if tests pass
            if test_results["passed"]:
                await self._deploy_changes()
                print("✅ Changes deployed successfully")
            else:
                await self._rollback_changes()
                print("⚠️  Changes rolled back due to test failures")
        
        # Generate final report
        await self._generate_improvement_report(improvement_achieved)
    
    async def _capture_and_analyze_ui(self, target_url: str) -> Dict[str, Any]:
        """Capture screenshot and analyze UI"""
        print("  📸 Capturing UI screenshot...")
        
        task = self.orchestrator.create_task(
            name="UI Analysis",
            description=f"Capture and analyze UI at {target_url}"
        )
        
        # Capture screenshot
        self.orchestrator.add_step(
            task,
            module="mcp-screenshot",
            capability="capture_screenshot",
            input_data={"target": target_url}
        )
        
        # Analyze UI
        self.orchestrator.add_step(
            task,
            module="mcp-screenshot",
            capability="analyze_ui",
            input_data={"image_path": "$step_1.image_path"},
            depends_on=["step_1"]
        )
        
        result = await self.orchestrator.execute_task(task.id)
        
        screenshot_data = result["outputs"]["step_1"]
        ui_analysis = result["outputs"]["step_2"]
        
        print(f"  ✅ Found {len(ui_analysis.get('elements', []))} UI elements")
        print(f"  ⚠️  {len(ui_analysis.get('accessibility_issues', []))} accessibility issues")
        
        return {
            "screenshot": screenshot_data,
            "analysis": ui_analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    def _evaluate_ui_quality(self, ui_analysis: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Evaluate if UI needs improvement"""
        issues = []
        analysis = ui_analysis["analysis"]
        
        # Check accessibility issues
        accessibility_issues = analysis.get("accessibility_issues", [])
        if accessibility_issues:
            issues.extend([f"Accessibility: {issue}" for issue in accessibility_issues])
            self.ui_metrics["accessibility_score"] = max(0, 100 - len(accessibility_issues) * 10)
        else:
            self.ui_metrics["accessibility_score"] = 100
        
        # Check layout issues
        layout = analysis.get("layout", {})
        if layout.get("overlapping_elements", 0) > 0:
            issues.append(f"Layout: {layout['overlapping_elements']} overlapping elements")
            self.ui_metrics["usability_score"] = 70
        else:
            self.ui_metrics["usability_score"] = 90
        
        # Check performance metrics (mock)
        elements_count = len(analysis.get("elements", []))
        if elements_count > 100:
            issues.append(f"Performance: Too many DOM elements ({elements_count})")
            self.ui_metrics["performance_score"] = 60
        else:
            self.ui_metrics["performance_score"] = 90
        
        # Calculate overall quality
        overall_score = sum(self.ui_metrics.values()) / len(self.ui_metrics)
        needs_improvement = overall_score < 85 or len(issues) > 0
        
        print(f"\n  📊 UI Quality Scores:")
        print(f"     • Accessibility: {self.ui_metrics['accessibility_score']}/100")
        print(f"     • Usability: {self.ui_metrics['usability_score']}/100")
        print(f"     • Performance: {self.ui_metrics['performance_score']}/100")
        print(f"     • Overall: {overall_score:.1f}/100")
        
        return needs_improvement, issues
    
    async def _generate_improvements(self, ui_analysis: Dict[str, Any], 
                                   issues: List[str]) -> Dict[str, Any]:
        """Generate code improvements using AI"""
        print("\n  🤔 Generating improvement suggestions...")
        
        task = self.orchestrator.create_task(
            name="Generate Improvements",
            description="Generate code improvements for UI issues"
        )
        
        # Use Sparta to analyze and suggest improvements
        self.orchestrator.add_step(
            task,
            module="sparta",
            capability="analyze_performance",
            input_data={
                "model_path": "ui_improvement_model",
                "context": {
                    "ui_analysis": ui_analysis["analysis"],
                    "issues": issues
                }
            }
        )
        
        result = await self.orchestrator.execute_task(task.id)
        suggestions = result["outputs"]["step_1"]["analysis"]
        
        # Convert suggestions to code improvements
        improvements = {
            "accessibility": [],
            "layout": [],
            "performance": [],
            "code_snippets": []
        }
        
        # Generate specific improvements based on issues
        for issue in issues:
            if "Accessibility" in issue:
                if "missing alt text" in issue.lower():
                    improvements["accessibility"].append({
                        "type": "add_alt_text",
                        "code": 'alt="Descriptive text for image"'
                    })
                if "color contrast" in issue.lower():
                    improvements["accessibility"].append({
                        "type": "improve_contrast",
                        "code": 'style={{ color: "#000", backgroundColor: "#fff" }}'
                    })
            
            elif "Layout" in issue:
                improvements["layout"].append({
                    "type": "fix_overlap",
                    "code": 'display: "flex", flexDirection: "column", gap: "1rem"'
                })
            
            elif "Performance" in issue:
                improvements["performance"].append({
                    "type": "lazy_load",
                    "code": 'loading="lazy"'
                })
        
        # Generate complete code snippets
        improvements["code_snippets"] = self._generate_code_snippets(improvements)
        
        print(f"  ✅ Generated {len(improvements['code_snippets'])} improvement suggestions")
        
        return improvements
    
    def _generate_code_snippets(self, improvements: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate actual code snippets for improvements"""
        snippets = []
        
        # Accessibility improvements
        if improvements["accessibility"]:
            snippet = {
                "description": "Accessibility improvements",
                "before": '<img src="logo.png">',
                "after": '<img src="logo.png" alt="Company logo" role="img">'
            }
            snippets.append(snippet)
        
        # Layout improvements  
        if improvements["layout"]:
            snippet = {
                "description": "Layout fixes for overlapping elements",
                "before": '''<div className="container">
  <div className="element1">Content 1</div>
  <div className="element2">Content 2</div>
</div>''',
                "after": '''<div className="container" style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
  <div className="element1">Content 1</div>
  <div className="element2">Content 2</div>
</div>'''
            }
            snippets.append(snippet)
        
        # Performance improvements
        if improvements["performance"]:
            snippet = {
                "description": "Performance optimization with lazy loading",
                "before": '<img src="large-image.jpg">',
                "after": '<img src="large-image.jpg" loading="lazy" decoding="async">'
            }
            snippets.append(snippet)
        
        return snippets
    
    async def _apply_improvements(self, component_path: str, 
                                 improvements: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the suggested improvements to the code"""
        print("\n  🔧 Applying code improvements...")
        
        # Read current component code
        component_file = Path(component_path)
        if component_file.exists():
            original_code = component_file.read_text()
        else:
            # Mock code for demo
            original_code = '''import React from 'react';

const MyComponent = () => {
  return (
    <div className="container">
      <img src="logo.png">
      <div className="element1">Content 1</div>
      <div className="element2">Content 2</div>
      <img src="large-image.jpg">
    </div>
  );
};

export default MyComponent;'''
        
        # Apply improvements
        modified_code = original_code
        for snippet in improvements["code_snippets"]:
            if snippet["before"] in modified_code:
                modified_code = modified_code.replace(snippet["before"], snippet["after"])
        
        # Save version
        self.code_versions.append({
            "version": len(self.code_versions) + 1,
            "timestamp": datetime.now().isoformat(),
            "original": original_code,
            "modified": modified_code,
            "changes": improvements
        })
        
        # Generate diff
        diff = list(difflib.unified_diff(
            original_code.splitlines(keepends=True),
            modified_code.splitlines(keepends=True),
            fromfile=f"{component_path} (original)",
            tofile=f"{component_path} (modified)"
        ))
        
        print("  📝 Code changes:")
        for line in diff[:20]:  # Show first 20 lines of diff
            print(f"    {line.rstrip()}")
        
        return {
            "original": original_code,
            "modified": modified_code,
            "diff": ''.join(diff),
            "improvements_applied": len(improvements["code_snippets"])
        }
    
    async def _test_changes(self, component_path: str) -> Dict[str, Any]:
        """Test the changes using claude-test-reporter"""
        print("\n  🧪 Testing changes...")
        
        task = self.orchestrator.create_task(
            name="Test UI Changes",
            description=f"Run tests for {component_path}"
        )
        
        # Run tests
        self.orchestrator.add_step(
            task,
            module="claude-test-reporter",
            capability="run_tests",
            input_data={
                "test_path": f"{Path(component_path).parent}/tests",
                "coverage": True
            }
        )
        
        # Generate test suggestions for new code
        self.orchestrator.add_step(
            task,
            module="claude-test-reporter",
            capability="generate_test_suggestions",
            input_data={"code_path": component_path}
        )
        
        result = await self.orchestrator.execute_task(task.id)
        
        test_results = result["outputs"].get("step_1", {
            "passed": 8,
            "failed": 2,
            "coverage": 85.5
        })
        
        test_suggestions = result["outputs"].get("step_2", {
            "suggestions": [
                "Add test for alt text on images",
                "Test layout responsiveness",
                "Verify lazy loading behavior"
            ]
        })
        
        print(f"  ✅ Tests: {test_results['passed']} passed, {test_results['failed']} failed")
        print(f"  📊 Coverage: {test_results['coverage']}%")
        
        if test_suggestions["suggestions"]:
            print("  💡 Test suggestions:")
            for suggestion in test_suggestions["suggestions"][:3]:
                print(f"     • {suggestion}")
        
        return {
            "passed": test_results["failed"] == 0,
            "results": test_results,
            "suggestions": test_suggestions
        }
    
    async def _document_changes(self, code_changes: Dict[str, Any], 
                               test_results: Dict[str, Any],
                               ui_analysis: Dict[str, Any]):
        """Document the improvements made"""
        print("\n  📚 Documenting changes...")
        
        task = self.orchestrator.create_task(
            name="Document Changes",
            description="Generate documentation for UI improvements"
        )
        
        # Use Marker to create documentation
        documentation = f"""# UI Improvement Report

## Summary
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Component**: {self.orchestrator.context.get('component_path', 'MyComponent')}
- **Improvements Applied**: {code_changes['improvements_applied']}
- **Test Status**: {'✅ Passed' if test_results['passed'] else '❌ Failed'}

## UI Analysis Results
- **Accessibility Score**: {self.ui_metrics['accessibility_score']}/100
- **Usability Score**: {self.ui_metrics['usability_score']}/100  
- **Performance Score**: {self.ui_metrics['performance_score']}/100

## Code Changes
```diff
{code_changes['diff'][:1000]}...
```

## Test Results
- **Tests Passed**: {test_results['results']['passed']}
- **Tests Failed**: {test_results['results']['failed']}
- **Code Coverage**: {test_results['results']['coverage']}%

## Recommendations
{chr(10).join(['- ' + s for s in test_results['suggestions']['suggestions'][:5]])}
"""
        
        # Save documentation
        self.improvement_history.append({
            "iteration": len(self.improvement_history) + 1,
            "documentation": documentation,
            "metrics": self.ui_metrics.copy(),
            "timestamp": datetime.now().isoformat()
        })
        
        print("  ✅ Documentation generated")
    
    async def _deploy_changes(self):
        """Deploy the changes (mock)"""
        print("\n  🚀 Deploying changes...")
        await asyncio.sleep(1)  # Simulate deployment
        print("  ✅ Deployment complete")
    
    async def _rollback_changes(self):
        """Rollback changes (mock)"""
        print("\n  ⏪ Rolling back changes...")
        await asyncio.sleep(0.5)  # Simulate rollback
        print("  ✅ Rollback complete")
    
    async def _generate_improvement_report(self, success: bool):
        """Generate final improvement report"""
        print("\n" + "="*60)
        print("🎨 UI SELF-IMPROVEMENT SUMMARY")
        print("="*60)
        
        report = {
            "success": success,
            "iterations": len(self.improvement_history),
            "final_scores": self.ui_metrics,
            "code_versions": len(self.code_versions),
            "improvements_applied": sum(v["improvements_applied"] for v in self.code_versions),
            "history": self.improvement_history
        }
        
        # Save report
        output_dir = Path("./reports")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"ui_improvement_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also save the final documentation as markdown
        if self.improvement_history:
            doc_path = output_dir / f"ui_improvement_doc_{timestamp}.md"
            with open(doc_path, 'w') as f:
                f.write(self.improvement_history[-1]["documentation"])
        
        print(f"\n📊 Final Scores:")
        print(f"  • Accessibility: {self.ui_metrics['accessibility_score']}/100")
        print(f"  • Usability: {self.ui_metrics['usability_score']}/100")
        print(f"  • Performance: {self.ui_metrics['performance_score']}/100")
        print(f"\n📈 Improvement Summary:")
        print(f"  • Iterations: {report['iterations']}")
        print(f"  • Total improvements: {report['improvements_applied']}")
        print(f"  • Success: {'✅ Yes' if success else '❌ No'}")
        print(f"\n📁 Reports saved to:")
        print(f"  • JSON: {report_path}")
        if self.improvement_history:
            print(f"  • Documentation: {doc_path}")

# Example usage
async def main():
    """Run the UI self-improvement scenario"""
    from orchestrator.task_orchestrator import ConversationalOrchestrator
    
    async with ConversationalOrchestrator() as orchestrator:
        scenario = UISelfImprovementScenario(orchestrator)
        
        # Run UI improvement on a component
        await scenario.run(
            target_url="http://localhost:3000/dashboard",
            component_path="/src/components/Dashboard.jsx",
            max_iterations=3
        )

if __name__ == "__main__":
    asyncio.run(main())