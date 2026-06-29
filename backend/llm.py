"""Azure OpenAI chat client, env-configurable, mockable.

Swap to real Microsoft Agent Framework agents in deployment; for local dev
and tests inject any object with a `complete(model, system, user)` method.
"""
import os


class AzureClient:
    def complete(self, model: str, system: str, user: str) -> str:
        from openai import AzureOpenAI

        endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        key = os.environ.get("AZURE_OPENAI_API_KEY")
        if key:
            client = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version=version)
        else:
            from azure.identity import DefaultAzureCredential, get_bearer_token_provider

            token = get_bearer_token_provider(
                DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
            )
            client = AzureOpenAI(
                azure_endpoint=endpoint, azure_ad_token_provider=token, api_version=version
            )
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return resp.choices[0].message.content or ""


class FoundryAgentClient:
    """Microsoft Agent Framework agent over an Azure AI Foundry model."""

    def complete(self, model: str, system: str, user: str) -> str:
        from agent_framework.azure import AzureAIAgentClient

        agent = AzureAIAgentClient(
            endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
            model_deployment=model,
        ).create_agent(instructions=system)
        return str(agent.run(user))


def default_client():
    if os.environ.get("USE_FOUNDRY_AGENT") == "1":
        return FoundryAgentClient()
    return AzureClient()
