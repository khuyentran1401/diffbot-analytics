"""
Diffbot API integration module.

Handles all interactions with the Diffbot API including client initialization,
authentication, and analysis requests.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from config import (
    API_TOKEN_ENV_VAR,
    DEFAULT_MODEL,
    DIFFBOT_BASE_URL,
)

# Load environment variables from .env file
load_dotenv()


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
    """Check if API key is provided and valid."""
    return bool(api_key and api_key.strip())
