# How to Use Gemini to Create More Scenarios

## Quick Start

1. **Open Gemini** (Google AI Studio or Vertex AI)

2. **Copy the entire prompt** from 

3. **Paste and send** to Gemini

4. **Iterate** using the follow-up prompts provided

## Files Created for You

### 1. GEMINI_SCENARIO_PROMPT.md
- Comprehensive context about all modules
- Detailed guidelines for scenario creation
- Examples and format specifications

### 2. GEMINI_INTERACTION_TIPS.md
- Strategies for effective prompting
- How to get creative combinations
- Quality check questions
- Advanced techniques

### 3. GEMINI_READY_TO_USE_PROMPT.md
- Copy-paste ready prompt
- Pre-formatted for immediate use
- Includes follow-up prompts
- Pro tips for refinement

## Best Practices

### Start Simple
Begin with the ready-to-use prompt to get initial scenarios, then refine based on what you need.

### Be Specific
If Gemini's responses are too generic, ask for:
- Specific satellite types (LEO, GEO, MEO)
- Particular threats (jamming, spoofing, cyber)
- Exact module parameters
- Real-world constraints

### Iterate Intelligently
1. First pass: Get broad ideas
2. Second pass: Add technical detail
3. Third pass: Focus on implementation

### Save Everything
Gemini doesn't maintain long context, so save good outputs immediately.

## Example Conversation



## Advanced Usage

### For Different Domains
"Modify these scenarios for:
- CubeSat constellations
- Deep space missions  
- Ground station networks
- Launch operations"

### For Different Threats
"Create scenarios specifically for:
- Supply chain attacks
- Insider threats
- Nation-state APTs
- Space weather events"

### For Different Phases
"Design scenarios for:
- Pre-launch security
- Launch day operations
- On-orbit maintenance
- End-of-life disposal"

## Combining with Claude

You can also:
1. Get scenarios from Gemini
2. Ask Claude to enhance them
3. Have both AIs debate the best approaches
4. Synthesize the best ideas from both

## Integration with Project

Once you have good scenarios from Gemini:

1. **Convert to Python**: Create  files in the scenarios folder
2. **Add to test suite**: Include in 
3. **Document**: Add to the scenarios summary
4. **Test**: Validate they work with the framework

## Tips for Space-Specific Scenarios

Remind Gemini about space constraints:
- "Consider 40-minute round-trip communication delays to Mars"
- "Account for radiation effects on electronics"
- "Include solar panel degradation impacts"
- "Factor in limited onboard processing power"
- "Consider bandwidth limitations (kbps not gbps)"

## Quality Metrics

Ask Gemini to rate scenarios on:
- Technical feasibility (1-10)
- Security impact (1-10)
- Implementation effort (hours)
- Business value (high/medium/low)

## Final Tip

End your session by asking:
"Based on all these scenarios, what are the top 5 capability gaps in our module ecosystem that we should address?"

This often reveals valuable insights for future development!

## Summary

Using Gemini effectively is about:
1. Providing clear context (use our prompts)
2. Iterating intelligently (start broad, get specific)
3. Focusing on real value (space cybersecurity challenges)
4. Saving good outputs (Gemini forgets context)
5. Combining creativity with practicality

Now you have everything needed to generate hundreds more scenarios with Gemini!
