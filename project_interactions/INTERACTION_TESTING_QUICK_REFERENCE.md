# Interaction Testing Quick Reference

## 🚨 Critical Rule: No Module is Complete Without Working Interactions

A module that works in isolation but can't communicate with other modules is **worthless** in the Granger ecosystem.

## Minimum Requirements Before Marking Module as "Tested"

### ✅ Level 0: Isolation (Prerequisite)
- [ ] Module has >30% real implementation (not skeleton)
- [ ] Basic unit tests pass
- [ ] Can perform its core function alone

### ✅ Level 1: Binary Interaction (REQUIRED)
- [ ] Communicates with Granger Hub
- [ ] Interacts with at least 1 other module
- [ ] Uses standard message format
- [ ] Handles errors from other modules

### ✅ Level 2: Pipeline Participation (REQUIRED) 
- [ ] Works in a 3+ module pipeline
- [ ] Can be middle module (receive and send)
- [ ] Maintains data integrity through chain
- [ ] Performance doesn't degrade >2x

### ✅ Level 3: Ecosystem Integration (RECOMMENDED)
- [ ] Participates in full Granger workflows
- [ ] Handles concurrent requests
- [ ] Graceful degradation when dependencies fail
- [ ] Provides telemetry to Test Reporter

## Quick Checks

```bash
# 1. Does module have interaction code?
grep -r "handle_message\|send_to\|GrangerHub" src/ || echo "❌ NO INTERACTIONS"

# 2. Does module have interaction tests?
ls tests/*interaction* tests/level_* || echo "❌ NO INTERACTION TESTS"

# 3. Can module actually connect?
python -c "from my_module import MyModule; m = MyModule(); print(m.test_connection())"
```

## Red Flags 🚩

1. **No imports of other Granger modules** - Module is isolated
2. **No message handling functions** - Can't participate in ecosystem
3. **Tests pass instantly (<0.01s)** - Likely mocked, not real
4. **Same output regardless of input** - Fake implementation
5. **No network activity during tests** - Not really communicating

## Standard Interaction Pattern

```python
# Every module MUST implement:
class MyModule:
    def register_with_hub(self, hub):
        """Register this module with Granger Hub"""
        
    def handle_message(self, message: Dict) -> Dict:
        """Process incoming messages from other modules"""
        
    def send_to(self, target: str, data: Dict) -> Dict:
        """Send data to another module"""
        
    def get_capabilities(self) -> List[str]:
        """List what this module can do"""
```

## Testing Progression

```
Start → Level 0 (Unit) → Level 1 (Binary) → Level 2 (Pipeline) → Level 3 (Ecosystem) → ✅ READY
         ↓ FAIL            ↓ FAIL            ↓ FAIL              ↓ FAIL
         FIX               FIX               FIX                 FIX
         ↑                 ↑                 ↑                   ↑
         └─────────────────┴─────────────────┴───────────────────┘
```

## Example Test Structure

```
tests/
├── test_unit.py           # Level 0: Basic functionality
├── test_interaction.py    # Level 1: Two-module tests
├── level_1/
│   ├── test_hub_communication.py
│   └── test_module_to_module.py
├── level_2/
│   ├── test_pipeline_participation.py
│   └── test_three_module_chain.py
└── level_3/
    └── test_full_ecosystem.py
```

## Commands to Add to Your Project

```bash
# Makefile or scripts/test.sh
test-interaction:
	@echo "=== Testing Module Interactions ==="
	pytest tests/test_interaction.py -v
	pytest tests/level_1/ -v
	pytest tests/level_2/ -v
	@echo "=== Checking Real Communication ==="
	@grep -r "handle_message" src/ | wc -l || (echo "❌ No message handlers" && exit 1)
	@echo "✅ Interaction tests complete"

test-all: test-unit test-interaction test-integration
```

## When to Run Interaction Tests

1. **Before marking any task complete** - Isolation isn't enough
2. **Before merging PRs** - Ensure compatibility maintained
3. **After modifying message formats** - Verify backward compatibility
4. **When adding new modules** - Ensure ecosystem integration
5. **During CI/CD** - Block deployment if interactions fail

## Remember

> "A module without connections is like a brain cell without synapses - technically alive but functionally useless."

**Always test interactions. No exceptions.**