#!/bin/bash

# Install Portia SDK in editable mode
echo "Installing Portia SDK..."
uv pip install -e /home/simrat12/portia-sdk-python

# Run Streamlit app
echo "Starting Streamlit app..."
streamlit run src/streamlit_app.py 