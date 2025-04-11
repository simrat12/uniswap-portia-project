"""
Another example that might ask for a more detailed set of slides or data.
"""
from src.main import run_pipeline

def main():
    prompt = ("Generate a short PPT about the top 5 trading pairs on Uniswap. "
              "Include trade volume and some insights from the last week.")
    outputs = run_pipeline(prompt)
    print("PlanRun Outputs:", outputs)

if __name__ == "__main__":
    main()
