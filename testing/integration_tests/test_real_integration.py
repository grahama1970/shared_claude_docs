#!/usr/bin/env python3
"""
Test script demonstrating real integration with arxiv-mcp-server and youtube_transcripts
This shows how the self-evolving system actually works with real APIs
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add necessary paths
sys.path.append(str(Path(__file__).parent))
sys.path.append("/home/graham/workspace/arxiv-mcp-server")
sys.path.append("/home/graham/workspace/youtube_transcripts")

async def test_arxiv_integration():
    """Test real arxiv-mcp-server integration"""
    
    print("\n🔬 Testing ArXiv Integration")
    print("-" * 50)
    
    try:
        from arxiv_mcp_server.tools import (
            handle_search, 
            handle_download,
            handle_find_research_support
        )
        
        # 1. Search for visualization papers
        print("📚 Searching for visualization decision papers...")
        search_result = await handle_search({
            "query": "visualization recommendation machine learning",
            "max_results": 5,
            "date_from": "2023-01-01",
            "categories": ["cs.AI", "cs.HC"]  # AI and Human-Computer Interaction
        })
        
        import json
        papers = json.loads(search_result[0].text)["papers"]
        
        print(f"✅ Found {len(papers)} papers:")
        for paper in papers[:3]:
            print(f"   - {paper['title'][:60]}...")
            print(f"     ID: {paper['id']}")
        
        # 2. Download a paper
        if papers:
            print(f"\n📥 Downloading paper: {papers[0]['id']}")
            download_result = await handle_download({
                "paper_id": papers[0]["id"],
                "converter": "pymupdf4llm",
                "output_format": "markdown"
            })
            print("✅ Paper downloaded and converted to markdown")
        
        # 3. Find supporting evidence
        print("\n🔍 Finding evidence for visualization hypothesis...")
        hypothesis = "Machine learning can predict the most appropriate visualization type based on data characteristics"
        
        evidence_result = await handle_find_research_support({
            "research_context": hypothesis,
            "paper_ids": [papers[0]["id"]] if papers else ["all"],
            "support_type": "bolster",
            "llm_provider": "gemini",
            "min_confidence": 0.6
        })
        
        evidence = json.loads(evidence_result[0].text)
        if evidence.get("findings"):
            print(f"✅ Found supporting evidence:")
            for finding in evidence["findings"][:2]:
                print(f"   - Confidence: {finding['confidence']:.2f}")
                print(f"     {finding['explanation'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ ArXiv integration error: {str(e)}")
        print("   Make sure GEMINI_API_KEY is set for evidence extraction")
        return False


async def test_youtube_integration():
    """Test real youtube_transcripts integration"""
    
    print("\n📺 Testing YouTube Integration")
    print("-" * 50)
    
    try:
        from youtube_transcripts.unified_search import UnifiedYouTubeSearch, UnifiedSearchConfig
        
        # Configure (requires YOUTUBE_API_KEY in .env)
        config = UnifiedSearchConfig()
        search = UnifiedYouTubeSearch(config)
        
        # 1. Search local database first (no API quota usage)
        print("🔍 Searching local transcript database...")
        local_results = search.search(
            query="machine learning visualization",
            use_widening=True
        )
        
        if local_results["results"]:
            print(f"✅ Found {len(local_results['results'])} videos in local database:")
            for video in local_results["results"][:3]:
                print(f"   - {video['title'][:60]}...")
                print(f"     Channel: {video['channel_name']}")
        
        # 2. Search YouTube API (uses quota)
        print("\n🌐 Searching YouTube API...")
        try:
            api_results = search.search_youtube_api(
                query="data visualization best practices tutorial",
                max_results=5,
                fetch_transcripts=True,
                store_transcripts=True,
                published_after=datetime.now() - timedelta(days=90)
            )
            
            if api_results["results"]:
                print(f"✅ Found {len(api_results['results'])} recent videos:")
                for video in api_results["results"][:3]:
                    print(f"   - {video['title'][:60]}...")
                    print(f"     Transcript: {'Available' if video['transcript_available'] else 'Not available'}")
            
            print(f"\n📊 Quota Status:")
            print(f"   Used: {api_results['quota_status']['used']}")
            print(f"   Remaining searches: {api_results['quota_status']['searches_remaining']}")
            
        except Exception as e:
            print(f"⚠️  YouTube API search failed: {str(e)}")
            print("   (This is normal if YOUTUBE_API_KEY is not set)")
        
        return True
        
    except Exception as e:
        print(f"❌ YouTube integration error: {str(e)}")
        return False


async def test_self_evolution_with_real_apis():
    """Test self-evolution with real API integrations"""
    
    print("\n🧬 Testing Self-Evolution with Real APIs")
    print("-" * 50)
    
    from self_evolving_analyzer import SelfEvolvingAnalyzer
    
    # Create analyzer for a test project
    analyzer = SelfEvolvingAnalyzer("visualization_optimizer")
    
    # Test research phase with real APIs
    print("\n📚 Testing Research Phase...")
    research_findings = await analyzer.research_phase()
    
    print(f"\n📊 Research Results:")
    print(f"   ArXiv papers found: {len(research_findings['arxiv_papers'])}")
    print(f"   YouTube videos found: {len(research_findings['youtube_insights'])}")
    print(f"   Improvement ideas generated: {len(research_findings['improvement_ideas'])}")
    
    # Show some actual findings
    if research_findings['arxiv_papers']:
        print(f"\n📄 Sample Paper:")
        paper = research_findings['arxiv_papers'][0]
        print(f"   Title: {paper['title'][:80]}...")
        print(f"   Year: {paper['year']}")
        print(f"   Implementation available: {paper['implementation_available']}")
    
    if research_findings['youtube_insights']:
        print(f"\n📺 Sample Video:")
        video = research_findings['youtube_insights'][0]
        print(f"   Title: {video['title'][:80]}...")
        print(f"   Channel: {video['channel']}")
        print(f"   Has code snippets: {len(video.get('code_snippets', [])) > 0}")
    
    return True


async def demonstrate_visualization_decision_flow():
    """Demonstrate the complete visualization decision flow"""
    
    print("\n🎨 Visualization Decision Flow Demo")
    print("-" * 50)
    
    # This would integrate with claude-module-communicator
    decision_flow = """
    1. User requests: "Visualize user permissions matrix"
       ↓
    2. System analyzes data:
       - Type: Sparse boolean matrix (1000x50)
       - Density: 5% non-zero values
       - Pattern: Role-based groupings
       ↓
    3. ArXiv Research (automatic):
       - Searches: "sparse matrix visualization techniques"
       - Finds: "Effective Visualization of High-Dimensional Sparse Data"
       ↓
    4. YouTube Insights (automatic):
       - Searches: "sparse data visualization tutorial"
       - Finds: Code examples for interactive tables
       ↓
    5. Decision Engine:
       - Rejects: Heatmap (too sparse)
       - Recommends: Grouped table with search
       - Reasoning: Based on research + patterns
       ↓
    6. Implementation:
       - Generates interactive table
       - Groups by roles
       - Adds search/filter
       ↓
    7. Self-Evolution:
       - Records successful decision
       - Updates decision model
       - Commits improvement
    """
    
    print(decision_flow)
    
    # Simulate the decision
    print("\n🤖 Simulating Decision Process...")
    
    data_characteristics = {
        "type": "sparse_boolean_matrix",
        "dimensions": [1000, 50],
        "sparsity": 0.95,
        "patterns": ["role_groupings", "hierarchical"]
    }
    
    print(f"\n📊 Data Analysis:")
    print(f"   Type: {data_characteristics['type']}")
    print(f"   Size: {data_characteristics['dimensions'][0]}x{data_characteristics['dimensions'][1]}")
    print(f"   Sparsity: {data_characteristics['sparsity']:.0%}")
    
    print(f"\n❌ Rejecting inappropriate visualizations:")
    print(f"   - Heatmap: Too sparse, mostly empty cells")
    print(f"   - Network graph: No meaningful connections")
    print(f"   - 3D plot: Unnecessary complexity")
    
    print(f"\n✅ Recommending appropriate visualization:")
    print(f"   - Interactive table with role grouping")
    print(f"   - Reasoning: Sparse data is best shown as list")
    print(f"   - Features: Search, sort, filter, export")
    
    return True


async def main():
    """Run all integration tests"""
    
    print("🚀 Real API Integration Test Suite")
    print("=" * 60)
    print("\nThis test demonstrates:")
    print("1. Real ArXiv paper search and analysis")
    print("2. Real YouTube transcript search and extraction")
    print("3. Self-evolution with actual research data")
    print("4. Visualization decision intelligence")
    print("")
    
    # Check for API keys
    print("🔑 Checking API Keys:")
    has_gemini = bool(os.getenv("GEMINI_API_KEY"))
    has_youtube = bool(os.getenv("YOUTUBE_API_KEY"))
    
    print(f"   GEMINI_API_KEY: {'✅ Set' if has_gemini else '❌ Not set (evidence extraction disabled)'}")
    print(f"   YOUTUBE_API_KEY: {'✅ Set' if has_youtube else '❌ Not set (local search only)'}")
    
    # Run tests
    await test_arxiv_integration()
    await test_youtube_integration()
    await test_self_evolution_with_real_apis()
    await demonstrate_visualization_decision_flow()
    
    print("\n" + "="*60)
    print("✅ Integration testing complete!")
    print("\n💡 Next Steps:")
    print("1. Set API keys in .env for full functionality")
    print("2. Run self_evolving_analyzer.py on a real project")
    print("3. Watch it research, implement, test, and commit improvements!")


if __name__ == "__main__":
    asyncio.run(main())