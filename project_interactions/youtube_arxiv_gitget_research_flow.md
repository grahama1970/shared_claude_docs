# YouTube → ArXiv → GitGet Research Flow

## Overview

This document describes the seamless interaction between YouTube Transcripts, ArXiv MCP Server, and GitGet for building a comprehensive research knowledge graph in ArangoDB.

## Agent API

### Simple One-Line Call

```python
# For agents (including Claude), it's this simple:
result = await process_research_video("https://www.youtube.com/watch?v=ABC123")
```

That's it! This single call triggers the entire pipeline.

## What Happens Behind the Scenes

### 1. YouTube Processing
- Downloads transcript with timestamps
- Extracts video metadata (title, channel, description)
- Identifies GitHub repos and arXiv papers from:
  - Video description (authoritative)
  - Comments (community contributions)
- Breaks transcript into semantic knowledge chunks

### 2. Link Extraction & Attribution
```python
# Automatically categorizes links:
{
    'github_authoritative': [...],  # From video author
    'github_community': [...],      # From comments
    'arxiv_authoritative': [...],   # From video author
    'arxiv_community': [...]        # From comments
}
```

### 3. ArXiv Processing
For each paper found:
- Calls ArXiv MCP Server automatically
- Fetches full paper metadata
- Extracts citations and references
- Finds related papers
- Identifies code implementations

### 4. GitHub Analysis
For each repository found:
- Calls GitGet automatically
- Analyzes code structure
- Extracts README and docs
- Identifies dependencies
- Maps to papers if mentioned

### 5. ArangoDB Storage & Enhancement

#### Collections Created
- `videos`: YouTube video metadata
- `chunks`: Knowledge chunks from transcript
- `papers`: ArXiv paper details
- `repositories`: GitHub repo information
- `authors`: All content creators
- `comments`: Valuable comments with links

#### Relationships Created
```
Video ──mentions──> Paper
  └──mentions──> Repository
  └──has_chunks──> Knowledge Chunks
  
Paper ──implemented_by──> Repository
  └──cites──> Other Papers
  
Repository ──depends_on──> Other Repos
  
Chunks ──semantically_similar──> Other Chunks
```

#### Automatic ArangoDB Features
Once data is stored, ArangoDB automatically:
- Generates semantic embeddings for all chunks
- Calculates similarity between chunks
- Builds graph indices for fast traversal
- Enables vector search on content
- Provides graph algorithms (PageRank, community detection)

## Usage Examples

### Basic Research Video Processing
```python
# Agent processes a video about RLHF
result = await process_research_video(
    "https://www.youtube.com/watch?v=rlhf_video"
)

# Returns:
{
    'status': 'success',
    'video_id': 'rlhf_video',
    'title': 'RLHF Explained',
    'knowledge_chunks': 23,
    'arxiv_papers': 5,
    'github_repos': 3,
    'graph_nodes': 32,
    'graph_edges': 78
}
```

### With Research Topic Context
```python
# Provide context for better processing
result = await process_research_video(
    video_url="https://www.youtube.com/watch?v=ABC123",
    research_topic="constitutional AI alignment"
)
```

## Querying the Knowledge Graph

After processing, agents can query the graph:

### Find Related Papers
```python
# AQL query to find papers mentioned in video
FOR video IN videos
    FILTER video._key == "ABC123"
    FOR paper IN 1..1 OUTBOUND video mentions
        FILTER paper.is_authoritative == true
        RETURN paper
```

### Find Implementation Code
```python
# Find repos that implement a paper
FOR paper IN papers
    FILTER paper._key == "2301.12345"
    FOR repo IN 1..1 INBOUND paper implements
        RETURN repo
```

### Semantic Search on Chunks
```python
# Find similar content across videos
FOR chunk IN chunks
    FILTER chunk.embedding != null
    LET similarity = COSINE_SIMILARITY(chunk.embedding, @query_embedding)
    FILTER similarity > 0.8
    SORT similarity DESC
    RETURN {
        text: chunk.text,
        video: FIRST(FOR v IN 1..1 INBOUND chunk chunk_of RETURN v.title),
        similarity: similarity
    }
```

## Integration Points

### 1. YouTube Transcripts Module
```python
from youtube_transcripts import download_youtube_transcript
from youtube_transcripts.link_extractor import extract_links_from_text
```

### 2. ArXiv MCP Server
```python
# Automatically called via MCP protocol
{
    "method": "tools/call",
    "params": {
        "name": "search_papers",
        "arguments": {"query": "paper_id:2301.12345"}
    }
}
```

### 3. GitGet
```python
# Automatically called via CLI
gitget analyze --url https://github.com/author/repo
```

### 4. ArangoDB
```python
from arango import ArangoClient

# All storage handled automatically
# Just query when needed
```

## Benefits for Agents

1. **One Simple Call**: No need to orchestrate multiple services
2. **Automatic Processing**: Links are followed and processed
3. **Rich Context**: Full knowledge graph available for queries
4. **Authoritative Sources**: Distinguishes creator content from community
5. **Semantic Search**: Find related content across all videos
6. **Citation Chains**: Follow research threads through papers

## Error Handling

The system gracefully handles:
- YouTube API rate limits (with exponential backoff)
- Missing transcripts (reports and continues)
- Invalid links (logs and skips)
- Processing failures (queues for retry)

## Performance

- Chunks transcripts for parallel processing
- Batches API calls to external services
- Uses ArangoDB indices for fast queries
- Caches processed results

## Future Enhancements

1. **Recursive Processing**: Follow papers/repos to find more videos
2. **Quality Scoring**: Rank content by citation count, stars, etc.
3. **Update Monitoring**: Track when papers/repos update
4. **Cross-Reference**: Link same paper mentioned in multiple videos
5. **Visualization**: Generate knowledge graph visualizations

## Summary

For agents, this entire complex pipeline is just:

```python
result = await process_research_video(video_url)
```

Everything else happens automatically, building a rich, queryable knowledge graph that connects videos, papers, and code in meaningful ways.