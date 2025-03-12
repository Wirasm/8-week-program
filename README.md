# 8-Week AI Concepts and Principles Series

This repository contains code examples and data for the "8-Week AI Concepts and Principles" series, focusing on effective AI prompt engineering and coding techniques.

## Overview

This repository demonstrates how to use information-dense keywords in prompts to get reliable, precise outputs from AI coding tools. The examples show how to structure prompts using the "What, Where, Detail" pattern to avoid hallucinations, bloat, and unintended code modifications.

## Repository Structure

- `week-1-idk/`: Contains example Python scripts demonstrating effective prompt results
  - `sales_analysis.py`: Analyzes sales data by region and product
  - `industry_analyzer.py`: Analyzes CRM data by industry and generates visualizations
- `data/`: Contains sample data files and data generation scripts
  - `sales_data.csv`: Sample sales data with date, region, product, and sales columns
  - `crm_data.csv`: Sample CRM data with company information
  - `gen_data.py`: Script to generate sample data
  - `icp_definition.md`: Ideal Customer Profile definition

## Key Concepts

This repository demonstrates the "What, Where, Detail" pattern for AI prompts:

1. **What**: Clearly specify what you want (e.g., sales analysis by region and product)
2. **Where**: Define exactly where you want it (e.g., a specific Python file and function)
3. **Detail**: Provide the necessary context for the AI to complete the task

## Running the Examples

This project uses [uv](https://github.com/astral-sh/uv) for Python package management. To run the examples:

1. Make sure you have Python 3.12+ and uv installed
2. Clone this repository
3. Navigate to the repository root directory
4. Run the following command
```bash
uv sync
```

### Running the Sales Analysis Example

```bash
uv run week-1-idk/sales_analysis.py
```

This will analyze the sales data and output:
- Total sales by region and product
- Product performance per region (top/worst products, average sales)

### Running the Industry Analyzer Example

```bash
uv run week-1-idk/industry_analyzer.py
```

This will:
- Analyze CRM data grouped by industry
- Generate a bar chart visualization saved as `week-1-idk/industry_analysis.png`
- Output industry statistics including total deal size, average deal size, and lead count

### Generating Sample Data

If you want to regenerate the sample data:

```bash
uv run data/gen_data.py
```

## Dependencies

- Python 3.12+
- pandas
- matplotlib

## Related Content

This repository is part of a series on AI concepts and principles:
- [LinkedIn Post](https://www.linkedin.com/posts/rasmuswiding_how-a-great-prompt-can-produce-the-desired-activity-7305529401071341568-FA85?utm_source=share&utm_medium=member_desktop&rcm=ACoAABRJiOkBdIgQir4T_C2OXsWokOancRby4I0)
- [Medium Article](https://medium.com/@rasmus.widing/how-a-great-prompt-can-produce-the-desired-output-reliably-from-ai-coding-tools-535cb20225a4)

## Next Steps

Future installments in this series will explore how to scale this approach for more complex multi-step tasks.
Meta prompting
Prototyping with AI
Agentic looping
and more

