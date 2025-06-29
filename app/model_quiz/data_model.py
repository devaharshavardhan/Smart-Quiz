import json
from typing import List, Dict, Any

def load_dataset(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("data", [])

def filter_dataset(dataset: List[Dict[str, Any]], goal: str, diff: str) -> List[Dict[str, Any]]:
    g = goal.lower().strip()
    return [item for item in dataset if item.get("goal", "").lower() == g and item.get("difficulty", "").lower() == diff]
