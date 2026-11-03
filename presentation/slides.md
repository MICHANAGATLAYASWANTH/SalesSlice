---
marp: true
theme: default
paginate: true
header: "SalesSlice – Interactive Retail Analytics Dashboard"
footer: "Presenter: Yaswanth Michanagatla | Power BI & SQL Server"
---

# SalesSlice – Interactive Retail Analytics Dashboard
### Executive Presentation & Technical Architecture (Jun 2024 – Aug 2024)
**Presenter**: Yaswanth Michanagatla  
**Tools**: Microsoft Power BI, SQL Server Management Studio (SSMS), T-SQL, Python  
**Live Demo**: [https://michanagatlayaswanth.github.io/SalesSlice/](https://michanagatlayaswanth.github.io/SalesSlice/)

---

## 1. Business Problem & Project Objectives
### Addressing Reporting Bottlenecks Across 8 Store Locations

* **Manual Reporting Overhead**: Regional store managers spent 15+ hours weekly assembling disconnected spreadsheets.
* **High Query Latency**: Legacy reporting queries experienced full table scans and 4+ second turnaround times.
* **Lack of Unified Analytics**: No single source of truth across 5 product lines and 8 store territories.
* **Primary Objective**: Design a centralized Kimball Star Schema data warehouse and an interactive Power BI dashboard with sub-second performance.

---

## 2. Executive Summary & Core Business Metrics
### 12-Month Consolidated Performance (July 2023 – June 2024)

* **$10,015,154 Total Net Sales Revenue** across 366 reporting calendar days.
* **$6,100,019 Total Gross Profit** realized with an overall **60.91% Gross Margin**.
* **77,033 Completed Customer Transactions** generating 110,933 physical units sold.
* **$130.01 Average Order Value (AOV)** across 1,200 unique segmented shoppers.
* **25% Reduction in manual reporting labor** achieved immediately upon deployment.

---

## 3. Kimball Star Schema Data Warehouse Design
### Engineered for VertiPaq Columnar Compression in Power BI

* **Central Fact Table**: `FactSales` (77,033 rows; grain = individual POS line item).
* **Store Dimension**: `DimStore` (8 metropolitan locations with square footage and sales targets).
* **Product Dimension**: `DimProduct` (40 SKUs across 5 core retail lines with margin thresholds).
* **Calendar Dimension**: `DimDate` (366 days with ISO attributes, seasonality, and holiday flags).
* **Customer & Promotion Dimensions**: `DimCustomer` (1,200 accounts) and `DimPromotion` (6 campaigns).
* **Deterministic 1-to-Many single-direction relationships** with zero bidirectional ambiguity.

---

## 4. SQL Server Query Optimization Case Study
### Achieving -30% Report Turnaround and -40% Dashboard Load Time

* **30.1% Faster Batch Turnaround**: Analytical execution time reduced from 4.21s to 2.94s.
* **40.0% Faster Dashboard Load**: Power BI DirectQuery visual loading dropped from 8.52s to 5.11s.
* **72.0% I/O Reduction**: Fact table logical page reads decreased from 14,820 to 4,149 pages.
* **SARGable Predicate Refactoring**: Replaced non-SARGable `YEAR()` calls with integer `DateKey` seeks.
* **Covering Index Strategy**: `IX_FactSales_Store_Date_Covering` with `INCLUDE` eliminated 100% of bookmark lookups.
* **Materialized Indexed Views**: Pre-aggregated store metrics with `SCHEMABINDING` and clustered index.

---

## 5. Power BI Semantic Model & DAX Library
### 18+ Robust Business Formulations Across 4 Operational Categories

* **Financial Core**: `[Total Sales]`, `[Total Cost]`, `[Gross Profit]`, `[Gross Margin %]`, `[AOV]`, `[Discount Rate %]`.
* **Time Intelligence**: `[Sales YTD]`, `[Sales Prior Month]`, `[MoM Sales Growth %]`, `[YoY Sales Growth %]`, `[3M Moving Avg]`.
* **Spatial Productivity**: `[Sales per Sq Ft]` ($/sq ft) measuring commercial floor space efficiency.
* **Target Attainment**: `[Annual Store Target]` and `[Target Attainment %]` tracking quota pace.
* **Performance Ranking**: Dynamic store leaderboard rank using dense rank formulations.

---

## 6. 4-Page Dashboard Visual Architecture
### Mapping 17 Interactive Visualizations to Stakeholder Decisions

* **Page 1: Executive KPI & Revenue Overview** (Visuals 1–7: Revenue, Margin, Orders, Quota, Seasonality, Line Share, Leaderboard).
* **Page 2: Store Locations & Spatial Efficiency** (Visuals 8–11: Sales vs Budget, $/SqFt, Regional Split, Traffic vs Basket Scatter).
* **Page 3: Product Line & Category Deep Dive** (Visuals 12–15: Quarterly Evolution, Margin vs Volume Quadrant, Top Subcategories, Waterfall).
* **Page 4: Customer Trends & Time Dynamics** (Visuals 16–17: Day-of-Week Sales Distribution, Loyalty Segment Share).
* **Global Interactive Slicers**: Filter by Store Location, Product Line, and Date Range across all pages.

---

## 7. Key Retail Insights & Strategic Findings
### Data-Driven Recommendations for Retail Operations Leadership

* **Spatial Champion**: Lincoln Road Center generated highest spatial productivity ($112/sq ft) despite smaller floor plan.
* **Category Volume Driver**: Electronics & Gadgets led gross turnover ($2.49M, 24.8% share).
* **Highest Margin Line**: Beauty & Personal Care delivered peak margins (65.4%) with lowest return rate.
* **Weekend Surge**: Friday through Sunday checkouts generated 50.1% ($5.02M) of consolidated sales.
* **Promotional Impact**: Discount markdowns averaged 5.96% of gross value, preserving 60.91% realized margin.

---

## 8. Stakeholder ROI & Business Value
### Tangible Operational Improvements Delivered by SalesSlice

* **25% Labor Reduction**: Eliminated 60+ monthly hours of manual spreadsheet compilation.
* **Sub-Second Executive Decisions**: Immediate cross-filtering across store and product dimensions.
* **Single Source of Truth**: Eradicated reporting discrepancies between store managers and corporate finance.
* **Enterprise Scalability**: Partition-ready architecture capable of ingesting multi-year retail transaction growth.

---

## 9. Conclusion, Repository & Live Demonstration
### Explore the Codebase, Database Scripts, and Interactive Dashboard

* **GitHub Repository**: [https://github.com/MICHANAGATLAYASWANTH/SalesSlice](https://github.com/MICHANAGATLAYASWANTH/SalesSlice)
* **Live Interactive Web Demo**: [https://michanagatlayaswanth.github.io/SalesSlice/](https://michanagatlayaswanth.github.io/SalesSlice/)
* **Technical Documentation**: Includes Data Dictionary, KPI Catalog, and SQL Optimization Report.
* **Tools Leveraged**: Microsoft Power BI, SQL Server Management Studio (SSMS), T-SQL, Python, Tailwind CSS, Chart.js.
