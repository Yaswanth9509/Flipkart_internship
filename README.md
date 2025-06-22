# Custom Multi-Source Sales Data Pipeline & Business Insights Dashboard

A comprehensive Python-based data pipeline that automatically ingests, processes, and analyzes sales data from multiple sources (CSV, JSON, Excel) to generate actionable business insights and visualizations.

## 🌟 Features

- **Multi-Format Data Ingestion**: Seamlessly loads data from CSV, JSON, and Excel files
- **Intelligent Data Cleaning**: Automatically detects and converts date/numeric columns
- **Smart Data Merging**: Intelligently combines multiple data sources based on common columns
- **Auto-Generated Insights**: Produces financial summaries, categorical analysis, time series insights, and correlation analysis
- **Dynamic Visualizations**: Creates publication-ready charts and dashboards
- **Export Capabilities**: Saves processed data and insights in multiple formats

## 🎯 Perfect For

- Data analysts building their portfolio
- Business intelligence projects
- Sales performance analysis
- Multi-source data integration tasks
- Automated reporting systems

## 📋 Requirements

### Python Version
- Python 3.7 or higher

### Required Libraries
```bash
pip install pandas numpy matplotlib seaborn tabulate openpyxl
```

Or install all at once:
```bash
pip install -r requirements.txt
```

### Create requirements.txt file:
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
tabulate>=0.8.0
openpyxl>=3.0.0
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/custom-sales-data-pipeline.git
cd custom-sales-data-pipeline
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare Your Data Files
Place your data files in the project directory or note their full paths:
- **CSV file**: Your main sales/transaction data
- **JSON file**: Product metadata or additional information
- **Excel file**: Regional data, categories, or supplementary data

### 4. Update File Paths
Edit the file paths in `Sales_Data_Pipeline_Main.py` (lines 445-449):

```python
# ====== MODIFY THESE PATHS TO YOUR ACTUAL FILES ======
your_csv_file = "path/to/your/sales_data.csv"
your_json_file = "path/to/your/product_metadata.json"  
your_excel_file = "path/to/your/region_info.xlsx"
# =====================================================
```

### 5. Run the Pipeline
```bash
python Sales_Data_Pipeline_Main.py
```

## 📊 What You'll Get

### Generated Files
1. **`auto_insights_dashboard.png`** - Comprehensive visualization dashboard
2. **`custom_merged_data.csv`** - Cleaned and merged dataset
3. **`custom_insights_report.txt`** - Detailed text-based insights report

### Console Output
- Data file inspection results
- Data loading progress and statistics
- Smart merging process details
- Comprehensive insights report
- Visualization creation status

## 🔧 Customization Options

### Custom Data Processing
The pipeline automatically detects column types, but you can customize:

```python
# Custom date columns
pipeline.load_csv_data(date_columns=['order_date', 'delivery_date'])

# Custom numeric columns  
pipeline.load_csv_data(numeric_columns=['price', 'quantity', 'revenue'])

# Custom merge keys
pipeline.smart_merge_data(merge_keys={
    'metadata': 'product_id',
    'region': 'region_code'
})
```

### Adding Custom Analysis
Extend the `auto_generate_insights()` method to include domain-specific analysis:

```python
# Add to the CustomSalesDataPipeline class
def custom_business_metrics(self):
    """Add your custom business logic here"""
    # Customer lifetime value calculation
    # Seasonal trend analysis
    # Product performance metrics
    # etc.
```

## 📁 Project Structure

```
custom-sales-data-pipeline/
│
├── Sales_Data_Pipeline_Main.py    # Main pipeline script
├── requirements.txt               # Python dependencies
├── README.md                     # This file
├── data/                         # Directory for your data files
│   ├── sales_data.csv
│   ├── product_metadata.json
│   └── region_info.xlsx
├── output/                       # Generated results
│   ├── auto_insights_dashboard.png
│   ├── custom_merged_data.csv
│   └── custom_insights_report.txt
└── examples/                     # Sample data and usage examples
    ├── sample_data/
    └── example_usage.py
```

## 🎓 Educational Value

This project demonstrates:

- **Data Engineering**: Multi-source data ingestion and transformation
- **Data Science**: Statistical analysis and insight generation
- **Business Intelligence**: Automated reporting and visualization
- **Software Engineering**: Clean, modular, and extensible code architecture
- **Project Management**: Complete end-to-end data pipeline implementation

## 🔍 Example Use Cases

### E-commerce Analysis
- Combine sales transactions (CSV) + product catalog (JSON) + regional data (Excel)
- Generate insights on product performance, regional trends, and customer behavior

### Financial Reporting
- Merge transaction data with account information and regional performance metrics
- Automatic calculation of KPIs and financial summaries

### Inventory Management
- Integrate sales data with product metadata and warehouse information
- Track inventory turnover and demand patterns

## 🛠️ Troubleshooting

### Common Issues

**File Not Found Error**
```
FileNotFoundError: [Errno 2] No such file or directory
```
**Solution**: Verify file paths are correct and files exist

**Import Error**
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution**: Install required packages using `pip install -r requirements.txt`

**Empty Results**
```
No data was successfully loaded
```
**Solution**: Check file formats and ensure at least one file contains valid data

### Data Format Requirements

**CSV Files**:
- Must have header row
- Numeric columns should contain only numbers (no currency symbols)
- Date columns should be in recognizable format (YYYY-MM-DD, MM/DD/YYYY, etc.)

**JSON Files**:
- Valid JSON format
- Can be array of objects or single object
- Nested structures are flattened automatically

**Excel Files**:
- .xlsx or .xls format
- First sheet is used by default
- Header row should be present

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution
- Additional data source connectors (databases, APIs)
- More sophisticated statistical analysis
- Interactive dashboard capabilities
- Performance optimizations
- Additional export formats

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for educational and portfolio development purposes
- Demonstrates real-world data engineering and analysis practices
- Suitable for beginners to intermediate data professionals

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review existing [Issues](https://github.com/yourusername/custom-sales-data-pipeline/issues)
3. Create a new issue with detailed description and error messages

## 🎨 Showcase Your Results

After running the pipeline, share your results:

- Include generated visualizations in your portfolio
- Write a blog post about your findings
- Present insights to stakeholders
- Use as foundation for more advanced analysis

---

**⭐ If you find this project helpful, please give it a star! ⭐**

Happy analyzing! 📊✨
