"""
UniswapTrader module for interacting with Uniswap and executing trades.
"""

import os
import logging
import json
from dotenv import load_dotenv
from portia.config import Config
from portia.trading.uniswap import UniswapTrader
from eth_utils import to_checksum_address, to_normalized_address

# Set up logging
logger = logging.getLogger("uniswap_portia.trader")

load_dotenv()

def get_uniswap_trader():
    """
    Set up a UniswapTrader instance with the project configuration.
    """
    logger.info("Initializing UniswapTrader")
    
    # Create a configuration
    config = Config.from_default(
        llm_provider="OPENAI",
        openai_api_key=os.getenv("OPENAI_API_KEY", "")
    )
    
    # Create a UniswapTrader instance
    trader = UniswapTrader(
        config=config,
        enso_api_key=os.getenv("ENSO_API_KEY", "")
    )
    
    logger.info("UniswapTrader initialized successfully")
    return trader

def execute_uniswap_trade(from_address, amount_in, token_in, token_out):
    """
    Execute a trade on Uniswap using the UniswapTrader.
    
    Args:
        from_address: The address initiating the trade
        amount_in: The amount of input token (in wei)
        token_in: The address of the input token (use 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee for ETH)
        token_out: The address of the output token
        
    Returns:
        The transaction hash of the executed trade
    """
    logger.info(f"Executing trade: {amount_in} from {from_address}")
    logger.info(f"Token in: {token_in}, Token out: {token_out}")
    
    trader = get_uniswap_trader()
    
    # Format parameters correctly for the Enso API
    # 1. fromAddress must be a single Ethereum address (checksummed)
    formatted_from_address = to_checksum_address(from_address)
    
    # 2. amountIn must be a list of strings
    formatted_amount_in = [str(amount_in)]
    
    # 3. tokenIn must be a list of Ethereum addresses
    # For ETH, use the special format with mixed case
    if token_in.lower() == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee":
        formatted_token_in = ["0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"]
    else:
        formatted_token_in = [token_in.lower()]
    
    # 4. tokenOut must be a list of Ethereum addresses
    formatted_token_out = [token_out.lower()]
    
    # Create the exact JSON structure that will be sent to Enso
    request_data = {
        "chainId": 1,
        "fromAddress": formatted_from_address,
        "routingStrategy": "router",
        "receiver": formatted_from_address,
        "spender": formatted_from_address,
        "amountIn": formatted_amount_in,
        "tokenIn": formatted_token_in,
        "tokenOut": formatted_token_out,
        "slippage": "50",
        "variableEstimates": None
    }
    
    # Log the formatted parameters
    logger.info(f"Formatted parameters:")
    logger.info(f"  from_address: {formatted_from_address}")
    logger.info(f"  amount_in: {formatted_amount_in}")
    logger.info(f"  token_in: {formatted_token_in}")
    logger.info(f"  token_out: {formatted_token_out}")
    
    # Log the final JSON being sent to Enso
    logger.info(f"FINAL JSON to Enso:\n{json.dumps(request_data, indent=2)}")
    
    logger.info("Getting optimal route")
    # Call the API with the correctly formatted parameters
    route_response = trader.get_optimal_route(
        from_address=formatted_from_address,
        amount_in=formatted_amount_in,
        token_in=formatted_token_in,
        token_out=formatted_token_out,
        variable_estimates=None
    )
    
    # Convert the response to match the SDK's expected format
    if isinstance(route_response, dict):
        # Create a new response object with all required fields
        formatted_response = {
            "amount_out": route_response.get("amountOut", "0"),
            "gas": route_response.get("gas", "0"),
            "price_impact": route_response.get("priceImpact", "0"),
            "fee_amount": ["0"],  # Default value if not provided, as a list
            "created_at": route_response.get("createdAt", 0),  # Use integer 0 as default
            "tx": route_response.get("tx", {}),
            "route": route_response.get("route", [])
        }
        
        # Replace the original response with the formatted one
        route_response = formatted_response
    
    logger.info(f"Route found: {route_response['amount_out']} {token_out} output")
    logger.info(f"Gas estimate: {route_response['gas']}")
    logger.info(f"Price impact: {route_response['price_impact']}%")
    
    logger.info("Executing trade")
    tx_hash = trader.execute_trade(route_response)
    logger.info(f"Trade executed with transaction hash: {tx_hash}")
    
    return tx_hash

if __name__ == "__main__":
    # Example usage
    from_address = os.getenv("WALLET_ADDRESS", "your-address")
    amount_in = "1000000000000000000"  # 1 ETH in wei
    token_in = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"  # ETH (all lowercase)
    token_out = "0x6b175474e89094c44da98b954eedeac495271d0f"  # DAI (all lowercase)
    
    # Get the optimal route
    trader = get_uniswap_trader()
    
    # Format parameters correctly for the Enso API
    # 1. fromAddress must be a single Ethereum address (checksummed)
    formatted_from_address = to_checksum_address(from_address)
    
    # 2. amountIn must be a list of strings
    formatted_amount_in = [str(amount_in)]
    
    # 3. tokenIn must be a list of Ethereum addresses
    # For ETH, use the special format with mixed case
    if token_in.lower() == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee":
        formatted_token_in = ["0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"]
    else:
        formatted_token_in = [token_in.lower()]
    
    # 4. tokenOut must be a list of Ethereum addresses
    formatted_token_out = [token_out.lower()]
    
    # Create the exact JSON structure that will be sent to Enso
    request_data = {
        "chainId": 1,
        "fromAddress": formatted_from_address,
        "routingStrategy": "router",
        "receiver": formatted_from_address,
        "spender": formatted_from_address,
        "amountIn": formatted_amount_in,
        "tokenIn": formatted_token_in,
        "tokenOut": formatted_token_out,
        "slippage": "50",
        "variableEstimates": None
    }
    
    # Log the final JSON being sent to Enso
    logger.info(f"FINAL JSON to Enso:\n{json.dumps(request_data, indent=2)}")
    
    # Call the API with the correctly formatted parameters
    route_response = trader.get_optimal_route(
        from_address=formatted_from_address,
        amount_in=formatted_amount_in,
        token_in=formatted_token_in,
        token_out=formatted_token_out,
        variable_estimates=None
    )
    
    # Convert the response to match the SDK's expected format
    if isinstance(route_response, dict):
        # Create a new response object with all required fields
        formatted_response = {
            "amount_out": route_response.get("amountOut", "0"),
            "gas": route_response.get("gas", "0"),
            "price_impact": route_response.get("priceImpact", "0"),
            "fee_amount": ["0"],  # Default value if not provided, as a list
            "created_at": route_response.get("createdAt", 0),  # Use integer 0 as default
            "tx": route_response.get("tx", {}),
            "route": route_response.get("route", [])
        }
        
        # Replace the original response with the formatted one
        route_response = formatted_response
    
    # Print the route information
    print("Route information:")
    print(f"  From: {route_response['route'][0]['from']}")
    print(f"  Amount in: {route_response['amount_in']}")
    print(f"  Token in: {route_response['route'][0]['tokenIn']}")
    print(f"  Token out: {route_response['route'][0]['tokenOut']}")
    print(f"  Estimated output: {route_response['amount_out']}")
    print(f"  Gas estimate: {route_response['gas']}")
    
    # Ask for confirmation before executing the trade
    confirm = input("Do you want to execute this trade? (y/n): ")
    if confirm.lower() == 'y':
        # Execute the trade
        print("Executing trade...")
        tx_hash = trader.execute_trade(route_response)
        print(f"Trade executed with transaction hash: {tx_hash}")
    else:
        print("Trade cancelled.") 