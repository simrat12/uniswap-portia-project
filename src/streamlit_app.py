"""
Streamlit UI for the Uniswap Portia Demo.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from .main import run_pipeline
from .uniswap_trader import get_uniswap_trader, execute_uniswap_trade

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
    st.title("Uniswap Portia Demo")
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Query Uniswap Data", "Execute Trades"])
    
    # Tab 1: Query Uniswap Data
    with tab1:
        st.header("Query Uniswap Data")
        user_prompt = st.text_area("Ask about Uniswap data:")
        if st.button("Submit Query"):
            result = run_pipeline(user_prompt)
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
                    trader = get_uniswap_trader()
                    route_response = trader.get_optimal_route(
                        from_address=wallet_address,
                        amount_in=amount_in,
                        token_in=token_in_address,
                        token_out=token_out_address
                    )
                    
                    # Display route information
                    st.subheader("Route Information")
                    st.json({
                        "From": wallet_address,
                        "Amount In": amount_in,
                        "Token In": token_in_address,
                        "Token Out": token_out_address,
                        "Estimated Output": route_response.amount_out,
                        "Gas Estimate": route_response.gas,
                        "Price Impact": f"{route_response.price_impact}%"
                    })
                    
                    # Execute trade button
                    if st.button("Execute Trade"):
                        with st.spinner("Executing trade..."):
                            try:
                                tx_hash = trader.execute_trade(route_response)
                                st.success(f"Trade executed successfully! Transaction hash: {tx_hash}")
                            except Exception as e:
                                st.error(f"Error executing trade: {str(e)}")
                except Exception as e:
                    st.error(f"Error getting optimal route: {str(e)}")

if __name__ == "__main__":
    main()
