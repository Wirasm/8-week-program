import pandas as pd
from typing import Dict, Any


def analyze_sales(csv_path: str) -> Dict[str, Any]:
    """
    Analyze sales data from a CSV file.
    
    Args:
        csv_path: Path to the CSV file containing sales data
        
    Returns:
        Dictionary containing sales analysis results:
        - 'total_sales_by_region_product': Total sales grouped by region and product
        - 'product_performance_per_region': Product performance metrics for each region
    """
    # Load the CSV data
    try:
        df = pd.read_csv(csv_path)
        
        # Ensure required columns exist
        required_columns = ['date', 'region', 'product', 'sales']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculate total sales by region and product
        total_sales_by_region_product = df.groupby(['region', 'product'])['sales'].sum().reset_index()
        
        # Calculate product performance per region
        # For each region, find the best and worst performing products
        product_performance = {}
        for region in df['region'].unique():
            region_data = df[df['region'] == region]
            region_product_sales = region_data.groupby('product')['sales'].sum()
            
            product_performance[region] = {
                'top_product': region_product_sales.idxmax(),
                'top_product_sales': region_product_sales.max(),
                'worst_product': region_product_sales.idxmin(),
                'worst_product_sales': region_product_sales.min(),
                'average_sales': region_product_sales.mean(),
                'product_sales': region_product_sales.to_dict()
            }
        
        return {
            'total_sales_by_region_product': total_sales_by_region_product.to_dict('records'),
            'product_performance_per_region': product_performance
        }
        
    except Exception as e:
        print(f"Error analyzing sales data: {e}")
        return {
            'error': str(e)
        }


if __name__ == "__main__":
    # Example usage
    results = analyze_sales("../data/sales_data.csv")
    
    print("\n=== Total Sales by Region and Product ===")
    for entry in results['total_sales_by_region_product']:
        print(f"Region: {entry['region']}, Product: {entry['product']}, Sales: {entry['sales']}")
    
    print("\n=== Product Performance per Region ===")
    for region, performance in results['product_performance_per_region'].items():
        print(f"\nRegion: {region}")
        print(f"Top Product: {performance['top_product']} (Sales: {performance['top_product_sales']})")
        print(f"Worst Product: {performance['worst_product']} (Sales: {performance['worst_product_sales']})")
        print(f"Average Product Sales: {performance['average_sales']}") 