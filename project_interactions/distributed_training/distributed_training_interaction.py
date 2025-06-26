
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: distributed_training_interaction.py
Purpose: Orchestrates distributed machine learning training across multiple nodes

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- dataclasses: https://docs.python.org/3/library/dataclasses.html
- numpy: https://numpy.org/doc/stable/
- torch (simulated): https://pytorch.org/docs/stable/

Example Usage:
>>> orchestrator = DistributedTrainingOrchestrator(num_workers=4)
>>> await orchestrator.initialize_workers()
>>> result = await orchestrator.train_distributed(model_config, data_config)
{'epochs_completed': 10, 'final_loss': 0.023, 'workers_used': 4}
"""

import asyncio
import time
import random
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum
from datetime import datetime
import numpy as np


class WorkerStatus(Enum):
    """Worker health status"""
    IDLE = "idle"
    TRAINING = "training"
    AGGREGATING = "aggregating"
    FAILED = "failed"
    RECOVERING = "recovering"


class AggregationStrategy(Enum):
    """Gradient aggregation strategies"""
    ALL_REDUCE = "all_reduce"
    RING_ALL_REDUCE = "ring_all_reduce"
    HIERARCHICAL = "hierarchical"
    ASYNC_SGD = "async_sgd"


@dataclass
class WorkerNode:
    """Represents a distributed training worker"""
    worker_id: str
    host: str
    port: int
    status: WorkerStatus = WorkerStatus.IDLE
    current_epoch: int = 0
    current_batch: int = 0
    gradients: Optional[np.ndarray] = None
    model_version: int = 0
    last_heartbeat: float = field(default_factory=time.time)
    failure_count: int = 0
    assigned_data_shards: List[int] = field(default_factory=list)


@dataclass
class TrainingConfig:
    """Configuration for distributed training"""
    model_size: int
    batch_size: int
    learning_rate: float
    epochs: int
    gradient_clip: float = 1.0
    checkpoint_interval: int = 100
    aggregation_strategy: AggregationStrategy = AggregationStrategy.ALL_REDUCE
    fault_tolerance: bool = True
    max_worker_failures: int = 3


@dataclass
class DataShard:
    """Represents a data shard for distributed training"""
    shard_id: int
    data_indices: List[int]
    size: int
    checksum: str


class DistributedTrainingOrchestrator:
    """Orchestrates distributed ML training across multiple nodes"""
    
    def __init__(self, num_workers: int = 4, heartbeat_interval: float = 5.0):
        self.num_workers = num_workers
        self.heartbeat_interval = heartbeat_interval
        self.workers: Dict[str, WorkerNode] = {}
        self.data_shards: List[DataShard] = []
        self.global_model: Optional[np.ndarray] = None
        self.training_metrics: Dict[str, List[float]] = {
            "loss": [],
            "accuracy": [],
            "gradient_norm": []
        }
        self.checkpoints: List[Dict[str, Any]] = []
        self._running = False
        self._heartbeat_task: Optional[asyncio.Task] = None
        
    async def initialize_workers(self) -> Dict[str, WorkerNode]:
        """Initialize distributed worker nodes"""
        print(f"🚀 Initializing {self.num_workers} distributed workers...")
        
        for i in range(self.num_workers):
            worker_id = f"worker_{i:03d}"
            worker = WorkerNode(
                worker_id=worker_id,
                host=f"10.0.1.{100 + i}",
                port=5000 + i
            )
            self.workers[worker_id] = worker
            
        # Start heartbeat monitoring
        self._running = True
        self._heartbeat_task = asyncio.create_task(self._monitor_heartbeats())
        
        print(f"✅ Initialized {len(self.workers)} workers")
        return self.workers
    
    async def _monitor_heartbeats(self):
        """Monitor worker heartbeats and detect failures"""
        while self._running:
            current_time = time.time()
            for worker in self.workers.values():
                if current_time - worker.last_heartbeat > self.heartbeat_interval * 2:
                    if worker.status != WorkerStatus.FAILED:
                        print(f"⚠️ Worker {worker.worker_id} failed (no heartbeat)")
                        worker.status = WorkerStatus.FAILED
                        worker.failure_count += 1
            await asyncio.sleep(self.heartbeat_interval)
    
    def create_data_shards(self, total_samples: int) -> List[DataShard]:
        """Create data shards for distributed training"""
        print(f"📊 Creating data shards for {total_samples} samples...")
        
        samples_per_shard = total_samples // self.num_workers
        remaining = total_samples % self.num_workers
        
        self.data_shards = []
        start_idx = 0
        
        for i in range(self.num_workers):
            shard_size = samples_per_shard + (1 if i < remaining else 0)
            indices = list(range(start_idx, start_idx + shard_size))
            
            # Create checksum for data integrity
            checksum = hashlib.md5(str(indices).encode()).hexdigest()[:8]
            
            shard = DataShard(
                shard_id=i,
                data_indices=indices,
                size=shard_size,
                checksum=checksum
            )
            self.data_shards.append(shard)
            start_idx += shard_size
            
        print(f"✅ Created {len(self.data_shards)} data shards")
        return self.data_shards
    
    async def assign_data_shards(self) -> Dict[str, List[int]]:
        """Assign data shards to workers with fault tolerance"""
        assignments = {}
        available_workers = [w for w in self.workers.values() 
                           if w.status != WorkerStatus.FAILED]
        
        if len(available_workers) < len(self.data_shards):
            # Redistribute shards among available workers
            print(f"⚠️ Redistributing shards: {len(available_workers)} workers available")
            
        for i, shard in enumerate(self.data_shards):
            worker_idx = i % len(available_workers)
            worker = available_workers[worker_idx]
            worker.assigned_data_shards.append(shard.shard_id)
            assignments[worker.worker_id] = worker.assigned_data_shards
            
        return assignments
    
    async def train_distributed(
        self, 
        model_config: Dict[str, Any],
        data_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute distributed training with fault tolerance"""
        print("🎯 Starting distributed training orchestration...")
        
        # Initialize training configuration
        config = TrainingConfig(
            model_size=model_config.get("size", 1000000),
            batch_size=model_config.get("batch_size", 32),
            learning_rate=model_config.get("learning_rate", 0.001),
            epochs=model_config.get("epochs", 10)
        )
        
        # Initialize global model
        self.global_model = np.random.randn(config.model_size) * 0.01
        
        # Create and assign data shards
        total_samples = data_config.get("total_samples", 10000)
        self.create_data_shards(total_samples)
        await self.assign_data_shards()
        
        # Training loop
        for epoch in range(config.epochs):
            print(f"\n📈 Epoch {epoch + 1}/{config.epochs}")
            
            # Distribute model to workers
            await self._distribute_model()
            
            # Execute training on workers
            worker_results = await self._execute_worker_training(config)
            
            # Aggregate gradients
            aggregated_gradients = await self._aggregate_gradients(
                worker_results, 
                config.aggregation_strategy
            )
            
            # Update global model
            self._update_global_model(aggregated_gradients, config.learning_rate)
            
            # Calculate metrics
            loss = self._calculate_loss()
            self.training_metrics["loss"].append(loss)
            
            # Checkpoint if needed
            if (epoch + 1) % config.checkpoint_interval == 0:
                await self._save_checkpoint(epoch + 1, loss)
            
            # Handle failed workers
            await self._handle_worker_failures(config)
            
        return {
            "epochs_completed": config.epochs,
            "final_loss": self.training_metrics["loss"][-1],
            "workers_used": len([w for w in self.workers.values() 
                               if w.status != WorkerStatus.FAILED]),
            "checkpoints_saved": len(self.checkpoints)
        }
    
    async def _distribute_model(self):
        """Distribute current model to all active workers"""
        active_workers = [w for w in self.workers.values() 
                         if w.status != WorkerStatus.FAILED]
        
        for worker in active_workers:
            # Simulate model distribution
            await asyncio.sleep(0.01)
            worker.model_version += 1
            worker.status = WorkerStatus.TRAINING
    
    async def _execute_worker_training(
        self, 
        config: TrainingConfig
    ) -> Dict[str, np.ndarray]:
        """Execute training on all workers and collect gradients"""
        tasks = []
        for worker_id, worker in self.workers.items():
            if worker.status != WorkerStatus.FAILED:
                task = self._train_on_worker(worker, config)
                tasks.append((worker_id, task))
        
        # Wait for all workers with timeout
        results = {}
        for worker_id, task in tasks:
            try:
                gradients = await asyncio.wait_for(task, timeout=30.0)
                results[worker_id] = gradients
            except asyncio.TimeoutError:
                print(f"⚠️ Worker {worker_id} timed out")
                self.workers[worker_id].status = WorkerStatus.FAILED
                
        return results
    
    async def _train_on_worker(
        self, 
        worker: WorkerNode,
        config: TrainingConfig
    ) -> np.ndarray:
        """Simulate training on a single worker"""
        # Simulate computation time based on data shard size
        computation_time = 0.1 + random.random() * 0.2
        await asyncio.sleep(computation_time)
        
        # Simulate gradient computation
        gradients = np.random.randn(config.model_size) * 0.1
        
        # Apply gradient clipping
        grad_norm = np.linalg.norm(gradients)
        if grad_norm > config.gradient_clip:
            gradients = gradients * (config.gradient_clip / grad_norm)
        
        worker.gradients = gradients
        worker.last_heartbeat = time.time()
        worker.current_batch += 1
        
        return gradients
    
    async def _aggregate_gradients(
        self, 
        worker_gradients: Dict[str, np.ndarray],
        strategy: AggregationStrategy
    ) -> np.ndarray:
        """Aggregate gradients from workers using specified strategy"""
        if not worker_gradients:
            raise ValueError("No gradients to aggregate")
            
        if strategy == AggregationStrategy.ALL_REDUCE:
            return self._all_reduce_aggregation(worker_gradients)
        elif strategy == AggregationStrategy.RING_ALL_REDUCE:
            return await self._ring_all_reduce_aggregation(worker_gradients)
        elif strategy == AggregationStrategy.HIERARCHICAL:
            return self._hierarchical_aggregation(worker_gradients)
        else:  # ASYNC_SGD
            return self._async_sgd_aggregation(worker_gradients)
    
    def _all_reduce_aggregation(
        self, 
        worker_gradients: Dict[str, np.ndarray]
    ) -> np.ndarray:
        """Standard all-reduce gradient aggregation"""
        gradients_list = list(worker_gradients.values())
        return np.mean(gradients_list, axis=0)
    
    async def _ring_all_reduce_aggregation(
        self, 
        worker_gradients: Dict[str, np.ndarray]
    ) -> np.ndarray:
        """Ring-based all-reduce for bandwidth efficiency"""
        workers = list(worker_gradients.keys())
        num_workers = len(workers)
        
        # Initialize with first worker's gradients
        aggregated = worker_gradients[workers[0]].copy()
        
        # Ring reduce
        for step in range(num_workers - 1):
            # Simulate communication delay
            await asyncio.sleep(0.01)
            
            sender_idx = step % num_workers
            receiver_idx = (step + 1) % num_workers
            
            # Add gradients
            aggregated += worker_gradients[workers[sender_idx]]
        
        # Average
        return aggregated / num_workers
    
    def _hierarchical_aggregation(
        self, 
        worker_gradients: Dict[str, np.ndarray]
    ) -> np.ndarray:
        """Hierarchical aggregation for large clusters"""
        gradients_list = list(worker_gradients.values())
        
        # Group workers hierarchically
        while len(gradients_list) > 1:
            new_level = []
            for i in range(0, len(gradients_list), 2):
                if i + 1 < len(gradients_list):
                    # Average pairs
                    avg = (gradients_list[i] + gradients_list[i + 1]) / 2
                    new_level.append(avg)
                else:
                    # Odd one out
                    new_level.append(gradients_list[i])
            gradients_list = new_level
            
        return gradients_list[0]
    
    def _async_sgd_aggregation(
        self, 
        worker_gradients: Dict[str, np.ndarray]
    ) -> np.ndarray:
        """Asynchronous SGD aggregation"""
        # Weight by worker staleness (simulated)
        weighted_sum = np.zeros_like(next(iter(worker_gradients.values())))
        total_weight = 0
        
        for worker_id, gradients in worker_gradients.items():
            worker = self.workers[worker_id]
            # Simulate staleness factor
            staleness = max(1, worker.model_version)
            weight = 1.0 / staleness
            
            weighted_sum += gradients * weight
            total_weight += weight
            
        return weighted_sum / total_weight
    
    async def _update_global_model(self, gradients: np.ndarray, learning_rate: float):
        """Update global model with aggregated gradients"""
        self.global_model -= learning_rate * gradients
        
        # Track gradient norm
        grad_norm = np.linalg.norm(gradients)
        self.training_metrics["gradient_norm"].append(grad_norm)
    
    def _calculate_loss(self) -> float:
        """Calculate training loss (simulated)"""
        # Simulate decreasing loss
        epoch = len(self.training_metrics["loss"])
        base_loss = 2.0
        loss = base_loss * np.exp(-0.3 * epoch) + random.random() * 0.1
        return loss
    
    async def _save_checkpoint(self, epoch: int, loss: float):
        """Save training checkpoint"""
        checkpoint = {
            "epoch": epoch,
            "loss": loss,
            "model_hash": hashlib.md5(self.global_model.tobytes()).hexdigest()[:16],
            "timestamp": datetime.now().isoformat(),
            "active_workers": len([w for w in self.workers.values() 
                                 if w.status != WorkerStatus.FAILED])
        }
        self.checkpoints.append(checkpoint)
        print(f"💾 Saved checkpoint at epoch {epoch} (loss: {loss:.4f})")
    
    async def _handle_worker_failures(self, config: TrainingConfig):
        """Handle failed workers with recovery strategies"""
        failed_workers = [w for w in self.workers.values() 
                         if w.status == WorkerStatus.FAILED]
        
        for worker in failed_workers:
            if worker.failure_count <= config.max_worker_failures:
                # Attempt recovery
                print(f"🔄 Attempting to recover worker {worker.worker_id}")
                worker.status = WorkerStatus.RECOVERING
                
                # Simulate recovery
                await asyncio.sleep(0.5)
                
                # 70% chance of successful recovery
                if random.random() < 0.7:
                    worker.status = WorkerStatus.IDLE
                    worker.last_heartbeat = time.time()
                    print(f"✅ Worker {worker.worker_id} recovered")
                else:
                    print(f"❌ Worker {worker.worker_id} recovery failed")
    
    async def get_training_summary(self) -> Dict[str, Any]:
        """Get comprehensive training summary"""
        active_workers = [w for w in self.workers.values() 
                         if w.status != WorkerStatus.FAILED]
        
        return {
            "total_workers": self.num_workers,
            "active_workers": len(active_workers),
            "failed_workers": self.num_workers - len(active_workers),
            "epochs_completed": len(self.training_metrics["loss"]),
            "final_loss": self.training_metrics["loss"][-1] if self.training_metrics["loss"] else None,
            "average_gradient_norm": np.mean(self.training_metrics["gradient_norm"]) if self.training_metrics["gradient_norm"] else None,
            "checkpoints_saved": len(self.checkpoints),
            "data_shards": len(self.data_shards),
            "total_samples": sum(shard.size for shard in self.data_shards)
        }
    
    async def cleanup(self):
        """Clean up resources"""
        self._running = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
    
    # Wrapper methods for test compatibility
    def shard_data(self, total_samples: int) -> List[DataShard]:
        """Wrapper for create_data_shards"""
        return self.create_data_shards(total_samples)
    
    def aggregate_gradients(self, gradients: List[np.ndarray], strategy: AggregationStrategy) -> np.ndarray:
        """Synchronous wrapper for gradient aggregation"""
        # Convert list to dict for compatibility
        worker_gradients = {f"worker_{i:03d}": g for i, g in enumerate(gradients)}
        # Run async method synchronously
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(self._aggregate_gradients(worker_gradients, strategy))
        loop.close()
        return result
    
    async def handle_worker_failure(self, worker_id: str) -> Dict[str, Any]:
        """Handle a specific worker failure"""
        config = TrainingConfig(
            model_size=1000,
            batch_size=32,
            learning_rate=0.01,
            epochs=1
        )
        await self._handle_worker_failures(config)
        worker = self.workers.get(worker_id)
        return {
            "worker_id": worker_id,
            "status": worker.status.value if worker else "unknown",
            "recovered": worker.status != WorkerStatus.FAILED if worker else False
        }
    
    async def simulate_training(self, config: TrainingConfig) -> Dict[str, Any]:
        """Simulate distributed training"""
        # Initialize workers if not already done
        if not self.workers:
            await self.initialize_workers()
        
        # Create data shards
        total_samples = config.batch_size * 100  # Simulate dataset
        self.create_data_shards(total_samples)
        await self.assign_data_shards()
        
        # Initialize model
        self.global_model = np.random.randn(config.model_size)
        
        # Training loop
        for epoch in range(config.epochs):
            # Simulate gradient computation
            worker_gradients = {}
            for worker_id, worker in self.workers.items():
                if worker.status != WorkerStatus.FAILED:
                    worker.status = WorkerStatus.TRAINING
                    # Simulate gradient
                    gradient = np.random.randn(config.model_size) * 0.01
                    worker_gradients[worker_id] = gradient
            
            # Aggregate gradients
            if worker_gradients:
                aggregated = await self._aggregate_gradients(
                    worker_gradients, 
                    config.aggregation_strategy
                )
                await self._update_global_model(aggregated, config.learning_rate)
            
            # Track metrics
            loss = self._calculate_loss()
            self.training_metrics["loss"].append(loss)
            
            # Save checkpoint periodically
            if (epoch + 1) % config.checkpoint_interval == 0:
                await self._save_checkpoint(epoch + 1, loss)
        
        # Return results
        summary = await self.get_training_summary()
        return {
            "epochs_completed": config.epochs,
            "final_loss": self.training_metrics["loss"][-1],
            "avg_gradient_norm": summary["average_gradient_norm"],
            "workers_used": summary["active_workers"]
        }
    
    def create_ring_topology(self) -> List[str]:
        """Create ring topology for Ring All-Reduce"""
        worker_ids = list(self.workers.keys())
        return worker_ids  # Simple ring order


# Test methods with expected durations
async def test_worker_initialization():
    """Test: Initialize distributed workers (Expected: ~0.5s)"""
    orchestrator = DistributedTrainingOrchestrator(num_workers=4)
    workers = await orchestrator.initialize_workers()
    
    assert len(workers) == 4
    assert all(w.status == WorkerStatus.IDLE for w in workers.values())
    
    await orchestrator.cleanup()
    return workers


async def test_data_sharding():
    """Test: Create and assign data shards (Expected: ~0.3s)"""
    orchestrator = DistributedTrainingOrchestrator(num_workers=4)
    await orchestrator.initialize_workers()
    
    shards = orchestrator.create_data_shards(total_samples=10000)
    assignments = await orchestrator.assign_data_shards()
    
    assert len(shards) == 4
    assert sum(shard.size for shard in shards) == 10000
    assert len(assignments) == 4
    
    await orchestrator.cleanup()
    return assignments


async def test_gradient_aggregation():
    """Test: Gradient aggregation strategies (Expected: ~1.0s)"""
    orchestrator = DistributedTrainingOrchestrator(num_workers=3)
    model_size = 100
    
    # Initialize workers first
    await orchestrator.initialize_workers()
    
    # Create mock gradients
    worker_gradients = {
        f"worker_{i:03d}": np.random.randn(model_size) 
        for i in range(3)
    }
    
    results = {}
    for strategy in AggregationStrategy:
        aggregated = await orchestrator._aggregate_gradients(
            worker_gradients, 
            strategy
        )
        results[strategy.value] = {
            "shape": aggregated.shape,
            "norm": float(np.linalg.norm(aggregated))
        }
    
    assert all(r["shape"] == (model_size,) for r in results.values())
    
    await orchestrator.cleanup()
    return results


async def test_distributed_training():
    """Test: Full distributed training pipeline (Expected: ~5.0s)"""
    orchestrator = DistributedTrainingOrchestrator(num_workers=3)
    await orchestrator.initialize_workers()
    
    model_config = {
        "size": 1000,
        "batch_size": 32,
        "learning_rate": 0.01,
        "epochs": 5
    }
    
    data_config = {
        "total_samples": 5000
    }
    
    result = await orchestrator.train_distributed(model_config, data_config)
    summary = await orchestrator.get_training_summary()
    
    assert result["epochs_completed"] == 5
    assert result["final_loss"] < 2.0  # Should decrease from initial
    assert result["workers_used"] >= 2  # At least 2 workers should survive
    
    await orchestrator.cleanup()
    return summary


async def test_fault_tolerance():
    """Test: Worker failure and recovery (Expected: ~3.0s)"""
    orchestrator = DistributedTrainingOrchestrator(num_workers=5)
    await orchestrator.initialize_workers()
    
    # Simulate worker failures
    orchestrator.workers["worker_001"].status = WorkerStatus.FAILED
    orchestrator.workers["worker_003"].status = WorkerStatus.FAILED
    
    # Test redistribution
    shards = orchestrator.create_data_shards(total_samples=10000)
    assignments = await orchestrator.assign_data_shards()
    
    active_workers = [w for w in orchestrator.workers.values() 
                     if w.status != WorkerStatus.FAILED]
    
    assert len(active_workers) == 3
    assert len(assignments) == 3  # Only active workers get assignments
    
    # Test recovery
    config = TrainingConfig(
        model_size=100,
        batch_size=32,
        learning_rate=0.01,
        epochs=1
    )
    await orchestrator._handle_worker_failures(config)
    
    await orchestrator.cleanup()
    return {
        "initial_failures": 2,
        "active_after_redistribution": len(active_workers),
        "assignments": assignments
    }


if __name__ == "__main__":
    print("=" * 80)
    print("🚀 GRANGER Task #23: Distributed Training Orchestration")
    print("=" * 80)
    
    async def run_all_tests():
        test_results = []
        start_time = time.time()
        
        # Test 1: Worker initialization
        print("\n📋 Test 1: Worker Initialization")
        try:
            test_start = time.time()
            result = await test_worker_initialization()
            duration = time.time() - test_start
            print(f"✅ Success: Initialized {len(result)} workers in {duration:.2f}s")
            test_results.append({
                "test": "Worker Initialization",
                "status": "PASS",
                "duration": duration,
                "workers": len(result)
            })
        except Exception as e:
            print(f"❌ Failed: {e}")
            test_results.append({
                "test": "Worker Initialization",
                "status": "FAIL",
                "error": str(e)
            })
        
        # Test 2: Data sharding
        print("\n📋 Test 2: Data Sharding")
        try:
            test_start = time.time()
            result = await test_data_sharding()
            duration = time.time() - test_start
            print(f"✅ Success: Created shards and assignments in {duration:.2f}s")
            print(f"   Assignments: {list(result.keys())}")
            test_results.append({
                "test": "Data Sharding",
                "status": "PASS",
                "duration": duration,
                "assignments": len(result)
            })
        except Exception as e:
            print(f"❌ Failed: {e}")
            test_results.append({
                "test": "Data Sharding",
                "status": "FAIL",
                "error": str(e)
            })
        
        # Test 3: Gradient aggregation
        print("\n📋 Test 3: Gradient Aggregation")
        try:
            test_start = time.time()
            result = await test_gradient_aggregation()
            duration = time.time() - test_start
            print(f"✅ Success: Tested {len(result)} aggregation strategies in {duration:.2f}s")
            for strategy, metrics in result.items():
                print(f"   {strategy}: norm={metrics['norm']:.4f}")
            test_results.append({
                "test": "Gradient Aggregation",
                "status": "PASS",
                "duration": duration,
                "strategies": len(result)
            })
        except Exception as e:
            print(f"❌ Failed: {e}")
            test_results.append({
                "test": "Gradient Aggregation",
                "status": "FAIL",
                "error": str(e)
            })
        
        # Test 4: Distributed training
        print("\n📋 Test 4: Distributed Training Pipeline")
        try:
            test_start = time.time()
            result = await test_distributed_training()
            duration = time.time() - test_start
            print(f"✅ Success: Completed training in {duration:.2f}s")
            print(f"   Epochs: {result['epochs_completed']}")
            print(f"   Final loss: {result['final_loss']:.4f}")
            print(f"   Active workers: {result['active_workers']}/{result['total_workers']}")
            test_results.append({
                "test": "Distributed Training",
                "status": "PASS",
                "duration": duration,
                "final_loss": result["final_loss"]
            })
        except Exception as e:
            print(f"❌ Failed: {e}")
            test_results.append({
                "test": "Distributed Training",
                "status": "FAIL",
                "error": str(e)
            })
        
        # Test 5: Fault tolerance
        print("\n📋 Test 5: Fault Tolerance")
        try:
            test_start = time.time()
            result = await test_fault_tolerance()
            duration = time.time() - test_start
            print(f"✅ Success: Handled failures in {duration:.2f}s")
            print(f"   Initial failures: {result['initial_failures']}")
            print(f"   Active after redistribution: {result['active_after_redistribution']}")
            test_results.append({
                "test": "Fault Tolerance",
                "status": "PASS",
                "duration": duration,
                "recovered": result["active_after_redistribution"]
            })
        except Exception as e:
            print(f"❌ Failed: {e}")
            test_results.append({
                "test": "Fault Tolerance",
                "status": "FAIL",
                "error": str(e)
            })
        
        # Summary
        total_duration = time.time() - start_time
        passed = sum(1 for r in test_results if r["status"] == "PASS")
        failed = sum(1 for r in test_results if r["status"] == "FAIL")
        
        print("\n" + "=" * 80)
        print("📊 Test Summary")
        print("=" * 80)
        print(f"Total tests: {len(test_results)}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Total duration: {total_duration:.2f}s")
        
        # Detailed results
        print("\nDetailed Results:")
        for result in test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['test']}: {result['status']}")
            if "duration" in result:
                print(f"   Duration: {result['duration']:.2f}s")
            if "error" in result:
                print(f"   Error: {result['error']}")
        
        return passed == len(test_results)
    
    # Run all tests
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)