# Granger Hub Architecture

## Overview

The Granger Hub (GH) is a central hub that enables different Granger-based projects to communicate with each other, share data, and coordinate workflows. It acts as a message broker and service registry for the entire ecosystem.

## How It Works

### 1. Service Registration

When a project starts up, it registers its available services with GH:



### 2. Service Discovery

Other projects can discover available services:



### 3. Inter-Project Communication

Projects communicate through standardized messages:



## Communication Flow



## Message Format

### Request


### Response


## Example: Marker ↔ ArangoDB Communication

This example shows how Marker and ArangoDB negotiate a schema for PDF extraction:

### Step 1: ArangoDB Requests Schema Format



### Step 2: Marker Provides Schema



### Step 3: Multiple Round Communication



### Step 4: Final Agreement



## Benefits

1. **Loose Coupling**: Projects don't need to know about each other's internals
2. **Service Discovery**: Dynamic discovery of available services
3. **Version Management**: Handle different schema versions gracefully
4. **Error Handling**: Centralized error handling and retry logic
5. **Monitoring**: Track all inter-project communications

## Implementation Details

The GH is implemented as:
- A Python package that can be imported by all projects
- A standalone MCP server for Claude Desktop integration
- A REST API for external integrations
- A message queue for asynchronous communication

## Setup

1. Install in your project:
   Defaulting to user installation because normal site-packages is not writeable

2. Configure in your project:
   

3. Register handlers:
   

## Troubleshooting

- Check GH server is running: 
- View logs: 
- Test connectivity: 
- List registered services: 