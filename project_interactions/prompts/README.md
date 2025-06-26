# Prompt Templates

This directory contains LLM prompt templates used throughout the application.

## Structure

```
prompts/
├── README.md
├── analysis/
│   ├── test_results.txt
│   ├── code_review.txt
│   └── performance.txt
├── generation/
│   ├── documentation.txt
│   ├── test_cases.txt
│   └── code_completion.txt
└── conversation/
    ├── chat_system.txt
    ├── qa_system.txt
    └── support_agent.txt
```

## Format

### Simple Templates (.txt)
Use `$variable_name` for substitution:
```
You are analyzing $task_type.
Input: $input_data
Expected output: $expected_format
```

### Jinja2 Templates (.j2)
For complex logic:
```
{% if error_count > 0 %}
ERRORS FOUND: {{ error_count }}
{% for error in errors %}
- {{ error.message }}
{% endfor %}
{% endif %}
```

## Naming Convention
- Use descriptive names: `analyze_test_results.txt` not `prompt1.txt`
- Group by functionality: `analysis/`, `generation/`, etc.
- Version with suffixes: `chat_system_v2.txt` for experiments