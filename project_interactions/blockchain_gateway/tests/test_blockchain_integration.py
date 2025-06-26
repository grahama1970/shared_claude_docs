"""
Module: test_blockchain_integration.py
Purpose: Integration tests for blockchain gateway

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://github.com/pytest-dev/pytest-asyncio

Example Usage:
>>> pytest test_blockchain_integration.py -v
"""

import asyncio
import pytest
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from blockchain_gateway_interaction import (
    BlockchainGateway, BlockchainType, TransactionStatus,
    Transaction, SmartContract, ChainEvent
)


@pytest.fixture
async def gateway():
    """Create blockchain gateway instance"""
    config = {
        "test_mode": True,
        "chains": {
            "ethereum": {"rpc_url": "http://localhost:8545"},
            "polygon": {"rpc_url": "http://localhost:8546"}
        }
    }
    return BlockchainGateway(config)


@pytest.mark.asyncio
async def test_multi_chain_support(gateway):
    """Test support for multiple blockchain networks"""
    # Verify all chains are initialized
    expected_chains = [
        BlockchainType.ETHEREUM,
        BlockchainType.POLYGON,
        BlockchainType.HYPERLEDGER
    ]
    
    for chain in expected_chains:
        assert chain in gateway.chains
        chain_config = gateway.chains[chain]
        assert "rpc_url" in chain_config
        assert "chain_id" in chain_config
        assert "explorer" in chain_config


@pytest.mark.asyncio
async def test_transaction_execution(gateway):
    """Test transaction execution on different chains"""
    # Execute Ethereum transaction
    eth_tx = await gateway.execute_transaction("ethereum", {
        "to": "0x742d35Cc6634C0532925a3b844Bc9e7595f02fD3",
        "value": "1000000000000000000",  # 1 ETH
        "gasPrice": "20000000000",
        "gasLimit": 21000
    })
    
    assert "transaction_hash" in eth_tx
    assert eth_tx["status"] == "confirmed"
    assert eth_tx["block_number"] is not None
    
    # Execute Polygon transaction
    poly_tx = await gateway.execute_transaction("polygon", {
        "to": "0x456",
        "value": "5000000000000000000",  # 5 MATIC
        "gasPrice": "30000000000"
    })
    
    assert "transaction_hash" in poly_tx
    assert poly_tx["transaction_hash"] != eth_tx["transaction_hash"]


@pytest.mark.asyncio
async def test_gas_optimization(gateway):
    """Test gas price optimization"""
    # Get optimized gas for Ethereum
    eth_gas = await gateway.optimize_gas("ethereum")
    
    assert "slow" in eth_gas
    assert "standard" in eth_gas
    assert "fast" in eth_gas
    assert "instant" in eth_gas
    
    # Verify gas price ordering
    assert int(eth_gas["slow"]) < int(eth_gas["standard"])
    assert int(eth_gas["standard"]) < int(eth_gas["fast"])
    assert int(eth_gas["fast"]) < int(eth_gas["instant"])


@pytest.mark.asyncio
async def test_event_monitoring(gateway):
    """Test blockchain event monitoring"""
    events_received = []
    
    async def event_callback(event: ChainEvent):
        events_received.append(event)
    
    # Monitor events
    contract_address = "0xTestContract"
    await gateway.monitor_events(
        contract_address,
        ["Transfer", "Approval"],
        event_callback
    )
    
    # Wait for event emission
    await asyncio.sleep(0.1)
    
    assert len(events_received) > 0
    event = events_received[0]
    assert event.contract_address == contract_address
    assert event.event_name in ["Transfer", "Approval"]
    assert event.block_number > 0


@pytest.mark.asyncio
async def test_chain_data_querying(gateway):
    """Test historical chain data queries"""
    # Query block data
    block_data = await gateway.query_chain_data(
        "ethereum",
        "block",
        {"block_number": 15000000}
    )
    
    assert block_data["number"] == 15000000
    assert "hash" in block_data
    assert "timestamp" in block_data
    assert len(block_data["transactions"]) > 0
    
    # Query transaction history
    tx_history = await gateway.query_chain_data(
        "ethereum",
        "transaction_history",
        {"address": "0x123"}
    )
    
    assert "transactions" in tx_history
    assert len(tx_history["transactions"]) > 0
    
    # Test caching
    cached_data = await gateway.query_chain_data(
        "ethereum",
        "block",
        {"block_number": 15000000}
    )
    assert cached_data == block_data  # Should return cached result


@pytest.mark.asyncio
async def test_wallet_integration(gateway):
    """Test wallet integration features"""
    wallet_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f02fD3"
    
    # Get wallet info
    wallet = await gateway.get_wallet_info(wallet_address, "ethereum")
    
    assert wallet.address == wallet_address
    assert wallet.chain == BlockchainType.ETHEREUM
    assert int(wallet.balance) > 0
    assert wallet.nonce >= 0
    assert wallet.transactions_count >= 0


@pytest.mark.asyncio
async def test_cross_chain_bridge(gateway):
    """Test cross-chain token bridging"""
    bridge_result = await gateway.bridge_tokens(
        from_chain="ethereum",
        to_chain="polygon",
        token_address="0xTokenContract",
        amount="1000000000000000000",  # 1 token
        recipient="0xRecipientAddress"
    )
    
    assert "bridge_id" in bridge_result
    assert "source_tx" in bridge_result
    assert "destination_tx" in bridge_result
    assert bridge_result["status"] == "completed"
    assert bridge_result["source_tx"] != bridge_result["destination_tx"]


@pytest.mark.asyncio
async def test_batch_transaction_processing(gateway):
    """Test batch transaction processing"""
    transactions = [
        {
            "chain": "ethereum",
            "to": "0x123",
            "value": "1000000000000000"
        },
        {
            "chain": "ethereum",
            "to": "0x456",
            "value": "2000000000000000"
        },
        {
            "chain": "polygon",
            "to": "0x789",
            "value": "5000000000000000"
        }
    ]
    
    results = await gateway.batch_transactions(transactions)
    
    assert len(results) == len(transactions)
    
    # Verify all transactions completed
    for result in results:
        assert "transaction_hash" in result
        assert result["status"] == "confirmed"
        assert "gas_used" in result
    
    # Verify transactions have different hashes
    hashes = [r["transaction_hash"] for r in results]
    assert len(set(hashes)) == len(hashes)


@pytest.mark.asyncio
async def test_chain_analytics(gateway):
    """Test blockchain analytics functionality"""
    # Get network statistics
    network_stats = await gateway.get_chain_analytics(
        "ethereum",
        "network_stats"
    )
    
    assert "block_height" in network_stats
    assert "total_transactions" in network_stats
    assert "tps" in network_stats
    assert network_stats["chain"] == "ethereum"
    
    # Get DeFi TVL
    defi_stats = await gateway.get_chain_analytics(
        "ethereum",
        "defi_tvl"
    )
    
    assert "total_value_locked" in defi_stats
    assert "protocols" in defi_stats
    assert int(defi_stats["total_value_locked"]) > 0


async def run_integration_tests():
    """Run all integration tests"""
    gateway = BlockchainGateway()
    
    print("Running blockchain integration tests...\n")
    
    # Test 1: Multi-chain support
    print("1. Testing multi-chain support...")
    await test_multi_chain_support(gateway)
    print("✅ Multi-chain support test passed\n")
    
    # Test 2: Transaction execution
    print("2. Testing transaction execution...")
    await test_transaction_execution(gateway)
    print("✅ Transaction execution test passed\n")
    
    # Test 3: Gas optimization
    print("3. Testing gas optimization...")
    await test_gas_optimization(gateway)
    print("✅ Gas optimization test passed\n")
    
    # Test 4: Event monitoring
    print("4. Testing event monitoring...")
    await test_event_monitoring(gateway)
    print("✅ Event monitoring test passed\n")
    
    # Test 5: Chain data querying
    print("5. Testing chain data querying...")
    await test_chain_data_querying(gateway)
    print("✅ Chain data querying test passed\n")
    
    # Test 6: Wallet integration
    print("6. Testing wallet integration...")
    await test_wallet_integration(gateway)
    print("✅ Wallet integration test passed\n")
    
    # Test 7: Cross-chain bridge
    print("7. Testing cross-chain bridge...")
    await test_cross_chain_bridge(gateway)
    print("✅ Cross-chain bridge test passed\n")
    
    # Test 8: Batch processing
    print("8. Testing batch transaction processing...")
    await test_batch_transaction_processing(gateway)
    print("✅ Batch processing test passed\n")
    
    # Test 9: Analytics
    print("9. Testing chain analytics...")
    await test_chain_analytics(gateway)
    print("✅ Chain analytics test passed\n")
    
    return True


if __name__ == "__main__":
    # Test with real data
    result = asyncio.run(run_integration_tests())
    assert result is True, "Integration tests failed"
    print("✅ All integration tests passed")