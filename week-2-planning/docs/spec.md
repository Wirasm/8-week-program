# CSV data analysis CLI

> Ingest and understand the information from this file, implement the Tasks one by one, and generate the code that will satisfy the Desired Outcome and Implementation Plan.

## The problem to solve
- Sales people has limited data analys skills and they need to be able to quickly analyse data in csv files 


## Desired Outcome
- A CSV data analyst LLM agent that can be used to analyse data in csv files through the CLI using anthropics 3.7 sonnet model, using Polars for data analysis



## Implementation Plan
Setup a modular CLI interface with argparse

Define required arguments for CSV file path, user prompt, and optional compute limit
Handle missing API key with informative error messages and instructions
Create clean error handling and user feedback throughout the process


Implement tool functions for CSV data exploration

Create functions that interact with CSV files using Polars
Add detailed logging with Rich to provide visibility into tool execution
Include robust error handling for each tool function


Define comprehensive tool schemas for Anthropic API

Build detailed JSON schemas for each tool with proper typing
Include clear descriptions of each parameter and its purpose
Structure tools as a pipeline from data exploration to final execution


Create an agent loop with thinking capability

Initialize Claude 3.7 client with thinking mode enabled
Process responses including thinking blocks, tool use, and text content
Track compute iterations with a configurable limit
Implement clean exit conditions when final code is executed or limit reached


Build a polished CLI experience with Rich

Use color-coded output and panels to distinguish different types of information
Create visual separators between agent loops
Format code and data samples for better readability
Provide clear error messages and suggestions when issues occur



## Details
- Add reasoning as an arg to each tool
Args:
    reasoning: Explanation of why we're running this tool


- List of agent tools
 - def list_columns(reasoning: str, csv_path: str) -> List[str]:
     """Returns a list of columns in the CSV file."""

 - def sample_csv(reasoning: str, csv_path: str, row_count: int) -> str:
    """Returns a sample of rows from the CSV file.
    Args:
        row_count: Number of rows to sample (3-5)
    """

 def run_test_polars_code(reasoning: str, polars_python_code: str, csv_path: str) -> str:
    """Executes test Polars Python code and returns results.

    The agent uses this to validate code before finalizing it.
    Results are only shown to the agent, not the user.
    """

    def run_final_polars_code(
    reasoning: str,
    polars_python_code: str,
    csv_path: str,
    output_file: Optional[str] = None,
) -> str:
    """Executes the final Polars code and returns results to user.

 - Define tool schemas for the Anthropic API

 - Define a detailed XML AGENT_PROMPT Here is a starting point = """
You are a world-class expert at crafting precise Polars data transformations in Python.
Your goal is to generate accurate code that exactly matches the user's data analysis needs.

Use the provided tools to explore the CSV data and construct the perfect Polars transformation:
1. Start by listing columns to understand what's available in the CSV.
2. Sample the CSV to see actual data patterns.
3. Test Polars code with run_test_polars_code before finalizing it. Run the run_test_polars_code tool as many times as needed to get the code working.
4. Only call run_final_polars_code when you're confident the code is perfect.
"""

- Main function with argparse
 - "-i", "--input", required=True, help="Path to input CSV file"
 - "-p", "--prompt", required=True, help="The user's request"
 - "-c", "--compute", type=int, default=10, help="Maximum number of agent loops (default: 10)"

## Needed Context
- [Tool use with Claude](claude_tool_use.md)

### Starting Point
- pyproject.toml
- .env (ANTHROPIC_API_KEY, MODEL)
- data/crm_data.csv (do not attempt to read this file)
- week-2-planning/docs/spec.md

### End State
- starting point + 
- week-2-planning/
  - agent.py
  - tools.py
  - cli.py
  - __init__.py
  - README.md

### Tasks

1. Create the tools.py file with CSV analysis functions

Where: week-2-planning/tools.py
What: Create all tool functions for CSV analysis
Details: Implement list_columns, sample_csv, run_test_polars_code, and run_final_polars_code functions with Rich console logging

2. Define the tool schemas and agent prompt

Where: week-2-planning/agent.py
What: Create TOOLS list and AGENT_PROMPT string
Details: Define JSON schemas for each tool and create detailed agent prompt with instructions for CSV exploration

3. Create the CLI interface and argument parsing

Where: week-2-planning/cli.py
What: Implement argparse setup and CLI entry point
Details: Define arguments for input CSV file, user prompt, and compute limit

4. Implement the agent loop with Claude

Where: week-2-planning/agent.py
What: Create main agent function
Details: Initialize Anthropic client, process messages, handle tool calls, manage conversation history

5. Create package initialization

Where: week-2-planning/init.py
What: Create package initialization file
Details: Import necessary components to make the package usable

6. Create documentation

Where: week-2-planning/README.md
What: Create usage documentation
Details: Explain how to use the CLI tool with examples, required environment variables, and arguments

7. Create the main execution script

Where: week-2-planning/agent_cli.py
What: Create the main CLI entry point
Details: Import components, set up main function, and implement error handling