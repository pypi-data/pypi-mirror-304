import json
from collections import namedtuple

LLMResult = namedtuple("LLMResult", ["raw", "content"])


def loadch(resp):
    try:
        return (
            json.loads(
                (resp.strip().removeprefix("```json").removesuffix("```").strip())
            ),
            True,
        )
    except (TypeError, json.decoder.JSONDecodeError):
        pass
    return None, False


class LLMMixin:
    def generate_checked(self, transformFn, system, prompt, retries=5):
        for i in range(retries):
            res = self.generate(system, prompt)
            transformed, success = transformFn(res.content)
            if success:
                return LLMResult(res.raw, transformed)
        return LLMResult(res.raw, None)

    def generate_json(self, system, prompt, retries=5):
        return self.generate_checked(loadch, system, prompt, retries=retries)
