"""
Example: Basic API Gateway Setup
Shows how to create and configure a simple API gateway
"""

import asyncio
from loguru import logger

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from api_gateway_interaction import (
    APIGateway, RateLimitConfig, RateLimitAlgorithm,
    logging_middleware, cors_middleware
)


async def main():
    """Run a basic API gateway"""
    # Create gateway with default rate limiting
    gateway = APIGateway(
        default_rate_limit=RateLimitConfig(
            requests_per_minute=60,
            algorithm=RateLimitAlgorithm.SLIDING_WINDOW
        )
    )
    
    # Register some routes
    gateway.register_route(
        "/api/users",
        "https://jsonplaceholder.typicode.com/users",
        cache_ttl=300  # Cache for 5 minutes
    )
    
    gateway.register_route(
        "/api/posts",
        "https://jsonplaceholder.typicode.com/posts",
        rate_limit=RateLimitConfig(
            requests_per_minute=100,
            burst_size=20,
            algorithm=RateLimitAlgorithm.TOKEN_BUCKET
        ),
        require_auth=True
    )
    
    gateway.register_route(
        "/api/todos",
        "https://jsonplaceholder.typicode.com/todos"
    )
    
    # Add middleware
    gateway.add_middleware(logging_middleware)
    gateway.add_middleware(cors_middleware)
    
    # Create some API keys
    basic_key = gateway.api_key_manager.create_api_key("Basic Application")
    premium_key = gateway.api_key_manager.create_api_key(
        "Premium Application",
        RateLimitConfig(
            requests_per_minute=1000,
            requests_per_hour=50000
        )
    )
    
    logger.info(f"Created API keys:")
    logger.info(f"  Basic: {basic_key}")
    logger.info(f"  Premium: {premium_key}")
    
    # Start the gateway
    logger.info("Starting API Gateway on http://localhost:8080")
    logger.info("Available endpoints:")
    logger.info("  GET /api/users - Public endpoint with caching")
    logger.info("  GET /api/posts - Requires API key")
    logger.info("  GET /api/todos - Public endpoint")
    logger.info("  GET /_metrics - Gateway metrics")
    logger.info("  GET /_health - Health check")
    
    await gateway.start(port=8080)


if __name__ == "__main__":
    asyncio.run(main())