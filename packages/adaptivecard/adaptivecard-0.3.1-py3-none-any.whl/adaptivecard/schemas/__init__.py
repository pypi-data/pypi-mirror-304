import json
from pathlib import Path

path = Path(__file__).parent / "schema.json"

with open(path) as f:
    schema = json.load(f)