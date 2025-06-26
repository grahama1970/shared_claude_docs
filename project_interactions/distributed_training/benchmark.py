
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Performance benchmarking for Distributed Training Orchestration
"""

import asyncio
import time
import statistics
from distributed_training_interaction import (
    DistributedTrainingOrchestrator,
    AggregationStrategy
)


async def benchmark_worker_scaling():
    """Benchmark training performance with different worker counts"""
    print("📊 Worker Scaling Benchmark")
    print("=" * 60)
    
    worker_counts = [2, 4, 8, 16, 32]
    results = []
    
    model_config = {
        "size": 100000,
        "batch_size": 64,
        "learning_rate": 0.01,
        "epochs": 5
    }
    
    data_config = {
        "total_samples": 50000
    }
    
    for num_workers in worker_counts:
        print(f"\n🔧 Testing with {num_workers} workers...")
        
        orchestrator = DistributedTrainingOrchestrator(num_workers=num_workers)
        await orchestrator.initialize_workers()
        
        start_time = time.time()
        result = await orchestrator.train_distributed(model_config, data_config)
        duration = time.time() - start_time
        
        throughput = (data_config["total_samples"] * model_config["epochs"]) / duration
        
        results.append({
            "workers": num_workers,
            "duration": duration,
            "throughput": throughput,
            "final_loss": result["final_loss"]
        })
        
        await orchestrator.cleanup()
    
    # Display results
    print("\n📈 Scaling Results:")
    print("-" * 60)
    print(f"{'Workers':<10} {'Duration (s)':<15} {'Throughput':<20} {'Final Loss':<15}")
    print("-" * 60)
    for r in results:
        print(f"{r['workers']:<10} {r['duration']:<15.2f} {r['throughput']:<20.0f} {r['final_loss']:<15.4f}")
    
    return results


async def benchmark_data_sizes():
    """Benchmark performance with different data sizes"""
    print("\n📊 Data Size Scaling Benchmark")
    print("=" * 60)
    
    data_sizes = [1000, 5000, 10000, 50000, 100000]
    results = []
    
    model_config = {
        "size": 50000,
        "batch_size": 128,
        "learning_rate": 0.01,
        "epochs": 3
    }
    
    for data_size in data_sizes:
        print(f"\n🔧 Testing with {data_size:,} samples...")
        
        orchestrator = DistributedTrainingOrchestrator(num_workers=8)
        await orchestrator.initialize_workers()
        
        data_config = {"total_samples": data_size}
        
        start_time = time.time()
        result = await orchestrator.train_distributed(model_config, data_config)
        duration = time.time() - start_time
        
        samples_per_second = (data_size * model_config["epochs"]) / duration
        
        results.append({
            "data_size": data_size,
            "duration": duration,
            "samples_per_second": samples_per_second,
            "final_loss": result["final_loss"]
        })
        
        await orchestrator.cleanup()
    
    # Display results
    print("\n📈 Data Scaling Results:")
    print("-" * 70)
    print(f"{'Data Size':<15} {'Duration (s)':<15} {'Samples/sec':<20} {'Final Loss':<15}")
    print("-" * 70)
    for r in results:
        print(f"{r['data_size']:<15,} {r['duration']:<15.2f} {r['samples_per_second']:<20,.0f} {r['final_loss']:<15.4f}")
    
    return results


async def benchmark_aggregation_strategies():
    """Benchmark different aggregation strategies"""
    print("\n📊 Aggregation Strategy Benchmark")
    print("=" * 60)
    
    strategies = list(AggregationStrategy)
    results = []
    
    model_config = {
        "size": 500000,
        "batch_size": 64,
        "learning_rate": 0.01,
        "epochs": 5
    }
    
    data_config = {
        "total_samples": 20000
    }
    
    # Run multiple iterations for each strategy
    iterations = 3
    
    for strategy in strategies:
        print(f"\n🔧 Testing {strategy.value} ({iterations} iterations)...")
        
        durations = []
        losses = []
        
        for i in range(iterations):
            orchestrator = DistributedTrainingOrchestrator(num_workers=8)
            await orchestrator.initialize_workers()
            
            config = model_config.copy()
            config["aggregation_strategy"] = strategy
            
            start_time = time.time()
            result = await orchestrator.train_distributed(config, data_config)
            duration = time.time() - start_time
            
            durations.append(duration)
            losses.append(result["final_loss"])
            
            await orchestrator.cleanup()
        
        avg_duration = statistics.mean(durations)
        std_duration = statistics.stdev(durations) if len(durations) > 1 else 0
        avg_loss = statistics.mean(losses)
        
        results.append({
            "strategy": strategy.value,
            "avg_duration": avg_duration,
            "std_duration": std_duration,
            "avg_loss": avg_loss
        })
    
    # Display results
    print("\n📈 Strategy Performance Results:")
    print("-" * 80)
    print(f"{'Strategy':<20} {'Avg Duration (s)':<18} {'Std Dev':<12} {'Avg Loss':<15}")
    print("-" * 80)
    for r in results:
        print(f"{r['strategy']:<20} {r['avg_duration']:<18.2f} {r['std_duration']:<12.3f} {r['avg_loss']:<15.4f}")
    
    return results


async def benchmark_fault_tolerance():
    """Benchmark performance impact of fault tolerance"""
    print("\n📊 Fault Tolerance Impact Benchmark")
    print("=" * 60)
    
    failure_rates = [0.0, 0.1, 0.2, 0.3, 0.5]
    results = []
    
    model_config = {
        "size": 100000,
        "batch_size": 64,
        "learning_rate": 0.01,
        "epochs": 5
    }
    
    data_config = {
        "total_samples": 20000
    }
    
    for failure_rate in failure_rates:
        print(f"\n🔧 Testing with {failure_rate*100:.0f}% failure rate...")
        
        orchestrator = DistributedTrainingOrchestrator(num_workers=10)
        await orchestrator.initialize_workers()
        
        # Simulate failures
        num_failures = int(orchestrator.num_workers * failure_rate)
        for i in range(num_failures):
            worker_id = f"worker_{i:03d}"
            orchestrator.workers[worker_id].status = orchestrator.workers[worker_id].status.__class__.FAILED
        
        start_time = time.time()
        result = await orchestrator.train_distributed(model_config, data_config)
        duration = time.time() - start_time
        
        summary = await orchestrator.get_training_summary()
        
        results.append({
            "failure_rate": failure_rate,
            "duration": duration,
            "active_workers": summary["active_workers"],
            "final_loss": result["final_loss"]
        })
        
        await orchestrator.cleanup()
    
    # Display results
    print("\n📈 Fault Tolerance Results:")
    print("-" * 70)
    print(f"{'Failure Rate':<15} {'Duration (s)':<15} {'Active Workers':<18} {'Final Loss':<15}")
    print("-" * 70)
    for r in results:
        print(f"{r['failure_rate']*100:>12.0f}% {r['duration']:<15.2f} {r['active_workers']:<18} {r['final_loss']:<15.4f}")
    
    return results


async def main():
    """Run all benchmarks"""
    print("🚀 Distributed Training Performance Benchmarks")
    print("=" * 60)
    
    # Run benchmarks
    worker_results = await benchmark_worker_scaling()
    data_results = await benchmark_data_sizes()
    strategy_results = await benchmark_aggregation_strategies()
    fault_results = await benchmark_fault_tolerance()
    
    print("\n✅ All benchmarks completed!")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 BENCHMARK SUMMARY")
    print("=" * 60)
    
    # Find optimal configurations
    optimal_workers = min(worker_results, key=lambda x: x["duration"])
    print(f"\n🏆 Optimal worker count: {optimal_workers['workers']} workers")
    print(f"   Duration: {optimal_workers['duration']:.2f}s")
    
    optimal_strategy = min(strategy_results, key=lambda x: x["avg_duration"])
    print(f"\n🏆 Fastest aggregation strategy: {optimal_strategy['strategy']}")
    print(f"   Avg duration: {optimal_strategy['avg_duration']:.2f}s ± {optimal_strategy['std_duration']:.3f}s")
    
    # Calculate scaling efficiency
    base_throughput = worker_results[0]["throughput"]
    for r in worker_results[1:]:
        efficiency = (r["throughput"] / base_throughput) / (r["workers"] / worker_results[0]["workers"])
        print(f"\n📈 Scaling efficiency ({r['workers']} workers): {efficiency:.1%}")


if __name__ == "__main__":
    asyncio.run(main())