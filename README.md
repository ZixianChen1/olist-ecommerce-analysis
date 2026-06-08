# Olist E-commerce Data Analysis Project

This project is a pre-learning data analysis task based on the Brazilian Olist e-commerce dataset.

## Project Description

The project uses Python and SQLite to analyse the Olist e-commerce dataset.  
The current stage focuses on loading the core CSV files, checking data types, missing values, and primary key uniqueness.

## Dataset

Dataset source: Olist Brazilian E-commerce Dataset on Kaggle.

Raw CSV files are included in the `data/` folder for this current version of the project.

## Project Structure

- `data/`: original Olist CSV datasets
- `python_scripts/`: Python scripts for data checking and analysis
- `output_csv/`: exported statistical checking results
- `figures/`: visualisation outputs to be added later
- `sql_scripts/`: SQL query scripts to be added later
- `report/`: final analysis report to be added later

## Current Progress

Completed:

- Loaded five core tables:
  - customers
  - orders
  - order_items
  - products
  - sellers
- Checked first five rows of each table
- Checked data types
- Checked missing values
- Checked primary key uniqueness
- Exported checking results to CSV files

## How to Run

Run the following Python script:

```bash
python python_scripts/01_data_check.py
