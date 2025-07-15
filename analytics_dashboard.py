"""
Conversational Analytics Dashboard using Diffbot LLM.

A Streamlit application for A/B testing analysis and market research
with transparent calculations.
"""

import os
from typing import Any, Tuple

import streamlit as st
from dotenv import load_dotenv
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig

from diffbot_api import analyze_with_diffbot, validate_api_key
from utils import (
	calculate_conversion_rate,
	create_ab_test_visualization,
)


def initialize_session_state(key: str, default_value: Any) -> None:
	"""Initialize session state variable if not exists."""
	if key not in st.session_state:
		st.session_state[key] = default_value


def setup_page_config(cfg: DictConfig) -> None:
	"""Configure Streamlit page settings."""
	st.set_page_config(
		page_title=cfg.page.title,
		page_icon=cfg.page.icon,
		layout=cfg.page.layout,
		initial_sidebar_state=cfg.page.sidebar_state,
	)


def render_sidebar(cfg: DictConfig) -> Tuple[str, str]:
	"""
	Render sidebar with API configuration and model selection.

	Returns:
		Tuple of (api_key, model_choice)
	"""
	st.sidebar.header("⚙️ Configuration")

	# API Key Configuration
	try:
		default_token_env = cfg.api.token_env_var
		signup_url = cfg.urls.diffbot_signup
	except Exception:
		# Fallback if config access fails
		default_token_env = "DIFFBOT_API_TOKEN"
		signup_url = "https://app.diffbot.com/get-started"

	api_key = st.sidebar.text_input(
		"🔑 Diffbot API Token",
		type="password",
		help=f"Enter your Diffbot API token. Get one at {signup_url}",
		value=st.session_state.get("api_key", "") or os.getenv(default_token_env, ""),
	)

	# Store API key in session state
	if api_key:
		st.session_state.api_key = api_key
		if validate_api_key(api_key):
			st.sidebar.success("✅ API key provided")
		else:
			st.sidebar.error("❌ API key required")
	else:
		try:
			env_var_name = cfg.api.token_env_var
		except Exception:
			env_var_name = "DIFFBOT_API_TOKEN"
		st.sidebar.info(f"💡 Set {env_var_name} environment variable to auto-fill")

	# Model Selection
	try:
		available_models = list(cfg.api.available_models)
	except Exception:
		# Fallback models if config access fails
		available_models = ["diffbot-small-xl", "diffbot-small"]

	model_choice = st.sidebar.selectbox(
		"🤖 Model Selection",
		available_models,
		help="Choose the AI model for analysis",
	)

	return api_key, model_choice


def render_ab_test_tab(cfg: DictConfig, api_key: str, model_choice: str) -> None:
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
			value=cfg.app_defaults.control_users,
			help="Total users in control group",
		)
		control_conversions = st.number_input(
			"Conversions",
			min_value=0,
			max_value=control_users,
			value=min(cfg.app_defaults.control_conversions, control_users),
			help="Number of conversions in control group",
		)
		control_rate = calculate_conversion_rate(control_conversions, control_users)
		st.metric("Conversion Rate", f"{control_rate:.2f}%")

	with col2:
		st.subheader("🧪 Treatment Group")
		treatment_users = st.number_input(
			"Number of Users",
			min_value=1,
			value=cfg.app_defaults.treatment_users,
			help="Total users in treatment group",
			key="treatment_users",
		)
		treatment_conversions = st.number_input(
			"Conversions",
			min_value=0,
			max_value=treatment_users,
			value=min(cfg.app_defaults.treatment_conversions, treatment_users),
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
		prompt = cfg.prompts.ab_test.format(
			control_users=control_users,
			control_conversions=control_conversions,
			control_rate=control_rate,
			treatment_users=treatment_users,
			treatment_conversions=treatment_conversions,
			treatment_rate=treatment_rate,
		)

		with st.spinner("🔍 Analyzing A/B test..."):
			try:
				result = analyze_with_diffbot(
					prompt,
					api_key,
					model_choice,
					cfg.api.base_url,
					cfg.api.token_env_var
				)
				st.markdown("### 📊 Analysis Results")
				st.markdown(result)

			except Exception as e:
				st.error(f"Analysis failed: {str(e)}")


def render_market_research_tab(cfg: DictConfig, api_key: str, model_choice: str) -> None:
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
			st.session_state.research_topic = cfg.research_examples.mobile_retention
			st.rerun()

		if st.button("🛒 E-commerce Conversion Benchmarks", use_container_width=True):
			st.session_state.research_topic = cfg.research_examples.ecommerce_conversion
			st.rerun()

	with col2:
		if st.button("💰 SaaS Pricing & Conversion Trends", use_container_width=True):
			st.session_state.research_topic = cfg.research_examples.saas_pricing
			st.rerun()

		if st.button("📧 Email Marketing Benchmarks", use_container_width=True):
			st.session_state.research_topic = cfg.research_examples.email_marketing
			st.rerun()

	if st.button("🔍 Research Topic", type="primary"):
		if not research_topic:
			st.warning("Please enter a research topic.")
			return

		if not api_key:
			st.error("Please configure your Diffbot API token in the sidebar.")
			return

		research_query = cfg.prompts.market_research.format(
			research_topic=research_topic
		)

		with st.spinner("🔍 Researching topic..."):
			try:
				result = analyze_with_diffbot(
					research_query,
					api_key,
					model_choice,
					cfg.api.base_url,
					cfg.api.token_env_var
				)
				st.markdown("### 📊 Research Results")
				st.markdown(result)

			except Exception as e:
				st.error(f"Research failed: {str(e)}")


# Main Streamlit Application
def main() -> None:
	"""Main Streamlit application function."""
	load_dotenv()  # Load environment variables from .env file

	# Initialize Hydra configuration
	try:
		if GlobalHydra().is_initialized():
			GlobalHydra.instance().clear()
		initialize(config_path=".", version_base=None)
		cfg = compose(config_name="config")
	except Exception:
		# If initialization fails, try clearing and reinitializing
		GlobalHydra.instance().clear()
		initialize(config_path=".", version_base=None)
		cfg = compose(config_name="config")

	setup_page_config(cfg)

	st.title("🤖 Conversational Analytics Dashboard")
	st.markdown(
		"*Powered by Diffbot LLM - Get instant insights with transparent calculations*"
	)

	api_key, model_choice = render_sidebar(cfg)

	tab1, tab2 = st.tabs(
		[
			"📈 A/B Test Analyzer",
			"🔍 Market Research",
		]
	)

	with tab1:
		render_ab_test_tab(cfg, api_key, model_choice)

	with tab2:
		render_market_research_tab(cfg, api_key, model_choice)

	st.divider()
	st.markdown(
		f"""
        <div style='text-align: center; color: gray;'>
        Built with ❤️ using Streamlit and Diffbot LLM |
        <a href='{cfg.urls.github_repo}' target='_blank'>View Source</a> |
        <a href='{cfg.urls.diffbot_signup}' target='_blank'>Get Diffbot API Key</a>
        </div>
        """,
		unsafe_allow_html=True,
	)


if __name__ == "__main__":
	main()
