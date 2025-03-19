import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

# Load environment variables from .env file
load_dotenv()

from agent import run_agent
from tools import list_columns, run_final_polars_code, run_test_polars_code, sample_csv

console = Console()


def setup_arg_parser() -> argparse.ArgumentParser:
    """Set up the argument parser for the CSV agent CLI."""
    parser = argparse.ArgumentParser(
        description="CSV data analyst powered by Claude 3.7 and Polars",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-i", "--input", required=True, help="Path to input CSV file")

    parser.add_argument(
        "-p", "--prompt", required=True, help="The user's request for data analysis"
    )

    parser.add_argument(
        "-c",
        "--compute",
        type=int,
        default=10,
        help="Maximum number of agent loops (default: 10)",
    )

    parser.add_argument(
        "-o", "--output", help="Optional path to save results (CSV or Parquet format)"
    )

    return parser


def validate_environment():
    """Validate that required environment variables are set."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print(
            "[bold red]Error:[/bold red] ANTHROPIC_API_KEY environment variable not set."
        )
        console.print("Please set your Anthropic API key:")
        console.print("  export ANTHROPIC_API_KEY=your-api-key-here")
        return False
    return True


def validate_file(file_path: str) -> bool:
    """Validate that the input file exists and is a CSV file."""
    path = Path(file_path)

    if not path.exists():
        console.print(f"[bold red]Error:[/bold red] File not found: {file_path}")
        return False

    if path.suffix.lower() != ".csv":
        console.print(f"[bold red]Error:[/bold red] File is not a CSV: {file_path}")
        return False

    return True


def main():
    """Main entry point for the CSV data analyst CLI."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Validate input file
    if not validate_file(args.input):
        sys.exit(1)

    # Map tools to their handlers
    tool_handlers = {
        "list_columns": list_columns,
        "sample_csv": sample_csv,
        "run_test_polars_code": run_test_polars_code,
        "run_final_polars_code": run_final_polars_code,
    }

    try:
        # Run the agent
        run_agent(
            csv_path=args.input,
            user_prompt=args.prompt,
            max_compute=args.compute,
            tool_handlers=tool_handlers,
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
