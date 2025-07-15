"""
Diffbot API integration module.

Handles all interactions with the Diffbot API including client initialization,
authentication, and analysis requests.
"""

import os
from typing import Optional

from openai import OpenAI


def analyze_with_diffbot(
	query: str,
	api_key: Optional[str] = None,
	model: str = "diffbot-small-xl",
	base_url: str = "https://llm.diffbot.com/rag/v1",
	token_env_var: str = "DIFFBOT_API_TOKEN"
) -> str:
	"""Send query to Diffbot and return response."""
	# Use provided api_key or get from environment
	effective_api_key = api_key or os.getenv(token_env_var)

	client = OpenAI(base_url=base_url, api_key=effective_api_key)
	response = client.chat.completions.create(
		model=model, messages=[{"role": "user", "content": query}]
	)
	return response.choices[0].message.content or ""


def validate_api_key(api_key: Optional[str] = None) -> bool:
	"""Check if API key is provided and valid."""
	return bool(api_key and api_key.strip())
