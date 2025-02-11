# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import openai
import os
import sys

from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def get_client(endpoint, key):
    # If the endpoint is passed as "default", pick it up from the environment variable.
    endpoint = os.getenv("ENDPOINT") if endpoint == "default" else endpoint

    if key is None or key == "":
        # Using Azure keyless access (Azure AD token provider)
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
        print("Token provider:", token_provider)
        print("Azure endpoint:", endpoint)
        client = openai.AzureOpenAI(
            api_version="2024-02-15-preview",
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider
        )
    elif endpoint == 'openai':
        # Standard OpenAI endpoint
        client = openai.OpenAI(api_key=key)
    elif endpoint == 'openrouter':
        # OpenRouter support: use a custom API base URL.
        # You can override the default base URL by setting the OPENROUTER_API_BASE environment variable.
        api_base = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
        client = openai.OpenAI(api_key=key, base_url=api_base)
    else:
        # Azure OpenAI with API key provided
        client = openai.AzureOpenAI(
            azure_endpoint=endpoint,  
            api_key=key,  
            api_version="2024-02-15-preview"
        )
    return client