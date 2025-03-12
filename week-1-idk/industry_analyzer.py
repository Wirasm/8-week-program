import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Dict, Any


def analyze_by_industry(crm_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Analyze CRM data grouped by industry.
    
    Args:
        crm_path: Path to the CRM data CSV file
        
    Returns:
        Dictionary with industry statistics including:
        - total_deal_size: Sum of all deal sizes for the industry
        - avg_deal_size: Average deal size for the industry
        - lead_count: Number of leads in the industry
    """
    # Check if file exists
    if not os.path.exists(crm_path):
        raise FileNotFoundError(f"CRM data file not found at {crm_path}")
    
    # Load CSV data
    crm_data = pd.read_csv(crm_path)
    
    # Ensure required columns exist
    required_columns = ['company_name', 'industry', 'pipeline_stage', 'deal_size']
    missing_columns = [col for col in required_columns if col not in crm_data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Group leads by industry
    industry_groups = crm_data.groupby('industry')
    
    # Calculate statistics per industry
    industry_stats = {}
    for industry, group in industry_groups:
        industry_stats[industry] = {
            'total_deal_size': group['deal_size'].sum(),
            'avg_deal_size': group['deal_size'].mean(),
            'lead_count': len(group)
        }
    
    # Sort results by total potential revenue (total deal size)
    sorted_stats = {k: v for k, v in sorted(
        industry_stats.items(), 
        key=lambda item: item[1]['total_deal_size'], 
        reverse=True
    )}
    
    # Generate bar chart comparing industries
    generate_industry_chart(sorted_stats)
    
    return sorted_stats


def generate_industry_chart(industry_stats: Dict[str, Dict[str, Any]]) -> None:
    """
    Generate a bar chart comparing industries by total deal size.
    
    Args:
        industry_stats: Dictionary with industry statistics
    """
    industries = list(industry_stats.keys())
    total_deal_sizes = [stats['total_deal_size'] for stats in industry_stats.values()]
    
    plt.figure(figsize=(12, 6))
    plt.bar(industries, total_deal_sizes)
    plt.title('Total Potential Revenue by Industry')
    plt.xlabel('Industry')
    plt.ylabel('Total Deal Size ($)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the chart
    output_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(output_dir, 'industry_analysis.png'))
    plt.close()


if __name__ == "__main__":
    # Example usage
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    crm_data_path = os.path.join(project_root, 'data', 'crm_data.csv')
    
    try:
        results = analyze_by_industry(crm_data_path)
        print("Industry Analysis Results:")
        for industry, stats in results.items():
            print(f"\n{industry}:")
            print(f"  Total Deal Size: ${stats['total_deal_size']:,.2f}")
            print(f"  Average Deal Size: ${stats['avg_deal_size']:,.2f}")
            print(f"  Lead Count: {stats['lead_count']}")
        
        print(f"\nChart saved to: {os.path.join(script_dir, 'industry_analysis.png')}")
    except Exception as e:
        print(f"Error: {e}") 