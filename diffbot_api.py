"""
Diffbot API integration module.

Handles all interactions with the Diffbot API including client initialization,
authentication, and analysis requests.
"""

import os
from typing import Optional

from openai import OpenAI

from config import (
    API_TOKEN_ENV_VAR,
    DEFAULT_MODEL,
    DIFFBOT_BASE_URL,
)


def analyze_with_diffbot(query: str, api_key: Optional[str] = None, model: str = DEFAULT_MODEL) -> str:
    """Send query to Diffbot and return response."""
    # Use provided api_key or get from environment
    effective_api_key = api_key or os.getenv(API_TOKEN_ENV_VAR)
    
    client = OpenAI(base_url=DIFFBOT_BASE_URL, api_key=effective_api_key)
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content


def validate_api_key(api_key: Optional[str] = None) -> bool:
    """Check if API key is configured and valid."""
    if api_key:
        return bool(api_key and api_key.strip())
    return bool(os.getenv(API_TOKEN_ENV_VAR))