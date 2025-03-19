#!/usr/bin/env python3
"""
CSV Data Analyst CLI

A command-line tool for analyzing CSV files using Polars and Claude 3.7 Sonnet.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path to allow imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import main function from local module
from cli import main

if __name__ == "__main__":
    main()