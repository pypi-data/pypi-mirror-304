import json
from typing import Optional

import requests
from ovos_utils.log import LOG

from ovos_plugin_manager.templates.solvers import QuestionSolver


class JabirLLMSolver(QuestionSolver):
    url = 'https://api.jabirproject.org/generate'
    enable_tx = False
    priority = 60

    def __init__(self, config=None):
        config = config or {}
        super().__init__(config)

    def get_spoken_answer(self, query: str,
                          lang: Optional[str] = None,
                          units: Optional[str] = None) -> Optional[str]:
        headers = {"apikey": self.config.get("key", "a4d5e154-31f0-4e0d-a66d-c3cc32542da5"),
                   "Content-Type": "application/json"}

        res = requests.post(self.url, headers=headers,
                            data=json.dumps(
                                {"messages": [{"role": "user", "content": query}]})
                            ).json()
        if "error" in res:
            LOG.error(res["error"])
            return None
        return res["result"]["content"]
