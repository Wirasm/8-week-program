# CSV Data Analyst

A powerful CLI tool for analyzing CSV data powered by Claude 3.7 Sonnet and Polars.

## Overview

This tool allows users with limited data analysis skills to quickly analyze CSV files using natural language prompts. The tool leverages:

- **Anthropic's Claude 3.7 Sonnet** for natural language understanding and code generation
- **Polars** for fast and efficient data analysis
- **Rich** for beautiful command-line interfaces

## Requirements

- Python 3.12+
- Anthropic API key

## Installation

1. Ensure your Python environment is set up
2. Create a `.env` file in the project root with your API key:

```
ANTHROPIC_API_KEY=your-api-key-here
MODEL=claude-3-7-sonnet-20250219
```

The MODEL variable is optional and defaults to Claude 3.7 Sonnet.

## Usage

Run the CLI tool with the following command:

```bash
# From the project root directory
cd week-2-planning
python agent_cli.py -i <csv_file> -p "<your analysis request>"
```

### Arguments

- `-i, --input`: Path to input CSV file (required)
- `-p, --prompt`: Your data analysis request in natural language (required)
- `-c, --compute`: Maximum number of agent loops (default: 10)
- `-o, --output`: Optional path to save results (CSV or Parquet format)

### Example Commands

```bash
# Basic analysis
python agent_cli.py -i ../data/sales_data.csv -p "Show me the top 5 products by revenue"

# More complex analysis
python agent_cli.py -i ../data/crm_data.csv -p "Analyze customer churn by segment and provide insights on retention factors"

# Save results to a file
python agent_cli.py -i ../data/sales_data.csv -p "Calculate monthly sales trends" -o results.csv

# Increase compute iterations for complex analyses
python agent_cli.py -i ../data/crm_data.csv -p "Build a customer segmentation model" -c 15
```

## How It Works

1. The tool parses your CSV file using Polars
2. It presents the CSV structure to Claude
3. Claude analyzes your request and generates optimal Polars code
4. The code is executed and results are displayed in a formatted way
5. The agent continues to refine its approach until it produces a satisfactory result

## Features

- **Fast Data Analysis**: Leverages Polars for performant data operations
- **Natural Language Interface**: Describe your analysis needs in plain English
- **Beautiful CLI Output**: Rich-formatted output with color-coding and formatting
- **Error Handling**: Robust error messages to help identify issues
- **CSV Export**: Save analysis results to CSV or Parquet files

## Developer Notes

The implementation follows a modular approach:

- `tools.py`: Core tool functions for CSV data exploration
- `agent.py`: Claude agent configuration and prompt construction
- `cli.py`: Command-line interface and argument parsing
- `agent_cli.py`: Main execution script
- `__init__.py`: Package initialization and exports