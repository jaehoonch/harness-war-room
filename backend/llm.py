"""Azure OpenAI chat client, env-configurable, mockable.

Swap to real Microsoft Agent Framework agents in deployment; for local dev
and tests inject any object with a `complete(model, system, user)` method.
"""
import os


class AzureClient:
    def complete(self, model: str, system: str, user: str) -> str:
        from openai import AzureOpenAI

        client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return resp.choices[0].message.content or ""


def default_client():
    return AzureClient()
