"""
Placeholder for a Streamlit UI that your colleague will fill in.
"""

import streamlit as st
from .main import run_pipeline

def main():
    st.title("Uniswap Portia Demo")
    user_prompt = st.text_area("Ask about Uniswap data:")
    if st.button("Submit"):
        result = run_pipeline(user_prompt)
        st.write("Plan Run Output:", result)

if __name__ == "__main__":
    main()
