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
from src.uniswap_trader import get_uniswap_trader
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
                        choices=["all", "trader", "pipeline", "app"],
                        help="The module to view logs from")
    parser.add_argument("--test", action="store_true",
                        help="Run a test to generate logs")
    
    args = parser.parse_args()
    
    # Set the log level
    logging.getLogger().setLevel(getattr(logging, args.level))
    
    # Filter logs by module if specified
    if args.module != "all":
        for name in logging.root.manager.loggerDict:
            if name.startswith("uniswap_portia") and not name.startswith(f"uniswap_portia.{args.module}"):
                logging.getLogger(name).setLevel(logging.WARNING)
    
    print(f"Log level: {args.level}")
    print(f"Module: {args.module}")
    print("-" * 80)
    
    # Run a test to generate logs if requested
    if args.test:
        print("Running tests to generate logs...")
        
        # Test the trader
        if args.module in ["all", "trader"]:
            print("\nTesting UniswapTrader...")
            trader = get_uniswap_trader()
            print("UniswapTrader initialized")
        
        # Test the pipeline
        if args.module in ["all", "pipeline"]:
            print("\nTesting Portia pipeline...")
            result = run_pipeline("What's the volume for WETH last week?")
            print(f"Pipeline result: {result}")
    
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