import os
import json
import anthropic
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

console = Console()

# Define tool schemas for the Anthropic API
TOOLS = [
    {
        "name": "list_columns",
        "description": "Returns a list of all column names in the CSV file. Use this tool first to understand what data is available in the dataset before performing any analysis. This is an essential first step to understand the structure of the data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Explanation of why you're running this tool"
                },
                "csv_path": {
                    "type": "string",
                    "description": "The path to the CSV file to analyze"
                }
            },
            "required": ["reasoning", "csv_path"]
        }
    },
    {
        "name": "sample_csv",
        "description": "Returns a sample of rows from the CSV file to help understand the data types and formats. Use this after listing columns to get a better understanding of the actual data values. The sample will show actual data values which is useful for understanding data patterns, formats, and potential issues.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Explanation of why you're running this tool"
                },
                "csv_path": {
                    "type": "string",
                    "description": "The path to the CSV file to analyze"
                },
                "row_count": {
                    "type": "integer",
                    "description": "Number of rows to sample (3-5 recommended, max 10)"
                }
            },
            "required": ["reasoning", "csv_path", "row_count"]
        }
    },
    {
        "name": "run_test_polars_code",
        "description": "Executes test Polars Python code and returns results. Use this to validate and test your code before finalizing it. The results are only shown to you, not the user. This is for iterative development of your solution. You can run this multiple times to refine your code until it works correctly.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Explanation of why you're running this code"
                },
                "polars_python_code": {
                    "type": "string",
                    "description": "The Polars Python code to execute. This should be valid Python code that uses the polars library (imported as pl). The code should read from the csv_path variable."
                },
                "csv_path": {
                    "type": "string",
                    "description": "The path to the CSV file to analyze"
                }
            },
            "required": ["reasoning", "polars_python_code", "csv_path"]
        }
    },
    {
        "name": "run_final_polars_code",
        "description": "Executes the final Polars code and returns results to the user. Only call this when you're confident the code is perfect and thoroughly tested. This will show the final output to the user, so make sure it's accurate, well-formatted, and answers their question completely.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Explanation of why this is the final solution"
                },
                "polars_python_code": {
                    "type": "string",
                    "description": "The final Polars Python code to execute"
                },
                "csv_path": {
                    "type": "string",
                    "description": "The path to the CSV file to analyze"
                },
                "output_file": {
                    "type": "string",
                    "description": "Optional path to save output (CSV or Parquet format)"
                }
            },
            "required": ["reasoning", "polars_python_code", "csv_path"]
        }
    }
]

# Agent prompt with detailed instructions
AGENT_PROMPT = """
You are a world-class expert at crafting precise Polars data transformations in Python.
Your goal is to generate accurate code that exactly matches the user's data analysis needs.

## Analysis Strategy
1. First, understand the CSV data structure by using the available tools:
   - Start by listing columns to understand available fields
   - Sample rows to examine data patterns and formats
   - Pay close attention to data types, missing values, and potential issues

2. Once you understand the data, plan your approach:
   - Break down the analysis into clear steps
   - Consider the most efficient Polars operations for each step
   - Prefer lazy evaluation when working with large datasets
   - Think about how to handle missing data, outliers, or inconsistencies

3. Implement your solution iteratively:
   - Start with simpler versions and refine
   - Test each component with run_test_polars_code before proceeding
   - Make your code efficient and readable
   - Add inline comments to explain complex transformations

4. Present the final solution:
   - Only call run_final_polars_code when you're confident your code works perfectly
   - Ensure your code is clean, efficient, and follows best practices
   - Make sure your final output addresses the user's original question completely

## Code Quality Standards
- Use Polars' lazy evaluation when appropriate for performance
- Write clearly formatted, readable code
- Use descriptive variable names
- Include comments for complex operations
- Follow functional programming patterns when possible

## Polars Best Practices
- Use pl.scan_csv() for lazy loading of large files
- When possible, complete all operations before calling .collect()
- Use method chaining for clarity
- Leverage Polars' vectorized operations for performance
- Use appropriate types for each column
- Consider memory usage for large datasets

## Tool Usage
1. Begin with list_columns to understand the dataset structure
2. Follow with sample_csv to see actual data values
3. Test your code with run_test_polars_code - use this repeatedly to refine your solution
4. Only when you're confident, use run_final_polars_code

Remember: You are helping users who may have limited data analysis skills. Your goal is to provide accurate, efficient code that solves their specific data analysis needs.
"""

def get_api_key() -> str:
    """Get the Anthropic API key from environment variable."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set. Please set it before running the agent.")
    return api_key

def get_model() -> str:
    """Get the model name from environment or use default."""
    return os.environ.get("MODEL", "claude-3-7-sonnet-20250219")

def extract_thinking(text: str) -> str:
    """Extract thinking from text using regex."""
    thinking_pattern = r'<thinking>(.*?)</thinking>'
    match = re.search(thinking_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def create_client() -> anthropic.Anthropic:
    """Create and return an Anthropic client."""
    return anthropic.Anthropic(api_key=get_api_key())

def run_agent(csv_path: str, user_prompt: str, max_compute: int = 10, 
             tool_handlers: Dict = None) -> None:
    """Run the agent to analyze CSV data based on user prompt."""
    
    if not os.path.exists(csv_path):
        console.print(f"[bold red]Error:[/bold red] CSV file not found: {csv_path}")
        return
    
    if not tool_handlers:
        console.print("[bold red]Error:[/bold red] No tool handlers provided.")
        return
    
    try:
        client = create_client()
        model = get_model()
        
        console.print(Panel.fit(
            Markdown(f"# CSV Data Analysis\n\n**File:** {csv_path}\n\n**Request:** {user_prompt}"),
            title="Starting Analysis",
            border_style="blue"
        ))
        
        # Initialize conversation with system and user messages
        messages = [
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text", 
                        "text": f"I need to analyze data in this CSV file: {csv_path}\n\nHere's what I want to do: {user_prompt}\n\nPlease help me create Polars code to solve this task."
                    }
                ]
            }
        ]
        
        # Agent loop for iterative analysis
        compute_iterations = 0
        while compute_iterations < max_compute:
            compute_iterations += 1
            
            console.print(f"[dim]Compute iteration {compute_iterations}/{max_compute}...[/dim]")
            
            # Get response from Claude
            response = client.messages.create(
                model=model,
                system=AGENT_PROMPT,
                tools=TOOLS,
                messages=messages,
                max_tokens=4096,
                stop_sequences=[],
                temperature=0
            )
            
            # Process assistant's response
            assistant_message = {"role": "assistant", "content": response.content}
            messages.append(assistant_message)
            
            # Display thinking if present in the response
            for content_block in response.content:
                if content_block.type == "text":
                    thinking = extract_thinking(content_block.text)
                    if thinking:
                        console.print(Panel(
                            Markdown(thinking),
                            title="Agent Thinking",
                            border_style="yellow"
                        ))
                    
                    # Display non-thinking text
                    filtered_text = re.sub(r'<thinking>.*?</thinking>', '', content_block.text, flags=re.DOTALL).strip()
                    if filtered_text:
                        console.print(Panel(
                            Markdown(filtered_text),
                            title="Agent Response",
                            border_style="green"
                        ))
                
                # Handle tool calls
                elif content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_input = content_block.input
                    tool_id = content_block.id
                    
                    if tool_name in tool_handlers:
                        # Extract required parameters
                        handler_fn = tool_handlers[tool_name]
                        
                        try:
                            console.print(f"[dim]Running tool: {tool_name}[/dim]")
                            
                            # Execute the tool with its input
                            result = handler_fn(**tool_input)
                            
                            # Create tool result message
                            tool_result_message = {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_id,
                                        "content": str(result)
                                    }
                                ]
                            }
                            
                            messages.append(tool_result_message)
                            
                        except Exception as e:
                            # Report errors back to the model
                            console.print(f"[bold red]Tool execution error:[/bold red] {str(e)}")
                            tool_result_message = {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_id,
                                        "content": f"Error executing tool: {str(e)}",
                                        "is_error": True
                                    }
                                ]
                            }
                            messages.append(tool_result_message)
                    else:
                        console.print(f"[bold red]Unknown tool:[/bold red] {tool_name}")
                        # Report the unknown tool back to the model
                        tool_result_message = {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_id,
                                    "content": f"Unknown tool: {tool_name}",
                                    "is_error": True
                                }
                            ]
                        }
                        messages.append(tool_result_message)
            
            # Check for completion
            if any(content_block.type == "tool_use" and content_block.name == "run_final_polars_code" 
                  for content_block in response.content):
                console.print("[bold green]Analysis completed with final code execution[/bold green]")
                break
                
        if compute_iterations >= max_compute:
            console.print(f"[bold yellow]Reached maximum compute iterations ({max_compute})[/bold yellow]")
            
    except Exception as e:
        console.print(f"[bold red]Error during agent execution:[/bold red] {str(e)}")