"""
CSV Data Analyst - A CLI tool for analyzing CSV files using Polars and Claude 3.7
"""

from .agent import run_agent, TOOLS, AGENT_PROMPT
from .tools import list_columns, sample_csv, run_test_polars_code, run_final_polars_code
from .cli import main

__all__ = [
    'run_agent',
    'TOOLS',
    'AGENT_PROMPT',
    'list_columns',
    'sample_csv',
    'run_test_polars_code',
    'run_final_polars_code',
    'main'
]