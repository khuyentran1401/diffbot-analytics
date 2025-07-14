"""
Conversational Analytics Dashboard using Diffbot LLM.

A Streamlit application for A/B testing analysis, market research,
with transparent calculations.

This file serves as both the main Streamlit app and provides
programmatic access to core analysis functions.
"""

from typing import Optional

import pandas as pd
import streamlit as st

from config import DEFAULT_MODEL
from data_utils import (
    calculate_conversion_rate,
    export_results_to_csv,
)
from diffbot_api import analyze_with_diffbot, validate_api_key
from ui_components import (
    render_ab_test_tab,
    render_history_tab,
    render_market_research_tab,
    render_sidebar,
    setup_page_config,
)


# Direct Analysis Functions for Programmatic Use
def analyze_ab_test(
    control_users: int,
    control_conversions: int,
    treatment_users: int,
    treatment_conversions: int,
    api_key: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Perform A/B test analysis programmatically.

    Args:
        control_users: Number of users in control group
        control_conversions: Number of conversions in control group
        treatment_users: Number of users in treatment group
        treatment_conversions: Number of conversions in treatment group
        api_key: Diffbot API key
        model: Model to use for analysis

    Returns:
        Analysis result as string
    """
    control_rate = calculate_conversion_rate(control_conversions, control_users)
    treatment_rate = calculate_conversion_rate(treatment_conversions, treatment_users)

    query = f"""
    Analyze my A/B test results:
    - Control: {control_users} users with {control_conversions} conversions ({control_rate:.2f}% conversion rate)
    - Treatment: {treatment_users} users with {treatment_conversions} conversions ({treatment_rate:.2f}% conversion rate)
    
    Calculate statistical significance, p-value, confidence intervals, and interpret results.
    Provide the executable JavaScript code for calculations.
    """

    return analyze_with_diffbot(query, model)


def research_topic(query: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    """
    Perform market research on a topic programmatically.

    Args:
        query: Research question or topic
        api_key: Diffbot API key
        model: Model to use for research

    Returns:
        Research result as string
    """
    research_query = f"""
    Research current trends and data about: {query}
    
    Provide:
    1. Specific statistics and metrics
    2. Recent industry data (prefer 2024 data)
    3. Cite recent, credible sources with URLs
    4. Compare different industries or segments if relevant
    5. Identify key trends and patterns
    """

    return analyze_with_diffbot(research_query, model)



# Utility Functions


def calculate_stats(conversions: int, users: int) -> dict:
    """
    Calculate basic conversion statistics.

    Args:
        conversions: Number of conversions
        users: Number of users

    Returns:
        Dictionary with conversion rate and other stats
    """
    rate = calculate_conversion_rate(conversions, users)
    return {
        "conversion_rate": rate,
        "conversion_rate_decimal": rate / 100,
        "conversions": conversions,
        "users": users,
        "non_conversions": users - conversions,
    }


def export_to_csv(data: list, filename: str) -> str:
    """
    Export data to CSV format.

    Args:
        data: List of dictionaries to export
        filename: Name for the CSV file

    Returns:
        HTML link for download
    """
    return export_results_to_csv(data, filename)


def setup_dashboard() -> None:
    """Initialize dashboard with default settings."""
    setup_page_config()


def validate_setup(api_key: Optional[str] = None) -> bool:
    """
    Check if dashboard is properly configured.

    Args:
        api_key: Optional API key to validate

    Returns:
        True if setup is valid
    """
    if api_key:
        import os
        from config import API_TOKEN_ENV_VAR

        os.environ[API_TOKEN_ENV_VAR] = api_key

    return validate_api_key()


# Main Streamlit Application
def main() -> None:
    """Main Streamlit application function."""
    setup_page_config()

    st.title("🤖 Conversational Analytics Dashboard")
    st.markdown(
        "*Powered by Diffbot LLM - Get instant insights with transparent calculations*"
    )

    api_key, model_choice = render_sidebar()

    tab1, tab2, tab3 = st.tabs(
        [
            "📈 A/B Test Analyzer",
            "🔍 Market Research",
            "📋 Analysis History",
        ]
    )

    with tab1:
        render_ab_test_tab(api_key, model_choice)

    with tab2:
        render_market_research_tab(api_key, model_choice)

    with tab3:
        render_history_tab()

    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        Built with ❤️ using Streamlit and Diffbot LLM | 
        <a href='https://github.com/yourusername/diffbot-analytics' target='_blank'>View Source</a> |
        <a href='https://app.diffbot.com/get-started' target='_blank'>Get Diffbot API Key</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
