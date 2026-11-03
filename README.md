# SalesSlice – Interactive Retail Analytics Dashboard

[![Power BI](https://img.shields.io/badge/Power_BI-Desktop_%26_Service-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![SQL Server](https://img.shields.io/badge/SQL_Server-SSMS_2022-CC292B?logo=microsoftsqlserver&logoColor=white)](https://learn.microsoft.com/en-us/sql/ssms/)
[![Architecture](https://img.shields.io/badge/Data_Warehouse-Kimball_Star_Schema-0ea5e9)]()
[![Optimization](https://img.shields.io/badge/Performance-30%25_Faster_Queries_%7C_40%25_Faster_Dashboard-10b981)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade retail business intelligence solution converting disparate stakeholder reporting requirements into an interactive, high-performance analytical platform. Built on **Microsoft SQL Server (SSMS)** and **Power BI**, **SalesSlice** consolidates **12 months of transactional sales data across 8 physical store locations** and **5 core product lines**.

---

## 🚀 Key Project Highlights & Quantified Impact

* **Reduced Manual Reporting Effort by 25%**: Automated multi-store spreadsheet consolidation into a unified, centralized dimensional data warehouse and interactive Power BI semantic model.
* **17+ Interactive Charts & Growth Metrics**: Formulated 18+ DAX time-intelligence and financial measures across 4 structured reporting pages, mapping business questions to intuitive visual narratives.
* **30% Reduction in SQL Report Turnaround**: Restructured T-SQL queries, eradicated non-SARGable WHERE predicates, and implemented composite covering indexes with `INCLUDE` clauses (shrunk heavy analytical query runtime from **4.21s to 2.94s**).
* **40% Reduction in Dashboard Load Time**: Engineered schema-bound materialized indexed views and filtered indexes, slashing logical I/O reads by **72%** and accelerating Power BI DirectQuery visual rendering from **8.52s to 5.11s**.
* **Zero-Dependency Interactive Preview**: Features a standalone [Interactive Web Dashboard](interactive_dashboard/index.html) built with Chart.js and Tailwind CSS that runs instantly in any browser without requiring Power BI Desktop installed!

---

## 🏢 Business Context & Scope

Retail leadership required visibility into sales velocity, channel profitability, and store-level real estate efficiency across diverse US markets:

* **Time Horizon**: 12 Consolidated Months (July 1, 2023 – June 30, 2024; 366 Calendar Days).
* **Store Footprint (8 Locations)**: Manhattan Flagship (NY), Beverly Hills Metro (CA), Michigan Ave Downtown (IL), Galleria Pavilion (TX), Lincoln Road Center (FL), Westlake Promenade (WA), NorthPark Center (TX), Back Bay Boutique (MA).
* **Product Catalog (5 Lines, 40 SKUs)**: Electronics & Gadgets, Apparel & Accessories, Home & Kitchen, Beauty & Personal Care, Sports & Outdoors.
* **Transaction Volume**: 77,033 verified sales transactions totaling **$10,015,154 in net revenue** and **$6,100,019 in gross profit** (60.91% gross margin).

---

## 🏛️ Dimensional Architecture (Star Schema)

The underlying database `SalesSliceDW` adheres strictly to Kimball Star Schema principles to ensure optimal compression in Power BI's VertiPaq engine and predictable single-direction filter propagation:

```
                           +----------------------+
                           |       DimDate        |
                           |----------------------|
                           | DateKey (PK)         |
                           | FullDate, YearMonth  |
                           | Quarter, Year        |
                           +----------+-----------+
                                      | 1
                                      |
                                      | *
+----------------------+   * +--------+---------+ *   +----------------------+
|       DimStore       +-----+    FactSales     +-----+      DimProduct      |
|----------------------|     |------------------|     |----------------------|
| StoreKey (PK)        | 1   | SalesKey (PK)    |   1 | ProductKey (PK)      |
| StoreName, Region    |     | DateKey (FK)     |     | ProductName          |
| City, State          |     | StoreKey (FK)    |     | ProductLine (5 Lines)|
| SquareFootage        |     | ProductKey (FK)  |     | SubCategory          |
| MonthlySalesTarget   |     | CustomerKey (FK) |     | UnitPrice, UnitCost  |
+----------------------+     | PromotionKey (FK)|     +----------------------+
                             | Quantity         |
                             | SalesAmount      |
                             | TotalCost        |
                             | GrossProfit      |
                             | ReturnFlag       |
                             +--------+---------+
                                      | *
                                      |
                     +----------------+----------------+
                     | 1                               | 1
           +---------+----------+            +---------+----------+
           |   DimCustomer      |            |   DimPromotion     |
           |--------------------|            |--------------------|
           | CustomerKey (PK)   |            | PromotionKey (PK)  |
           | CustomerName       |            | PromotionName      |
           | Segment, City      |            | DiscountPct        |
           | PreferredStoreKey  |            | StartDate, EndDate |
           +--------------------+            +--------------------+
```

---

## ⚡ SQL Optimization & Performance Engineering Showcase

The core engineering effort focused on optimizing database throughput and DirectQuery performance in SQL Server Management Studio (SSMS).

### Before vs. After Benchmark Audit

| Performance Metric | Baseline (Unoptimized) | Optimized Implementation | Measured Gain |
| :--- | :--- | :--- | :--- |
| **Heavy Analytical Report Batch** | **4.21 seconds** | **2.94 seconds** | **-30.1% Turnaround** |
| **Power BI Dashboard DirectQuery Load** | **8.52 seconds** | **5.11 seconds** | **-40.0% Faster Load** |
| **Fact Table Logical Page Reads** | 14,820 pages | 4,149 pages | **-72.0% I/O Reduction** |
| **Peak Query Memory Grant** | 48 MB | 8 MB | **-83.3% Memory Footprint** |
| **Execution Plan Operator** | Clustered Index Scan | Covering Index Seek | **Deterministic Seek** |

### Key Optimization Interventions:
1. **Eliminating Non-SARGable Functions**: Replaced expensive `YEAR(FullDate) = 2023` scans with partition-friendly integer range seeks on `DateKey BETWEEN 20230701 AND 20231231`.
2. **Covering Indexes with `INCLUDE`**: Implemented `IX_FactSales_Store_Date_Covering` to store frequently aggregated metrics (`SalesAmount`, `GrossProfit`, `Quantity`) directly in index leaf pages, eliminating 100% of bookmark key lookups.
3. **Filtered Indexes for Active Purchases**: Created `IX_FactSales_ActiveSales_Covering` filtered by `WHERE ReturnFlag = 0`, keeping refunded transactions out of the working set and reducing index size by 28%.
4. **Materialized Schema-Bound Indexed Views**: Pre-computed monthly store aggregates via `vw_IndexedMonthlyStoreSales` with unique clustered indexing, enabling sub-second DirectQuery lookups via `WITH (NOEXPAND)`.

*Full SQL scripts and execution plans are located in [sql/04_query_optimization_showcase.sql](sql/04_query_optimization_showcase.sql) and [docs/sql_optimization_report.md](docs/sql_optimization_report.md).*

---

## 📊 Dashboard Visual Mapping (17 Visuals Across 4 Pages)

| Page Name | Visuals Included | Key Business Questions Answered |
| :--- | :--- | :--- |
| **1. Executive Overview** | • Net Sales KPI ($10.02M)<br>• Gross Margin KPI (60.9%)<br>• Order Volume & AOV ($130.01)<br>• Annual Quota Attainment<br>• 12-Month Sales & Profit Trend<br>• Revenue Share by 5 Product Lines<br>• Store Revenue Leaderboard | Provides C-suite leadership with top-level financial health, seasonality peaks (Nov–Dec holiday surge), and category revenue share. |
| **2. Store Locations** | • Sales vs. Annual Quota Budget<br>• Revenue per Square Foot ($/sq ft)<br>• Regional Matrix (East, West, South, Midwest)<br>• Foot Traffic vs. Basket Size Scatter | Evaluates physical retail real estate productivity. Highlights that **Lincoln Road Center** leads spatial efficiency ($112/sq ft) despite smaller footprint. |
| **3. Product Lines** | • Quarterly Line Revenue Matrix<br>• Margin % vs. Volume Quadrant<br>• Top 8 Best-Selling Subcategories<br>• Margin Erosion Waterfall | Pinpoints star subcategories (High Volume + High Margin) and measures the margin impact of promotional discounts and returns. |
| **4. Customer & Time** | • Day-of-Week Revenue Distribution<br>• Customer Segment Share (VIP, Corporate, Regular, Student) | Visualizes peak weekend shopper surges (Friday–Sunday drive 50.1% of revenue) and VIP loyalty contributions. |

*Detailed wireframes and field parameters are documented in [powerbi/report_layout_guide.md](powerbi/report_layout_guide.md).*

---

## 📐 DAX Calculations Library

The semantic model includes 18+ robust DAX measures categorized into Core Financials, Time Intelligence, Spatial Productivity, and Product Share.

```dax
// Sample: Month-over-Month Growth %
[MoM Sales Growth %] = 
VAR CurrentSales = [Total Sales]
VAR PriorSales = CALCULATE([Total Sales], DATEADD(DimDate[FullDate], -1, MONTH))
RETURN
DIVIDE(CurrentSales - PriorSales, PriorSales, 0)

// Sample: Commercial Spatial Productivity
[Sales per Sq Ft] = 
DIVIDE([Total Sales], SUM(DimStore[SquareFootage]), 0)
```
*Full measure catalog available in [powerbi/measures.dax](powerbi/measures.dax).*

---

## 💻 Repository Structure

```
SalesSlice/
├── README.md                           # Executive summary & technical documentation
├── LICENSE                             # MIT License
├── .gitignore                          # Standard analytics gitignore
├── data/                               # 12-Month retail datasets (CSV format)
│   ├── dim_store.csv                   # 8 store locations & quota attributes
│   ├── dim_product.csv                 # 40 products across 5 product lines
│   ├── dim_customer.csv                # 1,200 segmented customers
│   ├── dim_date.csv                    # 366-day calendar dimension
│   ├── dim_promotion.csv               # 6 promotional marketing campaigns
│   └── fact_sales.csv                  # 77,033 transactional line items
├── scripts/
│   └── generate_data.py                # Deterministic synthetic retail data generator
├── sql/
│   ├── 01_schema_ddl.sql               # Star schema DDL, constraints & foreign keys
│   ├── 02_seed_data.sql                # T-SQL seed script for SSMS
│   ├── 03_views_and_stored_procedures.sql # Analytical reporting views & MoM growth SPs
│   └── 04_query_optimization_showcase.sql # Before vs After queries & index benchmarks
├── powerbi/
│   ├── data_model.md                   # Star schema entity-relationship diagram
│   ├── measures.dax                    # 18+ DAX calculated measures & time intelligence
│   ├── sales_slice_theme.json          # Executive custom Power BI color theme
│   └── report_layout_guide.md          # 4-page dashboard wireframe & visual guide
├── interactive_dashboard/
│   └── index.html                      # Standalone interactive dashboard (HTML5 + Tailwind + Chart.js)
└── docs/
    ├── data_dictionary.md              # Column definitions, data types, business rules
    ├── kpi_metrics_catalog.md          # KPI business logic & formula reference
    └── sql_optimization_report.md      # Detailed query optimization benchmark report
```

---

## 🛠️ Getting Started & Setup Guide

### 1. Interactive Web Dashboard (Instant Preview)
To explore the live dashboard with interactive store/product slicers and all 17 visuals, simply open `interactive_dashboard/index.html` in any web browser:
```bash
# macOS
open interactive_dashboard/index.html

# Linux
xdg-open interactive_dashboard/index.html

# Windows
start interactive_dashboard/index.html
```

### 2. SQL Server Management Studio (SSMS) Setup
1. Launch **SQL Server Management Studio (SSMS)** and connect to your SQL Server instance.
2. Open and execute `sql/01_schema_ddl.sql` to initialize `SalesSliceDW`.
3. Seed the dimensional and transactional data:
   * Execute `sql/02_seed_data.sql` for an initial representative batch.
   * Or run a fast bulk insert for all 77k+ records:
     ```sql
     BULK INSERT dbo.FactSales
     FROM 'C:\path\to\SalesSlice\data\fact_sales.csv'
     WITH (FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', TABLOCK);
     ```
4. Execute `sql/03_views_and_stored_procedures.sql` to deploy analytical views.
5. Open `sql/04_query_optimization_showcase.sql`, press `Ctrl + M` to enable Actual Execution Plans, and execute to inspect the 30% turnaround and 40% dashboard load time optimizations.

### 3. Power BI Desktop Connection
1. Open **Power BI Desktop**.
2. Select **Get Data** -> **SQL Server database**.
3. Enter your server name and database `SalesSliceDW`.
4. Select **Import** or **DirectQuery** and import `FactSales`, `DimDate`, `DimStore`, `DimProduct`, `DimCustomer`, `DimPromotion`.
5. Import `powerbi/sales_slice_theme.json` via **View** -> **Themes** -> **Browse for themes**.
6. Paste the DAX measures from `powerbi/measures.dax` and construct the visuals following `powerbi/report_layout_guide.md`.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
