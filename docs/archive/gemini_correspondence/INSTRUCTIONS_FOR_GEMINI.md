# Instructions for Google Gemini

## Current Status
You've created one good scenario, but we need more diverse and challenging test cases.

## What We Need From You

### 1. **Quantity**: Create 5-7 different scenarios (not just one)

### 2. **Diversity**: Each scenario should test different aspects:
   - Performance limits and stress testing
   - Failure modes and recovery
   - Conflicting information handling
   - Resource constraints
   - Temporal consistency
   - Schema evolution
   - Security vulnerabilities

### 3. **Depth**: For each scenario include:
   - Complete Python implementation code
   - Specific error conditions to test
   - Performance metrics to measure
   - Expected vs actual behavior
   - Edge cases and boundary conditions

### 4. **Creativity**: Think beyond happy paths:
   - What breaks the system?
   - What causes cascading failures?
   - What reveals hidden dependencies?
   - What triggers emergent behaviors?

## Example of What We Want

Instead of just:
```python
result = await comm.execute_mcp_tool_command(...)
print("Success!")
```

We want:
```python
# Test cascade failure when primary source fails
try:
    result = await comm.execute_mcp_tool_command(...)
except TimeoutError:
    # Primary failed, test fallback
    fallback_result = await comm.execute_http_api(...)
    # But what if fallback is overloaded?
    if fallback_result['queue_depth'] > 1000:
        # Test graceful degradation
        cached_result = await get_cached_data()
        # But what if cache is stale?
        if cached_result['age_days'] > 30:
            # Force system to make hard choices
            priority_result = await emergency_prioritization()
```

## Specific Test Scenarios Needed

1. **The Avalanche** - One failure triggers cascading failures
2. **The Contradiction** - Multiple sources disagree violently  
3. **The Resource Strangler** - System runs out of memory/CPU/bandwidth
4. **The Time Paradox** - Events reported before they happen
5. **The Schema Shapeshifter** - Data formats change mid-stream
6. **The Infinite Loop** - Circular dependencies emerge
7. **The Security Breach** - Malicious inputs try to break modules

## Your Mission

Create scenarios that will:
- Break the system in interesting ways
- Reveal hidden assumptions
- Test every error path
- Measure degradation patterns
- Discover emergent behaviors
- Validate recovery mechanisms

We want to know not just IF modules can communicate, but HOW WELL they handle adversity, ambiguity, and attack.

Please provide 5-7 complete scenarios with full implementation details.
