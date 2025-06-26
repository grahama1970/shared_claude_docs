# RunPod Operations Manager

## Overview

RunPod Operations Manager (`runpod_ops`) is a Granger ecosystem component that provides intelligent GPU instance management for LLM training and inference with Docker deployment support and cost optimization.

## Status: ✅ Production Ready

Full RunPod API integration with dynamic GPU optimization, FSDP support, and Docker deployment capabilities.

## Architecture

Follows standard Granger 3-layer architecture:

```
runpod_ops/
├── core/           # Business logic
│   ├── runpod_manager.py      # Instance lifecycle management
│   ├── gpu_optimizer.py       # Dynamic GPU selection
│   ├── gpu_benchmarks.py      # Real-world performance data
│   ├── instance_optimizer.py  # Legacy optimizer
│   └── cost_calculator.py     # Cost estimation
├── cli/            # Command-line interface
│   ├── main.py               # CLI commands
│   ├── slash_handler.py      # Slash command support
│   └── unified_cli.py        # Granger integration
├── mcp/            # MCP server
│   └── server.py
├── handlers/       # Granger handlers
│   └── runpod_handler.py
└── docker/         # Docker images
    ├── base/       # SGLang inference
    └── finetune/   # Training environment
```

## Key Features

### 1. **Dynamic GPU Optimization**
- Selects GPU based on **total cost**, not just speed
- Uses real benchmarks, not theoretical calculations
- Considers: Total Cost = (Tokens ÷ Tokens/Hour) × Hourly Rate
- May recommend slower but cheaper GPUs for better value

### 2. **FSDP Support**
- Automatically enables for 70B+ models
- Shards model across multiple GPUs
- Accurate memory calculations including optimizer states

### 3. **Docker Deployment**
- **Base Image**: `grahamco/runpod-sglang-base:latest`
  - SGLang for superior batching vs vLLM
  - Dynamic model loading (not baked in)
  - Multi-mode: inference, training, or shell
- **Fine-tune Image**: `grahamco/runpod-sglang-finetune:latest`
  - Complete training environment
  - SFT and ORPO support
  - Dataset preparation tools

### 4. **Cost Examples**
For 10M tokens:
- 7B model: RTX 4090 @ $2.09 total (cheapest)
- 13B model: RTX 4090 @ $3.54 total  
- 70B model: 2x H100 FSDP @ $125 total

## CLI Commands

```bash
# Create instance with auto GPU selection
runpod create-instance 70B --tokens 10000000

# Deploy Docker image
runpod deploy-docker grahamco/runpod-sglang-base --model meta-llama/Llama-2-70b-hf

# Optimize GPU selection
runpod optimize 13B --tokens 5000000

# Monitor instance
runpod monitor <instance-id>

# List instances
runpod list-instances
```

## Slash Commands

- `/runpod create` - Create optimized instance
- `/runpod optimize` - Find best GPU configuration
- `/runpod deploy` - Deploy Docker image
- `/runpod list` - List active instances
- `/runpod terminate` - Stop instance

## Handler Pattern

```python
from runpod_ops.handlers import RunPodHandler

handler = RunPodHandler()

# Optimize GPU selection
result = handler.handle({
    "operation": "optimize",
    "model_size": "70B",
    "tokens": 10000000,
    "is_training": False
})

# Create instance
result = handler.handle({
    "operation": "create",
    "model_size": "13B",
    "hours": 4
})
```

## Docker Deployment

### Quick Deploy

```bash
# Inference server
runpod deploy-docker grahamco/runpod-sglang-base \
  --model meta-llama/Llama-2-70b-hf

# Fine-tuning
runpod deploy-docker grahamco/runpod-sglang-finetune \
  --mode finetune \
  --model meta-llama/Llama-2-13b-hf
```

### Environment Variables

- `MODE`: inference/finetune/shell
- `MODEL_NAME`: HuggingFace model ID
- `HF_TOKEN`: For private models
- `TENSOR_PARALLEL`: Number of GPUs
- `QUANTIZATION`: awq/gptq/4bit

## Integration Points

- **Unsloth**: Deploy fine-tuned models
- **Claude Test Reporter**: Track training costs
- **ArangoDB**: Store optimization history
- **LLM Call**: Use deployed endpoints

## Configuration

```bash
# Set API key
export RUNPOD_API_KEY=your_key_here

# Optional: HuggingFace token
export HF_TOKEN=your_hf_token
```

## Testing

```bash
# Run tests with real API
pytest tests/ -v

# Test API keys
python test_api_keys.py
```

## Key Differentiators

1. **Total Cost Optimization**: Considers time × rate, not just GPU speed
2. **Real Benchmarks**: Uses actual performance data
3. **Dynamic Loading**: Models not baked into Docker images
4. **SGLang Integration**: Superior batching for inference
5. **FSDP Support**: Train 70B+ models efficiently

## Module Information

- **Type**: Infrastructure/Training
- **Dependencies**: runpod, transformers, torch, sglang
- **API Keys**: RUNPOD_API_KEY required
- **Docker Hub**: grahamco (password in .env)
- **Interaction Level**: 3 (Cross-module integration)

## References

- [RunPod API Docs](https://docs.runpod.io/)
- [SGLang Project](https://github.com/sgl-project/sglang)
- [Docker README](/docker/README.md)
- [GPU Optimization Guide](/docs/GPU_OPTIMIZATION_EXPLAINED.md)