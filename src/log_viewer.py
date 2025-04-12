#!/usr/bin/env python
"""
Log viewer for the Uniswap Portia project.
This script allows you to view logs from the command line.
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Import the modules to ensure their loggers are set up
from src.uniswap_trader import get_uniswap_trader, execute_uniswap_trade
from src.main import run_pipeline

def main():
    """
    Main function for the log viewer script.
    """
    parser = argparse.ArgumentParser(description="View logs from the Uniswap Portia project")
    parser.add_argument("--level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="The minimum log level to display")
    parser.add_argument("--module", type=str, default="all",
                        choices=["all", "trader", "pipeline", "app", "portia"],
                        help="The module to view logs from")
    parser.add_argument("--test", action="store_true",
                        help="Run a test to generate logs")
    parser.add_argument("--test-trade", action="store_true",
                        help="Run a test trade to generate logs")
    
    args = parser.parse_args()
    
    # Set the log level
    logging.getLogger().setLevel(getattr(logging, args.level))
    
    # Filter logs by module if specified
    if args.module != "all":
        for name in logging.root.manager.loggerDict:
            if name.startswith("uniswap_portia") and not name.startswith(f"uniswap_portia.{args.module}"):
                logging.getLogger(name).setLevel(logging.WARNING)
    
    # Also show Portia SDK logs if requested
    if args.module == "portia" or args.module == "all":
        logging.getLogger("portia").setLevel(getattr(logging, args.level))
    
    print(f"Log level: {args.level}")
    print(f"Module: {args.module}")
    print("-" * 80)
    
    # Run a test to generate logs if requested
    if args.test:
        print("Running tests to generate logs...")
        
        # Test the trader
        if args.module in ["all", "trader", "portia"]:
            print("\nTesting UniswapTrader...")
            trader = get_uniswap_trader()
            print("UniswapTrader initialized")
        
        # Test the pipeline
        if args.module in ["all", "pipeline"]:
            print("\nTesting Portia pipeline...")
            result = run_pipeline("What's the volume for WETH last week?")
            print(f"Pipeline result: {result}")
    
    # Run a test trade if requested
    if args.test_trade:
        print("\nTesting Uniswap trade...")
        # Use default values for testing
        from_address = os.getenv("WALLET_ADDRESS", "0xD599b4840Da7ABB19A7BAe8F70FBA422eabf783C")
        amount_in = "1000000000000000000"  # 1 ETH in wei
        token_in = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"  # ETH (all lowercase)
        token_out = "0x6b175474e89094c44da98b954eedeac495271d0f"  # DAI (all lowercase)
        
        try:
            tx_hash = execute_uniswap_trade(from_address, amount_in, token_in, token_out)
            print(f"Trade executed with transaction hash: {tx_hash}")
        except Exception as e:
            print(f"Error executing trade: {str(e)}")
    
    print("\nLog viewer is ready. Press Ctrl+C to exit.")
    print("Logs will be displayed as they are generated.")
    print("To generate logs, use the Streamlit app or run the example scripts.")
    
    # Keep the script running to display logs
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nLog viewer stopped.")

if __name__ == "__main__":
    main() 