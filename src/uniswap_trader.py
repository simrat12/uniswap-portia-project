"""
UniswapTrader module for interacting with Uniswap and executing trades.
"""

import os
import logging
from dotenv import load_dotenv
from portia.config import Config
from portia.trading.uniswap import UniswapTrader
from eth_utils import to_checksum_address

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
    
    # Ensure all parameters are properly formatted
    from_address = to_checksum_address(from_address)
    amount_in_str = str(amount_in)
    token_in_addr = to_checksum_address(token_in)
    token_out_addr = to_checksum_address(token_out)
    
    logger.info(f"Formatted parameters: from={from_address}, amount={amount_in_str}, tokenIn={token_in_addr}, tokenOut={token_out_addr}")
    
    logger.info("Getting optimal route")
    route_response = trader.get_optimal_route(
        from_address=from_address,
        amount_in=[amount_in_str],  # Wrap in list as required by the SDK
        token_in=[token_in_addr],   # Wrap in list as required by the SDK
        token_out=[token_out_addr]  # Wrap in list as required by the SDK
    )
    
    logger.info(f"Optimal route found: {route_response.amount_out} output")
    logger.info(f"Gas estimate: {route_response.gas}")
    logger.info(f"Price impact: {route_response.price_impact}%")
    
    logger.info("Executing trade")
    tx_hash = trader.execute_trade(route_response)
    logger.info(f"Trade executed with transaction hash: {tx_hash}")
    
    return tx_hash

if __name__ == "__main__":
    # Example usage
    from_address = os.getenv("WALLET_ADDRESS", "your-address")
    amount_in = "1000000000000000000"  # 1 ETH in wei
    token_in = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"  # ETH
    token_out = "0x6b175474e89094c44da98b954eedeac495271d0f"  # DAI
    
    # Get the optimal route
    trader = get_uniswap_trader()
    
    # Ensure all parameters are properly formatted
    from_address = to_checksum_address(from_address)
    amount_in_str = str(amount_in)
    token_in_addr = to_checksum_address(token_in)
    token_out_addr = to_checksum_address(token_out)
    
    route_response = trader.get_optimal_route(
        from_address=from_address,
        amount_in=[amount_in_str],  # Wrap in list as required by the SDK
        token_in=[token_in_addr],   # Wrap in list as required by the SDK
        token_out=[token_out_addr]  # Wrap in list as required by the SDK
    )
    
    # Print the route information
    print("Route information:")
    print(f"  From: {route_response.from_address}")
    print(f"  Amount in: {route_response.amount_in}")
    print(f"  Token in: {route_response.token_in}")
    print(f"  Token out: {route_response.token_out}")
    print(f"  Estimated output: {route_response.amount_out}")
    print(f"  Gas estimate: {route_response.gas}")
    
    # Ask for confirmation before executing the trade
    confirm = input("Do you want to execute this trade? (y/n): ")
    if confirm.lower() == 'y':
        # Execute the trade
        print("Executing trade...")
        tx_hash = trader.execute_trade(route_response)
        print(f"Trade executed with transaction hash: {tx_hash}")
    else:
        print("Trade cancelled.") 