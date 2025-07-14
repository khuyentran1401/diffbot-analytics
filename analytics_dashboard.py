"""
Conversational Analytics Dashboard using Diffbot LLM.

A Streamlit application for A/B testing analysis and market research
with transparent calculations.
"""

import os
from datetime import datetime
from typing import Any, Tuple

import streamlit as st

from config import (
    API_TOKEN_ENV_VAR,
    DEFAULT_CONTROL_CONVERSIONS,
    DEFAULT_CONTROL_USERS,
    DEFAULT_TREATMENT_CONVERSIONS,
    DEFAULT_TREATMENT_USERS,
    ERROR_ENTER_TOPIC,
    RESEARCH_EXAMPLES,
)
from diffbot_api import analyze_with_diffbot, validate_api_key
from utils import (
    calculate_conversion_rate,
    create_ab_test_visualization,
    export_results_to_csv,
)


def initialize_session_state(key: str, default_value: Any) -> None:
    """Initialize session state variable if not exists."""
    if key not in st.session_state:
        st.session_state[key] = default_value


def setup_page_config() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Diffbot Analytics Dashboard",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_sidebar() -> Tuple[str, str]:
    """
    Render sidebar with API configuration and model selection.

    Returns:
        Tuple of (api_key, model_choice)
    """
    st.sidebar.header("⚙️ Configuration")

    # API Key Configuration
    api_key = st.sidebar.text_input(
        "🔑 Diffbot API Token",
        type="password",
        help="Enter your Diffbot API token. Get one at https://app.diffbot.com/get-started",
        value=st.session_state.get("api_key", "") or os.getenv(API_TOKEN_ENV_VAR, ""),
    )

    # Store API key in session state
    if api_key:
        st.session_state.api_key = api_key
        if validate_api_key(api_key):
            st.sidebar.success("✅ API key valid")
        else:
            st.sidebar.error("❌ Invalid API key")
    else:
        st.sidebar.info(f"💡 Set {API_TOKEN_ENV_VAR} environment variable to auto-fill")

    # Model Selection
    model_choice = st.sidebar.selectbox(
        "🤖 Model Selection",
        ["diffbot-small-xl", "diffbot-medium-xl", "diffbot-large-xl"],
        help="Choose the AI model for analysis",
    )

    return api_key, model_choice


def render_ab_test_tab(api_key: str, model_choice: str) -> None:
    """Render A/B test analyzer tab."""
    st.header("📈 A/B Test Analysis")
    st.markdown(
        "Compare control and treatment groups with statistical significance testing."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Control Group")
        control_users = st.number_input(
            "Number of Users",
            min_value=1,
            value=DEFAULT_CONTROL_USERS,
            help="Total users in control group",
        )
        control_conversions = st.number_input(
            "Conversions",
            min_value=0,
            max_value=control_users,
            value=min(DEFAULT_CONTROL_CONVERSIONS, control_users),
            help="Number of conversions in control group",
        )
        control_rate = calculate_conversion_rate(control_conversions, control_users)
        st.metric("Conversion Rate", f"{control_rate:.2f}%")

    with col2:
        st.subheader("🧪 Treatment Group")
        treatment_users = st.number_input(
            "Number of Users",
            min_value=1,
            value=DEFAULT_TREATMENT_USERS,
            help="Total users in treatment group",
            key="treatment_users",
        )
        treatment_conversions = st.number_input(
            "Conversions",
            min_value=0,
            max_value=treatment_users,
            value=min(DEFAULT_TREATMENT_CONVERSIONS, treatment_users),
            help="Number of conversions in treatment group",
            key="treatment_conversions",
        )
        treatment_rate = calculate_conversion_rate(
            treatment_conversions, treatment_users
        )
        st.metric("Conversion Rate", f"{treatment_rate:.2f}%")

    # Analysis Button
    if st.button("🔍 Analyze A/B Test", type="primary"):
        if not api_key:
            st.error("Please configure your Diffbot API token in the sidebar.")
            return

        # Create visualization
        fig = create_ab_test_visualization(
            control_users, control_conversions, treatment_users, treatment_conversions
        )
        st.plotly_chart(fig, use_container_width=True)

        # Prepare analysis prompt
        prompt = f"""
        Analyze this A/B test with the following data:
        
        Control Group:
        - Users: {control_users}
        - Conversions: {control_conversions}
        - Conversion Rate: {control_rate:.2f}%
        
        Treatment Group:
        - Users: {treatment_users}
        - Conversions: {treatment_conversions}
        - Conversion Rate: {treatment_rate:.2f}%
        
        Please provide:
        1. Statistical significance test with p-value
        2. Confidence intervals for both groups
        3. Practical significance and business impact
        4. Recommendations based on results
        5. JavaScript code for calculations
        """

        with st.spinner("🔍 Analyzing A/B test..."):
            try:
                result = analyze_with_diffbot(prompt, api_key, model_choice)
                st.markdown("### 📊 Analysis Results")
                st.markdown(result)

                # Export button
                export_data = [
                    {
                        "timestamp": datetime.now().isoformat(),
                        "type": "A/B Test Analysis",
                        "control_users": control_users,
                        "control_conversions": control_conversions,
                        "treatment_users": treatment_users,
                        "treatment_conversions": treatment_conversions,
                        "result": result,
                    }
                ]
                filename = f"ab_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                st.markdown(
                    export_results_to_csv(export_data, filename), unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")


def render_market_research_tab(api_key: str, model_choice: str) -> None:
    """Render market research tab."""
    st.header("🔍 Real-time Market Research")
    st.markdown(
        "Get current market data, trends, and benchmarks with proper source citations."
    )

    initialize_session_state("research_topic", "")

    research_topic = st.text_input(
        "🎯 What would you like to research?",
        value=st.session_state.research_topic,
        placeholder="Click an example below or type your own research question...",
        help="Be specific for better results. Include year, industry, or metric type.",
    )

    st.session_state.research_topic = research_topic

    st.markdown("**Try these example research prompts:**")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📱 Mobile App Retention by Industry", use_container_width=True):
            st.session_state.research_topic = RESEARCH_EXAMPLES["mobile_retention"]
            st.rerun()

        if st.button("🛒 E-commerce Conversion Benchmarks", use_container_width=True):
            st.session_state.research_topic = RESEARCH_EXAMPLES["ecommerce_conversion"]
            st.rerun()

    with col2:
        if st.button("💰 SaaS Pricing & Conversion Trends", use_container_width=True):
            st.session_state.research_topic = RESEARCH_EXAMPLES["saas_pricing"]
            st.rerun()

        if st.button("📧 Email Marketing Benchmarks", use_container_width=True):
            st.session_state.research_topic = RESEARCH_EXAMPLES["email_marketing"]
            st.rerun()

    if st.button("🔍 Research Topic", type="primary"):
        if not research_topic:
            st.warning(ERROR_ENTER_TOPIC)
            return

        if not api_key:
            st.error("Please configure your Diffbot API token in the sidebar.")
            return

        research_query = f"""
        Research this topic thoroughly and provide current, accurate information: {research_topic}
        
        Please include:
        1. Current statistics and benchmarks
        2. Industry trends and insights
        3. Source citations for all data
        4. Actionable recommendations
        5. Relevant time periods and context
        """

        with st.spinner("🔍 Researching topic..."):
            try:
                result = analyze_with_diffbot(research_query, api_key, model_choice)
                st.markdown("### 📊 Research Results")
                st.markdown(result)

                # Export button
                export_data = [
                    {
                        "timestamp": datetime.now().isoformat(),
                        "type": "Market Research",
                        "query": research_topic,
                        "result": result,
                    }
                ]
                filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                st.markdown(
                    export_results_to_csv(export_data, filename), unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"Research failed: {str(e)}")


# Main Streamlit Application
def main() -> None:
    """Main Streamlit application function."""
    setup_page_config()

    st.title("🤖 Conversational Analytics Dashboard")
    st.markdown(
        "*Powered by Diffbot LLM - Get instant insights with transparent calculations*"
    )

    api_key, model_choice = render_sidebar()

    tab1, tab2 = st.tabs(
        [
            "📈 A/B Test Analyzer",
            "🔍 Market Research",
        ]
    )

    with tab1:
        render_ab_test_tab(api_key, model_choice)

    with tab2:
        render_market_research_tab(api_key, model_choice)

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
