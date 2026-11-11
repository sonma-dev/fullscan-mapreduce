import os
from contextlib import asynccontextmanager

from azure.core.credentials import TokenCredential
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from fastapi import Request

from plugins.talks_with_responses.talks_with_responses import TalksWithResponses
from server.models import AppServices


def build_credential() -> TokenCredential:
    env = os.getenv("APP_ENV", "development").lower()
    use_mid_env = ("prod", "production", "staging")

    if env in use_mid_env:
        client_id = os.getenv("AZURE_CLIENT_ID")
        if client_id:
            return ManagedIdentityCredential(client_id=client_id)
        return ManagedIdentityCredential()

    client_id = os.getenv("AZURE_CLIENT_ID")
    if client_id:
        return DefaultAzureCredential(managed_identity_client_id=client_id)
    return DefaultAzureCredential()


def build_services() -> AppServices:
    openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("You haven't defined AZURE_OPENAI_API_KEY.")

    openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not openai_endpoint:
        raise RuntimeError("You haven't defined AZURE_OPENAI_ENDPOINT.")

    openai_modelname = (
        os.getenv("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME")
        or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    )
    if not openai_modelname:
        raise RuntimeError(
            "You haven't defined AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME or AZURE_OPENAI_CHAT_DEPLOYMENT_NAME."
        )

    credential = build_credential()

    def openai_retrieve_token() -> str:
        env = os.getenv("APP_ENV", "development").lower()
        if env in ("prod", "production", "staging"):
            token_inst = credential.get_token("https://cognitiveservices.azure.com/.default")
            return token_inst.token
        return openai_api_key

    env = os.getenv("APP_ENV", "development").lower()
    auth_mode = "entra" if env in ("prod", "production", "staging") else "api_key"

    return AppServices(
        responses=TalksWithResponses(
            endpoint=openai_endpoint,
            token_provider=openai_retrieve_token,
            model_name=openai_modelname,
            api_version="2025-03-01-preview",
            auth_mode=auth_mode,
        ),
    )


def get_services(request: Request):
    return request.app.state.services


@asynccontextmanager
async def lifespan(app):
    app.state.services = build_services()
    try:
        yield
    finally:
        await app.state.services.responses.close()
