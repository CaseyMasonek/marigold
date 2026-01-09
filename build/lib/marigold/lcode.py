from pathlib import Path

here = Path(__file__).parent

with open(here / "lambdas.py") as f:
    lambdacode = f.read()