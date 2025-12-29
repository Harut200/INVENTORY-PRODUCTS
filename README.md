# Retail Inventory Data Pipeline (SQLite & Pandas)

## Overview

This project implements a backend data pipeline for a retail inventory system. It focuses on cleaning noisy CSV data, structuring a relational SQLite database, and applying SQL logic such as triggers and views to support inventory management and reporting. The project is designed as a backend-only solution with no frontend or API layer.

## Key Objectives

- Clean and standardize raw product and inventory data
- Design a normalized SQLite database schema
- Persist processed data into relational tables
- Implement SQL triggers for automatic stock updates
- Create analytical SQL views for reporting
- Apply business rules using SQL update statements

## Data Processing

Raw CSV files containing products and inventory information are processed using Pandas:

- Missing categories and warehouse codes are filled using statistical mode
- Invalid or missing prices are replaced with the median value
- Stock levels are cleaned and standardized
- Unique identifiers are generated for products and inventory records

Cleaned datasets are exported as processed CSV files for traceability.

## Database Design

The SQLite database contains three main tables:

- **products**: stores product metadata and pricing
- **inventory**: tracks stock levels by warehouse
- **sales**: records product sales transactions

Foreign key relationships are used to maintain referential integrity between tables.

## SQL Logic

- **Trigger**: Automatically updates inventory stock levels after a sale is inserted
- **View**: Aggregates total potential revenue by product category
- **Update Rule**: Applies a discount to products with low stock in a specific warehouse

These features demonstrate practical use of database-side logic for real-world scenarios.

## Technologies Used

- Python
- Pandas
- NumPy
- SQLite
- SQL (Triggers, Views, Joins)

## Scope

This project is intended for educational and backend data engineering purposes, emphasizing data quality, relational modeling, and SQL-based business logic rather than user interfaces.
