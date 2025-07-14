"""
Streamlit session state management utilities.

Handles initialization and management of session state variables
and analysis history storage.
"""

from datetime import datetime
from typing import Any

import streamlit as st


def initialize_session_state(key: str, default_value: Any) -> None:
    """Initialize session state variable if not exists."""
    if key not in st.session_state:
        st.session_state[key] = default_value


def store_analysis_result(analysis_type: str, query: str, result: str) -> None:
    """Store analysis result in session history."""
    initialize_session_state("analysis_history", [])

    st.session_state.analysis_history.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": analysis_type,
            "query": query,
            "result": result,
        }
    )