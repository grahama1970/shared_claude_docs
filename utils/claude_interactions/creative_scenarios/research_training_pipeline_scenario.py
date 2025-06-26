#!/usr/bin/env python3
"""
Research to Training Pipeline - Cross-Domain Translation
Transforms research papers into ML training configurations across different frameworks
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List
import json

class ResearchToTrainingPipelineScenario:
    """
    Tests complex multi-stage data transformation across conceptual domains:
    Research text → ML parameters → Framework configurations
    
    Communication Pattern: Sequential transformation with domain translation
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.transformation_stages = []
        self.frameworks = ["sparta", "unsloth_wip"]
        
    async def run(self, research_topic: str = "Efficient LoRA Fine-tuning Techniques"):
        """Run research to training pipeline"""
        print(f"\n🔬 RESEARCH TO TRAINING PIPELINE: {research_topic}")
        print("=" * 70)
        
        # Phase 1: Acquire research
        paper_data = await self._phase_1_acquire_research(research_topic)
        
        # Phase 2: Extract and translate
        ml_params = await self._phase_2_extract_parameters(paper_data)
        
        # Phase 3: Generate framework configs
        configs = await self._phase_3_generate_configs(ml_params)
        
        # Phase 4: Validate and deploy
        await self._phase_4_validate_deploy(configs)
        
        self._print_pipeline_summary()    
    async def _phase_1_acquire_research(self, topic: str):
        """Acquire and process research papers"""
        print("\n📚 Phase 1: Research Acquisition")
        print("-" * 50)
        
        task = self.orchestrator.create_task(
            name="Research Acquisition",
            description="Find and process relevant papers"
        )
        
        # Search, download, and extract
        self.orchestrator.add_step(
            task,
            module="arxiv-mcp-server",
            capability="search_papers",
            input_data={"query": topic, "max_results": 2}
        )
        
        self.orchestrator.add_step(
            task,
            module="arxiv-mcp-server",
            capability="download_paper",
            input_data={"paper_id": "$step_1.papers[0].id"},
            depends_on=["step_1"]
        )
        
        self.orchestrator.add_step(
            task,
            module="marker",
            capability="extract_text",
            input_data={
                "pdf_path": "$step_2.local_pdf_path",
                "extract_tables": True
            },
            depends_on=["step_2"]
        )
        
        result = await self.orchestrator.execute_task(task.id)
        
        self.transformation_stages.append({
            "stage": "research_acquisition",
            "transforms": "query → paper → text"
        })
        
        return result    
    async def _phase_2_extract_parameters(self, paper_data: Dict):
        """Extract ML parameters from research text"""
        print("\n🔧 Phase 2: Parameter Extraction & Translation")
        print("-" * 50)
        
        task = self.orchestrator.create_task(
            name="Parameter Extraction",
            description="Extract structured ML parameters"
        )
        
        # Use Claude as translator
        print("  🤖 Extracting ML parameters...")
        self.orchestrator.add_step(
            task,
            module="claude_max_proxy",
            capability="extract_structured",
            input_data={
                "text": "$research_acquisition.step_3.text",
                "schema": {
                    "model_architecture": "string",
                    "training_params": {
                        "epochs": "int",
                        "learning_rate": "float",
                        "batch_size": "int",
                        "optimizer": "string"
                    },
                    "lora_config": {
                        "rank": "int",
                        "alpha": "float",
                        "target_modules": "list"
                    }
                },
                "prompt": "Extract all ML training parameters from this paper"
            }
        )
        
        # Store extracted params
        self.orchestrator.add_step(
            task,
            module="arangodb",
            capability="create_node",
            input_data={
                "node_type": "MLParameters",
                "properties": "$step_1.extracted_data",
                "source": "$research_acquisition.step_1.papers[0].id"
            },
            depends_on=["step_1"]
        )
        
        result = await self.orchestrator.execute_task(task.id)
        
        self.transformation_stages.append({
            "stage": "parameter_extraction",
            "transforms": "text → structured_params"
        })
        
        return result
    
    async def _phase_3_generate_configs(self, ml_params: Dict):
        """Generate framework-specific configurations"""
        print("\n⚙️ Phase 3: Framework Configuration Generation")
        print("-" * 50)
        
        task = self.orchestrator.create_task(
            name="Config Generation",
            description="Generate framework configs"
        )
        
        configs = {}
        
        # Generate Sparta config
        print("  🏛️ Generating Sparta configuration...")
        self.orchestrator.add_step(
            task,
            module="claude_max_proxy",
            capability="translate_config",
            input_data={
                "source_params": "$parameter_extraction.step_1.extracted_data",
                "target_framework": "sparta",
                "template": "training_config"
            }
        )
        
        # Generate Unsloth config
        print("  🚀 Generating Unsloth configuration...")
        self.orchestrator.add_step(
            task,
            module="claude_max_proxy",
            capability="translate_config",
            input_data={
                "source_params": "$parameter_extraction.step_1.extracted_data",
                "target_framework": "unsloth",
                "template": "lora_finetuning"
            }
        )
        
        # Create training dataset spec
        self.orchestrator.add_step(
            task,
            module="youtube_transcripts",
            capability="find_tutorials",
            input_data={
                "topic": "$research_acquisition.topic",
                "filter": "implementation_tutorial"
            }
        )
        
        result = await self.orchestrator.execute_task(task.id)
        
        self.transformation_stages.append({
            "stage": "config_generation",
            "transforms": "params → framework_configs"
        })
        
        return result    
    async def _phase_4_validate_deploy(self, configs: Dict):
        """Validate configurations and prepare deployment"""
        print("\n✅ Phase 4: Validation & Deployment Prep")
        print("-" * 50)
        
        task = self.orchestrator.create_task(
            name="Validation",
            description="Validate and prepare deployment"
        )
        
        # Validate with ground truth
        print("  🎯 Validating configurations...")
        self.orchestrator.add_step(
            task,
            module="marker-ground-truth",
            capability="validate_config",
            input_data={
                "sparta_config": "$config_generation.step_1.config",
                "unsloth_config": "$config_generation.step_2.config",
                "validation_rules": "ml_best_practices"
            }
        )
        
        # Test with small dataset
        print("  🧪 Running test training...")
        self.orchestrator.add_step(
            task,
            module="sparta",
            capability="test_config",
            input_data={
                "config": "$config_generation.step_1.config",
                "test_samples": 10
            },
            depends_on=["step_1"]
        )
        
        # Generate deployment report
        self.orchestrator.add_step(
            task,
            module="claude-test-reporter",
            capability="generate_report",
            input_data={
                "test_name": "ResearchToTrainingPipeline",
                "pipeline_stages": self.transformation_stages,
                "validation_results": "$step_1.results",
                "test_results": "$step_2.results"
            },
            depends_on=["step_1", "step_2"]
        )
        
        result = await self.orchestrator.execute_task(task.id)
        
        self.transformation_stages.append({
            "stage": "validation_deployment",
            "transforms": "configs → validated_artifacts"
        })
        
        return result
    
    def _print_pipeline_summary(self):
        """Print pipeline transformation summary"""
        print("\n📊 PIPELINE SUMMARY")
        print("=" * 60)
        
        print("\nTransformation Stages:")
        for i, stage in enumerate(self.transformation_stages):
            print(f"  {i+1}. {stage['stage']}: {stage['transforms']}")
        
        print("\nKey Pattern Demonstrated:")
        print("  • Cross-domain translation (research → ML)")
        print("  • Multi-stage data transformation")
        print("  • Framework-agnostic parameter extraction")
        print("  • Automated config generation")
        
        print("\nData Flow:")
        print("  Research Paper → Text → Parameters → Configs → Validation")
        
        print("\nFrameworks Targeted:")
        for framework in self.frameworks:
            print(f"  • {framework}")


if __name__ == "__main__":
    print("ResearchToTrainingPipeline tests:")
    print("- Complex domain translation")
    print("- Sequential data transformation")
    print("- Multi-framework config generation")
    print("- Automated validation pipeline")