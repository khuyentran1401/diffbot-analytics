"""
Diffbot API integration module.

Handles all interactions with the Diffbot API including client initialization,
authentication, and analysis requests.
"""

import os
from typing import Optional

import streamlit as st
from openai import OpenAI

from config import (
    API_TOKEN_ENV_VAR,
    DEFAULT_MODEL,
    DIFFBOT_BASE_URL,
    ERROR_CONFIGURE_TOKEN,
    ERROR_NO_API_TOKEN,
)


@st.cache_resource
def get_diffbot_client() -> Optional[OpenAI]:
    """Initialize and cache the Diffbot client."""
    api_key = os.getenv(API_TOKEN_ENV_VAR)
    if not api_key:
        st.error(ERROR_NO_API_TOKEN)
        return None

    return OpenAI(base_url=DIFFBOT_BASE_URL, api_key=api_key)


def analyze_with_diffbot(query: str, model: str = DEFAULT_MODEL) -> str:
    """Send query to Diffbot and return response."""
    client = get_diffbot_client()
    if not client:
        return ERROR_CONFIGURE_TOKEN

    try:
        response = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def validate_api_key() -> bool:
    """Check if API key is configured."""
    return bool(os.getenv(API_TOKEN_ENV_VAR))