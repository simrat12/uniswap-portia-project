import os
import logging
from dotenv import load_dotenv
from portia import Portia, default_config
from custom_tool import CustomTool
from config import UniswapProjectConfig
from uniswap_trader import get_uniswap_trader, execute_uniswap_trade

# Set up logging
logger = logging.getLogger("uniswap_portia.pipeline")

load_dotenv()

def get_portia_instance():
    """
    Set up a Portia instance with default_config, adding your custom tool.
    """
    logger.info("Initializing Portia instance")
    
    # 1) Possibly create or retrieve your own config
    project_config = UniswapProjectConfig()
    # 2) Build a Portia config
    #    e.g. storage_class=MEMORY, or pass in your own logic
    config = default_config()

    # 3) If you want to store data in the cloud, ensure PORTIA_API_KEY is set, etc.

    # 4) Instantiate your custom tool
    custom_tool = CustomTool()
    logger.info("Custom tool initialized")

    # 5) Create the Portia instance with your custom tool
    portia = Portia(config=config, tools=[custom_tool])
    logger.info("Portia instance initialized successfully")
    return portia

def run_pipeline(user_prompt: str):
    """
    This function runs the entire pipeline:
      - Takes user prompt
      - Uses Portia to plan and run
      - Possibly calls your custom tool (Uniswap data) behind the scenes
      - Returns the final output or plan_run
    """
    logger.info(f"Running pipeline with user prompt: {user_prompt}")
    
    portia = get_portia_instance()
    
    logger.info("Planning with Portia")
    plan = portia.plan(user_prompt)
    logger.info(f"Plan created: {plan}")
    
    logger.info("Running plan with Portia")
    plan_run = portia.run_plan(plan)
    logger.info(f"Plan run completed with {len(plan_run.outputs.step_outputs)} outputs")
    
    return plan_run.outputs.step_outputs

if __name__ == "__main__":
    # Example usage from command line:
    # python -m src.main "What's the volume for WETH last week?"
    import sys
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = "Tell me about the last 10 trades on Uniswap"

    logger.info(f"Running main script with prompt: {user_prompt}")
    outputs = run_pipeline(user_prompt)
    logger.info(f"Pipeline outputs: {outputs}")
    print("[DEBUG] Outputs:", outputs)
    
    # Example of using the UniswapTrader
    # Uncomment and modify these values to execute a trade
    """
    from_address = "your-address"
    amount_in = "1000000000000000000"  # 1 ETH in wei
    token_in = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"  # ETH
    token_out = "0x6b175474e89094c44da98b954eedeac495271d0f"  # DAI
    
    tx_hash = execute_uniswap_trade(from_address, amount_in, token_in, token_out)
    print(f"Trade executed with transaction hash: {tx_hash}")
    """
