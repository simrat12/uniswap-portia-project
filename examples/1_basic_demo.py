from src.main import run_pipeline

def main():
    prompt = "What's the total swap volume on Uniswap for token DAI?"
    plan_run_outputs = run_pipeline(prompt)
    print("Final Outputs:", plan_run_outputs)

if __name__ == "__main__":
    main()
