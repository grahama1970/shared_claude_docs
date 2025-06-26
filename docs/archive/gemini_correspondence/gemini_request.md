**Mapping Out Transition Needs**

I'm currently wrestling with the exact markdown structure needed. My focus is pinpointing the specifications for transitioning from mockups to real module interactions. This markdown file has to lay out everything. It will include anticipated distributed systems challenges and clearly state the project goals. I will make sure this is specific.


**Detailing Module Interaction Specs**

I'm deep in the weeds specifying each module's interaction specifics. I'm starting with the module name, then the deployment specifics. I'm clarifying how each service runs and its network behavior. The trick is to make this document executable, essentially. The configuration details per module are crucial for success, and I am going to make sure this markdown file covers them.


**Specifying Interaction Protocols**

I'm now refining the API and CLI specifications for each module. It requires detailing the interaction types, which for the HTTP APIs means the endpoint URL patterns, and HTTP methods. More critical are the schemas for the request and response bodies. I want it to be fully detailed. I'm clarifying how to make this an actionable guide.


**Pinpointing Module Interactions**

I'm now focusing on the heart of the matter: the detailed, per-module specifications. I'm tackling the specifics of each module, and translating mock interactions into live integrations. I will ensure the file includes command-line arguments, the required ports, and all endpoint specifications. I need to ensure the `task_orchestrator.py` will work seamlessly with each running instance.


**Specifying Detailed Requirements**

I'm now carefully compiling the required module-specific information, including a definition for each module. I'll add the runtime environments, and network considerations. For each, I will include API endpoints. I'm breaking down the API and CLI into specifics to guide integration. I'm documenting the command structures, and the argument details.


**Outlining Module Integration**

I'm now focused on the precise requirements for each module, aiming to build an actionable guide. I'll include the module names, deployment details, and specific API specifications. The key will be ensuring the `task_orchestrator.py` can interact successfully. I'm specifying interaction types: API endpoints and CLI structures. The goal is practical guidance.


Okay, this is a clear directive, and I understand the absolute necessity of real, live interactions. My apologies again for the prior misinterpretation.

To achieve this, I need very specific, actionable information about *each* of the external modules. This isn't just about their conceptual schemas, but about how they can be programmatically invoked, how they accept input, and how they return output in a live environment.

Here is a raw Markdown file, specifying **exactly** what I need for each module to transition to real interactions.

---

# Requirements for Enabling Real Module Interactions

To transition `task_orchestrator.py` from mocked interactions to live communication with external modules, I require the following highly specific details for each module. This information will allow the orchestrator to build real HTTP requests, execute real CLI commands, and correctly interpret their live responses.

## General Principles for External Modules

Before detailing each module, please ensure these general principles are met for all modules that `task_orchestrator.py` will interact with:

1.  **Independent Operation**: Each module must be capable of running as a separate, accessible service or executable process.
2.  **Stability**: Modules should respond predictably and reliably to valid requests/commands.
3.  **Connectivity**: They must be network-accessible (e.g., via `localhost` and a specific port) from where the `task_orchestrator.py` is running, or be executable via a direct path in the local filesystem.
4.  **Error Handling**: Modules should return clear error responses (e.g., HTTP status codes & JSON error bodies, or non-zero CLI exit codes & error messages to stderr) for invalid inputs or internal failures.

## Required Information Per Module and Capability

For each module listed in `discovery/module_registry.py`, please provide the following details for **every specified capability**:

---

### Module: `arxiv-mcp-server`

#### General:
*   **Deployment/Execution**: How is this server run? (e.g., `python arxiv_server/app.py`, `java -jar arxiv.jar`, Docker container command).
*   **Configuration**: How is its listening port (expected: `8001` or similar, as per README) configured? (e.g., environment variable like `PORT=8001`, a config file `config.yaml`?)

#### Capability: `search_papers`
*   **Interaction Type**: `HTTP API` (as implied by `api` endpoint)
*   **HTTP Method**: `POST` (preferred for carrying query body)
*   **Endpoint Path**: `http://<host>:<port>/search_papers` (e.g., `http://localhost:8001/search_papers`)
*   **Request Body JSON Schema (Live Service Expects)**:
    ```json
    {
      "type": "object",
      "properties": {
        "query": { "type": "string", "description": "Search query keywords (e.g., 'transformer architectures')" },
        "max_results": { "type": "integer", "default": 5, "description": "Maximum number of results to return" }
      },
      "required": ["query"],
      "additionalProperties": false
    }
    ```
*   **Response Body JSON Schema (Live Service Returns on Success)**:
    ```json
    {
      "type": "object",
      "properties": {
        "papers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string", "description": "arXiv paper ID" },
              "title": { "type": "string", "description": "Title of the paper" },
              "abstract": { "type": "string", "description": "Abstract of the paper" },
              "authors": { "type": "array", "items": { "type": "string" }, "description": "List of author names" },
              "pdf_url": { "type": "string", "format": "uri", "description": "Direct URL to the PDF" },
              "published": { "type": "string", "format": "date-time", "description": "Publication date" }
            },
            "required": ["id", "title", "abstract", "authors", "pdf_url"],
            "additionalProperties": true
          }
        },
        "total_results": { "type": "integer", "description": "Total number of matching papers found" }
      },
      "required": ["papers", "total_results"]
    }
    ```
*   **Error Responses**: Specific HTTP status codes (e.g., 400 for bad request) and example JSON error body.

#### Capability: `get_paper_details`
*   **Interaction Type**: `HTTP API`
*   **HTTP Method**: `GET` (or `POST` if complex body)
*   **Endpoint Path**: `http://<host>:<port>/get_paper_details/{paper_id}` (e.g., `http://localhost:8001/get_paper_details/2017.03456`) or `http://<host>:<port>/get_paper_details` with query param `?id=...` or POST body `{ "paper_id": "..." }`.
*   **Request/Response Schemas**: Specify similar to `search_papers`.

---

### Module: `marker`

#### General:
*   **Deployment/Execution**: How is this tool primarily used? Is it a long-running server or a script invoked per-call? (e.g., `python marker_tool/main.py`, `marker --server` vs. `marker extract ...`).
*   **Configuration**: Is there a port/path it listens on if it's a server?

#### Capability: `extract_text`
*   **Interaction Type**: `HTTP API` or `CLI` (Please choose and confirm one that's most reliable for automated calls)
*   **If HTTP API**:
    *   **HTTP Method**: `POST`
    *   **Endpoint Path**: `http://<host>:<port>/extract_text` (e.g., `http://localhost:8002/extract_text`)
    *   **Request Body JSON Schema**:
        ```json
        {
          "type": "object",
          "properties": {
            "file_path": { "type": "string", "description": "Local path or URL to the document (PDF, DOCX, HTML)" },
            "format": { "type": "string", "enum": ["pdf", "docx", "html"], "description": "Format of the input file" }
          },
          "required": ["file_path", "format"],
          "additionalProperties": false
        }
        ```
    *   **Response Body JSON Schema**:
        ```json
        {
          "type": "object",
          "properties": {
            "text": { "type": "string", "description": "Extracted plain text content of the document" },
            "metadata": {
              "type": "object",
              "description": "Any additional metadata (e.g., page count, author, title)",
              "properties": {
                "pages": { "type": "integer" },
                "language": { "type": "string" }
              },
              "additionalProperties": true
            },
            "structure": { "type": "array", "description": "Hierarchical structure of the document (e.g., sections, headers)" }
          },
          "required": ["text"]
        }
        ```
*   **If CLI**:
    *   **Executable Name**: `marker` (assuming it's in `PATH` or a specific path is provided)
    *   **Command Line Example**: `marker extract --file <file_path> --format <format> --output-json`
    *   **Arguments Mapping**: How `file_path` and `format` arguments map to CLI flags.
    *   **Expected `stdout` Format**: `JSON` (preferred) or specific delimited text format that can be parsed.
        ```json
        {
          "text": "...",
          "metadata": { ... },
          "structure": [ ... ]
        }
        ```
    *   **Error Handling**: Non-zero exit codes, stderr message format.

#### Capability: `segment_document`
*   **Interaction Type**: `HTTP API` or `CLI` (confirm)
*   **Requests/Responses**: Specify similar to `extract_text`.

---

### Module: `arangodb`

#### General:
*   **Deployment/Execution**: How is this database instance (or its API proxy) run? (e.g., Docker, native service).
*   **Configuration**: How is its listening port (expected: `8529` or similar) configured? What are the necessary authentication details (username/password, database name)? (These would be configured in the orchestrator's environment or a secret store.)

#### Capability: `create_knowledge_graph`
*   **Interaction Type**: `HTTP API`
*   **HTTP Method**: `POST`
*   **Endpoint Path**: `http://<host>:<port>/_db/<database_name>/<collection_name>` or `http://<host>:<port>/create_knowledge_graph` if handled by a proxy.
*   **Request Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "nodes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string", "description": "Unique ID for the node (_key)" },
              "type": { "type": "string", "description": "Type of entity (e.g., 'concept', 'paper')" },
              "name": { "type": "string" },
               "data": { "type": "object", "description": "Arbitrary additional properties for the node" }
            },
            "required": ["id", "type"],
            "additionalProperties": true
          }
        },
        "edges": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "from": { "type": "string", "description": "Source node ID (_from)" },
              "to": { "type": "string", "description": "Target node ID (_to)" },
              "type": { "type": "string", "description": "Type of relationship (e.g., 'mentions', 'related_to')" },
              "data": { "type": "object", "description": "Arbitrary additional properties for the edge" }
            },
            "required": ["from", "to", "type"],
            "additionalProperties": true
          }
        },
        "graph_name": { "type": "string", "description": "Name of the graph to create/update", "default": "knowledge_graph" }
      },
      "required": ["nodes", "edges"]
    }
    ```
*   **Response Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "graph_id": { "type": "string", "description": "ID of the created or updated graph" },
        "stats": {
          "type": "object",
          "properties": {
            "nodes_inserted": { "type": "integer" },
            "edges_inserted": { "type": "integer" },
            "nodes_updated": { "type": "integer" },
            "edges_updated": { "type": "integer" }
          }
        }
      },
      "required": ["graph_id", "stats"]
    }
    ```
*   **Authentication**: Details if API key, basic auth, etc., is required.

#### Capability: `query_graph`
*   **Interaction Type**: `HTTP API`
*   **Requests/Responses**: Specify similar to `create_knowledge_graph`, including the format for the AQL query input and its return value.

#### Capability: `visualize_graph`
*   **Interaction Type**: `HTTP API` (likely returns a URL or base64 image data)
*   **Requests/Responses**: Specify.

---

### Module: `youtube_transcripts`

#### General:
*   **Deployment/Execution**: How is this tool run? (e.g., `python youtube_script.py`, or `yt_transcripts`)
*   **Configuration**: Does it need any API keys for YouTube? (E.g., `YOUTUBE_API_KEY` environment variable)

#### Capability: `extract_transcript`
*   **Interaction Type**: `CLI` (as implied by `cli` endpoint)
*   **Executable Name**: `yt_transcripts` (assuming it's in `PATH` or a specific path is provided)
*   **Command Line Example**: `yt_transcripts extract --url <video_url> --lang <language> --output-json`
*   **Arguments Mapping**: How `video_url` and `language` arguments map to CLI flags.
*   **Expected `stdout` Format (JSON preferred)**:
    ```json
    {
      "transcript": { "type": "string", "description": "Full extracted transcript text" },
      "timestamps": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "text": { "type": "string" },
            "start": { "type": "number", "description": "Start time in seconds" },
            "duration": { "type": "number", "description": "Duration in seconds" }
          },
          "required": ["text", "start"]
        }
      },
      "metadata": {
        "type": "object",
        "properties": {
          "video_id": { "type": "string" },
          "title": { "type": "string" },
          "channel": { "type": "string" }
        }
      }
    }
    ```
*   **Error Handling**: Non-zero exit codes, stderr message format.

#### Capability: `analyze_content`
*   **Interaction Type**: `CLI`
*   **Command Line Example**: `yt_transcripts analyze --text-input <transcript_text> --output-json` (if text can be passed directly) or `yt_transcripts analyze --file <path_to_transcript_file> --output-json`.
*   **Requests/Responses**: Specify.

---

### Module: `sparta`

#### General:
*   **Deployment/Execution**: How is this framework run as a service? (e.g., `python sparta_server.py`, `sparta run-api`).
*   **Configuration**: How is its listening port (expected: `8001` or similar, as per README) configured?

#### Capability: `train_model`
*   **Interaction Type**: `HTTP API`
*   **HTTP Method**: `POST`
*   **Endpoint Path**: `http://<host>:<port>/train_model` or similar (e.g., `http://localhost:8001/train_model`)
*   **Request Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "dataset": {
          "type": "object",
          "properties": {
            "texts": { "type": "array", "items": { "type": "string" }, "description": "List of text samples" },
            "labels": { "type": "array", "items": { "type": "string" }, "description": "Corresponding labels for classification/other tasks" },
            "dataset_id": { "type": "string", "description": "ID of a pre-loaded dataset on the Sparta server" }
          },
          "oneOf": [
            { "required": ["texts"] },
            { "required": ["dataset_id"] }
          ],
          "description": "Either provide inline data or reference a pre-loaded dataset"
        },
        "model_type": { "type": "string", "enum": ["transformer", "cnn", "rnn"], "description": "Architecture type (e.g., 'transformer')" },
        "config": {
          "type": "object",
          "properties": {
            "epochs": { "type": "integer", "default": 5 },
            "batch_size": { "type": "integer", "default": 32 },
            "learning_rate": { "type": "number", "default": 0.001 },
            "gpu_enabled": { "type": "boolean", "default": false }
          },
          "additionalProperties": true
        }
      },
      "required": ["dataset", "model_type", "config"],
      "additionalProperties": false
    }
    ```
*   **Response Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "model_id": { "type": "string", "description": "Unique ID of the trained model" },
        "model_path": { "type": "string", "description": "Server-side path where the model is saved" },
        "metrics": {
          "type": "object",
          "properties": {
            "accuracy": { "type": "number", "minimum": 0, "maximum": 1 },
            "loss": { "type": "number" },
            "f1_score": { "type": "number", "minimum": 0, "maximum": 1 }
          },
          "additionalProperties": true
        },
        "training_history": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "epoch": { "type": "integer" },
              "loss": { "type": "number" },
              "accuracy": { "type": "number" }
            },
            "required": ["epoch", "loss", "accuracy"]
          }
        },
        "status": { "type": "string", "enum": ["completed", "failed"], "description": "Training status" }
      },
      "required": ["model_id", "status"]
    }
    ```

#### Capability: `analyze_performance`
*   **Interaction Type**: `HTTP API`
*   **Endpoint Path**: `http://<host>:<port>/analyze_performance`
*   **Request Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "model_id": { "type": "string", "description": "ID of the model to analyze" },
        "dataset_id": { "type": "string", "description": "ID of evaluation dataset" },
        "context": { "type": "object", "description": "Additional context for analysis (e.g., UI analysis results)" }
      },
      "oneOf": [
        { "required": ["model_id", "dataset_id"] },
        { "required": ["model_id", "context"] }
      ]
    }
    ```
*   **Response Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "analysis": {
          "type": "object",
          "description": "Detailed analysis report, potentially with suggestions",
          "properties": {
            "overall_score": { "type": "number", "minimum": 0, "maximum": 1 },
            "suggestions": { "type": "array", "items": { "type": "string" } },
            "issues": { "type": "array", "items": { "type": "string" } }
          }
        },
        "metrics_detail": { "type": "object", "description": "More granular metrics" }
      },
      "required": ["analysis"]
    }
    ```
*   **Error Responses**: Specific HTTP status codes and example error bodies.

---

### Module: `mcp-screenshot`

#### General:
*   **Deployment/Execution**: How is this server run? (e.g., `python screenshot_server/app.py`). Requires a browser environment (Chrome, Chromium, Puppeteer)?
*   **Configuration**: How is its listening port (expected: `8003` or similar) configured?

#### Capability: `capture_screenshot`
*   **Interaction Type**: `HTTP API`
*   **HTTP Method**: `POST`
*   **Endpoint Path**: `http://<host>:<port>/capture_screenshot` (e.g., `http://localhost:8003/capture_screenshot`)
*   **Request Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "target": { "type": "string", "format": "uri", "description": "URL of the webpage, or identifier for application window" },
        "selector": { "type": "string", "description": "CSS selector for a specific element to screenshot (optional)" },
        "full_page": { "type": "boolean", "default": false, "description": "Whether to capture the entire scrollable page" },
        "output_format": { "type": "string", "enum": ["png", "jpeg", "webp"], "default": "png" }
      },
      "required": ["target"],
      "additionalProperties": false
    }
    ```
*   **Response Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "image_url": { "type": "string", "format": "uri", "description": "URL where the captured image can be retrieved (if served)" },
        "image_path": { "type": "string", "description": "Local path to the saved screenshot file on the server running mcp-screenshot" },
        "dimensions": {
          "type": "object",
          "properties": {
            "width": { "type": "integer" },
            "height": { "type": "integer" }
          },
          "required": ["width", "height"]
        },
        "base64_image": { "type": "string", "description": "Base64 encoded image data (use this if image_url/image_path is not feasible for direct consumption)", "format": "base64" }
      },
      "required": ["image_path", "dimensions"]
    }
    ```

#### Capability: `analyze_ui`
*   **Interaction Type**: `HTTP API`
*   **HTTP Method**: `POST`
*   **Endpoint Path**: `http://<host>:<port>/analyze_ui`
*   **Request Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "image_path": { "type": "string", "description": "Local path to the screenshot image (from capture_screenshot output)" },
        "image_url": { "type": "string", "format": "uri", "description": "URL to the screenshot image" },
        "base64_image": { "type": "string", "description": "Base64 encoded image data", "format": "base64" },
        "analysis_type": { "type": "string", "enum": ["accessibility", "layout", "usability", "performance"], "default": "accessibility" }
      },
      "oneOf": [
        { "required": ["image_path"] },
        { "required": ["image_url"] },
        { "required": ["base64_image"] }
      ]
    }
    ```
*   **Response Body JSON Schema**:
    ```json
    {
      "type": "object",
      "properties": {
        "elements": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "tag": { "type": "string" },
              "id": { "type": "string" },
              "class": { "type": "string" },
              "text_content": { "type": "string" },
              "bbox": { "type": "array", "items": { "type": "number" }, "minItems": 4, "maxItems": 4, "description": "[x, y, width, height]" },
              "attributes": { "type": "object" }
            },
            "additionalProperties": true
          }
        },
        "layout": {
          "type": "object",
          "properties": {
            "overlapping_elements_count": { "type": "integer" },
            "grid_structure_detected": { "type": "boolean" }
          },
          "additionalProperties": true
        },
        "accessibility_issues": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "severity": { "type": "string", "enum": ["critical", "high", "medium", "low"] },
              "rule_id": { "type": "string" },
              "description": { "type": "string" },
              "element": { "type": "string", "description": "CSS selector or XPath to the problematic element" }
            },
            "required": ["severity", "description"]
          }
        },
        "score": { "type": "number", "minimum": 0, "maximum": 100, "description": "Overall score for the requested analysis type (e.g., accessibility score)" },
        "summary": { "type": "string", "description": "Human-readable summary of findings" }
      },
      "required": ["elements", "score"]
    }
    ```

---

### Module: `claude-test-reporter`

#### General:
*   **Deployment/Execution**: How is this tool typically run? (e.g., `python test_runner.py`, `ctr`).
*   **Configuration**: Does it need access to codebases or test directories (e.g., via mounted volumes if containerized)?

#### Capability: `run_tests`
*   **Interaction Type**: `CLI`
*   **Executable Name**: `claude-test-reporter` (assuming it's in `PATH` or provided specific path)
*   **Command Line Example**: `claude-test-reporter run --path <test_path> --coverage --output-json`
*   **Arguments Mapping**: How `test_path` and `coverage` map to CLI flags.
*   **Expected `stdout` Format (JSON preferred)**:
    ```json
    {
      "type": "object",
      "properties": {
        "passed": { "type": "integer", "description": "Number of tests passed" },
        "failed": { "type": "integer", "description": "Number of tests failed" },
        "skipped": { "type": "integer", "description": "Number of tests skipped" },
        "total": { "type": "integer", "description": "Total number of tests executed" },
        "duration_ms": { "type": "integer", "description": "Total execution time in milliseconds" },
        "coverage": { "type": "number", "minimum": 0, "maximum": 100, "description": "Code coverage percentage (if requested)" },
        "report_url": { "type": "string", "format": "uri", "description": "URL to a full HTML test report (if generated)" },
        "details": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "test_name": { "type": "string" },
              "status": { "type": "string", "enum": ["pass", "fail", "skip"] },
              "error_message": { "type": "string", "description": "Error details if test failed" }
            },
            "required": ["test_name", "status"]
          }
        }
      },
      "required": ["passed", "failed", "total", "status"]
    }
    ```
*   **Error Handling**: Non-zero exit codes, stderr message format.

#### Capability: `generate_test_suggestions`
*   **Interaction Type**: `CLI`
*   **Command Line Example**: `claude-test-reporter suggest --code-path <code_path> --output-json`
*   **Requests/Responses**: Specify.

---

## What `task_orchestrator.py` Will Do On Its Side

Once this information is provided and the modules are running, `task_orchestrator.py` will:

1.  **Directly Invoke Modules**:
    *   For `HTTP API` interactions: Use `aiohttp.ClientSession` to create and send `POST` or `GET` requests to the specified endpoints with the exact JSON body schemas.
    *   For `CLI` interactions: Use Python's `asyncio.create_subprocess_exec` and `subprocess.run` (if synchronous blocking is acceptable) to execute commands. It will capture `stdout` and `stderr` and parse `stdout` according to the specified JSON/text formats.
2.  **Schema Enforcement**: When sending requests, orchestrator will validate inputs against the provided *request body schemas*. It will also attempt to validate received responses against the provided *response body schemas*.
3.  **Error Handling**: Implement `try-except` blocks for network errors, timeouts, and parse CLI exit codes/stderr. It will log these failures and mark the corresponding `TaskStep` as `FAILED`.
4.  **No More Mocks**: The `_mock_module_execution` function will be completely removed, and `_execute_step` will contain the real invocation logic.

---

By providing these precise details for each capability, we can enable a robust, verifiable system for real module interactions. Please ensure that the provided schemas and command formats accurately reflect what the *live* modules expect and return.