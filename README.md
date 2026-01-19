# Sales Analytics System
Student Name: Shaikh Sidra
Student id:[bitsom_ba_25071626]
Email: [sidra61224@gmail.com]
Date: 2025

# Project Overview

The Sales Analytics System is an end-to-end Python application designed to analyze sales transaction data, enrich it with external product information using an API, and generate a comprehensive sales report.

# The project demonstrates:

> Data cleaning and validation
> Analytical processing
> API integration
> File-based reporting
> Modular Python programming

It simulates a real-world analytics pipeline commonly used in data engineering and business intelligence systems.

# Technologies Used
> Python 3
> Pandas – data cleaning and transformation
> NumPy – numeric operations
> Requests – API integration (DummyJSON)
> File I/O – reading/writing pipe-delimited text files

# Database Setup
This project does not use a traditional database.
Instead:
> Raw data is stored in text files
> Cleaned and enriched data is saved back to files
> Reports are generated as formatted .txt files

This approach keeps the project lightweight and easy to run without database installation.

# Folder Structure

sales-analytics-system/
│
├─ data/
│   ├─ sales_data.txt                # Raw sales data
│   └─ enriched_sales_data.txt       # Enriched output data
│
├─ output/
│   └─ sales_report.txt              # Final analytics report
│
├─ utils/
│   ├─ file_handler.py               # Data reading & cleaning
│   ├─ data_processor.py             # Analysis & enrichment logic
│   └─ api_handler.py                # API integration logic
│
├─ main.py                           # Main application workflow
└─ README.md                         # Project documentation

# Setup Instructions

1. Clone the repository
  > git clone <repository-url>
cd sales-analytics-system

2. Install required libraries
  > pip install pandas numpy requests

3. Ensure input file exists
  > Place sales_data.txt inside the data/ folder

4. Run the application
  > python main.py

# Application Workflow

1. Reads and cleans raw sales data
2. Displays optional filter options (region-based)
3. Validates transaction records
4. Performs all sales analyses:
  > Region-wise performance
  > Top products
  > Customer analysis
  > Daily trends
  > Peak sales day
  > Low-performing products
5. Fetches product data from DummyJSON API
6. Enriches sales data with API product details
7. Saves enriched data to a new file
8. Generates a comprehensive text report

# Key Learnings
 > Handling real-world messy data using Python
 > Modular code design using utility files
 > Performing business analytics using Pandas
 > API integration and error handling
 > Data enrichment techniques
 > Generating structured reports programmatically
 > Building robust user-driven workflows

# Challenges Faced

 > Handling inconsistent and invalid transaction records
 > Managing encoding issues in input files
 > Ensuring enrichment works even when API data is missing
 > Avoiding program crashes using proper error handling
 > Designing flexible user input for filtering
 > Integrating multiple project parts into a single workflow

Each challenge helped strengthen understanding of real-world data engineering problems.

# Notes
 > All files use pipe (|) delimited format
 > API enrichment is optional and safely handled
 > Filtering supports single or multiple regions
 > The report is generated automatically — no manual file creation required
