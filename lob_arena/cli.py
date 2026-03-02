import typer
app = typer.Typer()

@app.command()
def battle(strategies: str, steps: int = 10000):
    """Run strategy battle"""
    print(f"🚀 Battling {strategies} for {steps} steps!")
    # TODO: Implement

if __name__ == "__main__":
    app()
