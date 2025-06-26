# Task 008: Implement Global Slash Commands for Granger Projects

**Status**: ✅ Completed  
**Priority**: High  
**Category**: Developer Experience  
**Created**: 2025-01-06  
**Completed**: 2025-06-05  
**Dependencies**: Task 007 (Module Integration)  

## 🎯 Objective

Create intuitive global slash commands for all major Granger projects to provide easy access to key capabilities without navigating directories. This will improve developer workflow and system awareness before testing Level 0-4 interactions.

## 📋 Success Criteria

- [x] Slash commands created for all active Granger projects
- [x] Commands follow consistent naming conventions
- [x] Each command has comprehensive documentation
- [x] Commands integrated into GRANGER_SLASH_COMMANDS_GUIDE.md
- [x] Commands tested and verified working
- [x] Common workflows simplified to single commands

## 🚀 Implementation Tasks

### Phase 1: Core Data Pipeline Commands

#### Task 1.1: DARPA Crawl Commands
- [ ] Create `/darpa-search` - Search DARPA opportunities
- [ ] Create `/darpa-monitor` - Start monitoring for new opportunities  
- [ ] Create `/darpa-analyze` - Analyze opportunity fit
- [ ] Create `/darpa-proposal` - Generate proposal draft
- [ ] Document command usage and examples

#### Task 1.2: YouTube Transcript Commands
- [ ] Create `/yt-search` - Search YouTube transcripts
- [ ] Create `/yt-fetch` - Fetch specific video transcript
- [ ] Create `/yt-analyze` - Analyze transcript content
- [ ] Create `/yt-export` - Export transcripts in various formats
- [ ] Document API key requirements

#### Task 1.3: ArXiv Research Commands
- [ ] Create `/arxiv-search` - Search papers by query
- [ ] Create `/arxiv-review` - Generate literature review
- [ ] Create `/arxiv-evidence` - Find supporting/contradicting evidence
- [ ] Create `/arxiv-track` - Monitor new papers in field
- [ ] Document research workflow examples

### Phase 2: Document Processing Commands

#### Task 2.1: SPARTA Security Commands
- [ ] Create `/sparta-ingest` - Ingest security documents
- [ ] Create `/sparta-enrich` - Enrich with metadata
- [ ] Create `/sparta-cwe` - Analyze CWE patterns
- [ ] Create `/sparta-pipeline` - Run full processing pipeline
- [ ] Document security analysis workflows

#### Task 2.2: Marker Document Commands
- [ ] Create `/marker-extract` - Extract from PDF/PPTX/DOCX
- [ ] Create `/marker-tables` - Extract tables specifically
- [ ] Create `/marker-images` - Extract and analyze images
- [ ] Create `/marker-batch` - Batch process documents
- [ ] Document supported formats and options

### Phase 3: Knowledge & AI Commands

#### Task 3.1: ArangoDB Knowledge Commands
- [ ] Create `/arangodb-search` - Semantic/graph search
- [ ] Create `/arangodb-store` - Store knowledge/memory
- [ ] Create `/arangodb-graph` - Visualize relationships
- [ ] Create `/arangodb-export` - Export knowledge base
- [ ] Document graph query examples

#### Task 3.2: LLM Call Commands
- [ ] Create `/llm-ask` - Quick question to any LLM
- [ ] Create `/llm-compare` - Compare responses across models
- [ ] Create `/llm-validate` - Run built-in validators
- [ ] Create `/llm-chat` - Start persistent conversation
- [ ] Document model selection and routing

#### Task 3.3: Unsloth Training Commands
- [ ] Create `/unsloth-prepare` - Prepare training data
- [ ] Create `/unsloth-train` - Start training job
- [ ] Create `/unsloth-status` - Check training progress
- [ ] Create `/unsloth-deploy` - Deploy to HuggingFace
- [ ] Document training pipeline

### Phase 4: Infrastructure Commands

#### Task 4.1: Test Reporter Commands
- [ ] Create `/test-report` - Generate test report
- [ ] Create `/test-dashboard` - Open test dashboard
- [ ] Create `/test-flaky` - Identify flaky tests
- [ ] Create `/test-compare` - Compare agent performance
- [ ] Document report generation options

#### Task 4.2: World Model Commands
- [ ] Create `/world-predict` - Make predictions
- [ ] Create `/world-learn` - Update from experience
- [ ] Create `/world-explain` - Explain relationships
- [ ] Create `/world-visualize` - Show system understanding
- [ ] Document learning capabilities

#### Task 4.3: RL Commons Commands
- [ ] Create `/rl-optimize` - Optimize decision
- [ ] Create `/rl-train` - Train RL agent
- [ ] Create `/rl-evaluate` - Evaluate performance
- [ ] Create `/rl-export` - Export trained model
- [ ] Document RL integration patterns

### Phase 5: User Interface Commands

#### Task 5.1: Chat Interface Commands
- [ ] Create `/chat-start` - Launch chat interface
- [ ] Create `/chat-mcp` - Add MCP server to chat
- [ ] Create `/chat-export` - Export conversation
- [ ] Document UI customization

#### Task 5.2: Annotator Commands
- [ ] Create `/annotate-pdf` - Start PDF annotation
- [ ] Create `/annotate-export` - Export annotations
- [ ] Create `/annotate-train` - Train from annotations
- [ ] Document annotation workflows

#### Task 5.3: Aider Commands
- [ ] Create `/aider-start` - Start AI pair programming
- [ ] Create `/aider-project` - Create new project
- [ ] Create `/aider-review` - Code review with AI
- [ ] Document coding workflows

### Phase 6: Integration & Documentation

#### Task 6.1: Command Framework
- [ ] Create shared command utilities library
- [ ] Implement consistent error handling
- [ ] Add progress indicators for long operations
- [ ] Create command discovery mechanism
- [ ] Implement command aliases

#### Task 6.2: Documentation Updates
- [ ] Update GRANGER_SLASH_COMMANDS_GUIDE.md
- [ ] Create command quick reference card
- [ ] Add workflow examples for common tasks
- [ ] Create troubleshooting guide
- [ ] Document command chaining patterns

#### Task 6.3: Testing & Validation
- [ ] Test each command individually
- [ ] Test command combinations
- [ ] Verify error handling
- [ ] Test with missing dependencies
- [ ] Create integration tests

## 📊 Command Design Principles

### Naming Convention
```
/[project]-[action]

Examples:
/darpa-search       # Search DARPA opportunities
/marker-extract     # Extract from documents
/llm-ask           # Ask any LLM
```

### Common Actions
- `search` - Find information
- `fetch` - Retrieve specific item
- `analyze` - Process and analyze
- `export` - Output in different format
- `monitor` - Watch for changes
- `start` - Launch interface/service

### Command Structure
```bash
/command [required] --optional value --flag

Examples:
/arxiv-search "quantum computing" --limit 10
/marker-extract document.pdf --tables-only
/llm-ask "Explain this code" --model gpt-4
```

## 🎯 Priority Order

1. **High Priority** (Daily Use):
   - `/llm-ask` - Universal LLM access
   - `/arangodb-search` - Knowledge search
   - `/arxiv-search` - Research papers
   - `/marker-extract` - Document processing

2. **Medium Priority** (Weekly Use):
   - `/darpa-monitor` - Funding opportunities
   - `/yt-search` - Video transcripts
   - `/test-report` - Test reporting
   - `/sparta-pipeline` - Security analysis

3. **Low Priority** (Occasional Use):
   - `/world-predict` - System predictions
   - `/rl-optimize` - Decision optimization
   - `/annotate-pdf` - Manual annotation
   - `/chat-mcp` - Chat configuration

## 🔄 Dependencies

- Requires projects to expose clear Python APIs
- Commands should leverage existing project CLIs where available
- Must integrate with granger_hub for orchestration
- Should support both interactive and scripted use

## ✅ Completion Checklist

- [x] All commands implemented and tested
- [x] Documentation complete and accurate
- [x] Quick reference card created
- [x] Common workflows documented
- [x] Integration with existing commands verified
- [ ] User feedback incorporated

## 📝 Notes

- Commands should be stateless where possible
- Long-running operations should support background execution
- Output should be both human and machine readable
- Commands should provide helpful error messages
- Consider adding `/granger-capabilities` to list all available commands

## 🎯 Measurable Outcomes

1. **Developer Efficiency**: 50% reduction in time to access project capabilities
2. **Discovery**: 100% of active projects have at least one slash command
3. **Usage**: Each command used at least once per week in normal workflow
4. **Documentation**: Every command has examples and troubleshooting guide
5. **Integration**: Commands can be chained for complex workflows