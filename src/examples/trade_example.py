#!/usr/bin/env python
"""
Example script demonstrating how to use the UniswapTrader functionality from the command line.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.uniswap_trader import get_uniswap_trader

# Load environment variables
load_dotenv()

# Common token addresses
COMMON_TOKENS = {
    "ETH": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "WBTC": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "WETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
}

def main():
    """
    Main function for the trade example script.
    """
    parser = argparse.ArgumentParser(description="Execute a trade on Uniswap")
    parser.add_argument("--from-address", type=str, default=os.getenv("WALLET_ADDRESS", ""),
                        help="The Ethereum address that will execute the trade")
    parser.add_argument("--token-in", type=str, default="ETH",
                        help="The token to swap from (e.g., ETH, DAI, USDC)")
    parser.add_argument("--token-out", type=str, default="DAI",
                        help="The token to swap to (e.g., ETH, DAI, USDC)")
    parser.add_argument("--amount-in", type=str, default="1000000000000000000",
                        help="The amount of tokenIn to swap in wei (e.g., 1000000000000000000 for 1 ETH)")
    parser.add_argument("--execute", action="store_true",
                        help="Execute the trade after getting the optimal route")
    
    args = parser.parse_args()
    
    # Validate token names
    if args.token_in not in COMMON_TOKENS:
        print(f"Error: Token '{args.token_in}' not found. Available tokens: {', '.join(COMMON_TOKENS.keys())}")
        return
    
    if args.token_out not in COMMON_TOKENS:
        print(f"Error: Token '{args.token_out}' not found. Available tokens: {', '.join(COMMON_TOKENS.keys())}")
        return
    
    # Get token addresses
    token_in_address = COMMON_TOKENS[args.token_in]
    token_out_address = COMMON_TOKENS[args.token_out]
    
    # Get the optimal route
    print("Getting optimal route...")
    trader = get_uniswap_trader()
    route_response = trader.get_optimal_route(
        from_address=args.from_address,
        amount_in=args.amount_in,
        token_in=token_in_address,
        token_out=token_out_address
    )
    
    # Print the route information
    print("\nRoute information:")
    print(f"  From: {args.from_address}")
    print(f"  Amount in: {args.amount_in} ({args.token_in})")
    print(f"  Token in: {token_in_address}")
    print(f"  Token out: {token_out_address}")
    print(f"  Estimated output: {route_response.amount_out}")
    print(f"  Gas estimate: {route_response.gas}")
    print(f"  Price impact: {route_response.price_impact}%")
    
    # Execute the trade if requested
    if args.execute:
        confirm = input("\nDo you want to execute this trade? (y/n): ")
        if confirm.lower() == 'y':
            print("Executing trade...")
            tx_hash = trader.execute_trade(route_response)
            print(f"Trade executed with transaction hash: {tx_hash}")
        else:
            print("Trade cancelled.")
    else:
        print("\nTo execute the trade, run the script again with the --execute flag.")

if __name__ == "__main__":
    main() 