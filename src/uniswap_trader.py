"""
UniswapTrader module for interacting with Uniswap and executing trades.
"""

import os
from dotenv import load_dotenv
from portia.config import Config
from portia.trading.uniswap import UniswapTrader

load_dotenv()

def get_uniswap_trader():
    """
    Set up a UniswapTrader instance with the project configuration.
    """
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
    trader = get_uniswap_trader()
    route_response = trader.get_optimal_route(
        from_address=from_address,
        amount_in=amount_in,
        token_in=token_in,
        token_out=token_out
    )
    tx_hash = trader.execute_trade(route_response)
    return tx_hash

if __name__ == "__main__":
    # Example usage
    from_address = os.getenv("WALLET_ADDRESS", "your-address")
    amount_in = "1000000000000000000"  # 1 ETH in wei
    token_in = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"  # ETH
    token_out = "0x6b175474e89094c44da98b954eedeac495271d0f"  # DAI
    
    # Get the optimal route
    trader = get_uniswap_trader()
    route_response = trader.get_optimal_route(
        from_address=from_address,
        amount_in=amount_in,
        token_in=token_in,
        token_out=token_out
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