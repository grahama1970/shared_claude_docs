"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_14_arangodb_to_unsloth_pipeline.py
Description: Test ArangoDB → Unsloth training data pipeline
Level: 1
Modules: ArangoDB, Unsloth, Test Reporter
Expected Bugs: Data format issues, training data quality, memory constraints
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import json

class ArangoDBToUnslothPipelineTest(BaseInteractionTest):
    """Level 1: Test ArangoDB to Unsloth pipeline"""
    
    def __init__(self):
        super().__init__(
            test_name="ArangoDB to Unsloth Pipeline",
            level=1,
            modules=["ArangoDB", "Unsloth", "Test Reporter"]
        )
    
    def test_training_data_extraction(self):
        """Test extracting training data from ArangoDB for Unsloth"""
        self.print_header()
        
        # Import modules
        try:
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            from unsloth import UnslothTrainer, prepare_dataset
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run pipeline"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize handlers
        try:
            arango = ArangoDocumentHandler()
            trainer = UnslothTrainer()
            self.record_test("handlers_init", True, {})
        except Exception as e:
            self.add_bug(
                "Handler initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("handlers_init", False, {"error": str(e)})
            return
        
        # Test data extraction scenarios
        test_scenarios = [
            {
                "name": "Q&A pairs extraction",
                "collection": "qa_pairs",
                "query": {"type": "qa", "quality": {"$gte": 0.8}},
                "format": "qa"
            },
            {
                "name": "Document pairs extraction",
                "collection": "documents",
                "query": {"type": "research_paper"},
                "format": "document"
            },
            {
                "name": "Conversation extraction",
                "collection": "conversations",
                "query": {"type": "dialog", "turns": {"$gte": 3}},
                "format": "conversation"
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\nTesting: {scenario['name']}")
            pipeline_start = time.time()
            
            try:
                # Step 1: Query ArangoDB for training data
                print(f"Querying collection: {scenario['collection']}")
                query_start = time.time()
                
                result = arango.handle({
                    "operation": "search",
                    "collection": scenario["collection"],
                    "query": scenario["query"],
                    "limit": 1000  # Limit for testing
                })
                
                query_time = time.time() - query_start
                
                if not result or "documents" not in result:
                    self.add_bug(
                        "Failed to query training data",
                        "HIGH",
                        scenario=scenario["name"],
                        error=result.get("error", "No documents returned")
                    )
                    continue
                
                documents = result["documents"]
                print(f"✅ Retrieved {len(documents)} documents in {query_time:.2f}s")
                
                if not documents:
                    print("   ⚠️ No documents found, skipping...")
                    continue
                
                # Step 2: Transform to training format
                print("Transforming to training format...")
                transform_start = time.time()
                
                training_data = []
                transform_errors = []
                
                for doc in documents:
                    try:
                        if scenario["format"] == "qa":
                            # Q&A format
                            if "question" in doc and "answer" in doc:
                                training_data.append({
                                    "instruction": doc["question"],
                                    "output": doc["answer"],
                                    "input": doc.get("context", "")
                                })
                            else:
                                transform_errors.append("Missing Q&A fields")
                        
                        elif scenario["format"] == "document":
                            # Document summarization format
                            if "content" in doc and "title" in doc:
                                training_data.append({
                                    "instruction": "Summarize this document",
                                    "input": doc["content"][:2000],  # Truncate
                                    "output": doc.get("summary", doc["title"])
                                })
                            else:
                                transform_errors.append("Missing document fields")
                        
                        elif scenario["format"] == "conversation":
                            # Conversation format
                            if "messages" in doc:
                                for i in range(0, len(doc["messages"]) - 1, 2):
                                    if i + 1 < len(doc["messages"]):
                                        training_data.append({
                                            "instruction": doc["messages"][i]["content"],
                                            "output": doc["messages"][i + 1]["content"],
                                            "input": ""
                                        })
                            else:
                                transform_errors.append("Missing messages field")
                                
                    except Exception as e:
                        transform_errors.append(str(e))
                
                transform_time = time.time() - transform_start
                
                print(f"✅ Transformed {len(training_data)} examples in {transform_time:.2f}s")
                print(f"   Transform errors: {len(transform_errors)}")
                
                # Check transformation quality
                if len(transform_errors) > len(documents) * 0.1:
                    self.add_bug(
                        "High transformation error rate",
                        "HIGH",
                        error_rate=len(transform_errors)/len(documents),
                        scenario=scenario["name"]
                    )
                
                if not training_data:
                    self.add_bug(
                        "No training data produced",
                        "HIGH",
                        scenario=scenario["name"],
                        documents_retrieved=len(documents)
                    )
                    continue
                
                # Step 3: Prepare dataset for Unsloth
                print("Preparing dataset for training...")
                prep_start = time.time()
                
                dataset = prepare_dataset(training_data)
                prep_time = time.time() - prep_start
                
                if dataset:
                    print(f"✅ Dataset prepared in {prep_time:.2f}s")
                    
                    # Validate dataset
                    if hasattr(dataset, 'num_rows'):
                        num_rows = dataset.num_rows
                    else:
                        num_rows = len(dataset)
                    
                    print(f"   Dataset size: {num_rows} examples")
                    
                    # Quality checks
                    if num_rows < 10:
                        self.add_bug(
                            "Dataset too small for training",
                            "HIGH",
                            size=num_rows,
                            scenario=scenario["name"]
                        )
                    
                    # Check for data quality issues
                    sample = training_data[0] if training_data else {}
                    if not sample.get("instruction") or not sample.get("output"):
                        self.add_bug(
                            "Empty instruction or output in training data",
                            "HIGH",
                            scenario=scenario["name"],
                            sample=sample
                        )
                    
                    self.record_test(f"pipeline_{scenario['name']}", True, {
                        "documents_retrieved": len(documents),
                        "training_examples": len(training_data),
                        "transform_errors": len(transform_errors),
                        "query_time": query_time,
                        "transform_time": transform_time,
                        "prep_time": prep_time,
                        "total_time": time.time() - pipeline_start
                    })
                else:
                    self.add_bug(
                        "Dataset preparation failed",
                        "HIGH",
                        scenario=scenario["name"]
                    )
                    self.record_test(f"pipeline_{scenario['name']}", False, {})
                    
            except Exception as e:
                self.add_bug(
                    f"Pipeline exception for {scenario['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"pipeline_{scenario['name']}", False, {"error": str(e)})
    
    def test_incremental_training(self):
        """Test incremental training with new data"""
        print("\n\nTesting Incremental Training...")
        
        try:
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            from unsloth import UnslothTrainer
            
            arango = ArangoDocumentHandler()
            trainer = UnslothTrainer()
            
            # Simulate getting new training data over time
            print("Simulating incremental data updates...")
            
            for batch in range(3):
                print(f"\nBatch {batch + 1}:")
                
                # Get new data since last timestamp
                timestamp = time.time() - (3 - batch) * 3600  # 1 hour ago
                
                result = arango.handle({
                    "operation": "search",
                    "collection": "training_data",
                    "query": {"timestamp": {"$gte": timestamp}},
                    "limit": 100
                })
                
                if result and result.get("documents"):
                    docs = result["documents"]
                    print(f"   Found {len(docs)} new documents")
                    
                    # Convert to training format
                    training_data = []
                    for doc in docs:
                        if "input" in doc and "output" in doc:
                            training_data.append({
                                "instruction": doc.get("instruction", ""),
                                "input": doc["input"],
                                "output": doc["output"]
                            })
                    
                    if training_data:
                        # Incremental training
                        print(f"   Training on {len(training_data)} examples...")
                        
                        train_result = trainer.train_incremental(
                            training_data,
                            epochs=1,
                            batch_size=8
                        )
                        
                        if train_result:
                            print(f"   ✅ Incremental training complete")
                            self.record_test(f"incremental_batch_{batch}", True, {
                                "examples": len(training_data),
                                "loss": train_result.get("loss")
                            })
                        else:
                            self.add_bug(
                                "Incremental training failed",
                                "HIGH",
                                batch=batch
                            )
                    else:
                        print("   ⚠️ No valid training data in batch")
                else:
                    print("   ⚠️ No new documents found")
                
                # Simulate time passing
                time.sleep(0.5)
                
        except AttributeError:
            print("❌ Incremental training not implemented")
            self.record_test("incremental_training", False, {"error": "Not implemented"})
        except Exception as e:
            self.add_bug(
                "Exception in incremental training",
                "HIGH",
                error=str(e)
            )
            self.record_test("incremental_training", False, {"error": str(e)})
    
    def test_model_evaluation(self):
        """Test evaluating trained model quality"""
        print("\n\nTesting Model Evaluation...")
        
        try:
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            from unsloth import UnslothTrainer, evaluate_model
            
            arango = ArangoDocumentHandler()
            trainer = UnslothTrainer()
            
            # Get evaluation dataset from ArangoDB
            print("Retrieving evaluation dataset...")
            
            result = arango.handle({
                "operation": "search",
                "collection": "evaluation_data",
                "query": {"type": "eval", "used": False},
                "limit": 100
            })
            
            if result and result.get("documents"):
                eval_data = result["documents"]
                print(f"✅ Retrieved {len(eval_data)} evaluation examples")
                
                # Evaluate model
                print("Evaluating model performance...")
                
                metrics = evaluate_model(trainer.model, eval_data)
                
                if metrics:
                    print(f"\nEvaluation Metrics:")
                    print(f"   Accuracy: {metrics.get('accuracy', 'N/A')}")
                    print(f"   Perplexity: {metrics.get('perplexity', 'N/A')}")
                    print(f"   Loss: {metrics.get('loss', 'N/A')}")
                    
                    self.record_test("model_evaluation", True, metrics)
                    
                    # Quality checks
                    if metrics.get("accuracy", 0) < 0.5:
                        self.add_bug(
                            "Poor model accuracy",
                            "HIGH",
                            accuracy=metrics.get("accuracy")
                        )
                    
                    if metrics.get("perplexity", float('inf')) > 100:
                        self.add_bug(
                            "High perplexity indicates poor model",
                            "HIGH",
                            perplexity=metrics.get("perplexity")
                        )
                    
                    # Mark evaluation data as used
                    for doc in eval_data:
                        arango.handle({
                            "operation": "update",
                            "collection": "evaluation_data",
                            "key": doc.get("_key"),
                            "data": {"used": True}
                        })
                else:
                    self.add_bug(
                        "Model evaluation failed",
                        "HIGH"
                    )
                    self.record_test("model_evaluation", False, {})
            else:
                print("❌ No evaluation data available")
                self.record_test("model_evaluation", False, {"error": "No eval data"})
                
        except Exception as e:
            self.add_bug(
                "Exception in model evaluation",
                "HIGH",
                error=str(e)
            )
            self.record_test("model_evaluation", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_training_data_extraction()
        self.test_incremental_training()
        self.test_model_evaluation()
        return self.generate_report()


def main():
    """Run the test"""
    tester = ArangoDBToUnslothPipelineTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)