# GRANGER Architecture Visual Diagrams

## Overview
This document provides visual representations of the GRANGER system architecture, data flows, and integration patterns discovered during Phase 2 testing.

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        CVE[CVE Database<br/>NVD API]
        NASA[NASA APIs<br/>Mission Data]
        ARXIV[ArXiv<br/>Research Papers]
        YT[YouTube<br/>Transcripts]
    end
    
    subgraph "GRANGER Core"
        CMC[Claude Module<br/>Communicator<br/>🔄 Hub]
        
        subgraph "Processing Modules"
            SPARTA[SPARTA<br/>Cybersecurity]
            MARKER[Marker<br/>PDF→Markdown]
            LLMCALL[llm_call<br/>Multi-Tier LLM Router]
        end
        
        subgraph "Storage & Search"
            ARANGO[ArangoDB<br/>Knowledge Graph]
            MEMORY[Memory Agent<br/>Conversation Tracking]
        end
        
        subgraph "ML/RL"
            UNSLOTH[Unsloth<br/>Fine-tuning]
            RL[RL Commons<br/>Decision Making]
        end
    end
    
    subgraph "Outputs"
        API[API Gateway]
        UI[Web Interface]
        REPORTS[Reports]
    end
    
    CVE --> SPARTA
    NASA --> SPARTA
    ARXIV --> MARKER
    YT --> CMC
    
    SPARTA --> CMC
    MARKER --> CMC
    CMC --> LLMCALL
    CMC --> ARANGO
    
    ARANGO --> MEMORY
    ARANGO --> UNSLOTH
    RL --> CMC
    
    CMC --> API
    API --> UI
    API --> REPORTS
    
    style CMC fill:#f9f,stroke:#333,stroke-width:4px
    style ARANGO fill:#bbf,stroke:#333,stroke-width:2px
    style LLMCALL fill:#ff9,stroke:#333,stroke-width:2px
```

### LLM Infrastructure Note
The `llm_call` module provides intelligent routing across GRANGER's multi-tiered LLM infrastructure:
- **Claude API**: Complex reasoning and orchestration
- **Ollama**: Local inference for RL loops (zero latency)
- **RunPod**: 30B-70B model training and inference
- **LiteLLM**: Access to all frontier models

See [GRANGER_LLM_INFRASTRUCTURE.md](./GRANGER_LLM_INFRASTRUCTURE.md) for detailed architecture.

## 2. Data Flow Pipeline

```mermaid
flowchart LR
    subgraph "Phase 1: Discovery"
        A1[Search CVEs] --> A2[Find Vulnerabilities]
        A3[Search Papers] --> A4[Download PDFs]
    end
    
    subgraph "Phase 2: Processing"
        B1[Convert PDFs] --> B2[Extract Text]
        B3[Parse Metadata] --> B4[Generate Embeddings]
    end
    
    subgraph "Phase 3: Storage"
        C1[Store Documents] --> C2[Create Relationships]
        C3[Build Graph] --> C4[Index for Search]
    end
    
    subgraph "Phase 4: Intelligence"
        D1[Semantic Search] --> D2[Find Connections]
        D3[Generate Q&A] --> D4[Train Models]
    end
    
    A2 --> B3
    A4 --> B1
    B2 --> C1
    B4 --> C3
    C2 --> D1
    C4 --> D2
    D2 --> D3
    D3 --> D4
    
    style A1 fill:#faa,stroke:#333
    style D4 fill:#afa,stroke:#333
```

## 3. Module Integration Levels

```mermaid
graph TD
    subgraph "Level 0: Individual Modules"
        L0A[SPARTA<br/>✅ 40%]
        L0B[ArXiv<br/>✅ 100%]
        L0C[ArangoDB<br/>✅ 33%]
        L0D[Marker<br/>⚠️ Fallback]
    end
    
    subgraph "Level 1: Two-Module Pipelines"
        L1A[ArXiv → Marker<br/>✅ Working]
        L1B[Marker → ArangoDB<br/>⚠️ Issues]
        L1C[SPARTA → ArangoDB<br/>⚠️ Partial]
    end
    
    subgraph "Level 2: Three-Module Chains"
        L2A[ArXiv → Marker → ArangoDB<br/>⚠️ Storage Issues]
        L2B[SPARTA → ArXiv → ArangoDB<br/>⚠️ Integration Issues]
    end
    
    subgraph "Level 3: Full Pipeline"
        L3[Complete GRANGER Pipeline<br/>❌ 1/4 Modules Working]
    end
    
    L0A --> L1C
    L0B --> L1A
    L0C --> L1B
    L0D --> L1A
    
    L1A --> L2A
    L1B --> L2A
    L1C --> L2B
    
    L2A --> L3
    L2B --> L3
    
    style L0B fill:#afa,stroke:#333,stroke-width:2px
    style L3 fill:#faa,stroke:#333,stroke-width:2px
```

## 4. Error Handling Architecture

```mermaid
flowchart TB
    subgraph "Error Detection"
        E1[Connection Error]
        E2[Missing Dependency]
        E3[API Rate Limit]
        E4[Parameter Mismatch]
        E5[Data Validation]
    end
    
    subgraph "Recovery Strategies"
        R1[URL Correction]
        R2[Fallback Chain]
        R3[Rate Limiter]
        R4[Parameter Adapter]
        R5[Data Sanitizer]
    end
    
    subgraph "Resilience Patterns"
        P1[Retry Logic]
        P2[Circuit Breaker]
        P3[Bulkhead]
        P4[Timeout]
        P5[Compensation]
    end
    
    E1 --> R1 --> P1
    E2 --> R2 --> P3
    E3 --> R3 --> P2
    E4 --> R4 --> P5
    E5 --> R5 --> P4
    
    P1 --> S[Stable System]
    P2 --> S
    P3 --> S
    P4 --> S
    P5 --> S
    
    style S fill:#afa,stroke:#333,stroke-width:2px
```

## 5. Performance Optimization Flow

```mermaid
graph LR
    subgraph "Before Optimization"
        B1[Sequential Search<br/>4.67s] --> B2[Individual Downloads<br/>3-5s each]
        B2 --> B3[Single Inserts<br/>0.5s each]
        B3 --> B4[No Caching<br/>Repeated Work]
    end
    
    subgraph "Optimizations Applied"
        O1[Caching Layer<br/>98% Hit Rate]
        O2[Connection Pool<br/>10 Connections]
        O3[Parallel Processing<br/>5 Workers]
        O4[Batch Operations<br/>100 at Once]
    end
    
    subgraph "After Optimization"
        A1[Cached Search<br/>0.1s] --> A2[Parallel Downloads<br/>2.5s for 5]
        A2 --> A3[Batch Inserts<br/>1.2s for 100]
        A3 --> A4[Smart Caching<br/>No Repeated Work]
    end
    
    B1 -.->|Cache| O1 -.-> A1
    B2 -.->|Parallelize| O3 -.-> A2
    B3 -.->|Batch| O4 -.-> A3
    B4 -.->|Pool| O2 -.-> A4
    
    style B1 fill:#faa
    style A1 fill:#afa
```

## 6. Handler Communication Pattern

```mermaid
sequenceDiagram
    participant Client
    participant Handler
    participant Module
    participant ErrorHandler
    participant Cache
    
    Client->>Handler: handle(params)
    Handler->>Cache: check(key)
    
    alt Cache Hit
        Cache-->>Handler: cached_result
        Handler-->>Client: {"success": true, "data": cached_result}
    else Cache Miss
        Handler->>Module: process(params)
        
        alt Success
            Module-->>Handler: result
            Handler->>Cache: store(key, result)
            Handler-->>Client: {"success": true, "data": result}
        else Error
            Module-->>ErrorHandler: error
            ErrorHandler->>ErrorHandler: retry_logic()
            
            alt Retry Success
                ErrorHandler-->>Handler: result
                Handler-->>Client: {"success": true, "data": result}
            else Final Failure
                ErrorHandler-->>Handler: error_info
                Handler-->>Client: {"success": false, "error": error_info}
            end
        end
    end
```

## 7. Knowledge Graph Structure

```mermaid
graph TD
    subgraph "Document Nodes"
        D1[CVE-2023-1234]
        D2[ArXiv:2301.00123]
        D3[Research Paper X]
        D4[NASA Mission Y]
    end
    
    subgraph "Concept Nodes"
        C1[Buffer Overflow]
        C2[Memory Safety]
        C3[Quantum Computing]
        C4[Satellite Systems]
    end
    
    subgraph "Entity Nodes"
        E1[Author: Smith]
        E2[Organization: NASA]
        E3[Tool: SPARTA]
    end
    
    D1 -->|addresses| C1
    D1 -->|relates_to| C2
    D2 -->|discusses| C1
    D2 -->|authored_by| E1
    D3 -->|mentions| D1
    D3 -->|uses| E3
    D4 -->|managed_by| E2
    D4 -->|requires| C4
    
    C1 -->|type_of| C2
    C3 -->|impacts| C4
    
    style D1 fill:#faa
    style D2 fill:#afa
    style C1 fill:#aaf
```

## 8. Testing Architecture

```mermaid
flowchart TD
    subgraph "Test Levels"
        T0[Level 0: Unit Tests<br/>Individual Modules]
        T1[Level 1: Integration Tests<br/>Two Modules]
        T2[Level 2: Chain Tests<br/>Three Modules]
        T3[Level 3: E2E Tests<br/>Full Pipeline]
    end
    
    subgraph "Test Types"
        TT1[Real API Tests]
        TT2[Performance Tests]
        TT3[Error Recovery Tests]
        TT4[Load Tests]
    end
    
    subgraph "Validation"
        V1[Duration Check<br/>>0.1s = Real]
        V2[Data Validation]
        V3[Error Handling]
        V4[Performance Metrics]
    end
    
    T0 --> TT1
    T1 --> TT2
    T2 --> TT3
    T3 --> TT4
    
    TT1 --> V1
    TT2 --> V4
    TT3 --> V3
    TT4 --> V2
    
    V1 --> R[Test Report]
    V2 --> R
    V3 --> R
    V4 --> R
    
    style R fill:#ff9,stroke:#333,stroke-width:2px
```

## 9. Deployment Architecture

```mermaid
graph TB
    subgraph "Development"
        DEV[Local Development<br/>Docker Compose]
    end
    
    subgraph "Testing"
        TEST[Test Environment<br/>Real APIs]
    end
    
    subgraph "Production"
        subgraph "Frontend"
            LB[Load Balancer]
            API1[API Gateway 1]
            API2[API Gateway 2]
        end
        
        subgraph "Processing"
            W1[Worker Pool 1<br/>ArXiv/Marker]
            W2[Worker Pool 2<br/>SPARTA/CVE]
            W3[Worker Pool 3<br/>ML/Training]
        end
        
        subgraph "Storage"
            DB1[(ArangoDB<br/>Primary)]
            DB2[(ArangoDB<br/>Replica)]
            CACHE[(Redis<br/>Cache)]
        end
    end
    
    DEV -->|CI/CD| TEST
    TEST -->|Deploy| LB
    
    LB --> API1
    LB --> API2
    
    API1 --> W1
    API1 --> W2
    API2 --> W2
    API2 --> W3
    
    W1 --> DB1
    W2 --> DB1
    W3 --> DB1
    
    DB1 -.->|Sync| DB2
    W1 --> CACHE
    W2 --> CACHE
    
    style LB fill:#f9f,stroke:#333,stroke-width:2px
    style DB1 fill:#bbf,stroke:#333,stroke-width:2px
```

## 10. RL Decision Flow

```mermaid
flowchart LR
    subgraph "Context"
        C1[Query Type]
        C2[Module Status]
        C3[Load Metrics]
        C4[Error History]
    end
    
    subgraph "RL Agent"
        A1[State<br/>Encoder]
        A2[Policy<br/>Network]
        A3[Action<br/>Selector]
    end
    
    subgraph "Actions"
        D1[Route to ArXiv]
        D2[Route to SPARTA]
        D3[Use Cache]
        D4[Retry Failed]
        D5[Circuit Break]
    end
    
    subgraph "Rewards"
        R1[Success +10]
        R2[Failure -5]
        R3[Timeout -10]
        R4[Cache Hit +5]
    end
    
    C1 --> A1
    C2 --> A1
    C3 --> A1
    C4 --> A1
    
    A1 --> A2
    A2 --> A3
    
    A3 --> D1
    A3 --> D2
    A3 --> D3
    A3 --> D4
    A3 --> D5
    
    D1 --> R1
    D2 --> R2
    D3 --> R4
    D4 --> R3
    
    R1 --> A2
    R2 --> A2
    R3 --> A2
    R4 --> A2
    
    style A2 fill:#f9f,stroke:#333,stroke-width:2px
```

## Diagram Usage Guide

### Viewing Diagrams
1. **GitHub**: Automatically renders Mermaid diagrams
2. **VS Code**: Install "Markdown Preview Mermaid Support" extension
3. **Online**: Use [Mermaid Live Editor](https://mermaid.live/)
4. **Export**: Can export as PNG/SVG for presentations

### Updating Diagrams
1. Edit the Mermaid code blocks directly
2. Follow Mermaid syntax guidelines
3. Test in live editor before committing
4. Keep diagrams focused and readable

### Integration Status Legend
- ✅ Fully working
- ⚠️ Partially working / Has issues
- ❌ Not working / Major issues
- 🔄 In progress

## Summary

These visual diagrams capture the GRANGER architecture and key insights from Phase 2 testing:

1. **Architecture**: Hub-and-spoke with CMC at center
2. **Data Flow**: Four-phase pipeline from discovery to intelligence
3. **Integration Levels**: Progressive complexity testing approach
4. **Error Handling**: Comprehensive recovery strategies
5. **Performance**: 67% improvement through optimizations
6. **Communication**: Standardized handler pattern
7. **Knowledge Graph**: Rich interconnected data model
8. **Testing**: Multi-level validation approach
9. **Deployment**: Scalable production architecture
10. **RL Integration**: Intelligent routing decisions

These diagrams serve as visual documentation for developers, architects, and stakeholders to understand the GRANGER system at a glance.