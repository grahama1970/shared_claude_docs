
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Standardized Interaction Framework Template

This template provides base classes for implementing module interactions at different levels.
Copy this to each project's tests/interactions/ or interactions/ directory.

External Dependencies:
- typing: Built-in Python type annotations
- abc: Built-in abstract base classes
- dataclasses: Built-in dataclass support

Example Usage:
>>> from interaction_framework import Level0Interaction
>>> class SearchPapersInteraction(Level0Interaction):
...     def execute(self):
...         return self.module.search("quantum computing")
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union
from datetime import datetime
import json
import time
from enum import Enum


class InteractionLevel(Enum):
    """Interaction complexity levels"""
    LEVEL_0 = "Single module functionality"
    LEVEL_1 = "Two module pipeline"
    LEVEL_2 = "Parallel/branching workflows"
    LEVEL_3 = "Orchestrated collaboration"


@dataclass
class InteractionResult:
    """Result of an interaction execution"""
    interaction_name: str
    level: InteractionLevel
    success: bool
    duration: float
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "interaction_name": self.interaction_name,
            "level": self.level.value,
            "success": self.success,
            "duration": self.duration,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "error": self.error,
            "timestamp": self.timestamp.isoformat(),
            "metrics": self.metrics
        }


class BaseInteraction(ABC):
    """Base class for all interaction levels"""
    
    def __init__(self, name: str, description: str, level: InteractionLevel):
        self.name = name
        self.description = description
        self.level = level
        self.setup_time = None
        self.teardown_time = None
        
    @abstractmethod
    def setup(self) -> None:
        """Setup required resources"""
        pass
        
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the interaction"""
        pass
        
    @abstractmethod
    def validate_output(self, output: Any) -> bool:
        """Validate the output meets expectations"""
        pass
        
    def teardown(self) -> None:
        """Cleanup resources (optional override)"""
        pass
        
    def run(self, **kwargs) -> InteractionResult:
        """Run the complete interaction with timing and error handling"""
        start_time = time.time()
        error = None
        output = None
        success = False
        
        try:
            # Setup
            setup_start = time.time()
            self.setup()
            self.setup_time = time.time() - setup_start
            
            # Execute
            output = self.execute(**kwargs)
            
            # Validate
            success = self.validate_output(output)
            
        except Exception as e:
            error = str(e)
            success = False
            
        finally:
            # Teardown
            teardown_start = time.time()
            self.teardown()
            self.teardown_time = time.time() - teardown_start
            
        duration = time.time() - start_time
        
        return InteractionResult(
            interaction_name=self.name,
            level=self.level,
            success=success,
            duration=duration,
            input_data=kwargs,
            output_data={"result": output} if output else {},
            error=error,
            metrics={
                "setup_time": self.setup_time,
                "teardown_time": self.teardown_time
            }
        )


class Level0Interaction(BaseInteraction):
    """Level 0: Single module interaction"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description, InteractionLevel.LEVEL_0)
        self.module = None
        
    @abstractmethod
    def initialize_module(self) -> Any:
        """Initialize the module to test"""
        pass
        
    def setup(self) -> None:
        """Setup the module"""
        self.module = self.initialize_module()


class Level1Interaction(BaseInteraction):
    """Level 1: Two module pipeline interaction"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description, InteractionLevel.LEVEL_1)
        self.module1 = None
        self.module2 = None
        
    @abstractmethod
    def initialize_modules(self) -> tuple:
        """Initialize both modules - return (module1, module2)"""
        pass
        
    @abstractmethod
    def transform_output(self, output1: Any) -> Any:
        """Transform module1 output for module2 input"""
        pass
        
    def setup(self) -> None:
        """Setup both modules"""
        self.module1, self.module2 = self.initialize_modules()
        
    def execute(self, **kwargs) -> Any:
        """Execute pipeline: module1 -> transform -> module2"""
        # Execute first module
        output1 = self.execute_module1(**kwargs)
        
        # Transform output
        input2 = self.transform_output(output1)
        
        # Execute second module
        output2 = self.execute_module2(input2)
        
        return {
            "module1_output": output1,
            "module2_output": output2,
            "pipeline_result": output2
        }
        
    @abstractmethod
    def execute_module1(self, **kwargs) -> Any:
        """Execute first module"""
        pass
        
    @abstractmethod
    def execute_module2(self, input_data: Any) -> Any:
        """Execute second module"""
        pass


class InteractionRunner:
    """Runs and reports on interactions"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.results: List[InteractionResult] = []
        
    def run_interaction(self, interaction: BaseInteraction, **kwargs) -> InteractionResult:
        """Run a single interaction"""
        print(f"\nRunning {interaction.level.name}: {interaction.name}")
        print(f"Description: {interaction.description}")
        
        result = interaction.run(**kwargs)
        self.results.append(result)
        
        # Print summary
        status = "✅ PASSED" if result.success else "❌ FAILED"
        print(f"Status: {status}")
        print(f"Duration: {result.duration:.2f}s")
        if result.error:
            print(f"Error: {result.error}")
            
        return result
        
    def run_all(self, interactions: List[BaseInteraction], **kwargs) -> Dict[str, Any]:
        """Run all interactions and generate report"""
        print(f"\n{'='*60}")
        print(f"Running {self.project_name} Interactions")
        print(f"{'='*60}")
        
        for interaction in interactions:
            self.run_interaction(interaction, **kwargs)
            
        return self.generate_report()
        
    def generate_report(self) -> Dict[str, Any]:
        """Generate summary report"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed
        
        report = {
            "project": self.project_name,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "success_rate": (passed / total * 100) if total > 0 else 0
            },
            "results": [r.to_dict() for r in self.results],
            "by_level": {}
        }
        
        # Group by level
        for level in InteractionLevel:
            level_results = [r for r in self.results if r.level == level]
            if level_results:
                level_passed = sum(1 for r in level_results if r.success)
                report["by_level"][level.name] = {
                    "total": len(level_results),
                    "passed": level_passed,
                    "failed": len(level_results) - level_passed
                }
                
        # Print summary
        print(f"\n{'='*60}")
        print(f"Summary for {self.project_name}")
        print(f"{'='*60}")
        print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
        print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
        
        return report


# RL Commons Integration Support
@dataclass
class InteractionMetrics:
    """Metrics for RL optimization"""
    execution_time: float
    success_rate: float
    resource_usage: Dict[str, float]
    quality_score: float
    cost: float = 0.0
    
    def to_reward(self, weights: Dict[str, float] = None) -> float:
        """Convert metrics to reward signal for RL"""
        if weights is None:
            weights = {
                "success": 10.0,
                "speed": 1.0,
                "quality": 5.0,
                "cost": -0.1
            }
            
        reward = 0.0
        reward += weights["success"] * self.success_rate
        reward += weights["speed"] * (1.0 / (self.execution_time + 1))
        reward += weights["quality"] * self.quality_score
        reward += weights["cost"] * self.cost
        
        return reward


class OptimizableInteraction(BaseInteraction):
    """Base class for interactions that can be optimized with RL"""
    
    def __init__(self, name: str, description: str, level: InteractionLevel):
        super().__init__(name, description, level)
        self.metrics_history: List[InteractionMetrics] = []
        
    @abstractmethod
    def get_action_space(self) -> Dict[str, Any]:
        """Define the action space for RL optimization"""
        pass
        
    @abstractmethod
    def apply_action(self, action: Dict[str, Any]) -> None:
        """Apply an RL action to modify behavior"""
        pass
        
    def collect_metrics(self, result: InteractionResult) -> InteractionMetrics:
        """Collect metrics from execution"""
        metrics = InteractionMetrics(
            execution_time=result.duration,
            success_rate=1.0 if result.success else 0.0,
            resource_usage=result.metrics,
            quality_score=self.calculate_quality_score(result)
        )
        self.metrics_history.append(metrics)
        return metrics
        
    def calculate_quality_score(self, result: InteractionResult) -> float:
        """Override to implement quality scoring"""
        return 1.0 if result.success else 0.0


if __name__ == "__main__":
    # Example Level 0 interaction
    class ExampleLevel0(Level0Interaction):
        def initialize_module(self):
            return {"name": "test_module"}
            
        def execute(self, **kwargs):
            return {"result": "test_output"}
            
        def validate_output(self, output):
            return output.get("result") == "test_output"
    
    # Example Level 1 interaction
    class ExampleLevel1(Level1Interaction):
        def initialize_modules(self):
            return {"name": "module1"}, {"name": "module2"}
            
        def transform_output(self, output1):
            return {"input": output1["result"]}
            
        def execute_module1(self, **kwargs):
            return {"result": "module1_output"}
            
        def execute_module2(self, input_data):
            return {"result": f"processed_{input_data['input']}"}
            
        def validate_output(self, output):
            return output["pipeline_result"]["result"] == "processed_module1_output"
    
    # Run examples
    runner = InteractionRunner("Example Project")
    
    # Test Level 0
    level0 = ExampleLevel0("Example Level 0", "Test single module")
    runner.run_interaction(level0)
    
    # Test Level 1
    level1 = ExampleLevel1("Example Level 1", "Test two module pipeline")
    runner.run_interaction(level1)
    
    # Generate report
    report = runner.generate_report()
    print(f"\nReport: {json.dumps(report, indent=2)}")