# 🗺️ Visual Project Map

A visual guide to navigating the shared_claude_docs project.

## 🏗️ Project Structure Overview

```mermaid
graph TD
    A[shared_claude_docs] --> B[testing/]
    A --> C[analysis/]
    A --> D[docs/]
    A --> E[utils/]
    A --> F[guides/]
    
    B --> B1[interaction_tests/]
    B --> B2[visualization_tests/]
    B --> B3[self_evolution/]
    B --> B4[integration_tests/]
    
    C --> C1[project_analysis/]
    C --> C2[research_tools/]
    
    D --> D1[big_picture/]
    D --> D2[architecture/]
    D --> D3[tutorials/]
    
    B1 --> B1a[interaction_test_framework.py]
    B1 --> B1b[interaction_runner.py]
    B1 --> B1c[stress_test_interactions.py]
    
    B2 --> B2a[visualization_decision_tests.py]
    B2 --> B2b[arangodb_visualization_interactions.py]
    
    B3 --> B3a[self_evolving_analyzer.py]
    B3 --> B3b[demo_self_evolution.py]
    
    C1 --> C1a[big_picture_analyzer.py]
    C1 --> C1b[enhanced_big_picture_analyzer.py]
    
    C2 --> C2a[research_driven_improvements.py]
    
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
    style D fill:#ffb,stroke:#333,stroke-width:2px
```

## 🎯 Purpose-Based Navigation

### "I want to TEST something"

```mermaid
graph LR
    A[What to test?] --> B{Type?}
    B --> C[Module Interactions]
    B --> D[Visualization Logic]
    B --> E[Self-Evolution]
    B --> F[Full Integration]
    
    C --> C1[testing/interaction_tests/]
    D --> D1[testing/visualization_tests/]
    E --> E1[testing/self_evolution/]
    F --> F1[testing/integration_tests/]
    
    style A fill:#f9f
    style B fill:#bbf
```

### "I want to ANALYZE something"

```mermaid
graph LR
    A[What to analyze?] --> B{Type?}
    B --> C[Project Codebase]
    B --> D[Research Improvements]
    
    C --> C1[analysis/project_analysis/]
    D --> D1[analysis/research_tools/]
    
    style A fill:#f9f
    style B fill:#bfb
```

### "I want to LEARN something"

```mermaid
graph LR
    A[What to learn?] --> B{Topic?}
    B --> C[Interaction Levels]
    B --> D[System Architecture]
    B --> E[How-to Guides]
    B --> F[Testing Guide]
    
    C --> C1[docs/big_picture/MODULE_INTERACTION_LEVELS.md]
    D --> D1[docs/architecture/]
    E --> E1[docs/tutorials/]
    F --> F1[docs/INTERACTION_TESTING_GUIDE.md]
    
    style A fill:#f9f
    style B fill:#ffb
```

## 📊 Interaction Level Testing Flow

```mermaid
graph TB
    subgraph "Level 0: Direct Calls"
        L0[Single Module] --> L0R[Result]
    end
    
    subgraph "Level 1: Sequential"
        L1A[Module A] --> L1B[Module B] --> L1C[Module C]
    end
    
    subgraph "Level 2: Parallel"
        L2S[Start] --> L2A[Module A]
        L2S --> L2B[Module B]
        L2A --> L2M[Merge]
        L2B --> L2M
    end
    
    subgraph "Level 3: Orchestrated"
        L3O[Orchestrator] --> L3A[Module A]
        L3O --> L3B[Module B]
        L3A --> L3F[Feedback]
        L3B --> L3F
        L3F --> L3O
    end
    
    style L0 fill:#e1f5fe
    style L1A fill:#f3e5f5
    style L2S fill:#e8f5e9
    style L3O fill:#fff3e0
```

## 🔄 Development Workflow

```mermaid
graph LR
    A[1. Develop] --> B[2. Test]
    B --> C[3. Document]
    C --> D[4. Analyze]
    D --> E[5. Deploy]
    
    A --> A1[testing/*/]
    B --> B1[Run test frameworks]
    C --> C1[docs/*/]
    D --> D1[analysis/*/]
    E --> E1[claude-module-communicator]
    
    style A fill:#bbf
    style B fill:#bfb
    style C fill:#ffb
    style D fill:#fbf
    style E fill:#fbb
```

## 📈 Testing Hierarchy

```mermaid
graph TD
    A[All Tests] --> B[Unit Tests]
    A --> C[Integration Tests]
    A --> D[System Tests]
    
    B --> B1[Level 0: Direct Calls]
    
    C --> C1[Level 1: Sequential]
    C --> C2[Level 2: Parallel]
    
    D --> D1[Level 3: Orchestrated]
    D --> D2[Self-Evolution]
    D --> D3[Full System]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#e3f2fd
    style C fill:#f3e5f5
    style D fill:#e8f5e9
```

## 🎨 Color Legend

- 🟦 **Blue**: Testing-related
- 🟩 **Green**: Analysis tools
- 🟨 **Yellow**: Documentation
- 🟪 **Purple**: Main directories
- 🟧 **Orange**: Workflows

---

*This visual map helps you quickly navigate to the right part of the project based on your needs.*