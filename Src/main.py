# Imports and DB Path
import json
import sqlite3
import requests
import numpy as np
import pandas as pd
from pathlib import Path

DB_PATH = Path("../Data/DB/INVENTORY_PRODUCTS.db")


# Load Data products
prod_raw = pd.read_csv(
    Path.cwd().parent / "Data" / "Row" / "products_noisy.csv"
)


# Data cleaning (products)
prod_raw["ProductID"] = range(101, len(prod_raw) + 101)

prod_raw["ProductName"] = [f"Product_{i}" for i in range(1, 1001)]

prod_raw["Category"] = prod_raw["Category"].fillna(prod_raw["Category"].mode()[0])

prod_raw["Price"] = prod_raw["Price"].mask(prod_raw["Price"] <= 0, prod_raw["Price"].median()).fillna(prod_raw["Price"].median())



# Load Data inventory
inv_raw = pd.read_csv(
    Path.cwd().parent / "Data" / "Row" / "inventory_noisy.csv"
)
inv_raw


# Data cleaning (inventory)
inv_raw["ProductID"] = range(101, len(inv_raw) + 101)

inv_raw["InventoryID"] = range(1, len(inv_raw) + 1)

inv_raw["WarehouseCode"] = inv_raw["WarehouseCode"].fillna(inv_raw["WarehouseCode"].mode()[0])

inv_raw["StockLevel"] = inv_raw["StockLevel"].fillna(inv_raw["StockLevel"].median())

inv_raw.to_csv(Path.cwd().parent / "Data" / "Processed" / "inventory_levels.csv")

prod_raw.to_csv(Path.cwd().parent / "Data" / "Processed" / "products.csv")


# DB Creation
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS products(
    ProductID INTEGER PRIMARY KEY, 
    ProductName TEXT,
    Category TEXT,
    Price REAL
    );
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS inventory(
    InventoryID INTEGER PRIMARY KEY,
    ProductID INTEGER REFERENCES products (ProductID),
    WarehouseCode TEXT,
    StockLevel INTEGER
    );
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS sales(
    SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductID INTEGER REFERENCES products (ProductID),
    QuantitySold INTEGER,
    SaleDate TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """
)

conn.commit()


# SQL Insert
prod_raw.to_sql("products", conn, if_exists="replace", index=False)
inv_raw.to_sql("inventory", conn, if_exists="replace", index=False)


# SQL Tasks
cur.execute(
    """
    CREATE TRIGGER IF NOT EXISTS UpdateStockAfterSale
    AFTER INSERT ON sales
    BEGIN
        UPDATE Inventory
        SET StockLevel = StockLevel - NEW.QuantitySold
        WHERE ProductID = NEW.ProductID;
    END;
    """
)

cur.execute("""
    CREATE VIEW IF NOT EXISTS CategoryRevenueSummary AS
    SELECT
        p.Category,
        SUM(p.Price * i.StockLevel) AS TotalPotentialRevenue
    FROM products p
    JOIN inventory i
    ON p.ProductID = i.ProductID
    GROUP BY p.Category;
    """
)

cur.execute("""
    UPDATE products
    SET Price = Price * 0.8
    WHERE ProductID IN (
        SELECT ProductID
        FROM investory
        WHERE WarehouseCode = 'WH-A'
          AND StockLevel < 40
    );
    """
)

conn.commit()
conn.close()