# GRANGER Integration Flow Diagrams

## Module Integration Patterns

### 1. ArXiv → Marker → ArangoDB Flow

```mermaid
flowchart TD
    Start([User Query:<br/>"quantum computing security"])
    
    subgraph "ArXiv Module"
        A1[Search Papers]
        A2{Papers Found?}
        A3[Extract Metadata]
        A4[Get PDF URLs]
        A5[Download PDFs]
    end
    
    subgraph "Marker Module"
        M1{Marker Available?}
        M2[Convert with Marker]
        M3[Try PyPDF2]
        M4[Try pdfplumber]
        M5[Basic Extraction]
        M6[Return Markdown]
    end
    
    subgraph "ArangoDB Module"
        D1[Fix Connection URL]
        D2[Adapt Parameters]
        D3[Create Document]
        D4{Success?}
        D5[Store in Cache]
        D6[Update Graph]
        D7[Return Error]
    end
    
    Start --> A1
    A1 --> A2
    A2 -->|Yes| A3
    A2 -->|No| End1([No Results])
    A3 --> A4
    A4 --> A5
    A5 --> M1
    
    M1 -->|Yes| M2
    M1 -->|No| M3
    M3 -->|Fail| M4
    M4 -->|Fail| M5
    M2 --> M6
    M3 --> M6
    M4 --> M6
    M5 --> M6
    
    M6 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    D4 -->|Yes| D5
    D5 --> D6
    D6 --> End2([Success])
    D4 -->|No| D7
    D7 --> End3([Failed])
    
    style Start fill:#aaf
    style End2 fill:#afa
    style End3 fill:#faa
    style M1 fill:#ff9
    style D4 fill:#ff9
```

### 2. SPARTA CVE Discovery Flow

```mermaid
flowchart LR
    subgraph "Input"
        I1[Vulnerability Keyword]
        I2[Limit: 10]
        I3[Time Range]
    end
    
    subgraph "SPARTA Processing"
        subgraph "API Selection"
            S1{API Available?}
            S2[NVD API]
            S3[MITRE Fallback]
            S4[Local Cache]
        end
        
        subgraph "Data Processing"
            P1[Parse CVE Data]
            P2[Extract Severity]
            P3[Format Description]
            P4[Add Metadata]
        end
        
        subgraph "Error Handling"
            E1[Rate Limit?]
            E2[Auth Error?]
            E3[Network Error?]
            E4[Apply Backoff]
        end
    end
    
    subgraph "Output"
        O1[CVE List]
        O2[Severity Scores]
        O3[Relationships]
    end
    
    I1 --> S1
    I2 --> S1
    I3 --> S1
    
    S1 -->|Yes| S2
    S1 -->|No| S3
    S3 -->|Fail| S4
    
    S2 --> E1
    E1 -->|Yes| E4
    E1 -->|No| P1
    E4 --> S2
    
    S2 --> E2
    E2 -->|Yes| S3
    
    S2 --> E3
    E3 -->|Yes| S4
    
    P1 --> P2
    P2 --> P3
    P3 --> P4
    
    P4 --> O1
    P4 --> O2
    P4 --> O3
    
    style S1 fill:#ff9
    style E1 fill:#faa
    style O1 fill:#afa
```

### 3. Full Pipeline Error Recovery Flow

```mermaid
stateDiagram-v2
    [*] --> Idle
    
    Idle --> Processing: New Request
    
    Processing --> CVESearch: Start Pipeline
    
    CVESearch --> CVEError: API Failure
    CVEError --> CVERetry: Retry Logic
    CVERetry --> CVESearch: Attempt 2
    CVERetry --> PaperSearch: Max Retries
    
    CVESearch --> PaperSearch: Success
    
    PaperSearch --> DownloadPDFs: Papers Found
    PaperSearch --> PartialResult: No Papers
    
    DownloadPDFs --> ConvertPDFs: PDFs Ready
    DownloadPDFs --> DownloadError: Network Issue
    DownloadError --> ParallelDownload: Switch Strategy
    ParallelDownload --> ConvertPDFs: Success
    
    ConvertPDFs --> MarkerError: Missing Dependency
    MarkerError --> FallbackChain: Use Fallback
    FallbackChain --> StoreData: Converted
    
    ConvertPDFs --> StoreData: Success
    
    StoreData --> ConnectionError: DB Issue
    ConnectionError --> FixURL: Correct URL
    FixURL --> StoreData: Retry
    
    StoreData --> UpdateGraph: Stored
    UpdateGraph --> Success: Complete
    
    PartialResult --> Success: With Warnings
    
    Success --> Idle: Reset
    
    note right of CVEError
        Circuit breaker may
        activate after 5 failures
    end note
    
    note right of FallbackChain
        Marker → PyPDF2 →
        pdfplumber → basic
    end note
```

### 4. Performance Optimization Impact

```mermaid
graph TB
    subgraph "Original Performance"
        O1[Search: 4.67s] --> O2[Download: 15s<br/>5 PDFs Sequential]
        O2 --> O3[Convert: 10s<br/>Sequential]
        O3 --> O4[Store: 5s<br/>Individual Inserts]
        O4 --> O5[Total: 34.67s]
    end
    
    subgraph "Optimizations"
        OP1[Add Cache<br/>LRU + Disk]
        OP2[Parallelize<br/>ThreadPool]
        OP3[Batch Ops<br/>Bulk Insert]
        OP4[Connection Pool<br/>Reuse]
    end
    
    subgraph "Optimized Performance"
        N1[Search: 0.1s<br/>98% Cache Hit] --> N2[Download: 3s<br/>5 PDFs Parallel]
        N2 --> N3[Convert: 2s<br/>Parallel Workers]
        N3 --> N4[Store: 0.2s<br/>Batch Insert]
        N4 --> N5[Total: 5.3s<br/>84.7% Faster]
    end
    
    O1 -.-> OP1 -.-> N1
    O2 -.-> OP2 -.-> N2
    O3 -.-> OP2 -.-> N3
    O4 -.-> OP3 -.-> N4
    O4 -.-> OP4 -.-> N4
    
    style O5 fill:#faa
    style N5 fill:#afa
    style OP1 fill:#ff9
    style OP2 fill:#ff9
    style OP3 fill:#ff9
    style OP4 fill:#ff9
```

### 5. Circuit Breaker State Machine

```mermaid
stateDiagram-v2
    [*] --> Closed: Initial State
    
    Closed --> Closed: Success
    Closed --> Closed: Failure < Threshold
    Closed --> Open: Failure >= Threshold
    
    Open --> HalfOpen: After Timeout
    Open --> Open: Reject Calls
    
    HalfOpen --> Closed: Test Success
    HalfOpen --> Open: Test Failure
    
    note right of Closed
        Normal operation
        All calls go through
    end note
    
    note right of Open
        Circuit broken
        Fast fail all calls
        Wait for timeout
    end note
    
    note right of HalfOpen
        Testing recovery
        Allow one call
        Monitor result
    end note
```

### 6. Cache Strategy Flow

```mermaid
flowchart TD
    Request[API Request]
    
    subgraph "Cache Layers"
        L1{In-Memory<br/>Cache?}
        L2{Disk<br/>Cache?}
        L3[Make API Call]
    end
    
    subgraph "Cache Management"
        M1[Check TTL]
        M2[Validate Data]
        M3[Update LRU]
        M4[Store Result]
    end
    
    Request --> L1
    L1 -->|Hit| M1
    L1 -->|Miss| L2
    
    M1 -->|Valid| M3
    M1 -->|Expired| L2
    
    L2 -->|Hit| M2
    L2 -->|Miss| L3
    
    M2 -->|Valid| M3
    M2 -->|Invalid| L3
    
    L3 --> M4
    M4 --> Response[Return Data]
    M3 --> Response
    
    M4 -.->|Update| L1
    M4 -.->|Update| L2
    
    style L1 fill:#aaf
    style L2 fill:#bbf
    style L3 fill:#faa
    style M4 fill:#afa
```

### 7. Parallel Processing Architecture

```mermaid
graph LR
    subgraph "Task Queue"
        Q1[Paper 1]
        Q2[Paper 2]
        Q3[Paper 3]
        Q4[Paper 4]
        Q5[Paper 5]
    end
    
    subgraph "Thread Pool (size=3)"
        W1[Worker 1]
        W2[Worker 2]
        W3[Worker 3]
    end
    
    subgraph "Processing"
        P1[Download PDF]
        P2[Convert to MD]
        P3[Store in DB]
    end
    
    Q1 --> W1
    Q2 --> W2
    Q3 --> W3
    Q4 -.->|Wait| W1
    Q5 -.->|Wait| W2
    
    W1 --> P1
    W2 --> P1
    W3 --> P1
    
    P1 --> P2
    P2 --> P3
    
    P3 --> Results[Completed: 5 papers in 3s<br/>vs 15s sequential]
    
    style W1 fill:#afa
    style W2 fill:#afa
    style W3 fill:#afa
    style Results fill:#ff9
```

### 8. Data Validation Pipeline

```mermaid
flowchart LR
    subgraph "Input Data"
        I1[Raw CVE Data]
        I2[ArXiv Metadata]
        I3[PDF Content]
    end
    
    subgraph "Validation Layer"
        subgraph "Schema Check"
            V1[Required Fields]
            V2[Type Validation]
            V3[Format Check]
        end
        
        subgraph "Sanitization"
            S1[Remove Nulls]
            S2[Truncate Long]
            S3[Escape Special]
        end
        
        subgraph "Enrichment"
            E1[Add Defaults]
            E2[Compute Fields]
            E3[Add Metadata]
        end
    end
    
    subgraph "Output"
        O1[Clean Data]
        O2[Error Report]
        O3[Warnings]
    end
    
    I1 --> V1
    I2 --> V1
    I3 --> V1
    
    V1 --> V2
    V2 --> V3
    
    V3 -->|Pass| S1
    V3 -->|Fail| O2
    
    S1 --> S2
    S2 --> S3
    S3 --> E1
    E1 --> E2
    E2 --> E3
    
    E3 --> O1
    E3 --> O3
    
    style V1 fill:#faa
    style E3 fill:#afa
```

### 9. Module Health Monitoring

```mermaid
graph TD
    subgraph "Health Checks"
        H1[API Connectivity]
        H2[Response Time]
        H3[Error Rate]
        H4[Queue Depth]
    end
    
    subgraph "Modules"
        M1[SPARTA<br/>✅ 40%]
        M2[ArXiv<br/>✅ 100%]
        M3[ArangoDB<br/>✅ 33%]
        M4[Marker<br/>⚠️ Fallback]
    end
    
    subgraph "Actions"
        A1[Normal Operation]
        A2[Degraded Mode]
        A3[Circuit Break]
        A4[Alert Team]
    end
    
    H1 --> M1
    H2 --> M1
    H3 --> M1
    H4 --> M1
    
    H1 --> M2
    H2 --> M2
    H3 --> M2
    H4 --> M2
    
    M1 -->|Healthy| A1
    M1 -->|Slow| A2
    M1 -->|Failed| A3
    
    M2 -->|Healthy| A1
    M3 -->|Issues| A2
    M4 -->|Degraded| A2
    
    A3 --> A4
    
    style M2 fill:#afa
    style M1 fill:#ff9
    style M3 fill:#ff9
    style M4 fill:#faa
```

### 10. Request Routing Logic

```mermaid
flowchart TD
    Request[Incoming Request]
    
    subgraph "Request Analysis"
        R1{Request Type?}
        R2{Module Status?}
        R3{Load Level?}
    end
    
    subgraph "Routing Decision"
        D1[Primary Route]
        D2[Fallback Route]
        D3[Cache Only]
        D4[Queue for Later]
    end
    
    subgraph "Execution"
        E1[Process Request]
        E2[Return Cached]
        E3[Add to Queue]
        E4[Use Fallback]
    end
    
    Request --> R1
    
    R1 -->|CVE| R2
    R1 -->|Paper| R2
    R1 -->|Store| R2
    
    R2 -->|Healthy| R3
    R2 -->|Degraded| D2
    R2 -->|Failed| D3
    
    R3 -->|Low| D1
    R3 -->|Medium| D1
    R3 -->|High| D4
    
    D1 --> E1
    D2 --> E4
    D3 --> E2
    D4 --> E3
    
    E1 --> Response[Return Result]
    E2 --> Response
    E3 --> Response
    E4 --> Response
    
    style R2 fill:#ff9
    style D1 fill:#afa
    style D3 fill:#faa
```

## Usage Notes

### Understanding the Flows
1. **Colors**: Green = Success, Red = Failure, Yellow = Decision Point
2. **Arrows**: Solid = Normal Flow, Dashed = Alternative/Error Flow
3. **Shapes**: Rectangles = Process, Diamonds = Decision, Rounded = Start/End

### Key Insights from Diagrams
1. **Error Recovery**: Multiple fallback paths ensure resilience
2. **Performance**: Parallel processing and caching provide major gains
3. **Flexibility**: System adapts to module availability
4. **Monitoring**: Health checks enable proactive management

### Integration Patterns Visualized
- **Fallback Chains**: Marker → PyPDF2 → pdfplumber → basic
- **Circuit Breakers**: Prevent cascading failures
- **Connection Pooling**: Reuse expensive connections
- **Batch Processing**: Group operations for efficiency

These diagrams complement the architecture diagrams by showing the dynamic behavior and flow of data through the GRANGER system during actual operation.