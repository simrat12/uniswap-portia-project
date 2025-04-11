import os
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv

# You may also import relevant Portia enums if you want to unify them with your own config
# e.g. from portia import LLMProvider, StorageClass, Config as PortiaConfig

load_dotenv()

class UniswapProjectConfig(BaseModel):
    """
    Example configuration for your Uniswap pipeline.
    Extend with whatever fields you need for your custom logic or tool.
    """
    # We'll store the subgraph endpoint in an env var
    uniswap_endpoint: str = Field(
        default_factory=lambda: os.getenv("UNISWAP_SUBGRAPH_ENDPOINT", ""),
        description="GraphQL endpoint for the Uniswap subgraph"
    )
    openai_api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("OPENAI_API_KEY", "")),
        description="OpenAI API key"
    )
    portia_api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("PORTIA_API_KEY", "")),
        description="Portia API key for cloud usage"
    )
    enso_api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("ENSO_API_KEY", "")),
        description="Enso API key for Uniswap trading"
    )

    # Optionally, add more toggles or references to LLM providers
    # or reuse the actual Portia Config if you want.
