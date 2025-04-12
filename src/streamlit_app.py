"""
Streamlit UI for the Uniswap Portia Demo.
"""

import streamlit as st
import os
import logging
import sys
import json
from io import StringIO
from dotenv import load_dotenv
from main import run_pipeline
from uniswap_trader import get_uniswap_trader, execute_uniswap_trade
from eth_utils import to_checksum_address, to_normalized_address

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uniswap_portia")

# Create a custom handler to capture logs
class StreamlitLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_stream = StringIO()
        
    def emit(self, record):
        msg = self.format(record)
        self.log_stream.write(msg + '\n')
        
    def get_logs(self):
        return self.log_stream.getvalue()
        
    def clear_logs(self):
        self.log_stream = StringIO()

# Add the custom handler to the logger
log_handler = StreamlitLogHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(log_handler)

# Common token addresses - ensure ETH is all lowercase
COMMON_TOKENS = {
    "ETH": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",  # All lowercase for ETH
    "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f",  # All lowercase for DAI
    "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # All lowercase for USDC
    "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # All lowercase for USDT
    "WBTC": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",  # All lowercase for WBTC
    "WETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # All lowercase for WETH
}

def main():
    st.title("Uniswap Portia Demo")
    
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Query Uniswap Data", "Execute Trades", "View Logs"])
    
    # Tab 1: Query Uniswap Data
    with tab1:
        st.header("Query Uniswap Data")
        user_prompt = st.text_area("Ask about Uniswap data:")
        if st.button("Submit Query"):
            logger.info(f"User submitted query: {user_prompt}")
            result = run_pipeline(user_prompt)
            logger.info(f"Query result: {result}")
            st.write("Plan Run Output:", result)
    
    # Tab 2: Execute Trades
    with tab2:
        st.header("Execute Trades on Uniswap")
        
        # Get wallet address
        wallet_address = st.text_input(
            "Your Wallet Address", 
            value=os.getenv("WALLET_ADDRESS", ""),
            help="The Ethereum address that will execute the trade"
        )
        
        # Create two columns for token selection
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Token In")
            token_in_option = st.selectbox(
                "Select Token In",
                options=list(COMMON_TOKENS.keys()),
                index=0
            )
            token_in_address = COMMON_TOKENS[token_in_option]
            st.text(f"Address: {token_in_address}")
            
            # Amount input
            amount_in = st.text_input(
                "Amount In (in wei)",
                value="1000000000000000000",  # 1 ETH in wei
                help="Amount in wei (e.g., 1000000000000000000 for 1 ETH)"
            )
        
        with col2:
            st.subheader("Token Out")
            token_out_option = st.selectbox(
                "Select Token Out",
                options=list(COMMON_TOKENS.keys()),
                index=1
            )
            token_out_address = COMMON_TOKENS[token_out_option]
            st.text(f"Address: {token_out_address}")
        
        # Get optimal route
        if st.button("Get Optimal Route"):
            with st.spinner("Calculating optimal route..."):
                try:
                    logger.info(f"Getting optimal route for {amount_in} {token_in_option} to {token_out_option}")
                    trader = get_uniswap_trader()
                    
                    # Format parameters correctly for the Enso API
                    # 1. fromAddress must be a single Ethereum address (checksummed)
                    formatted_from_address = to_checksum_address(wallet_address)
                    
                    # 2. amountIn must be a list of strings
                    formatted_amount_in = [str(amount_in)]
                    
                    # 3. tokenIn must be a list of Ethereum addresses
                    # For ETH, use the special format with mixed case
                    if token_in_address.lower() == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee":
                        formatted_token_in = ["0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"]
                    else:
                        formatted_token_in = [token_in_address.lower()]
                    
                    # 4. tokenOut must be a list of Ethereum addresses
                    formatted_token_out = [token_out_address.lower()]
                    
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
                    
                    # Call the API with the correctly formatted parameters
                    route_response = trader.get_optimal_route(
                        from_address=formatted_from_address,
                        amount_in=formatted_amount_in,
                        token_in=formatted_token_in,
                        token_out=formatted_token_out,
                        variable_estimates=None
                    )
                    
                    # Handle the case where route_response is a dictionary instead of a UniswapRouteResponse object
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
                        
                        # Display route information
                        st.subheader("Route Information")
                        st.json({
                            "From": formatted_from_address,
                            "Amount In": formatted_amount_in,
                            "Token In": formatted_token_in,
                            "Token Out": formatted_token_out,
                            "Estimated Output": route_response["amount_out"],
                            "Gas Estimate": route_response["gas"],
                            "Price Impact": f"{route_response['price_impact']}%"
                        })
                    else:
                        # Display route information for UniswapRouteResponse object
                        st.subheader("Route Information")
                        st.json({
                            "From": formatted_from_address,
                            "Amount In": formatted_amount_in,
                            "Token In": formatted_token_in,
                            "Token Out": formatted_token_out,
                            "Estimated Output": route_response.amount_out,
                            "Gas Estimate": route_response.gas,
                            "Price Impact": f"{route_response.price_impact}%"
                        })
                    
                    # Execute trade button
                    if st.button("Execute Trade"):
                        with st.spinner("Executing trade..."):
                            try:
                                logger.info(f"Executing trade for {amount_in} {token_in_option} to {token_out_option}")
                                tx_hash = trader.execute_trade(route_response)
                                logger.info(f"Trade executed successfully with tx hash: {tx_hash}")
                                st.success(f"Trade executed successfully! Transaction hash: {tx_hash}")
                            except Exception as e:
                                logger.error(f"Error executing trade: {str(e)}")
                                st.error(f"Error executing trade: {str(e)}")
                except Exception as e:
                    logger.error(f"Error getting optimal route: {str(e)}")
                    st.error(f"Error getting optimal route: {str(e)}")
    
    # Tab 3: View Logs
    with tab3:
        st.header("Application Logs")
        
        # Add a button to clear logs
        if st.button("Clear Logs"):
            log_handler.clear_logs()
            st.success("Logs cleared!")
        
        # Display logs
        logs = log_handler.get_logs()
        st.text_area("Logs", value=logs, height=400)
        
        # Add a button to download logs
        st.download_button(
            label="Download Logs",
            data=logs,
            file_name="uniswap_portia_logs.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
