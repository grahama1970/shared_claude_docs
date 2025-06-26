# Task 009: Comprehensive UI Projects Testing

**Status**: 🟡 In Progress  
**Priority**: High  
**Category**: Quality Assurance  
**Created**: 2025-06-05  
**Dependencies**: Task 008 (Slash Commands)  

## 🎯 Objective

Test all User Interface projects in the Granger ecosystem, ensuring both JavaScript/TypeScript and Python tests pass. Fix or deprecate any failing tests to achieve 100% test suite reliability.

## 📋 Success Criteria

- [ ] All UI project test suites execute successfully
- [ ] JavaScript/TypeScript tests pass or are fixed
- [ ] Python tests pass or are fixed  
- [ ] Deprecated tests moved to archive/ directories
- [ ] Test reports generated for each project
- [ ] Documentation updated with test status

## 🚀 Implementation Tasks

### Phase 1: Granger UI Design System Testing

#### Task 1.1: Setup and Discovery
- [ ] Navigate to `/home/graham/workspace/granger-ui/`
- [ ] Identify test framework (Jest, Vitest, etc.)
- [ ] Check for package.json test scripts
- [ ] Verify dependencies are installed

#### Task 1.2: Run Component Tests
- [ ] Execute React component tests
- [ ] Execute terminal UI component tests
- [ ] Fix any failing tests
- [ ] Check for deprecated components
- [ ] Generate test coverage report

#### Task 1.3: Run Integration Tests
- [ ] Test design token system
- [ ] Test component interactions
- [ ] Verify accessibility compliance
- [ ] Test responsive behavior

### Phase 2: Annotator Web Interface Testing

#### Task 2.1: Backend Python Tests
- [ ] Navigate to `/home/graham/workspace/experiments/annotator/`
- [ ] Run pytest suite
- [ ] Test PDF processing functionality
- [ ] Test active learning algorithms
- [ ] Verify database operations

#### Task 2.2: Frontend JavaScript Tests
- [ ] Check for frontend test suite
- [ ] Test annotation UI components
- [ ] Test WebSocket connections
- [ ] Verify PDF.js integration
- [ ] Test multi-annotator workflows

#### Task 2.3: End-to-End Tests
- [ ] Test complete annotation workflow
- [ ] Verify recipe system functionality
- [ ] Test export functionality
- [ ] Check API endpoints

### Phase 3: Chat Interface Testing

#### Task 3.1: React Frontend Tests
- [ ] Navigate to `/home/graham/workspace/experiments/chat/`
- [ ] Run React test suite
- [ ] Test message components
- [ ] Test MCP server integration
- [ ] Verify state management

#### Task 3.2: FastAPI Backend Tests
- [ ] Run Python API tests
- [ ] Test WebSocket handlers
- [ ] Verify authentication
- [ ] Test message persistence
- [ ] Check rate limiting

#### Task 3.3: Docker Integration Tests
- [ ] Test containerized deployment
- [ ] Verify environment configurations
- [ ] Test multi-container communication
- [ ] Check resource limits

### Phase 4: Aider-Daemon Terminal Interface Testing

#### Task 4.1: CLI Command Tests
- [ ] Navigate to `/home/graham/workspace/experiments/aider-daemon/`
- [ ] Test command parsing
- [ ] Verify Git integration
- [ ] Test file operations
- [ ] Check LLM interactions

#### Task 4.2: Daemon Process Tests
- [ ] Test daemon startup/shutdown
- [ ] Verify process management
- [ ] Test signal handling
- [ ] Check resource cleanup

#### Task 4.3: Integration Tests
- [ ] Test with real repositories
- [ ] Verify code modifications
- [ ] Test rollback functionality
- [ ] Check error recovery

### Phase 5: Test Cleanup and Archival

#### Task 5.1: Identify Deprecated Tests
- [ ] Find tests for removed features
- [ ] Identify outdated test patterns
- [ ] List tests using old APIs
- [ ] Check for broken imports

#### Task 5.2: Archive Deprecated Tests
- [ ] Create archive/ directories in each project
- [ ] Move deprecated tests with documentation
- [ ] Update test configurations
- [ ] Document why tests were archived

#### Task 5.3: Fix Remaining Issues
- [ ] Update test dependencies
- [ ] Fix import paths
- [ ] Update mocked data
- [ ] Resolve async/timing issues

### Phase 6: Reporting and Documentation

#### Task 6.1: Generate Test Reports
- [ ] Create test report for each project
- [ ] Include coverage metrics
- [ ] Document test execution time
- [ ] List any skipped tests

#### Task 6.2: Update Documentation
- [ ] Update project READMEs with test status
- [ ] Document test commands
- [ ] Add troubleshooting guides
- [ ] Update CI/CD configurations

## 📊 Testing Approach

### JavaScript/TypeScript Testing
```bash
# Common test commands
npm test                    # Run tests
npm run test:coverage      # With coverage
npm run test:watch        # Watch mode
npm run test:debug        # Debug mode
```

### Python Testing
```bash
# Common test commands
pytest                     # Run all tests
pytest -v                 # Verbose output
pytest --cov=src          # With coverage
pytest -x                 # Stop on first failure
```

### Test Verification Criteria
Following TEST_VERIFICATION_TEMPLATE_GUIDE:
- No mocked external services (use real connections)
- Minimum test duration thresholds
- Honeypot tests included
- Real data validation
- Proper error handling

## 🎯 Priority Order

1. **granger-ui** - Core design system affects all UIs
2. **chat** - Primary user interface
3. **annotator** - Critical for training data
4. **aider-daemon** - Developer tool

## 🔄 Dependencies

- Node.js and npm/yarn for JavaScript tests
- Python 3.9+ for Python tests
- Docker for integration tests
- Actual services running (ArangoDB, Redis, etc.)

## ✅ Completion Checklist

- [ ] All test suites run without errors
- [ ] Coverage meets minimum thresholds (80%+)
- [ ] Deprecated tests properly archived
- [ ] Documentation fully updated
- [ ] Test reports generated and saved
- [ ] CI/CD pipelines verified

## 📝 Notes

- Use `/granger-verify --project PROJECT_NAME` for initial assessment
- Run tests in isolation first, then integration
- Document any environment-specific requirements
- Consider creating test data fixtures
- Ensure tests work in CI/CD environment

## 🎯 Measurable Outcomes

1. **Test Success Rate**: 100% of active tests passing
2. **Code Coverage**: Minimum 80% for each project
3. **Execution Time**: Tests complete within reasonable time
4. **Documentation**: Every project has clear test instructions
5. **Maintainability**: No flaky or intermittent failures