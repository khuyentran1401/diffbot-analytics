"""
Data processing and utility functions.

Handles data calculations, sample data generation, and export functionality.
"""

import base64
from typing import Any, Dict, List

import pandas as pd


def calculate_conversion_rate(conversions: int, users: int) -> float:
    """Calculate conversion rate as percentage."""
    return (conversions / users) * 100 if users > 0 else 0.0


def create_sample_data(data_type: str) -> pd.DataFrame:
    """Create sample data for testing."""
    if data_type == "ab_test":
        return pd.DataFrame(
            {
                "user_id": range(1, 2001),
                "group": ["control" if i < 1000 else "treatment" for i in range(2000)],
                "converted": [
                    1
                    if (i < 1000 and i % 20 == 0) or (i >= 1000 and i % 15 == 0)
                    else 0
                    for i in range(2000)
                ],
            }
        )
    elif data_type == "sales":
        dates = pd.date_range("2023-01-01", "2023-12-31", freq="D")
        return pd.DataFrame(
            {
                "date": dates,
                "sales": [100 + (i % 30) * 10 + (i % 7) * 5 for i in range(len(dates))],
                "visitors": [1000 + (i % 50) * 20 for i in range(len(dates))],
            }
        )
    return pd.DataFrame()


def create_export_data(data_type: str, **kwargs) -> List[Dict[str, Any]]:
    """Create standardized export data structure."""
    base_data = {"Type": data_type}
    base_data.update(kwargs)
    return [base_data]


def export_results_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """Export analysis results to CSV format."""
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">📄 Download CSV Report</a>'