# Feature Flag Management System

A comprehensive feature flag management system with targeting, rollouts, and A/B testing capabilities.

## Features

### Core Functionality
- **Multiple Flag Types**: Boolean, String, Number, and JSON flags
- **Flag Management**: Create, update, delete, and list flags
- **Environment-Specific Flags**: Different configurations per environment
- **Flag Dependencies**: Flags can depend on other flags
- **Kill Switches**: Emergency disable for any flag

### Targeting & Segmentation
- **User Targeting**: Target specific users or user segments
- **Rule-Based Targeting**: Complex rules with multiple operators
- **Segment Management**: Create and manage user segments
- **Attribute-Based Evaluation**: Evaluate flags based on user attributes

### Rollout Strategies
- **Percentage Rollout**: Roll out to a percentage of users
- **Gradual Rollout**: Increase rollout percentage over time
- **Ring Deployment**: Deploy to specific user rings
- **Canary Deployment**: Test with a small percentage first
- **Targeted Rollout**: Roll out only to specific segments

### A/B Testing
- **Multiple Variants**: Support for multiple test variants
- **Weighted Distribution**: Control variant distribution
- **Consistent Assignment**: Users always get the same variant
- **Variant Analytics**: Track variant performance

### Additional Features
- **SDK Generation**: Generate SDKs for JavaScript, Python, Java, and Go
- **Audit Logging**: Track all flag changes
- **Analytics**: Track flag usage and performance
- **Webhooks**: Notify external systems of flag changes
- **Caching**: Fast evaluation with intelligent caching

## Usage

### Basic Flag Creation

```python
from feature_flags import FeatureFlagsInteraction, FlagType

interaction = FeatureFlagsInteraction()

# Create a boolean flag
flag = await interaction.create_flag(
    key="new-feature",
    name="New Feature",
    flag_type=FlagType.BOOLEAN,
    enabled=True,
    description="Enable new feature"
)

# Create with rollout percentage
flag = await interaction.create_flag(
    key="gradual-feature",
    name="Gradual Feature",
    rollout_percentage=25  # 25% of users
)
```

### Targeting Users

```python
from feature_flags import Segment, TargetingRule, TargetingOperator

# Create a segment for premium users
segment = Segment(
    name="premium_users",
    rules=[
        TargetingRule("plan", TargetingOperator.EQUALS, "premium"),
        TargetingRule("country", TargetingOperator.IN, ["US", "UK", "CA"])
    ]
)

await interaction.add_segment("new-feature", segment)
```

### A/B Testing

```python
from feature_flags import Variant

# Add variants for A/B testing
await interaction.add_variant(
    "button-color",
    Variant(name="control", value="blue", weight=50)
)
await interaction.add_variant(
    "button-color",
    Variant(name="variant_a", value="green", weight=30)
)
await interaction.add_variant(
    "button-color",
    Variant(name="variant_b", value="red", weight=20)
)
```

### Evaluating Flags

```python
from feature_flags import EvaluationContext

# Simple evaluation
is_enabled = await interaction.evaluate_flag(
    "new-feature",
    user_id="user123"
)

# Evaluation with context
context = EvaluationContext(
    user_id="user123",
    attributes={
        "plan": "premium",
        "country": "US",
        "account_age_days": 45
    }
)

result = await interaction.evaluate_flag_detailed("new-feature", context)
print(f"Value: {result.value}, Reason: {result.reason}")
```

### SDK Generation

```python
# Generate JavaScript SDK
js_sdk = await interaction.generate_sdk("javascript")

# Generate Python SDK
py_sdk = await interaction.generate_sdk("python")
```

## Targeting Operators

- `EQUALS`: Exact match
- `NOT_EQUALS`: Not equal to value
- `CONTAINS`: String contains substring
- `NOT_CONTAINS`: String doesn't contain substring
- `IN`: Value in list
- `NOT_IN`: Value not in list
- `GREATER_THAN`: Numeric greater than
- `LESS_THAN`: Numeric less than
- `REGEX`: Regular expression match

## Rollout Strategies

### Percentage Rollout
Roll out to a fixed percentage of users.

### Gradual Rollout
Gradually increase rollout percentage over time.

### Ring Deployment
Deploy to specific user rings (e.g., internal → beta → GA).

### Canary Deployment
Test with a small percentage before full rollout.

## Architecture

The system consists of:

- **FeatureFlagsInteraction**: Main interaction class
- **FlagStorage**: Persistent storage interface
- **EvaluationEngine**: Flag evaluation logic
- **TargetingEngine**: User targeting and segmentation
- **RolloutEngine**: Rollout strategy implementation
- **CacheManager**: Performance optimization

## Testing

Run the test suite:

```bash
# Run all tests
pytest feature_flags/tests/ -v

# Run specific test file
pytest feature_flags/tests/test_flag_management.py -v

# Run validation script
python test_task_58.py
```

## Performance

- Evaluation results are cached for 10 seconds
- Flag definitions are cached for 60 seconds
- Consistent hashing ensures users always get the same variant
- Async operations for non-blocking evaluation

## Integration

The feature flag system can be integrated with:
- Web applications for feature toggling
- Mobile apps via generated SDKs
- Microservices for configuration management
- CI/CD pipelines for progressive deployments