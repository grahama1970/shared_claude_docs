#!/usr/bin/env python3
"""
Module: unsloth_fixes.py
Description: Unsloth-specific bug fixes implementation

External Dependencies:
- granger_common: Our standardized components
- torch: PyTorch deep learning framework
"""

from pathlib import Path
import re

def apply_unsloth_fixes():
    """Apply all Unsloth-specific fixes."""
    print("\n🚀 Applying Unsloth fixes...")
    
    # 1. Fix memory leaks during training
    memory_leak_fixes_code = '''
import gc
import torch
from typing import Optional, Dict, Any
import psutil
import os

class MemoryManager:
    """Manage GPU and system memory during training."""
    
    def __init__(self, threshold_percent: float = 80.0):
        self.threshold_percent = threshold_percent
        self.initial_memory = self._get_memory_usage()
        self.cleanup_frequency = 100  # Clean every N batches
        
    def _get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage."""
        memory = {
            "system_percent": psutil.virtual_memory().percent,
            "system_used_gb": psutil.virtual_memory().used / (1024**3)
        }
        
        if torch.cuda.is_available():
            memory["gpu_allocated_gb"] = torch.cuda.memory_allocated() / (1024**3)
            memory["gpu_reserved_gb"] = torch.cuda.memory_reserved() / (1024**3)
            memory["gpu_percent"] = (torch.cuda.memory_allocated() / torch.cuda.max_memory_allocated()) * 100
            
        return memory
    
    def check_memory(self) -> bool:
        """Check if memory usage is above threshold."""
        current = self._get_memory_usage()
        
        if current["system_percent"] > self.threshold_percent:
            return True
            
        if torch.cuda.is_available() and current.get("gpu_percent", 0) > self.threshold_percent:
            return True
            
        return False
    
    def cleanup(self, force: bool = False):
        """Perform memory cleanup."""
        if not force and not self.check_memory():
            return
            
        # Clear Python garbage
        gc.collect()
        
        # Clear CUDA cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        
        # Log memory after cleanup
        after = self._get_memory_usage()
        logger.info(f"Memory cleanup: System {after['system_percent']:.1f}%, GPU {after.get('gpu_percent', 0):.1f}%")

class GradientAccumulator:
    """Efficient gradient accumulation with memory management."""
    
    def __init__(self, accumulation_steps: int = 4):
        self.accumulation_steps = accumulation_steps
        self.step_count = 0
        
    def should_update(self) -> bool:
        """Check if we should update weights."""
        self.step_count += 1
        return self.step_count % self.accumulation_steps == 0
    
    def scale_loss(self, loss: torch.Tensor) -> torch.Tensor:
        """Scale loss for gradient accumulation."""
        return loss / self.accumulation_steps
        
    def reset(self):
        """Reset accumulation counter."""
        self.step_count = 0

# Enhanced training loop with memory management
def train_with_memory_management(
    model, 
    train_loader, 
    optimizer, 
    epochs: int,
    memory_manager: Optional[MemoryManager] = None
):
    """Training loop with automatic memory management."""
    
    if memory_manager is None:
        memory_manager = MemoryManager()
    
    accumulator = GradientAccumulator(accumulation_steps=4)
    
    for epoch in range(epochs):
        for batch_idx, batch in enumerate(train_loader):
            # Forward pass
            outputs = model(batch["input_ids"])
            loss = compute_loss(outputs, batch["labels"])
            
            # Scale loss for accumulation
            scaled_loss = accumulator.scale_loss(loss)
            scaled_loss.backward()
            
            # Update weights after accumulation
            if accumulator.should_update():
                optimizer.step()
                optimizer.zero_grad()
            
            # Memory cleanup
            if batch_idx % memory_manager.cleanup_frequency == 0:
                memory_manager.cleanup()
            
            # Delete intermediate variables
            del outputs, loss, scaled_loss
            
            # Force cleanup on high memory
            if memory_manager.check_memory():
                logger.warning("High memory usage detected, forcing cleanup")
                memory_manager.cleanup(force=True)
'''
    
    # 2. Fix checkpoint loading/saving with memory efficiency
    checkpoint_fixes_code = '''
import torch
from pathlib import Path
from typing import Dict, Any, Optional
import shutil

class CheckpointManager:
    """Manage model checkpoints efficiently."""
    
    def __init__(self, checkpoint_dir: str, max_checkpoints: int = 3):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.max_checkpoints = max_checkpoints
        
    def save_checkpoint(
        self,
        model,
        optimizer,
        epoch: int,
        loss: float,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        """Save checkpoint with memory efficiency."""
        checkpoint_path = self.checkpoint_dir / f"checkpoint_epoch_{epoch}.pt"
        
        # Prepare checkpoint data
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": loss,
            "additional_info": additional_info or {}
        }
        
        # Save with memory mapping for large models
        torch.save(checkpoint, checkpoint_path, _use_new_zipfile_serialization=True)
        
        # Manage checkpoint history
        self._cleanup_old_checkpoints()
        
        logger.info(f"Checkpoint saved: {checkpoint_path}")
        
    def load_checkpoint(self, checkpoint_path: str, model, optimizer=None, map_location=None):
        """Load checkpoint with memory efficiency."""
        if map_location is None:
            map_location = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load with memory mapping
        checkpoint = torch.load(
            checkpoint_path,
            map_location=map_location,
            weights_only=False
        )
        
        # Load model state
        model.load_state_dict(checkpoint["model_state_dict"])
        
        # Load optimizer state if provided
        if optimizer is not None and "optimizer_state_dict" in checkpoint:
            optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        
        # Clear memory after loading
        del checkpoint
        gc.collect()
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        return model, optimizer
    
    def _cleanup_old_checkpoints(self):
        """Remove old checkpoints to save disk space."""
        checkpoints = sorted(
            self.checkpoint_dir.glob("checkpoint_epoch_*.pt"),
            key=lambda p: p.stat().st_mtime
        )
        
        # Keep only the most recent checkpoints
        if len(checkpoints) > self.max_checkpoints:
            for checkpoint in checkpoints[:-self.max_checkpoints]:
                checkpoint.unlink()
                logger.info(f"Removed old checkpoint: {checkpoint}")
'''
    
    # 3. Fix mixed precision training issues
    mixed_precision_fixes_code = '''
from torch.cuda.amp import GradScaler, autocast
import torch.nn as nn

class MixedPrecisionTrainer:
    """Handle mixed precision training correctly."""
    
    def __init__(self, model, optimizer, loss_scale: str = "dynamic"):
        self.model = model
        self.optimizer = optimizer
        self.scaler = GradScaler(init_scale=2**16, growth_interval=2000)
        
        # Ensure model is in correct dtype
        self._prepare_model()
        
    def _prepare_model(self):
        """Prepare model for mixed precision."""
        # Keep batch norm in float32
        def apply_float32_bn(module):
            if isinstance(module, nn.BatchNorm2d):
                module.float()
        
        self.model.apply(apply_float32_bn)
        
    def train_step(self, batch: Dict[str, torch.Tensor]) -> float:
        """Single training step with mixed precision."""
        self.optimizer.zero_grad()
        
        # Use autocast for forward pass
        with autocast():
            outputs = self.model(**batch)
            loss = outputs.loss if hasattr(outputs, 'loss') else outputs
        
        # Scale loss and backward
        self.scaler.scale(loss).backward()
        
        # Unscale gradients for clipping
        self.scaler.unscale_(self.optimizer)
        
        # Clip gradients to prevent instability
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        
        # Step optimizer with scaler
        self.scaler.step(self.optimizer)
        self.scaler.update()
        
        return loss.item()
    
    def save_scaler_state(self) -> dict:
        """Save scaler state for resuming."""
        return self.scaler.state_dict()
    
    def load_scaler_state(self, state_dict: dict):
        """Load scaler state."""
        self.scaler.load_state_dict(state_dict)
'''
    
    # 4. Fix data loading bottlenecks
    data_loading_fixes_code = '''
from torch.utils.data import DataLoader, Dataset
import torch.multiprocessing as mp
from typing import Iterator

class EfficientDataLoader:
    """Optimized data loading for training."""
    
    def __init__(
        self,
        dataset: Dataset,
        batch_size: int,
        num_workers: int = 4,
        pin_memory: bool = True,
        prefetch_factor: int = 2
    ):
        # Set multiprocessing start method
        try:
            mp.set_start_method('spawn', force=True)
        except RuntimeError:
            pass
        
        self.dataloader = DataLoader(
            dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            pin_memory=pin_memory and torch.cuda.is_available(),
            prefetch_factor=prefetch_factor,
            persistent_workers=num_workers > 0,
            drop_last=True,  # Avoid variable batch sizes
            shuffle=True
        )
        
    def __iter__(self) -> Iterator:
        """Iterate with memory efficiency."""
        for batch in self.dataloader:
            # Move to GPU if available
            if torch.cuda.is_available():
                batch = {k: v.cuda(non_blocking=True) if isinstance(v, torch.Tensor) else v 
                        for k, v in batch.items()}
            yield batch

class StreamingDataset(Dataset):
    """Dataset that streams data to avoid loading everything in memory."""
    
    def __init__(self, data_path: str, chunk_size: int = 1000):
        self.data_path = Path(data_path)
        self.chunk_size = chunk_size
        self._initialize_index()
        
    def _initialize_index(self):
        """Build index of data positions for random access."""
        self.index = []
        
        with open(self.data_path, 'r') as f:
            position = 0
            for line_no, line in enumerate(f):
                if line_no % self.chunk_size == 0:
                    self.index.append(position)
                position = f.tell()
        
        self.total_lines = line_no + 1
        
    def __len__(self):
        return self.total_lines
        
    def __getitem__(self, idx):
        """Get item by seeking to position."""
        chunk_idx = idx // self.chunk_size
        line_offset = idx % self.chunk_size
        
        with open(self.data_path, 'r') as f:
            f.seek(self.index[chunk_idx])
            
            # Skip to the target line
            for _ in range(line_offset):
                f.readline()
            
            # Read the target line
            line = f.readline().strip()
            
        return self._process_line(line)
    
    def _process_line(self, line: str) -> dict:
        """Process a single line of data."""
        # Implement your processing logic here
        return {"text": line}
'''
    
    # 5. Fix distributed training synchronization
    distributed_fixes_code = '''
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
import os

class DistributedTrainingManager:
    """Manage distributed training properly."""
    
    def __init__(self):
        self.is_distributed = False
        self.rank = 0
        self.world_size = 1
        
    def setup_distributed(self):
        """Initialize distributed training."""
        if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
            self.rank = int(os.environ["RANK"])
            self.world_size = int(os.environ["WORLD_SIZE"])
            self.is_distributed = True
            
            # Initialize process group
            dist.init_process_group(
                backend="nccl",
                init_method="env://",
                world_size=self.world_size,
                rank=self.rank
            )
            
            # Set device
            torch.cuda.set_device(self.rank)
            
            logger.info(f"Distributed training: rank {self.rank}/{self.world_size}")
    
    def wrap_model(self, model):
        """Wrap model for distributed training."""
        if self.is_distributed:
            model = model.cuda(self.rank)
            model = DDP(
                model,
                device_ids=[self.rank],
                output_device=self.rank,
                find_unused_parameters=False,
                gradient_as_bucket_view=True  # Memory optimization
            )
        return model
    
    def all_reduce_metrics(self, metrics: dict) -> dict:
        """Aggregate metrics across all processes."""
        if not self.is_distributed:
            return metrics
        
        reduced_metrics = {}
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                tensor = torch.tensor(value).cuda(self.rank)
                dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
                reduced_metrics[key] = tensor.item() / self.world_size
            else:
                reduced_metrics[key] = value
        
        return reduced_metrics
    
    def cleanup(self):
        """Clean up distributed training."""
        if self.is_distributed:
            dist.destroy_process_group()
'''
    
    print("✅ Unsloth fixes defined - ready for implementation")
    
    # Create implementation guide
    implementation_guide = '''
# Unsloth Module Fix Implementation Guide

## 1. Memory Management (CRITICAL)
Location: src/unsloth/training/memory_manager.py
- Implement MemoryManager class
- Set cleanup threshold at 80% usage
- Clean every 100 batches
- Force cleanup on high memory
- Use gradient accumulation

## 2. Checkpoint Management (HIGH)
Location: src/unsloth/checkpointing/manager.py
- Implement CheckpointManager
- Keep only 3 most recent checkpoints
- Use memory-mapped loading
- Clear memory after loading
- Save with compression

## 3. Mixed Precision (HIGH)
Location: src/unsloth/training/mixed_precision.py
- Use torch.cuda.amp properly
- Keep BatchNorm in float32
- Implement gradient clipping
- Save/load scaler state
- Handle loss scaling

## 4. Data Loading (MEDIUM)
Location: src/unsloth/data/loader.py
- Use persistent workers
- Enable pin_memory for GPU
- Implement streaming dataset
- Use non-blocking transfers
- Optimize batch size

## 5. Distributed Training (MEDIUM)
Location: src/unsloth/distributed/manager.py
- Setup NCCL backend
- Use gradient bucketing
- Implement metric reduction
- Handle process cleanup
- Sync batch normalization

## Configuration
```yaml
training:
  batch_size: 16
  gradient_accumulation: 4
  mixed_precision: true
  
  memory:
    cleanup_threshold: 80
    cleanup_frequency: 100
    
  checkpoints:
    save_dir: "./checkpoints"
    max_to_keep: 3
    save_frequency: 1000
    
  data:
    num_workers: 4
    prefetch_factor: 2
    pin_memory: true
    
  distributed:
    backend: "nccl"
    find_unused_parameters: false
```

## Best Practices
1. Monitor GPU memory usage continuously
2. Use gradient checkpointing for large models
3. Clear intermediate activations
4. Batch similar-length sequences
5. Profile training to find bottlenecks

## Testing
1. Memory test: Train for 1000 steps, monitor usage
2. Checkpoint test: Save/load with 7B parameter model
3. Mixed precision: Verify no NaN losses
4. Data loading: Measure GPU utilization
5. Distributed: Test with 4 GPUs

## Common Issues
- OOM errors: Reduce batch size or use gradient accumulation
- Slow training: Check data loading bottlenecks
- NaN losses: Reduce learning rate or disable mixed precision
- Checkpoint corruption: Use atomic writes
- Distributed hangs: Check NCCL timeout settings
'''
    
    # Save implementation guide
    guide_path = Path("/home/graham/workspace/shared_claude_docs/module_specific_fixes/unsloth_implementation_guide.md")
    guide_path.parent.mkdir(exist_ok=True)
    guide_path.write_text(implementation_guide)
    print(f"📝 Implementation guide saved to: {guide_path}")


if __name__ == "__main__":
    apply_unsloth_fixes()