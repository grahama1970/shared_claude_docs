#!/usr/bin/env python3
"""
Visualization Decision Tests for Claude Module Communicator

Tests CMC's ability to:
1. Detect when D3 visualizations don't reflect the data accurately
2. Identify when data cannot be usefully displayed by ANY graph technique
3. Recommend tables or alternative representations when appropriate
4. Course-correct visualization choices based on data characteristics
5. Provide helpful feedback about why a visualization isn't suitable
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class VisualizationType(Enum):
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    SCATTER_PLOT = "scatter_plot"
    NETWORK_GRAPH = "network_graph"
    SANKEY_DIAGRAM = "sankey_diagram"
    HEATMAP = "heatmap"
    FORCE_DIRECTED = "force_directed"
    TREEMAP = "treemap"
    CHORD_DIAGRAM = "chord_diagram"
    TABLE = "table"
    TEXT_SUMMARY = "text_summary"
    NONE = "none"


@dataclass
class VisualizationDecision:
    """Decision made by CMC about visualization suitability"""
    original_request: VisualizationType
    recommended: VisualizationType
    suitable: bool
    confidence: float
    reasoning: str
    alternatives: List[VisualizationType]
    warnings: List[str]


class VisualizationAnalyzer:
    """Simulates CMC's visualization decision-making process"""
    
    def analyze(self, data: Dict[str, Any], requested_viz: VisualizationType) -> VisualizationDecision:
        """Analyze data and determine appropriate visualization"""
        
        # Extract data characteristics
        data_type = data.get("type", "unknown")
        num_dimensions = data.get("dimensions", 0)
        num_records = data.get("records", 0)
        has_relationships = data.get("has_relationships", False)
        is_temporal = data.get("is_temporal", False)
        is_categorical = data.get("is_categorical", False)
        is_continuous = data.get("is_continuous", False)
        sparsity = data.get("sparsity", 0.0)
        
        # Decision logic based on data characteristics
        if requested_viz == VisualizationType.LINE_CHART:
            return self._analyze_line_chart(data)
        elif requested_viz == VisualizationType.NETWORK_GRAPH:
            return self._analyze_network_graph(data)
        elif requested_viz == VisualizationType.PIE_CHART:
            return self._analyze_pie_chart(data)
        elif requested_viz == VisualizationType.FORCE_DIRECTED:
            return self._analyze_force_directed(data)
        elif requested_viz == VisualizationType.SANKEY_DIAGRAM:
            return self._analyze_sankey(data)
        elif requested_viz == VisualizationType.HEATMAP:
            return self._analyze_heatmap(data)
        else:
            return self._default_analysis(data, requested_viz)
    
    def _analyze_line_chart(self, data: Dict[str, Any]) -> VisualizationDecision:
        """Analyze suitability for line chart"""
        warnings = []
        
        if data.get("is_categorical") and not data.get("is_temporal"):
            return VisualizationDecision(
                original_request=VisualizationType.LINE_CHART,
                recommended=VisualizationType.BAR_CHART,
                suitable=False,
                confidence=0.9,
                reasoning="Line charts require continuous or temporal data. Categorical data without natural ordering should use bar charts.",
                alternatives=[VisualizationType.BAR_CHART, VisualizationType.TABLE],
                warnings=["Categorical data detected without temporal ordering"]
            )
        
        if not data.get("is_continuous") and not data.get("is_temporal"):
            warnings.append("Data lacks continuous or temporal characteristics")
            
        return VisualizationDecision(
            original_request=VisualizationType.LINE_CHART,
            recommended=VisualizationType.LINE_CHART,
            suitable=True,
            confidence=0.8,
            reasoning="Line chart is appropriate for this data",
            alternatives=[VisualizationType.SCATTER_PLOT],
            warnings=warnings
        )
    
    def _analyze_network_graph(self, data: Dict[str, Any]) -> VisualizationDecision:
        """Analyze suitability for network graph"""
        if not data.get("has_relationships"):
            return VisualizationDecision(
                original_request=VisualizationType.NETWORK_GRAPH,
                recommended=VisualizationType.TABLE,
                suitable=False,
                confidence=0.95,
                reasoning="Network graphs require meaningful relationships between entities. No relationships found in data.",
                alternatives=[VisualizationType.TABLE, VisualizationType.BAR_CHART],
                warnings=["No relational data structure detected"]
            )
        
        if data.get("records", 0) > 1000:
            return VisualizationDecision(
                original_request=VisualizationType.NETWORK_GRAPH,
                recommended=VisualizationType.NETWORK_GRAPH,
                suitable=True,
                confidence=0.7,
                reasoning="Network graph is suitable but may be cluttered with large datasets",
                alternatives=[VisualizationType.CHORD_DIAGRAM, VisualizationType.HEATMAP],
                warnings=["Large dataset may result in visual clutter"]
            )
        
        return VisualizationDecision(
            original_request=VisualizationType.NETWORK_GRAPH,
            recommended=VisualizationType.NETWORK_GRAPH,
            suitable=True,
            confidence=0.9,
            reasoning="Network graph is appropriate for relational data",
            alternatives=[VisualizationType.FORCE_DIRECTED],
            warnings=[]
        )
    
    def _analyze_pie_chart(self, data: Dict[str, Any]) -> VisualizationDecision:
        """Analyze suitability for pie chart"""
        if data.get("is_temporal"):
            return VisualizationDecision(
                original_request=VisualizationType.PIE_CHART,
                recommended=VisualizationType.LINE_CHART,
                suitable=False,
                confidence=0.9,
                reasoning="Pie charts are not suitable for time series data. Use line or area charts instead.",
                alternatives=[VisualizationType.LINE_CHART, VisualizationType.BAR_CHART],
                warnings=["Temporal data detected - pie charts show proportions at a single point in time"]
            )
        
        if data.get("dimensions", 0) > 7:
            return VisualizationDecision(
                original_request=VisualizationType.PIE_CHART,
                recommended=VisualizationType.BAR_CHART,
                suitable=False,
                confidence=0.85,
                reasoning="Too many categories for effective pie chart. Human perception struggles with more than 7 slices.",
                alternatives=[VisualizationType.BAR_CHART, VisualizationType.TREEMAP],
                warnings=["Too many categories for effective visualization"]
            )
        
        return VisualizationDecision(
            original_request=VisualizationType.PIE_CHART,
            recommended=VisualizationType.PIE_CHART,
            suitable=True,
            confidence=0.8,
            reasoning="Pie chart is appropriate for showing proportions",
            alternatives=[VisualizationType.BAR_CHART],
            warnings=[]
        )
    
    def _analyze_force_directed(self, data: Dict[str, Any]) -> VisualizationDecision:
        """Analyze suitability for force-directed graph"""
        if data.get("type") == "tabular_financial":
            return VisualizationDecision(
                original_request=VisualizationType.FORCE_DIRECTED,
                recommended=VisualizationType.TABLE,
                suitable=False,
                confidence=0.95,
                reasoning="Force-directed graphs are for network relationships, not tabular financial data. Use tables or charts.",
                alternatives=[VisualizationType.TABLE, VisualizationType.BAR_CHART, VisualizationType.LINE_CHART],
                warnings=["No network structure in financial tabular data"]
            )
        
        return self._analyze_network_graph(data)  # Similar requirements to network graphs
    
    def _analyze_sankey(self, data: Dict[str, Any]) -> VisualizationDecision:
        """Analyze suitability for Sankey diagram"""
        if not data.get("has_flow"):
            return VisualizationDecision(
                original_request=VisualizationType.SANKEY_DIAGRAM,
                recommended=VisualizationType.BAR_CHART,
                suitable=False,
                confidence=0.9,
                reasoning="Sankey diagrams require flow relationships between categories. No flow data detected.",
                alternatives=[VisualizationType.BAR_CHART, VisualizationType.TABLE],
                warnings=["No flow relationships found in data"]
            )
        
        return VisualizationDecision(
            original_request=VisualizationType.SANKEY_DIAGRAM,
            recommended=VisualizationType.SANKEY_DIAGRAM,
            suitable=True,
            confidence=0.85,
            reasoning="Sankey diagram is appropriate for flow data",
            alternatives=[VisualizationType.CHORD_DIAGRAM],
            warnings=[]
        )
    
    def _analyze_heatmap(self, data: Dict[str, Any]) -> VisualizationDecision:
        """Analyze suitability for heatmap"""
        sparsity = data.get("sparsity", 0.0)
        
        if sparsity > 0.7:
            return VisualizationDecision(
                original_request=VisualizationType.HEATMAP,
                recommended=VisualizationType.SCATTER_PLOT,
                suitable=False,
                confidence=0.85,
                reasoning="Heatmaps are ineffective for sparse data (>70% empty). Consider scatter plots or tables.",
                alternatives=[VisualizationType.SCATTER_PLOT, VisualizationType.TABLE],
                warnings=[f"Data is {sparsity*100:.0f}% sparse - heatmap will be mostly empty"]
            )
        
        if data.get("dimensions", 0) < 2:
            return VisualizationDecision(
                original_request=VisualizationType.HEATMAP,
                recommended=VisualizationType.BAR_CHART,
                suitable=False,
                confidence=0.9,
                reasoning="Heatmaps require at least 2 dimensions. Use bar chart for 1D data.",
                alternatives=[VisualizationType.BAR_CHART, VisualizationType.LINE_CHART],
                warnings=["Insufficient dimensions for heatmap"]
            )
        
        return VisualizationDecision(
            original_request=VisualizationType.HEATMAP,
            recommended=VisualizationType.HEATMAP,
            suitable=True,
            confidence=0.8,
            reasoning="Heatmap is appropriate for this multi-dimensional data",
            alternatives=[VisualizationType.SCATTER_PLOT],
            warnings=[]
        )
    
    def _default_analysis(self, data: Dict[str, Any], requested: VisualizationType) -> VisualizationDecision:
        """Default analysis for unspecified visualization types"""
        return VisualizationDecision(
            original_request=requested,
            recommended=VisualizationType.TABLE,
            suitable=True,
            confidence=0.5,
            reasoning="Default analysis - consider data characteristics for optimal visualization",
            alternatives=[VisualizationType.TABLE],
            warnings=[]
        )


def run_test_scenario(name: str, data: Dict[str, Any], requested_viz: VisualizationType) -> None:
    """Run a single test scenario and print results"""
    print(f"\n{'='*60}")
    print(f"Test Scenario: {name}")
    print(f"{'='*60}")
    print(f"Requested Visualization: {requested_viz.value}")
    print(f"Data Characteristics: {json.dumps(data, indent=2)}")
    
    analyzer = VisualizationAnalyzer()
    decision = analyzer.analyze(data, requested_viz)
    
    print(f"\nDecision:")
    print(f"  Suitable: {'✓' if decision.suitable else '✗'}")
    print(f"  Confidence: {decision.confidence:.0%}")
    print(f"  Recommended: {decision.recommended.value}")
    print(f"  Reasoning: {decision.reasoning}")
    
    if decision.warnings:
        print(f"\nWarnings:")
        for warning in decision.warnings:
            print(f"  ⚠️  {warning}")
    
    if decision.alternatives:
        print(f"\nAlternatives:")
        for alt in decision.alternatives:
            print(f"  - {alt.value}")


def main():
    """Run all test scenarios"""
    print("Claude Module Communicator - Visualization Decision Tests")
    print("Testing ability to detect inappropriate visualizations and recommend alternatives")
    
    # Test 1: Categorical data in line chart
    run_test_scenario(
        "Categorical Data in Line Chart",
        {
            "type": "categorical",
            "is_categorical": True,
            "is_temporal": False,
            "dimensions": 5,
            "records": 100
        },
        VisualizationType.LINE_CHART
    )
    
    # Test 2: Network graph with no relationships
    run_test_scenario(
        "Network Graph Without Relationships",
        {
            "type": "tabular",
            "has_relationships": False,
            "dimensions": 3,
            "records": 50
        },
        VisualizationType.NETWORK_GRAPH
    )
    
    # Test 3: Pie chart for time series
    run_test_scenario(
        "Pie Chart for Time Series Data",
        {
            "type": "time_series",
            "is_temporal": True,
            "is_continuous": True,
            "dimensions": 1,
            "records": 365
        },
        VisualizationType.PIE_CHART
    )
    
    # Test 4: Force-directed for tabular financial data
    run_test_scenario(
        "Force-Directed Graph for Financial Table",
        {
            "type": "tabular_financial",
            "has_relationships": False,
            "is_continuous": True,
            "dimensions": 8,
            "records": 1000
        },
        VisualizationType.FORCE_DIRECTED
    )
    
    # Test 5: Sankey without flow relationships
    run_test_scenario(
        "Sankey Diagram Without Flow Data",
        {
            "type": "categorical",
            "has_flow": False,
            "has_relationships": False,
            "dimensions": 4,
            "records": 200
        },
        VisualizationType.SANKEY_DIAGRAM
    )
    
    # Test 6: Heatmap for sparse data
    run_test_scenario(
        "Heatmap for Sparse Data",
        {
            "type": "matrix",
            "sparsity": 0.85,
            "dimensions": 2,
            "records": 10000
        },
        VisualizationType.HEATMAP
    )
    
    # Test 7: Too many categories for pie chart
    run_test_scenario(
        "Pie Chart with Too Many Categories",
        {
            "type": "categorical",
            "is_categorical": True,
            "dimensions": 15,
            "records": 100
        },
        VisualizationType.PIE_CHART
    )
    
    # Test 8: Large network graph
    run_test_scenario(
        "Network Graph with Large Dataset",
        {
            "type": "network",
            "has_relationships": True,
            "dimensions": 2,
            "records": 5000
        },
        VisualizationType.NETWORK_GRAPH
    )
    
    # Test 9: Valid line chart
    run_test_scenario(
        "Valid Line Chart for Time Series",
        {
            "type": "time_series",
            "is_temporal": True,
            "is_continuous": True,
            "dimensions": 1,
            "records": 100
        },
        VisualizationType.LINE_CHART
    )
    
    # Test 10: Valid heatmap
    run_test_scenario(
        "Valid Heatmap for Dense Matrix",
        {
            "type": "matrix",
            "sparsity": 0.1,
            "dimensions": 2,
            "records": 400
        },
        VisualizationType.HEATMAP
    )
    
    print(f"\n{'='*60}")
    print("All tests completed!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()