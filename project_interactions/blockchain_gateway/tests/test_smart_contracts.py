"""
Module: test_smart_contracts.py
Purpose: Smart contract interaction tests for blockchain gateway

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://github.com/pytest-dev/pytest-asyncio

Example Usage:
>>> pytest test_smart_contracts.py -v
"""

import asyncio
import pytest
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from blockchain_gateway_interaction import (
    BlockchainGateway, BlockchainType, SmartContract
)


@pytest.fixture
async def gateway():
    """Create blockchain gateway instance"""
    return BlockchainGateway()


@pytest.fixture
async def deployed_contract(gateway):
    """Deploy a test contract"""
    result = await gateway.deploy_contract("ethereum", {
        "name": "TestToken",
        "bytecode": "0x608060405234801561001057600080fd5b50...",
        "abi": [
            {
                "name": "balanceOf",
                "type": "function",
                "inputs": [{"name": "account", "type": "address"}],
                "outputs": [{"name": "balance", "type": "uint256"}]
            },
            {
                "name": "transfer",
                "type": "function",
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "amount", "type": "uint256"}
                ],
                "outputs": [{"name": "success", "type": "bool"}]
            },
            {
                "name": "approve",
                "type": "function",
                "inputs": [
                    {"name": "spender", "type": "address"},
                    {"name": "amount", "type": "uint256"}
                ],
                "outputs": [{"name": "success", "type": "bool"}]
            },
            {
                "name": "totalSupply",
                "type": "function",
                "inputs": [],
                "outputs": [{"name": "supply", "type": "uint256"}]
            },
            {
                "name": "symbol",
                "type": "function",
                "inputs": [],
                "outputs": [{"name": "symbol", "type": "string"}]
            }
        ]
    })
    return result["contract_address"]


@pytest.mark.asyncio
async def test_contract_deployment(gateway):
    """Test smart contract deployment"""
    contract_data = {
        "name": "SimpleStorage",
        "bytecode": "0x608060405234801561001057600080fd5b50610150806100206000396000f3fe",
        "abi": [
            {
                "name": "store",
                "type": "function",
                "inputs": [{"name": "value", "type": "uint256"}]
            },
            {
                "name": "retrieve",
                "type": "function",
                "outputs": [{"name": "value", "type": "uint256"}]
            }
        ]
    }
    
    # Deploy on Ethereum
    eth_result = await gateway.deploy_contract("ethereum", contract_data)
    assert "contract_address" in eth_result
    assert eth_result["contract_address"].startswith("0x")
    assert len(eth_result["contract_address"]) == 42
    assert "transaction_hash" in eth_result
    assert "gas_used" in eth_result
    
    # Deploy on Polygon
    poly_result = await gateway.deploy_contract("polygon", contract_data)
    assert poly_result["contract_address"] != eth_result["contract_address"]
    
    # Verify contract is stored
    assert eth_result["contract_address"] in gateway.contracts
    contract = gateway.contracts[eth_result["contract_address"]]
    assert contract.name == "SimpleStorage"
    assert contract.verified is True


@pytest.mark.asyncio
async def test_contract_method_calls(gateway, deployed_contract):
    """Test calling smart contract methods"""
    # Call balanceOf
    balance = await gateway.call_contract_method(
        deployed_contract,
        "balanceOf",
        ["0x742d35Cc6634C0532925a3b844Bc9e7595f02fD3"]
    )
    assert balance == "1000000000000000000"  # 1 ETH in wei
    
    # Call totalSupply
    supply = await gateway.call_contract_method(
        deployed_contract,
        "totalSupply",
        []
    )
    assert int(supply) > 0
    
    # Call symbol
    symbol = await gateway.call_contract_method(
        deployed_contract,
        "symbol",
        []
    )
    assert symbol == "TEST"


@pytest.mark.asyncio
async def test_contract_abi_validation(gateway):
    """Test contract ABI validation and parsing"""
    # Valid ABI
    valid_abi = [
        {
            "name": "transfer",
            "type": "function",
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "amount", "type": "uint256"}
            ],
            "outputs": [{"name": "success", "type": "bool"}]
        }
    ]
    
    result = await gateway.deploy_contract("ethereum", {
        "name": "ValidContract",
        "bytecode": "0x123",
        "abi": valid_abi
    })
    
    contract = gateway.contracts[result["contract_address"]]
    assert len(contract.abi) == 1
    assert contract.abi[0]["name"] == "transfer"


@pytest.mark.asyncio
async def test_multiple_contract_deployment(gateway):
    """Test deploying multiple contracts"""
    contracts = []
    
    # Deploy 5 different contracts
    for i in range(5):
        result = await gateway.deploy_contract("ethereum", {
            "name": f"Contract{i}",
            "bytecode": f"0x60806040{i}",
            "abi": [{"name": f"function{i}", "type": "function"}]
        })
        contracts.append(result["contract_address"])
    
    # Verify all contracts are unique
    assert len(set(contracts)) == 5
    
    # Verify all contracts are stored
    for addr in contracts:
        assert addr in gateway.contracts


@pytest.mark.asyncio
async def test_contract_event_handling(gateway, deployed_contract):
    """Test smart contract event handling"""
    events_received = []
    
    async def handle_event(event):
        events_received.append(event)
    
    # Monitor Transfer events
    await gateway.monitor_events(
        deployed_contract,
        ["Transfer"],
        handle_event
    )
    
    # Wait for event
    await asyncio.sleep(0.1)
    
    assert len(events_received) == 1
    event = events_received[0]
    assert event.event_name == "Transfer"
    assert event.contract_address == deployed_contract
    assert "from" in event.args
    assert "to" in event.args
    assert "value" in event.args


@pytest.mark.asyncio
async def test_contract_verification(gateway):
    """Test contract verification status"""
    # Deploy verified contract
    verified_result = await gateway.deploy_contract("ethereum", {
        "name": "VerifiedToken",
        "bytecode": "0xverified",
        "abi": [],
        "verified": True
    })
    
    contract = gateway.contracts[verified_result["contract_address"]]
    assert contract.verified is True
    
    # Check deployed_at block number
    assert contract.deployed_at > 0


@pytest.mark.asyncio
async def test_contract_interaction_errors(gateway):
    """Test error handling for contract interactions"""
    # Call method on non-existent contract
    with pytest.raises(ValueError, match="Contract .* not found"):
        await gateway.call_contract_method(
            "0xNonExistent",
            "balanceOf",
            ["0x123"]
        )


@pytest.mark.asyncio
async def test_defi_protocol_integration(gateway, deployed_contract):
    """Test DeFi protocol integration with contracts"""
    # Uniswap swap
    swap_result = await gateway.interact_defi_protocol(
        "uniswap",
        "swap",
        {
            "amount_in": "1000000000000000000",
            "token_in": deployed_contract,
            "token_out": "USDC",
            "slippage": 0.5
        }
    )
    
    assert "amount_out" in swap_result
    assert int(swap_result["amount_out"]) > 0
    assert "price_impact" in swap_result
    assert "gas_used" in swap_result
    
    # Aave lending
    lend_result = await gateway.interact_defi_protocol(
        "aave",
        "lend",
        {
            "amount": "5000000000000000000",
            "asset": deployed_contract
        }
    )
    
    assert "apy" in lend_result
    assert "a_token_received" in lend_result
    assert lend_result["amount_lent"] == "5000000000000000000"


@pytest.mark.asyncio
async def test_nft_contract_operations(gateway):
    """Test NFT contract operations"""
    # Deploy NFT contract
    nft_contract = await gateway.deploy_contract("ethereum", {
        "name": "TestNFT",
        "bytecode": "0xnft",
        "abi": [
            {"name": "mint", "type": "function"},
            {"name": "tokenURI", "type": "function"},
            {"name": "ownerOf", "type": "function"}
        ]
    })
    
    # Mint NFT
    mint_result = await gateway.manage_nft("mint", {
        "contract": nft_contract["contract_address"],
        "recipient": "0xRecipient",
        "metadata_uri": "ipfs://QmTest123"
    })
    
    assert "token_id" in mint_result
    assert "transaction_hash" in mint_result
    assert mint_result["owner"] == "0xRecipient"
    
    # Transfer NFT
    transfer_result = await gateway.manage_nft("transfer", {
        "contract": nft_contract["contract_address"],
        "from": "0xRecipient",
        "to": "0xNewOwner",
        "token_id": mint_result["token_id"]
    })
    
    assert transfer_result["from"] == "0xRecipient"
    assert transfer_result["to"] == "0xNewOwner"


async def run_smart_contract_tests():
    """Run all smart contract tests"""
    gateway = BlockchainGateway()
    
    print("Running smart contract tests...\n")
    
    # Test 1: Contract deployment
    print("1. Testing contract deployment...")
    await test_contract_deployment(gateway)
    print("✅ Contract deployment test passed\n")
    
    # Test 2: Deploy test contract for other tests
    print("2. Deploying test contract...")
    deployed = await deployed_contract(gateway)
    print(f"✅ Test contract deployed at: {deployed}\n")
    
    # Test 3: Method calls
    print("3. Testing contract method calls...")
    await test_contract_method_calls(gateway, deployed)
    print("✅ Method calls test passed\n")
    
    # Test 4: ABI validation
    print("4. Testing ABI validation...")
    await test_contract_abi_validation(gateway)
    print("✅ ABI validation test passed\n")
    
    # Test 5: Multiple deployments
    print("5. Testing multiple contract deployments...")
    await test_multiple_contract_deployment(gateway)
    print("✅ Multiple deployment test passed\n")
    
    # Test 6: Event handling
    print("6. Testing contract event handling...")
    await test_contract_event_handling(gateway, deployed)
    print("✅ Event handling test passed\n")
    
    # Test 7: Verification
    print("7. Testing contract verification...")
    await test_contract_verification(gateway)
    print("✅ Verification test passed\n")
    
    # Test 8: DeFi integration
    print("8. Testing DeFi protocol integration...")
    await test_defi_protocol_integration(gateway, deployed)
    print("✅ DeFi integration test passed\n")
    
    # Test 9: NFT operations
    print("9. Testing NFT contract operations...")
    await test_nft_contract_operations(gateway)
    print("✅ NFT operations test passed\n")
    
    return True


if __name__ == "__main__":
    # Test with real data
    result = asyncio.run(run_smart_contract_tests())
    assert result is True, "Smart contract tests failed"
    print("✅ All smart contract tests passed")