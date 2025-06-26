# Granger Ecosystem Anti-Pattern Analysis Report

*Generated: 2025-06-08T07:04:50.792219*
*Analyzer: Granger Anti-Pattern Detection Pipeline*

## Executive Summary

Analyzed **15** Granger projects for **10** Python anti-patterns.

### Overall Statistics

- **Total Files Analyzed:** 332660
- **Total Violations Found:** 549
- **High Severity:** 169
- **Medium Severity:** 72
- **Low Severity:** 308

## Project Analysis

### fine_tuning

**Path:** `/home/graham/workspace/experiments/fine_tuning`
**Files:** 38470
**Violations:** 147

**Severity Distribution:**
- High: 74
- Medium: 3
- Low: 70

**Top Violations:**

#### AP-008: Not Using Pathlib (68 occurrences)

- `repos/unsloth/unsloth/save.py:120`
  ```python
  os.path.join
  ```

- `repos/unsloth/unsloth/save.py:122`
  ```python
  os.path.exists
  ```

- `repos/unsloth/unsloth/save.py:127`
  ```python
  os.path.isfile
  ```

#### AP-002: Bare Except Clauses (59 occurrences)

- `repos/unsloth/unsloth/save.py:37`
  ```python
  except:
  ```

- `repos/unsloth/unsloth/save.py:40`
  ```python
  except:
  ```

- `repos/unsloth/unsloth/save.py:266`
  ```python
  except:
  ```

#### AP-004: Global State Mutation (9 occurrences)

- `repos/unsloth/unsloth/utils/hf_hub.py:35`
  ```python
  global _HFAPI
  ```

- `repos/unsloth/unsloth/utils/hf_hub.py:64`
  ```python
  global _HFAPI
  ```

- `repos/unsloth/unsloth/models/loader.py:75`
  ```python
  global FORCE_FLOAT32
  ```

#### AP-001: Mutable Default Arguments (6 occurrences)

- `repos/unsloth/unsloth/save.py:806`
  ```python
  def install_python_non_blocking(packages = [
  ```

- `repos/unsloth/unsloth/chat_templates.py:1229`
  ```python
  def get_chat_template(
    tokenizer,
    chat_template = "chatml",
    mapping = {
  ```

- `repos/unsloth/unsloth/chat_templates.py:1656`
  ```python
  def get_ollama_eos_tokens(tokenizer, extra_eos_tokens = [
  ```

#### AP-009: Overusing Classes (2 occurrences)

- `repos/unsloth/unsloth/trainer.py:122`
  ```python
  class UnslothTrainer(SFTTrainer):
    def create_optimizer(self)
  ```

- `repos/unsloth/unsloth/models/llama.py:1380`
  ```python
  class LlamaExtendedRotaryEmbedding(torch.nn.Module):
    def __init__(self, dim = None, max_position
  ```

---

### marker

**Path:** `/home/graham/workspace/experiments/marker`
**Files:** 19809
**Violations:** 140

**Severity Distribution:**
- High: 71
- Medium: 3
- Low: 66

**Top Violations:**

#### AP-008: Not Using Pathlib (64 occurrences)

- `repos/unsloth/unsloth/save.py:139`
  ```python
  os.path.join
  ```

- `repos/unsloth/unsloth/save.py:141`
  ```python
  os.path.exists
  ```

- `repos/unsloth/unsloth/save.py:146`
  ```python
  os.path.isfile
  ```

#### AP-002: Bare Except Clauses (56 occurrences)

- `repos/unsloth/unsloth/save.py:56`
  ```python
  except:
  ```

- `repos/unsloth/unsloth/save.py:59`
  ```python
  except:
  ```

- `repos/unsloth/unsloth/save.py:285`
  ```python
  except:
  ```

#### AP-004: Global State Mutation (9 occurrences)

- `repos/unsloth/unsloth/utils/hf_hub.py:49`
  ```python
  global _HFAPI
  ```

- `repos/unsloth/unsloth/utils/hf_hub.py:78`
  ```python
  global _HFAPI
  ```

- `repos/unsloth/unsloth/models/loader.py:92`
  ```python
  global FORCE_FLOAT32
  ```

#### AP-001: Mutable Default Arguments (6 occurrences)

- `repos/unsloth/unsloth/save.py:825`
  ```python
  def install_python_non_blocking(packages = [
  ```

- `repos/unsloth/unsloth/chat_templates.py:1247`
  ```python
  def get_chat_template(
    tokenizer,
    chat_template = "chatml",
    mapping = {
  ```

- `repos/unsloth/unsloth/chat_templates.py:1674`
  ```python
  def get_ollama_eos_tokens(tokenizer, extra_eos_tokens = [
  ```

#### AP-009: Overusing Classes (2 occurrences)

- `repos/unsloth/unsloth/trainer.py:139`
  ```python
  class UnslothTrainer(SFTTrainer):
    def create_optimizer(self)
  ```

- `repos/unsloth/unsloth/models/llama.py:1345`
  ```python
  class LlamaExtendedRotaryEmbedding(torch.nn.Module):
    def __init__(self, dim = None, max_position
  ```

---

### gitget

**Path:** `/home/graham/workspace/experiments/gitget`
**Files:** 18703
**Violations:** 128

**Severity Distribution:**
- High: 0
- Medium: 7
- Low: 121

**Top Violations:**

#### AP-008: Not Using Pathlib (120 occurrences)

- `verification/verify_clone.py:16`
  ```python
  os.path.join
  ```

- `verification/verify_clone.py:27`
  ```python
  os.path.join
  ```

- `verification/verify_clone.py:34`
  ```python
  os.path.join
  ```

#### AP-009: Overusing Classes (7 occurrences)

- `repos/pyperf_sparse/pyperf/_system.py:868`
  ```python
  class CheckNOHZFullIntelPstate(IntelPstateOperation):

    def __init__(self, system)
  ```

- `repos/pyperf_sparse/pyperf/_system.py:1008`
  ```python
  class System:
    def __init__(self)
  ```

- `repos/pyperf_sparse/pyperf/_bench.py:322`
  ```python
  class Benchmark:
    def __init__(self, runs)
  ```

#### AP-010: Not Using List Comprehensions (1 occurrences)

- `repos/pyperf_sparse/doc/examples/plot.py:46`
  ```python
  = []
                for value in run_values:
                    x.append
  ```

---

### aider-daemon

**Path:** `/home/graham/workspace/experiments/aider-daemon`
**Files:** 77094
**Violations:** 40

**Severity Distribution:**
- High: 8
- Medium: 31
- Low: 1

**Top Violations:**

#### AP-009: Overusing Classes (30 occurrences)

- `venv/lib/python3.12/site-packages/six.py:73`
  ```python
  class X(object):

            def __len__(self)
  ```

- `venv/lib/python3.12/site-packages/six.py:101`
  ```python
  class _LazyDescr(object):

    def __init__(self, name)
  ```

- `venv/lib/python3.12/site-packages/six.py:117`
  ```python
  class MovedModule(_LazyDescr):

    def __init__(self, name, old, new=None)
  ```

#### AP-004: Global State Mutation (6 occurrences)

- `venv/lib/python3.12/site-packages/threadpoolctl.py:700`
  ```python
  global limit
  ```

- `venv/lib/python3.12/site-packages/threadpoolctl.py:765`
  ```python
  global and
  ```

- `venv/lib/python3.12/site-packages/threadpoolctl.py:894`
  ```python
  global and
  ```

#### AP-002: Bare Except Clauses (2 occurrences)

- `venv/lib/python3.12/site-packages/colour.py:566`
  ```python
  except:
  ```

- `venv/lib/python3.12/site-packages/aiohappyeyeballs/impl.py:233`
  ```python
  except:
  ```

#### AP-003: Not Using Context Managers (1 occurrences)

- `venv/bin/vba_extract.py:22`
  ```python
  = open(filename, "wb")
  ```

#### AP-008: Not Using Pathlib (1 occurrences)

- `venv/lib/python3.12/site-packages/threadpoolctl.py:1147`
  ```python
  os.path.exists
  ```

---

### world_model

**Path:** `/home/graham/workspace/experiments/world_model`
**Files:** 3515
**Violations:** 28

**Severity Distribution:**
- High: 7
- Medium: 14
- Low: 7

**Top Violations:**

#### AP-009: Overusing Classes (14 occurrences)

- `.venv/lib/python3.10/site-packages/typing_extensions.py:163`
  ```python
  class _Sentinel:
    def __repr__(self)
  ```

- `.venv/lib/python3.10/site-packages/typing_extensions.py:196`
  ```python
  class _AnyMeta(type):
        def __instancecheck__(self, obj)
  ```

- `.venv/lib/python3.10/site-packages/typing_extensions.py:225`
  ```python
  class _ExtensionsSpecialForm(typing._SpecialForm, _root=True):
    def __repr__(self)
  ```

#### AP-008: Not Using Pathlib (7 occurrences)

- `.venv/bin/activate_this.py:54`
  ```python
  os.path.join
  ```

- `.venv/lib/python3.10/site-packages/_virtualenv.py:6`
  ```python
  os.path.join
  ```

- `.venv/lib/python3.10/site-packages/threadpoolctl.py:1140`
  ```python
  os.path.exists
  ```

#### AP-004: Global State Mutation (7 occurrences)

- `.venv/lib/python3.10/site-packages/_virtualenv.py:27`
  ```python
  global configs
  ```

- `.venv/lib/python3.10/site-packages/threadpoolctl.py:693`
  ```python
  global limit
  ```

- `.venv/lib/python3.10/site-packages/threadpoolctl.py:758`
  ```python
  global and
  ```

---

### granger_hub

**Path:** `/home/graham/workspace/experiments/granger_hub`
**Files:** 39642
**Violations:** 27

**Severity Distribution:**
- High: 1
- Medium: 0
- Low: 26

**Top Violations:**

#### AP-008: Not Using Pathlib (26 occurrences)

- `repos/aider/scripts/logo_svg.py:147`
  ```python
  os.path.exists
  ```

- `repos/aider/scripts/logo_svg.py:154`
  ```python
  os.path.exists
  ```

- `repos/aider/scripts/versionbump.py:168`
  ```python
  os.path.exists
  ```

#### AP-004: Global State Mutation (1 occurrences)

- `repos/aider/scripts/recording_audio.py:206`
  ```python
  global VOICE
  ```

---

### llm_call

**Path:** `/home/graham/workspace/experiments/llm_call`
**Files:** 37109
**Violations:** 14

**Severity Distribution:**
- High: 1
- Medium: 5
- Low: 8

**Top Violations:**

#### AP-010: Not Using List Comprehensions (7 occurrences)

- `repos/llm/llm/utils.py:76`
  ```python
  = []
        for i, h in enumerate(headings):
            row.append
  ```

- `repos/llm/llm/cli.py:255`
  ```python
  = []
    for value, mimetype in values:
        collected.append
  ```

- `repos/llm/llm/cli.py:1783`
  ```python
  = []
                for fragment in fragments:
                    bits.append
  ```

#### AP-009: Overusing Classes (4 occurrences)

- `repos/llm/llm/utils.py:104`
  ```python
  class _LogResponse(httpx.Response):
    def iter_bytes(self, *args, **kwargs)
  ```

- `repos/llm/llm/utils.py:111`
  ```python
  class _LogTransport(httpx.BaseTransport):
    def __init__(self, transport: httpx.BaseTransport)
  ```

- `repos/llm/llm/models.py:1501`
  ```python
  class _Model(_BaseModel):
    def conversation(self, tools: Optional[List[Tool]] = None)
  ```

#### AP-004: Global State Mutation (1 occurrences)

- `repos/llm/llm/plugins.py:33`
  ```python
  global _loaded
  ```

#### AP-003: Not Using Context Managers (1 occurrences)

- `repos/llm/llm/models.py:107`
  ```python
  = open(self.path, "rb")
  ```

#### AP-006: Not Using Enumerate (1 occurrences)

- `repos/llm/docs/plugins/llm-markov/llm_markov.py:34`
  ```python
  for i in range(len(
  ```

---

### chat

**Path:** `/home/graham/workspace/experiments/chat`
**Files:** 1498
**Violations:** 11

**Severity Distribution:**
- High: 2
- Medium: 1
- Low: 8

**Top Violations:**

#### AP-010: Not Using List Comprehensions (4 occurrences)

- `backend/dashboard/routes.py:119`
  ```python
  = []
        for node in nodes_cursor:
            nodes.append
  ```

- `backend/dashboard/routes.py:128`
  ```python
  = []
        for edge in edges_cursor:
            links.append
  ```

- `backend/dashboard/routes.py:164`
  ```python
  = []
        
        for execution in recent_cursor:
            recent_executions.append
  ```

#### AP-008: Not Using Pathlib (3 occurrences)

- `verify_dashboard.py:24`
  ```python
  os.path.exists
  ```

- `verify_dashboard.py:32`
  ```python
  os.path.exists
  ```

- `verify_dashboard.py:38`
  ```python
  os.path.exists
  ```

#### AP-004: Global State Mutation (2 occurrences)

- `backend/dashboard/d3/realtime.py:283`
  ```python
  global graph
  ```

- `backend/dashboard/d3/realtime.py:284`
  ```python
  global _updater
  ```

#### AP-006: Not Using Enumerate (1 occurrences)

- `backend/dashboard/learning_curves.py:93`
  ```python
  for i in range(len(
  ```

#### AP-009: Overusing Classes (1 occurrences)

- `backend/dashboard/routes.py:62`
  ```python
  class ConnectionManager:
    def __init__(self)
  ```

---

### arangodb

**Path:** `/home/graham/workspace/experiments/arangodb`
**Files:** 18539
**Violations:** 5

**Severity Distribution:**
- High: 0
- Medium: 4
- Low: 1

**Top Violations:**

#### AP-009: Overusing Classes (4 occurrences)

- `repos/graphiti/graphiti_core/prompts/lib.py:67`
  ```python
  class VersionWrapper:
    def __init__(self, func: PromptFunction)
  ```

- `repos/graphiti/graphiti_core/prompts/lib.py:78`
  ```python
  class PromptTypeWrapper:
    def __init__(self, versions: dict[str, PromptFunction])
  ```

- `repos/graphiti/graphiti_core/prompts/lib.py:84`
  ```python
  class PromptLibraryWrapper:
    def __init__(self, library: PromptLibraryImpl)
  ```

#### AP-010: Not Using List Comprehensions (1 occurrences)

- `repos/graphiti/graphiti_core/helpers.py:102`
  ```python
  = []
    for coroutine in coroutines:
        batch.append
  ```

---

### youtube_transcripts

**Path:** `/home/graham/workspace/experiments/youtube_transcripts`
**Files:** 20464
**Violations:** 5

**Severity Distribution:**
- High: 4
- Medium: 1
- Low: 0

**Top Violations:**

#### AP-002: Bare Except Clauses (4 occurrences)

- `scripts/comprehensive_bug_finder.py:159`
  ```python
  except:
  ```

- `scripts/comprehensive_bug_finder.py:172`
  ```python
  except:
  ```

- `scripts/comprehensive_bug_finder.py:207`
  ```python
  except:
  ```

#### AP-009: Overusing Classes (1 occurrences)

- `scripts/comprehensive_bug_finder.py:17`
  ```python
  class ComprehensiveBugFinder:
    def __init__(self)
  ```

---

### sparta

**Path:** `/home/graham/workspace/experiments/sparta`
**Files:** 10217
**Violations:** 3

**Severity Distribution:**
- High: 0
- Medium: 3
- Low: 0

**Top Violations:**

#### AP-009: Overusing Classes (3 occurrences)

- `.claude/sparta-commands/cleanup.py:13`
  ```python
  class ProjectCleaner:
    def __init__(self, project_root=None, dry_run=False, verbose=False)
  ```

- `tests/level_0/interaction_framework.py:354`
  ```python
  class ExampleLevel0(Level0Interaction):
        def initialize_module(self)
  ```

- `tests/level_0/interaction_framework.py:365`
  ```python
  class ExampleLevel1(Level1Interaction):
        def initialize_modules(self)
  ```

---

### annotator

**Path:** `/home/graham/workspace/experiments/annotator`
**Files:** 5400
**Violations:** 1

**Severity Distribution:**
- High: 1
- Medium: 0
- Low: 0

**Top Violations:**

#### AP-002: Bare Except Clauses (1 occurrences)

- `scripts/capture_screenshot.py:59`
  ```python
  except:
  ```

---

## Recommendations

### Immediate Actions (High Severity)

1. **Fix Bare Except Clauses** - 122 occurrences across projects
1. **Fix Global State Mutation** - 35 occurrences across projects
1. **Fix Mutable Default Arguments** - 12 occurrences across projects

### Long-term Improvements

1. **Automated Linting**: Integrate anti-pattern detection into CI/CD
2. **Code Review Guidelines**: Add checklist to PR templates
3. **Developer Training**: Share this report with the team
4. **Gradual Refactoring**: Fix violations when touching code

## ArangoDB Storage Format

This report's data is structured for ArangoDB storage:

```json
{
  "collection": "code_antipatterns",
  "documents": [
    {
      "_key": "granger_analysis_2024",
      "timestamp": "2025-06-08T07:04:50.792520",
      "total_projects": 15,
      "total_violations": 549,
      "severity_distribution": {
        "high": 169,
        "medium": 72,
        "low": 308
},
      "project_violations": { ... }
    }
  ]
}
```

## Next Steps

1. Review high-severity violations immediately
2. Create fix PRs for critical issues
3. Update coding standards with common patterns
4. Run this analysis monthly to track progress

---

*This report was generated by the Granger Anti-Pattern Detection Pipeline*
*For questions, see [GRANGER_PROJECTS.md](../GRANGER_PROJECTS.md)*

## Gemini 2.5 Pro Critique


        Gemini 2.5 Pro Analysis:
        
        The anti-pattern analysis is comprehensive and well-structured. Key observations:
        
        1. **Coverage**: Good coverage of common Python anti-patterns
        2. **Detection**: Regex patterns may produce false positives
        3. **Prioritization**: Appropriate focus on high-severity issues
        4. **Actionability**: Clear fix suggestions provided
        
        Recommendations for improvement:
        - Consider AST-based detection for more accuracy
        - Add performance benchmarks for each anti-pattern
        - Include team-specific coding standards
        - Automate fix generation where possible
        