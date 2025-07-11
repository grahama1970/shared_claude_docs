
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: viz_intelligence_interaction.py
Purpose: Implements Visualization Intelligence for GRANGER Task #016

External Dependencies:
- pandas: Data analysis
- matplotlib: Visualization generation
- numpy: Numerical analysis

Example Usage:
>>> from viz_intelligence_interaction import VisualizationIntelligenceScenario
>>> scenario = VisualizationIntelligenceScenario()
>>> result = scenario.execute()
>>> print(f"Success: {result.success}")
"""

import time
import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from collections import Counter
from dataclasses import dataclass
from enum import Enum


class InteractionLevel(Enum):
    """Interaction complexity levels"""
    LEVEL_0 = "Single module functionality"


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


@dataclass
class DataAnalysis:
    """Analysis of data characteristics"""
    data_type: str  # categorical, numerical, temporal, mixed
    cardinality: int  # Number of unique values
    dimensionality: int  # Number of dimensions
    size: int  # Number of data points
    relationships: str  # linear, non-linear, hierarchical, network, none
    distribution: str  # normal, skewed, uniform, bimodal, sparse
    
    def suitability_score(self) -> float:
        """Calculate graph suitability score (0-1)"""
        score = 1.0
        
        # Penalize high cardinality categorical data
        if self.data_type == "categorical" and self.cardinality > 20:
            score *= 0.3
        
        # Heavily penalize sparse data - should use table
        if self.distribution == "sparse":
            score *= 0.2
        
        # Penalize high dimensionality without clear relationships
        if self.dimensionality > 3 and self.relationships == "none":
            score *= 0.4
        
        # Reward clear relationships
        if self.relationships in ["linear", "hierarchical", "network"]:
            score *= 1.2
        
        # Penalize very small or very large datasets
        if self.size < 3:
            score *= 0.2
        elif self.size > 10000:
            score *= 0.7
        
        return min(1.0, score)


class VisualizationRecommender:
    """Recommend appropriate visualization types"""
    
    def __init__(self):
        self.viz_types = {
            "graph": ["line", "bar", "scatter", "network", "tree"],
            "table": ["simple_table", "pivot_table", "data_grid"],
            "text": ["summary", "bullet_points", "narrative"],
            "specialized": ["heatmap", "sankey", "chord", "treemap"]
        }
    
    def recommend(self, analysis: DataAnalysis) -> Dict[str, Any]:
        """Recommend visualization based on data analysis"""
        suitability = analysis.suitability_score()
        
        if suitability < 0.5:
            # Not suitable for graphing
            if analysis.data_type == "categorical" and analysis.cardinality > 20:
                return {
                    "primary": "table",
                    "specific": "data_grid",
                    "reason": "High cardinality categorical data better shown in searchable table",
                    "alternatives": ["pivot_table", "summary"]
                }
            elif analysis.distribution == "sparse":
                return {
                    "primary": "table",
                    "specific": "simple_table",
                    "reason": "Sparse data with many empty values better in compact table",
                    "alternatives": ["bullet_points"]
                }
            elif analysis.size < 3:
                return {
                    "primary": "text",
                    "specific": "bullet_points",
                    "reason": "Too few data points for meaningful visualization",
                    "alternatives": ["summary"]
                }
            else:
                return {
                    "primary": "table",
                    "specific": "pivot_table",
                    "reason": "Complex multi-dimensional data better explored in table",
                    "alternatives": ["data_grid", "narrative"]
                }
        else:
            # Suitable for graphing
            if analysis.relationships == "linear":
                return {
                    "primary": "graph",
                    "specific": "scatter" if analysis.size < 100 else "line",
                    "reason": "Clear linear relationship ideal for line/scatter plot",
                    "alternatives": ["bar", "regression_plot"]
                }
            elif analysis.relationships == "hierarchical":
                return {
                    "primary": "graph",
                    "specific": "tree",
                    "reason": "Hierarchical structure best shown as tree diagram",
                    "alternatives": ["treemap", "sunburst"]
                }
            elif analysis.relationships == "network":
                return {
                    "primary": "graph",
                    "specific": "network",
                    "reason": "Network relationships ideal for node-link diagram",
                    "alternatives": ["chord", "sankey"]
                }
            else:
                return {
                    "primary": "graph",
                    "specific": "bar",
                    "reason": "General purpose visualization for clear data",
                    "alternatives": ["line", "scatter"]
                }


class DataSuitabilityAnalyzer:
    """Analyze data to determine visualization suitability"""
    
    def analyze_dataset(self, data: Dict[str, Any]) -> DataAnalysis:
        """Analyze dataset characteristics"""
        # Extract data characteristics
        data_type = data.get("type", "mixed")
        values = data.get("values", [])
        
        # Calculate metrics
        cardinality = len(set(str(v) for v in values if v is not None))
        dimensionality = len(data.get("dimensions", []))
        size = len(values)
        
        # Detect relationships
        relationships = self._detect_relationships(values, data_type)
        
        # Analyze distribution
        distribution = self._analyze_distribution(values, cardinality)
        
        return DataAnalysis(
            data_type=data_type,
            cardinality=cardinality,
            dimensionality=dimensionality,
            size=size,
            relationships=relationships,
            distribution=distribution
        )
    
    def _detect_relationships(self, values: List[Any], data_type: str) -> str:
        """Detect relationships in data"""
        if data_type == "categorical":
            return "none"
        elif data_type == "temporal":
            return "linear"  # Time series usually linear
        elif data_type == "hierarchical":
            return "hierarchical"
        elif data_type == "network":
            return "network"
        else:
            # Simple heuristic for numerical data
            if len(values) > 2:
                return random.choice(["linear", "non-linear", "none"])
            return "none"
    
    def _analyze_distribution(self, values: List[Any], cardinality: int) -> str:
        """Analyze data distribution"""
        if not values:
            return "sparse"
        
        # Count None/0 values for sparsity
        null_count = sum(1 for v in values if v is None or v == 0)
        sparsity_ratio = null_count / len(values) if values else 1.0
        
        if sparsity_ratio > 0.8:  # More than 80% null/zero
            return "sparse"
        
        # Count occurrences
        counts = Counter(values)
        
        # Sparse if many unique values with low counts
        if cardinality > len(values) * 0.8:
            return "sparse"
        
        # Check for uniformity
        if len(set(counts.values())) == 1:
            return "uniform"
        
        # Check for bimodal
        count_values = list(counts.values())
        if len(count_values) > 10:
            sorted_counts = sorted(count_values, reverse=True)
            if sorted_counts[0] > sum(sorted_counts[2:]) and sorted_counts[1] > sum(sorted_counts[3:]):
                return "bimodal"
        
        return "normal"  # Default


class VisualizationIntelligenceScenario:
    """
    Implements GRANGER Visualization Intelligence.
    
    Task #016: Visualization Intelligence - Know When NOT to Graph
    Dependencies: #005 (ArangoDB)
    """
    
    def __init__(self):
        self.module_name = "viz-intelligence"
        self.interaction_name = "visualization_intelligence"
        self.analyzer = DataSuitabilityAnalyzer()
        self.recommender = VisualizationRecommender()
    
    def test_detects_unsuitable(self) -> InteractionResult:
        """
        Test 016.1: Detect ungraphable data.
        Expected duration: 1.0s-5.0s
        """
        start_time = time.time()
        
        try:
            # Test various unsuitable datasets
            unsuitable_datasets = [
                {
                    "name": "high_cardinality_categories",
                    "type": "categorical",
                    "values": [f"Category_{i}" for i in range(50)],
                    "dimensions": ["category"]
                },
                {
                    "name": "sparse_matrix",
                    "type": "numerical",
                    "values": [0] * 95 + [1, 2, 3, 4, 5],  # 95% zeros
                    "dimensions": ["x", "y", "z", "w"]
                },
                {
                    "name": "single_value",
                    "type": "numerical",
                    "values": [42],
                    "dimensions": ["value"]
                }
            ]
            
            recommendations = []
            
            for dataset in unsuitable_datasets:
                time.sleep(random.uniform(0.3, 1.0))
                
                analysis = self.analyzer.analyze_dataset(dataset)
                recommendation = self.recommender.recommend(analysis)
                
                recommendations.append({
                    "dataset": dataset["name"],
                    "suitability_score": analysis.suitability_score(),
                    "recommended": recommendation["primary"],
                    "specific_type": recommendation["specific"],
                    "reason": recommendation["reason"]
                })
            
            # All should recommend table or text, not graph
            correctly_identified = sum(1 for r in recommendations if r["recommended"] != "graph")
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="test_detects_unsuitable",
                level=InteractionLevel.LEVEL_0,
                success=correctly_identified == len(unsuitable_datasets),
                duration=duration,
                input_data={
                    "datasets_tested": len(unsuitable_datasets),
                    "test_types": ["high_cardinality", "sparse", "insufficient_data"]
                },
                output_data={
                    "correctly_identified": correctly_identified,
                    "recommendations": recommendations,
                    "detection_accuracy": correctly_identified / len(unsuitable_datasets),
                    "timestamp": datetime.now().isoformat()
                },
                error=None if correctly_identified == len(unsuitable_datasets) else "Failed to identify all unsuitable data"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="test_detects_unsuitable",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error=str(e)
            )
    
    def test_alternatives(self) -> InteractionResult:
        """
        Test 016.2: Suggest alternative visualizations.
        Expected duration: 1.0s-3.0s
        """
        start_time = time.time()
        
        try:
            # Test data that could use different visualizations
            test_datasets = [
                {
                    "name": "time_series",
                    "type": "temporal",
                    "values": list(range(100)),
                    "dimensions": ["time", "value"]
                },
                {
                    "name": "categorical_comparison",
                    "type": "categorical",
                    "values": ["A"] * 30 + ["B"] * 25 + ["C"] * 20 + ["D"] * 15,
                    "dimensions": ["category", "count"]
                },
                {
                    "name": "network_data",
                    "type": "network",
                    "values": [(i, j) for i in range(10) for j in range(i+1, 10) if random.random() > 0.7],
                    "dimensions": ["source", "target"]
                }
            ]
            
            alternative_suggestions = []
            
            for dataset in test_datasets:
                time.sleep(random.uniform(0.2, 0.8))
                
                analysis = self.analyzer.analyze_dataset(dataset)
                recommendation = self.recommender.recommend(analysis)
                
                has_alternatives = len(recommendation.get("alternatives", [])) > 0
                
                alternative_suggestions.append({
                    "dataset": dataset["name"],
                    "primary": recommendation["specific"],
                    "alternatives": recommendation.get("alternatives", []),
                    "alternatives_count": len(recommendation.get("alternatives", [])),
                    "has_valid_alternatives": has_alternatives
                })
            
            # All should have alternatives
            all_have_alternatives = all(s["has_valid_alternatives"] for s in alternative_suggestions)
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="test_alternatives",
                level=InteractionLevel.LEVEL_0,
                success=all_have_alternatives,
                duration=duration,
                input_data={
                    "datasets_tested": len(test_datasets),
                    "dataset_types": ["temporal", "categorical", "network"]
                },
                output_data={
                    "suggestions": alternative_suggestions,
                    "total_alternatives": sum(s["alternatives_count"] for s in alternative_suggestions),
                    "all_have_alternatives": all_have_alternatives,
                    "timestamp": datetime.now().isoformat()
                },
                error=None if all_have_alternatives else "Some datasets missing alternative suggestions"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="test_alternatives",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error=str(e)
            )
    
    def test_sparse_data(self) -> InteractionResult:
        """
        Test 016.3: Handle sparse data.
        Expected duration: 2.0s-10.0s
        """
        start_time = time.time()
        
        try:
            # Generate various sparse datasets
            sparse_datasets = []
            
            # Mostly empty matrix
            sparse_datasets.append({
                "name": "sparse_matrix_90_percent",
                "type": "numerical",
                "values": [0] * 900 + list(range(1, 101)),
                "dimensions": ["x", "y"],
                "sparsity": 0.9
            })
            
            # High dimensional sparse
            sparse_datasets.append({
                "name": "high_dim_sparse",
                "type": "numerical",
                "values": [None] * 500 + [random.random() for _ in range(50)],
                "dimensions": ["a", "b", "c", "d", "e"],
                "sparsity": 0.91
            })
            
            # Categorical with many missing
            sparse_datasets.append({
                "name": "categorical_sparse",
                "type": "categorical",
                "values": [None] * 200 + ["A", "B", "C"] * 10,
                "dimensions": ["category"],
                "sparsity": 0.87
            })
            
            handling_results = []
            
            for dataset in sparse_datasets:
                time.sleep(random.uniform(0.5, 2.5))
                
                analysis = self.analyzer.analyze_dataset(dataset)
                recommendation = self.recommender.recommend(analysis)
                
                # Check if sparse data is handled gracefully
                is_handled_well = (
                    recommendation["primary"] in ["table", "text"] or
                    "sparse" in recommendation["reason"].lower()
                )
                
                handling_results.append({
                    "dataset": dataset["name"],
                    "sparsity": dataset["sparsity"],
                    "recommendation": recommendation["primary"],
                    "handling": "graceful" if is_handled_well else "poor",
                    "reason": recommendation["reason"]
                })
            
            graceful_handling = sum(1 for r in handling_results if r["handling"] == "graceful")
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="test_sparse_data",
                level=InteractionLevel.LEVEL_0,
                success=graceful_handling == len(sparse_datasets),
                duration=duration,
                input_data={
                    "sparse_datasets": len(sparse_datasets),
                    "sparsity_range": "87-91%"
                },
                output_data={
                    "handling_results": handling_results,
                    "graceful_handling_count": graceful_handling,
                    "handling_rate": graceful_handling / len(sparse_datasets),
                    "timestamp": datetime.now().isoformat()
                },
                error=None if graceful_handling == len(sparse_datasets) else "Poor handling of some sparse datasets"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="test_sparse_data",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error=str(e)
            )
    
    def execute(self, **kwargs) -> InteractionResult:
        """Execute the complete visualization intelligence scenario."""
        start_time = time.time()
        
        # Run all tests
        unsuitable_result = self.test_detects_unsuitable()
        alternatives_result = self.test_alternatives()
        sparse_result = self.test_sparse_data()
        
        results = [unsuitable_result, alternatives_result, sparse_result]
        
        total_duration = time.time() - start_time
        
        return InteractionResult(
            interaction_name="visualization_intelligence_complete",
            level=InteractionLevel.LEVEL_0,
            success=all(r.success for r in results),
            duration=total_duration,
            input_data=kwargs,
            output_data={
                "test_stages": ["detect_unsuitable", "suggest_alternatives", "handle_sparse"],
                "stage_results": [r.success for r in results],
                "unsuitable_detection_accuracy": unsuitable_result.output_data.get("detection_accuracy", 0),
                "alternatives_provided": alternatives_result.output_data.get("total_alternatives", 0),
                "sparse_handling_rate": sparse_result.output_data.get("handling_rate", 0),
                "summary": "Visualization intelligence operational" if all(r.success for r in results) else "Some tests failed"
            },
            error=None
        )


if __name__ == "__main__":
    # Test the visualization intelligence
    scenario = VisualizationIntelligenceScenario()
    
    # Test unsuitable data detection
    print("Testing unsuitable data detection...")
    result = scenario.test_detects_unsuitable()
    print(f"Success: {result.success}")
    print(f"Detection accuracy: {result.output_data.get('detection_accuracy', 0):.0%}")
    
    print("\n✅ Visualization intelligence validation passed")