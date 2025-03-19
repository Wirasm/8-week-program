import polars as pl
from typing import List, Optional
from rich.console import Console
from pathlib import Path
import traceback

console = Console()

def list_columns(reasoning: str, csv_path: str) -> List[str]:
    """Returns a list of columns in the CSV file."""
    console.print(f"[bold blue]LIST COLUMNS[/bold blue]: {reasoning}")
    try:
        df = pl.scan_csv(csv_path)
        columns = df.collect().columns
        console.print(f"[dim]Found {len(columns)} columns[/dim]")
        return columns
    except Exception as e:
        error = f"Error listing columns: {str(e)}"
        console.print(f"[bold red]ERROR[/bold red]: {error}")
        return [f"Error: {error}"]

def sample_csv(reasoning: str, csv_path: str, row_count: int) -> str:
    """Returns a sample of rows from the CSV file.
    Args:
        row_count: Number of rows to sample (3-5)
    """
    console.print(f"[bold blue]SAMPLE CSV[/bold blue]: {reasoning}")
    try:
        if row_count < 1 or row_count > 10:
            row_count = min(max(row_count, 1), 10)
            console.print(f"[yellow]Adjusting row_count to {row_count} (must be between 1-10)[/yellow]")
        
        df = pl.scan_csv(csv_path).fetch(row_count)
        result = df.to_pandas().to_string()
        console.print(f"[dim]Sampled {len(df)} rows[/dim]")
        return result
    except Exception as e:
        error = f"Error sampling CSV: {str(e)}"
        console.print(f"[bold red]ERROR[/bold red]: {error}")
        return f"Error: {error}"

def run_test_polars_code(reasoning: str, polars_python_code: str, csv_path: str) -> str:
    """Executes test Polars Python code and returns results.

    The agent uses this to validate code before finalizing it.
    Results are only shown to the agent, not the user.
    """
    console.print(f"[bold yellow]TEST POLARS CODE[/bold yellow]: {reasoning}")
    try:
        # Create a safe local environment with polars and Path
        local_vars = {
            "pl": pl,
            "Path": Path,
            "csv_path": csv_path
        }
        
        # Make sure code reads from the provided csv_path
        if "csv_path" not in polars_python_code:
            console.print("[yellow]Warning: Code doesn't reference csv_path variable[/yellow]")
        
        # Execute the code
        exec_result = {}
        exec(polars_python_code, {"__builtins__": __builtins__}, local_vars)
        
        # Find the result variable - the last assigned variable that's not a DataFrame
        result_var = None
        result = None
        
        for var_name, var_value in local_vars.items():
            if var_name not in ["pl", "Path", "csv_path"] and var_name != "__builtins__":
                result_var = var_name
                result = var_value
        
        if result is None:
            return "No result found. Make sure your code assigns the final result to a variable."
        
        # Convert result to string representation
        if isinstance(result, (pl.DataFrame, pl.LazyFrame)):
            # For DataFrames, convert to pandas for better string representation
            # Limit to first 10 rows for large DataFrames
            if hasattr(result, "collect"):
                result = result.collect()
            
            if len(result) > 10:
                output = result.head(10).to_pandas().to_string()
                output += f"\n\n[Showing 10/{len(result)} rows]"
            else:
                output = result.to_pandas().to_string()
        else:
            output = str(result)
            
        console.print(f"[dim]Code executed successfully[/dim]")
        return output
        
    except Exception as e:
        error_details = traceback.format_exc()
        error = f"Error executing code: {str(e)}\n\n{error_details}"
        console.print(f"[bold red]ERROR[/bold red]: {error}")
        return f"Error: {error}"

def run_final_polars_code(
    reasoning: str,
    polars_python_code: str,
    csv_path: str,
    output_file: Optional[str] = None,
) -> str:
    """Executes the final Polars code and returns results to user."""
    console.print(f"[bold green]FINAL POLARS CODE[/bold green]: {reasoning}")
    console.print(f"[dim]Processing CSV: {csv_path}[/dim]")
    
    try:
        # Create a safe local environment with polars and Path
        local_vars = {
            "pl": pl,
            "Path": Path,
            "csv_path": csv_path
        }
        
        # Execute the code
        exec(polars_python_code, {"__builtins__": __builtins__}, local_vars)
        
        # Find the result variable - typically the last variable assigned
        result_var = None
        result = None
        
        for var_name, var_value in local_vars.items():
            if var_name not in ["pl", "Path", "csv_path"] and var_name != "__builtins__":
                result_var = var_name
                result = var_value
        
        if result is None:
            return "No result found. Make sure your code assigns the final result to a variable."
        
        # Save to output file if specified
        if output_file and isinstance(result, pl.DataFrame):
            output_path = Path(output_file)
            
            if output_path.suffix.lower() == '.csv':
                result.write_csv(output_file)
                console.print(f"[green]Results saved to CSV: {output_file}[/green]")
            elif output_path.suffix.lower() == '.parquet':
                result.write_parquet(output_file)
                console.print(f"[green]Results saved to Parquet: {output_file}[/green]")
            else:
                console.print(f"[yellow]Unsupported output format: {output_path.suffix}[/yellow]")
        
        # Convert result to string representation
        if isinstance(result, (pl.DataFrame, pl.LazyFrame)):
            # For DataFrames, convert to pandas for better string representation
            if hasattr(result, "collect"):
                result = result.collect()
                
            if len(result) > 20:
                output = result.head(20).to_pandas().to_string()
                output += f"\n\n[Showing 20/{len(result)} rows]"
            else:
                output = result.to_pandas().to_string()
        else:
            output = str(result)
            
        console.print(f"[green]Code executed successfully[/green]")
        return output
        
    except Exception as e:
        error_details = traceback.format_exc()
        error = f"Error executing code: {str(e)}\n\n{error_details}"
        console.print(f"[bold red]ERROR[/bold red]: {error}")
        return f"Error: {error}"