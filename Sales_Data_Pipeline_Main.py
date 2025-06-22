#!/usr/bin/env python3
"""
Custom Multi-Source Sales Data Pipeline & Business Insights Dashboard
Modified to work with your existing data files

This project demonstrates:
1. Multi-format data ingestion (CSV, JSON, Excel) - YOUR FILES
2. Data cleaning and transformation
3. Data merging and integration
4. Business insights generation
5. Visualization and reporting

Required Libraries: pandas, numpy, matplotlib, seaborn, tabulate, openpyxl, json
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from datetime import datetime, timedelta
import warnings
import os
from pathlib import Path

# Configure display settings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class CustomSalesDataPipeline:
    """
    A comprehensive sales data pipeline that handles YOUR data files,
    performs data cleaning, transformation, and generates business insights.
    """
    
    def __init__(self, csv_file=None, json_file=None, excel_file=None):
        self.csv_file = csv_file
        self.json_file = json_file
        self.excel_file = excel_file
        self.sales_data = None
        self.metadata = None
        self.region_data = None
        self.merged_data = None
        self.insights = {}
        
    def inspect_data_files(self):
        """Inspect your data files to understand their structure"""
        print("🔍 INSPECTING YOUR DATA FILES")
        print("=" * 50)
        
        # Inspect CSV file
        if self.csv_file and os.path.exists(self.csv_file):
            print(f"\n📊 CSV File: {self.csv_file}")
            print("-" * 30)
            try:
                df_sample = pd.read_csv(self.csv_file, nrows=5)
                print("Columns:", list(df_sample.columns))
                print("Shape:", df_sample.shape)
                print("Sample data:")
                print(df_sample.head())
                print("\nData types:")
                print(df_sample.dtypes)
            except Exception as e:
                print(f"Error reading CSV: {e}")
        
        # Inspect JSON file
        if self.json_file and os.path.exists(self.json_file):
            print(f"\n📋 JSON File: {self.json_file}")
            print("-" * 30)
            try:
                with open(self.json_file, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, list) and len(data) > 0:
                    print("Type: List of objects")
                    print("Number of records:", len(data))
                    print("Sample record keys:", list(data[0].keys()) if data else "Empty")
                    print("Sample record:")
                    print(json.dumps(data[0] if data else {}, indent=2))
                elif isinstance(data, dict):
                    print("Type: Dictionary")
                    print("Keys:", list(data.keys()))
                    print("Sample structure:")
                    print(json.dumps(data, indent=2)[:500] + "..." if len(str(data)) > 500 else json.dumps(data, indent=2))
            except Exception as e:
                print(f"Error reading JSON: {e}")
        
        # Inspect Excel file
        if self.excel_file and os.path.exists(self.excel_file):
            print(f"\n📈 Excel File: {self.excel_file}")
            print("-" * 30)
            try:
                # Check available sheets
                excel_file = pd.ExcelFile(self.excel_file)
                print("Available sheets:", excel_file.sheet_names)
                
                # Read first sheet sample
                df_sample = pd.read_excel(self.excel_file, nrows=5)
                print("Columns:", list(df_sample.columns))
                print("Shape:", df_sample.shape)
                print("Sample data:")
                print(df_sample.head())
                print("\nData types:")
                print(df_sample.dtypes)
            except Exception as e:
                print(f"Error reading Excel: {e}")
    
    def load_csv_data(self, date_columns=None, numeric_columns=None):
        """Load and validate CSV data with flexible column detection"""
        if not self.csv_file or not os.path.exists(self.csv_file):
            print(f"CSV file not found: {self.csv_file}")
            return None
            
        try:
            print(f"Loading CSV data from {self.csv_file}...")
            data = pd.read_csv(self.csv_file)
            print(f"Loaded {len(data)} records with {len(data.columns)} columns")
            
            # Auto-detect date columns if not specified
            if date_columns is None:
                date_columns = []
                for col in data.columns:
                    if any(keyword in col.lower() for keyword in ['date', 'time', 'created', 'updated']):
                        date_columns.append(col)
            
            # Convert date columns
            for col in date_columns:
                if col in data.columns:
                    try:
                        data[col] = pd.to_datetime(data[col])
                        print(f"✓ Converted {col} to datetime")
                    except:
                        print(f"⚠ Could not convert {col} to datetime")
            
            # Auto-detect numeric columns if not specified
            if numeric_columns is None:
                numeric_columns = []
                for col in data.columns:
                    if any(keyword in col.lower() for keyword in ['price', 'cost', 'revenue', 'amount', 'quantity', 'units', 'sales']):
                        numeric_columns.append(col)
            
            # Convert numeric columns
            for col in numeric_columns:
                if col in data.columns:
                    try:
                        data[col] = pd.to_numeric(data[col], errors='coerce')
                        print(f"✓ Converted {col} to numeric")
                    except:
                        print(f"⚠ Could not convert {col} to numeric")
            
            # Remove rows with all NaN values
            data = data.dropna(how='all')
            
            print(f"✓ Cleaned data: {len(data)} records")
            return data
            
        except Exception as e:
            print(f"✗ Error loading CSV: {str(e)}")
            return None
    
    def load_json_data(self):
        """Load and validate JSON metadata with flexible structure"""
        if not self.json_file or not os.path.exists(self.json_file):
            print(f"JSON file not found: {self.json_file}")
            return None
            
        try:
            print(f"Loading JSON data from {self.json_file}...")
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to find the main data array
                if 'data' in data:
                    df = pd.DataFrame(data['data'])
                elif 'products' in data:
                    df = pd.DataFrame(data['products'])
                elif 'items' in data:
                    df = pd.DataFrame(data['items'])
                else:
                    # Convert dict to single-row DataFrame
                    df = pd.DataFrame([data])
            else:
                print("Unsupported JSON structure")
                return None
            
            print(f"✓ Loaded {len(df)} records from JSON")
            return df
            
        except Exception as e:
            print(f"✗ Error loading JSON: {str(e)}")
            return None
    
    def load_excel_data(self, sheet_name=0):
        """Load and validate Excel data with flexible sheet selection"""
        if not self.excel_file or not os.path.exists(self.excel_file):
            print(f"Excel file not found: {self.excel_file}")
            return None
            
        try:
            print(f"Loading Excel data from {self.excel_file}...")
            
            # Read the specified sheet
            data = pd.read_excel(self.excel_file, sheet_name=sheet_name)
            
            # Clean column names (remove spaces, special characters)
            data.columns = data.columns.str.strip()
            
            print(f"✓ Loaded {len(data)} records from Excel")
            return data
            
        except Exception as e:
            print(f"✗ Error loading Excel: {str(e)}")
            return None
    
    def smart_merge_data(self, merge_keys=None):
        """Intelligently merge data sources based on common columns"""
        print("\n" + "="*50)
        print("SMART DATA MERGING")
        print("="*50)
        
        if self.sales_data is None:
            print("✗ No primary data available for merging")
            return None
        
        merged = self.sales_data.copy()
        print(f"Starting with primary data: {len(merged)} records")
        
        # Smart merge with metadata
        if self.metadata is not None:
            print("\nMerging with metadata...")
            
            # Find common columns for merging
            if merge_keys is None:
                common_cols = list(set(merged.columns) & set(self.metadata.columns))
                if common_cols:
                    merge_key = common_cols[0]
                    print(f"Auto-detected merge key: {merge_key}")
                else:
                    print("No common columns found for merging metadata")
                    merge_key = None
            else:
                merge_key = merge_keys.get('metadata')
            
            if merge_key and merge_key in merged.columns and merge_key in self.metadata.columns:
                merged = pd.merge(merged, self.metadata, on=merge_key, how='left', suffixes=('', '_meta'))
                print(f"✓ Merged with metadata: {len(merged)} records")
            else:
                print("⚠ Skipping metadata merge - no suitable key found")
        
        # Smart merge with region/additional data
        if self.region_data is not None:
            print("\nMerging with additional data...")
            
            if merge_keys is None:
                common_cols = list(set(merged.columns) & set(self.region_data.columns))
                if common_cols:
                    merge_key = common_cols[0]
                    print(f"Auto-detected merge key: {merge_key}")
                else:
                    print("No common columns found for merging additional data")
                    merge_key = None
            else:
                merge_key = merge_keys.get('region')
            
            if merge_key and merge_key in merged.columns and merge_key in self.region_data.columns:
                merged = pd.merge(merged, self.region_data, on=merge_key, how='left', suffixes=('', '_region'))
                print(f"✓ Merged with additional data: {len(merged)} records")
            else:
                print("⚠ Skipping additional data merge - no suitable key found")
        
        self.merged_data = merged
        print(f"\n✓ Final merged dataset: {len(merged)} records with {len(merged.columns)} columns")
        
        # Display merged data sample
        print("\nSample of merged data:")
        print(merged.head())
        
        return merged
    
    def auto_generate_insights(self):
        """Automatically generate insights based on available data"""
        if self.merged_data is None:
            print("No merged data available for analysis")
            return
        
        print("\n" + "="*50)
        print("AUTO-GENERATING INSIGHTS")
        print("="*50)
        
        df = self.merged_data
        insights = {}
        
        # Basic statistics
        print("Analyzing data structure...")
        insights['basic_stats'] = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
            'text_columns': len(df.select_dtypes(include=['object']).columns),
            'date_columns': len(df.select_dtypes(include=['datetime']).columns)
        }
        
        # Find numeric columns for analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
        
        print(f"Found {len(numeric_cols)} numeric columns: {numeric_cols}")
        print(f"Found {len(text_cols)} text columns: {text_cols}")
        print(f"Found {len(date_cols)} date columns: {date_cols}")
        
        # Revenue/Sales analysis (look for money-related columns)
        revenue_cols = [col for col in numeric_cols if any(keyword in col.lower() for keyword in ['revenue', 'sales', 'amount', 'price', 'cost', 'total'])]
        if revenue_cols:
            insights['financial_summary'] = {}
            for col in revenue_cols:
                insights['financial_summary'][col] = {
                    'total': df[col].sum(),
                    'average': df[col].mean(),
                    'median': df[col].median(),
                    'min': df[col].min(),
                    'max': df[col].max()
                }
        
        # Categorical analysis
        categorical_insights = {}
        for col in text_cols:
            if df[col].nunique() < 20:  # Only analyze columns with reasonable number of categories
                value_counts = df[col].value_counts()
                categorical_insights[col] = {
                    'unique_values': df[col].nunique(),
                    'top_values': value_counts.head().to_dict(),
                    'distribution': value_counts.to_dict()
                }
        
        if categorical_insights:
            insights['categorical_analysis'] = categorical_insights
        
        # Time series analysis (if date columns exist)
        if date_cols and revenue_cols:
            insights['time_analysis'] = {}
            for date_col in date_cols[:1]:  # Analyze first date column
                for rev_col in revenue_cols[:1]:  # Analyze first revenue column
                    df_time = df.groupby(pd.Grouper(key=date_col, freq='D'))[rev_col].sum().reset_index()
                    insights['time_analysis'][f'{rev_col}_by_{date_col}'] = {
                        'daily_average': df_time[rev_col].mean(),
                        'best_day': df_time.loc[df_time[rev_col].idxmax(), date_col] if len(df_time) > 0 else None,
                        'worst_day': df_time.loc[df_time[rev_col].idxmin(), date_col] if len(df_time) > 0 else None
                    }
        
        # Correlation analysis
        if len(numeric_cols) > 1:
            correlation_matrix = df[numeric_cols].corr()
            # Find strong correlations (> 0.7 or < -0.7)
            strong_correlations = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        strong_correlations.append({
                            'col1': correlation_matrix.columns[i],
                            'col2': correlation_matrix.columns[j],
                            'correlation': corr_value
                        })
            
            if strong_correlations:
                insights['correlations'] = strong_correlations
        
        self.insights = insights
        print("✓ Insights generated successfully!")
    
    def print_auto_insights_report(self):
        """Print comprehensive insights report"""
        if not self.insights:
            print("No insights available. Run auto_generate_insights() first.")
            return
        
        print("\n" + "="*60)
        print("AUTOMATED BUSINESS INSIGHTS REPORT")
        print("="*60)
        
        # Basic Statistics
        if 'basic_stats' in self.insights:
            print("\n📊 DATA OVERVIEW")
            print("-" * 20)
            stats = self.insights['basic_stats']
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Financial Summary
        if 'financial_summary' in self.insights:
            print("\n💰 FINANCIAL SUMMARY")
            print("-" * 25)
            for col, stats in self.insights['financial_summary'].items():
                print(f"\n{col.upper()}:")
                for metric, value in stats.items():
                    print(f"  {metric.title()}: {value:,.2f}")
        
        # Categorical Analysis
        if 'categorical_analysis' in self.insights:
            print("\n📂 CATEGORICAL ANALYSIS")
            print("-" * 30)
            for col, analysis in self.insights['categorical_analysis'].items():
                print(f"\n{col.upper()}:")
                print(f"  Unique values: {analysis['unique_values']}")
                print("  Top categories:")
                for category, count in list(analysis['top_values'].items())[:5]:
                    print(f"    {category}: {count}")
        
        # Time Analysis
        if 'time_analysis' in self.insights:
            print("\n📅 TIME SERIES ANALYSIS")
            print("-" * 30)
            for analysis_name, data in self.insights['time_analysis'].items():
                print(f"\n{analysis_name.upper()}:")
                for metric, value in data.items():
                    print(f"  {metric.replace('_', ' ').title()}: {value}")
        
        # Correlations
        if 'correlations' in self.insights:
            print("\n🔗 STRONG CORRELATIONS")
            print("-" * 25)
            for corr in self.insights['correlations']:
                print(f"{corr['col1']} ↔ {corr['col2']}: {corr['correlation']:.3f}")
    
    def create_auto_visualizations(self):
        """Create visualizations based on available data"""
        if self.merged_data is None:
            print("No data available for visualization")
            return
        
        print("\n" + "="*50)
        print("CREATING AUTO VISUALIZATIONS")
        print("="*50)
        
        df = self.merged_data
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
        
        # Calculate number of subplots needed
        n_plots = min(6, len(numeric_cols) + len(text_cols))
        if n_plots == 0:
            print("No suitable columns found for visualization")
            return
        
        # Set up the plotting environment
        fig = plt.figure(figsize=(15, 10))
        plot_count = 0
        
        # Plot numeric columns (histograms)
        for i, col in enumerate(numeric_cols[:3]):
            if plot_count >= 6:
                break
            plot_count += 1
            plt.subplot(2, 3, plot_count)
            plt.hist(df[col].dropna(), bins=20, alpha=0.7, color='skyblue')
            plt.title(f'Distribution of {col}', fontsize=12, fontweight='bold')
            plt.xlabel(col)
            plt.ylabel('Frequency')
        
        # Plot categorical columns (bar charts)
        for i, col in enumerate(text_cols[:3]):
            if plot_count >= 6:
                break
            if df[col].nunique() <= 10:  # Only plot if reasonable number of categories
                plot_count += 1
                plt.subplot(2, 3, plot_count)
                value_counts = df[col].value_counts().head(10)
                plt.bar(range(len(value_counts)), value_counts.values, color='lightcoral')
                plt.title(f'Top Values in {col}', fontsize=12, fontweight='bold')
                plt.ylabel('Count')
                plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
        
        # Time series plot if available
        if date_cols and numeric_cols and plot_count < 6:
            plot_count += 1
            plt.subplot(2, 3, plot_count)
            date_col = date_cols[0]
            num_col = numeric_cols[0]
            
            # Group by date and sum
            time_data = df.groupby(pd.Grouper(key=date_col, freq='D'))[num_col].sum()
            plt.plot(time_data.index, time_data.values, marker='o', linewidth=2)
            plt.title(f'{num_col} Over Time', fontsize=12, fontweight='bold')
            plt.xlabel('Date')
            plt.ylabel(num_col)
            plt.xticks(rotation=45)
        
        # Correlation heatmap if multiple numeric columns
        if len(numeric_cols) > 1 and plot_count < 6:
            plot_count += 1
            plt.subplot(2, 3, plot_count)
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
            plt.title('Correlation Matrix', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('auto_insights_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ Visualizations created and saved as 'auto_insights_dashboard.png'")
    
    def run_custom_pipeline(self):
        """Run the complete data pipeline with your files"""
        print("🚀 STARTING CUSTOM DATA PIPELINE")
        print("=" * 60)
        
        # Inspect your files first
        self.inspect_data_files()
        
        # Load data from your files
        print("\n📥 LOADING YOUR DATA FILES")
        print("-" * 35)
        
        if self.csv_file:
            self.sales_data = self.load_csv_data()
        
        if self.json_file:
            self.metadata = self.load_json_data()
        
        if self.excel_file:
            self.region_data = self.load_excel_data()
        
        # Check if at least one file was loaded
        if all(data is None for data in [self.sales_data, self.metadata, self.region_data]):
            print("❌ No data was successfully loaded. Please check your file paths and formats.")
            return
        
        # Use the largest dataset as primary data
        datasets = []
        if self.sales_data is not None:
            datasets.append(('CSV', self.sales_data))
        if self.metadata is not None:
            datasets.append(('JSON', self.metadata))
        if self.region_data is not None:
            datasets.append(('Excel', self.region_data))
        
        # Sort by size and use largest as primary
        datasets.sort(key=lambda x: len(x[1]), reverse=True)
        primary_type, self.sales_data = datasets[0]
        print(f"\nUsing {primary_type} data as primary dataset ({len(self.sales_data)} records)")
        
        # Reassign other datasets
        if len(datasets) > 1:
            if primary_type != 'JSON' and any(t[0] == 'JSON' for t in datasets[1:]):
                self.metadata = next(t[1] for t in datasets[1:] if t[0] == 'JSON')
            if primary_type != 'Excel' and any(t[0] == 'Excel' for t in datasets[1:]):
                self.region_data = next(t[1] for t in datasets[1:] if t[0] == 'Excel')
        
        # Merge data sources
        self.smart_merge_data()
        
        # Generate insights
        self.auto_generate_insights()
        
        # Print report
        self.print_auto_insights_report()
        
        # Create visualizations
        self.create_auto_visualizations()
        
        # Export results
        self.export_custom_results()
        
        print("\n" + "="*60)
        print("🎉 CUSTOM PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nFiles generated:")
        print("- auto_insights_dashboard.png (Visualizations)")
        print("- custom_merged_data.csv (Processed data)")
        print("- custom_insights_report.txt (Text insights)")
    
    def export_custom_results(self):
        """Export results from your custom data"""
        print("\n📤 EXPORTING CUSTOM RESULTS")
        print("-" * 30)
        
        # Export merged data if available
        if self.merged_data is not None:
            self.merged_data.to_csv('custom_merged_data.csv', index=False)
            print("✓ Merged data exported to 'custom_merged_data.csv'")
        
        # Export insights to text file
        if self.insights:
            with open('custom_insights_report.txt', 'w') as f:
                f.write("CUSTOM DATA INSIGHTS REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                for section, data in self.insights.items():
                    f.write(f"{section.upper().replace('_', ' ')}\n")
                    f.write("-" * 30 + "\n")
                    f.write(str(data))
                    f.write("\n\n")
            
            print("✓ Insights exported to 'custom_insights_report.txt'")

# Example usage with your files
if __name__ == "__main__":
    print("🔧 CUSTOM DATA PIPELINE SETUP")
    print("=" * 40)
    print("Please update the file paths below to point to your actual files:")
    print()
    
    # ====== MODIFY THESE PATHS TO YOUR ACTUAL FILES ======
    your_csv_file = r"c:\Users\yaswa\OneDrive\Desktop\Flipkart Project\multisource_sales_dashboard_demo\sales_data.csv"      # Replace with your CSV file path
    your_json_file = r"c:\Users\yaswa\OneDrive\Desktop\Flipkart Project\multisource_sales_dashboard_demo\product_metadata.json"      # Replace with your JSON file path  
    your_excel_file = r"c:\Users\yaswa\OneDrive\Desktop\Flipkart Project\multisource_sales_dashboard_demo\region_info.xlsx"      # Replace with your Excel file path
    # =====================================================
    
    # Initialize the pipeline with your files
    pipeline = CustomSalesDataPipeline(
        csv_file=your_csv_file,
        json_file=your_json_file, 
        excel_file=your_excel_file
    )
    
    # Run the complete pipeline
    pipeline.run_custom_pipeline()
    
    print("\n📝 NEXT STEPS:")
    print("1. Update the file paths in the code to point to your actual files")
    print("2. Run the script to analyze your data")
    print("3. Review the generated insights and visualizations")
    print("4. Customize the analysis based on your specific needs")
    print("\n🎓 Perfect for your data analysis portfolio!")