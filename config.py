"""
Configuration constants for the Diffbot Analytics Dashboard.

Contains all application constants, default values, error messages,
and configuration settings.
"""

# API Configuration
DEFAULT_MODEL = "diffbot-small-xl"
DIFFBOT_BASE_URL = "https://llm.diffbot.com/rag/v1"
API_TOKEN_ENV_VAR = "DIFFBOT_API_TOKEN"

# Application Defaults
DEFAULT_CONTROL_USERS = 1000
DEFAULT_CONTROL_CONVERSIONS = 50
DEFAULT_TREATMENT_USERS = 1000
DEFAULT_TREATMENT_CONVERSIONS = 65

# Error Messages
ERROR_NO_API_TOKEN = "⚠️ Diffbot API token not found. Please add it in the sidebar."
ERROR_CONFIGURE_TOKEN = "Please configure your Diffbot API token first."
ERROR_ENTER_TOPIC = "Please enter a research topic."

# Research Example Prompts
RESEARCH_EXAMPLES = {
    "mobile_retention": "What are mobile app retention rates by industry in 2024? Include fintech, gaming, and e-commerce benchmarks with day 1, day 7, and day 30 retention rates.",
    "ecommerce_conversion": "E-commerce conversion rate benchmarks by device type and industry for 2024. Include average order values and cart abandonment rates.",
    "saas_pricing": "Current SaaS pricing trends for B2B software in 2024. Include average price per seat, conversion rates by company size, and freemium vs paid model performance.",
    "email_marketing": "Email marketing benchmarks 2024: open rates, click rates, and conversion rates by industry. Include data for B2B vs B2C and mobile vs desktop performance."
}

