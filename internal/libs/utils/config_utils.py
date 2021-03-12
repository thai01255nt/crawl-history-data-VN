import os
from typing import Dict


def get_system_config(config: Dict) -> Dict:
    results = {k: os.environ[v] for k, v in config.items()}
    return results
