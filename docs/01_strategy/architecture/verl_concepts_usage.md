# Projects Using VERL-like Concepts

## Overview

VERL (Volcano Engine Reinforcement Learning for LLMs) is a framework for training LLMs using reinforcement learning techniques like RLHF. After analyzing the projects, here are the ones using similar concepts:

## Projects with VERL-like Features

### 1. ADVANCED-fine-tuning

**Location**: /home/graham/workspace/experiments/ADVANCED-fine-tuning/RL/

**VERL Concepts Used**:
- **GRPO (Group Relative Policy Optimization)** - Direct match with VERL support
  - train_unsloth_grpo.py
  - train_unsloth_grpo_arc.py
- **ORPO (Odds Ratio Preference Optimization)** - Preference-based training
  - train_unsloth_orpo.py
  - train_transformers_orpo.py
- **SFT (Supervised Fine-Tuning)** - Pre-training step before RL
  - train_unsloth_sft.py
  - train_transformers_sft.py
- **Unsloth Integration** - Efficient training framework

**Key Features**:
- Uses TRL (Transformers Reinforcement Learning) library
- Implements reward modeling for reasoning tasks (GSM8K, ARC)
- Batch inference capabilities
- Support for LoRA adapters

### 2. fine_tuning

**Location**: /home/graham/workspace/experiments/fine_tuning/

**VERL-related Aspects**:
- Focus on efficient fine-tuning using Unsloth
- Integration with RunPod for distributed training
- Phi-3.5 model fine-tuning notebooks

### 3. agent_tools

**Location**: /home/graham/workspace/experiments/agent_tools/

**VERL-related Aspects**:
- Contains references to LoRA training
- Has infrastructure for dataset formatting for fine-tuning

## Comparison with VERL

| Feature | VERL | ADVANCED-fine-tuning | Notes |
|---------|------|---------------------|-------|
| RLHF Support | Yes | Yes | Via GRPO/ORPO |
| PPO Algorithm | Yes | No | Uses GRPO instead |
| Multi-GPU Training | Yes | Yes | Via Unsloth |
| LoRA Support | Yes | Yes | Implemented |
| Reward Modeling | Yes | Yes | For math/reasoning |
| Flash Attention | Yes | Yes | Via Unsloth |
| VLM Support | Yes | No | Not found |

## Key Differences

1. **Algorithm Choice**: ADVANCED-fine-tuning uses GRPO/ORPO instead of PPO
2. **Framework**: Uses Unsloth + TRL instead of VERL custom framework
3. **Scale**: Appears focused on smaller-scale experiments vs VERL 70B+ support

## Recommendations

1. **Consider VERL Integration**: For larger scale training (>7B models)
2. **Leverage VERL PPO**: If PPO is needed for specific use cases
3. **Multi-modal RL**: VERL supports VLMs which could benefit projects like marker

## Conclusion

The ADVANCED-fine-tuning project is the primary user of VERL-like concepts in your ecosystem, implementing reinforcement learning techniques for LLM training. While it does not use VERL directly, it implements similar ideas using the TRL library and Unsloth for efficient training.
