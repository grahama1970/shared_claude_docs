# Tips for Getting High-Quality Scenarios from Gemini

## Effective Prompting Strategies

### 1. Start with Context
Begin your conversation with Gemini by saying:
"I need your help creating test scenarios for a space cybersecurity project. I'll provide you with detailed context about the available modules and what I need."

### 2. Provide the Full Prompt
Copy and paste the entire content from GEMINI_SCENARIO_PROMPT.md

### 3. Use Follow-Up Prompts

#### For More Detail:
"Can you expand scenario #X with more specific technical details about how each module would process the data?"

#### For Different Perspectives:
"Now create 5 scenarios focusing specifically on defending against nation-state attackers"

#### For Integration Ideas:
"Show me scenarios where modules create feedback loops or circular workflows"

#### For Validation:
"For each scenario, add potential failure points and how the system would handle them"

### 4. Request Specific Formats

#### Python Implementation:
"Convert scenario #X into a Python class following this pattern:
- Inherit from ScenarioBase
- Implement setup_modules()
- Implement create_workflow()
- Implement process_results()"

#### Mermaid Diagrams:
"Create a mermaid diagram showing the data flow for scenario #X"

#### Risk Analysis:
"Add a risk assessment section to each scenario identifying potential security vulnerabilities"

### 5. Iterative Refinement

#### First Pass:
"Create 10 high-level scenario concepts"

#### Second Pass:
"Now pick the 5 most interesting and expand them with full details"

#### Third Pass:
"Add specific configuration parameters for each module in these scenarios"

## Example Conversation Flow

### You:
"I'm working on testing a module orchestration system for space cybersecurity. I need creative scenarios that combine multiple specialized modules. Here's the context: [paste GEMINI_SCENARIO_PROMPT.md]"

### Gemini:
[Creates initial scenarios]

### You:
"Excellent! Now for scenarios 102-105, can you:
1. Add specific NIST control numbers from SPARTA
2. Include example PDF titles for Marker to process
3. Specify which LLM models to use in LLM Call
4. Add performance metrics we should track"

### Gemini:
[Provides enhanced scenarios]

### You:
"Now create 5 scenarios that specifically address the challenge of secure satellite firmware updates in contested environments"

## Getting Creative Combinations

### Ask for Unusual Pairings:
"Create scenarios that use MCP Screenshot with Unsloth - how could visual data improve model training?"

### Request Complex Workflows:
"Design a scenario where the output of one module triggers different paths based on conditions"

### Explore Edge Cases:
"What scenarios would help test the system's behavior under degraded communication conditions?"

## Quality Checks

After Gemini provides scenarios, ask:
1. "Which of these scenarios would provide the most value for satellite operators?"
2. "Are there any missing module combinations that could be powerful?"
3. "How would these scenarios need to be modified for military vs commercial satellites?"

## Saving and Organizing

### Request Categorization:
"Group these scenarios by:
- Difficulty (easy/medium/hard)
- Time to implement (hours/days/weeks)
- Business value (high/medium/low)"

### Ask for Prioritization:
"If we could only implement 5 of these scenarios, which would give us the best test coverage?"

## Advanced Techniques

### 1. Role-Playing:
"Act as a red team attacker. What scenarios would best test our defenses?"

### 2. Constraint-Based:
"Create scenarios that must complete in under 5 minutes of execution time"

### 3. Failure Mode:
"Design scenarios that test graceful degradation when modules fail"

### 4. Integration Testing:
"Create scenarios specifically for testing module communication interfaces"

## Remember

- Gemini excels at creative combinations when given clear structure
- Provide specific examples of what good output looks like
- Ask for variations on themes rather than completely new concepts
- Use iterative refinement to get exactly what you need
- Save good outputs immediately as context can be lost

## Final Tip

End with: "Based on all these scenarios, what patterns do you see that could lead to a reusable scenario template system?"

This often leads to valuable architectural insights!
