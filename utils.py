"""
Data processing, calculations, and visualization utilities.

Handles data calculations, export functionality, and chart creation 
for the Diffbot Analytics Dashboard.
"""

import base64
from typing import Any, Dict, List

import pandas as pd
import plotly.graph_objects as go


def calculate_conversion_rate(conversions: int, users: int) -> float:
    """Calculate conversion rate as percentage."""
    return (conversions / users) * 100 if users > 0 else 0.0


def export_results_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """Export analysis results to CSV format."""
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">📄 Download CSV Report</a>'


def create_ab_test_visualization(
    control_users: int,
    control_conversions: int,
    treatment_users: int,
    treatment_conversions: int,
) -> go.Figure:
    """Create bar chart visualization for A/B test results."""
    control_rate = calculate_conversion_rate(control_conversions, control_users)
    treatment_rate = calculate_conversion_rate(treatment_conversions, treatment_users)

    fig = go.Figure(
        data=[
            go.Bar(
                name="Control",
                x=["Conversion Rate (%)"],
                y=[control_rate],
                marker_color="lightblue",
            ),
            go.Bar(
                name="Treatment",
                x=["Conversion Rate (%)"],
                y=[treatment_rate],
                marker_color="lightcoral",
            ),
        ]
    )

    fig.update_layout(
        title="A/B Test Conversion Rates Comparison",
        yaxis_title="Conversion Rate (%)",
        barmode="group",
        showlegend=True,
    )

    return fig