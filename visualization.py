"""
Visualization and chart creation functions.

Handles creation of interactive charts and plots for data analysis results.
"""

import plotly.graph_objects as go

from data_utils import calculate_conversion_rate


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