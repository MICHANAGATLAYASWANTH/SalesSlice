# SalesSlice Dashboard Visual Mapping & Wireframe Specification

This document maps user business requirements to **17 interactive visualizations and KPI metrics** across 4 dedicated report pages in Power BI, consolidating 12 months of sales data across 8 store locations and 5 product lines.

---

## Global Slicers & Filters (Top Persistent Header Bar)
- **Date Range Slicer**: Relative / Slider across 12 months (July 1, 2023 – June 30, 2024).
- **Store Location Slicer**: Multi-select dropdown for all 8 stores (Manhattan Flagship, Beverly Hills Metro, Michigan Ave Downtown, Galleria Pavilion, Lincoln Road Center, Westlake Promenade, NorthPark Center, Back Bay Boutique).
- **Product Line Slicer**: Horizontal pill selector for 5 lines (Electronics & Gadgets, Apparel & Accessories, Home & Kitchen, Beauty & Personal Care, Sports & Outdoors).
- **Customer Segment Slicer**: Dropdown for Retail VIP, Regular, Corporate, Student.

---

## Page 1: Executive KPI & Revenue Overview

| Visual # | Visual Name | Visual Type | Primary Measures & Fields | Business Question Answered |
| :--- | :--- | :--- | :--- | :--- |
| **Visual 01** | Total Net Revenue KPI Card | Multi-row KPI Card | `[Total Sales]`, `[YoY Sales Growth %]`, Trend Sparkline | What is the top-line dollar revenue, and is it pacing positively YoY? |
| **Visual 02** | Gross Profit & Margin Card | KPI Card | `[Total Gross Profit]`, `[Gross Margin %]` | How much gross profit was preserved after product costs and markdowns? |
| **Visual 03** | Order Volume & Basket Size | Dual KPI Card | `[Total Transactions]`, `[Average Order Value (AOV)]` | What is overall shopper volume and ticket size? |
| **Visual 04** | Annual Target Attainment | Radial Gauge / KPI Card | `[Total Sales]`, `[Annual Store Target]`, `[Target Attainment %]` | Are our physical retail stores on track against corporate annual quota? |
| **Visual 05** | Monthly Revenue & Profit Trend | Line & Clustered Column | X-Axis: `DimDate[YearMonth]`<br>Columns: `[Total Sales]`<br>Line: `[Gross Margin %]` | How do sales and margins fluctuate seasonally across the 12 months? |
| **Visual 06** | Revenue by Product Line | Donut / Donut Matrix | Legend: `DimProduct[ProductLine]`<br>Values: `[Total Sales]`, `[Product Line Revenue Share %]` | Which product line contributes the largest share to total turnover? |
| **Visual 07** | Store Revenue Leaderboard | Ranked Horizontal Bar Chart | Y-Axis: `DimStore[StoreName]`<br>X-Axis: `[Total Sales]`<br>Color: `DimStore[Region]` | Which store locations are the top commercial performers? |

---

## Page 2: Store Location Performance & Spatial Efficiency

| Visual # | Visual Name | Visual Type | Primary Measures & Fields | Business Question Answered |
| :--- | :--- | :--- | :--- | :--- |
| **Visual 08** | Store Sales vs Monthly Quota | Clustered Column + Goal Line | X-Axis: `DimStore[StoreName]`<br>Values: `[Total Sales]`<br>Target Line: `[Annual Store Target]` | Which individual store locations met or missed their assigned quotas? |
| **Visual 09** | Revenue per Square Foot | Horizontal Bar Chart | Y-Axis: `DimStore[StoreName]`<br>X-Axis: `[Sales per Sq Ft]` | Which store generates the highest dollar productivity per square foot of physical retail space? |
| **Visual 10** | Regional Performance Matrix | Matrix / Treemap | Grouping: `DimStore[Region]` -> `DimStore[City]`<br>Values: `[Total Sales]`, `[Gross Margin %]`, `[Total Units Sold]` | How do East, West, Midwest, and South regions compare in profitability? |
| **Visual 11** | Traffic vs Basket Size Correlation | Scatter Plot | X-Axis: `[Total Transactions]`<br>Y-Axis: `[Average Order Value]`<br>Size: `[Total Sales]`<br>Details: `DimStore[StoreName]` | Do higher traffic stores have lower average basket sizes? |

---

## Page 3: Product Line & Profitability Deep Dive

| Visual # | Visual Name | Visual Type | Primary Measures & Fields | Business Question Answered |
| :--- | :--- | :--- | :--- | :--- |
| **Visual 12** | Product Line MoM Heatmap | Matrix with Conditional Formatting | Rows: `DimProduct[ProductLine]`<br>Columns: `DimDate[MonthName]`<br>Values: `[MoM Sales Growth %]` | Which product categories experienced sharp accelerations or contractions month-over-month? |
| **Visual 13** | Margin % vs Sales Volume Quadrant | 4-Quadrant Bubble Chart | X-Axis: `[Total Units Sold]`<br>Y-Axis: `[Gross Margin %]`<br>Details: `DimProduct[SubCategory]`<br>Color: `DimProduct[ProductLine]` | Which subcategories are High Volume / High Margin "Stars" vs Low Margin "Drains"? |
| **Visual 14** | Top 10 Best Sellers vs Bottom 10 | Tornado / Ranked Bar Chart | Y-Axis: `DimProduct[ProductName]`<br>X-Axis: `[Total Sales]`<br>Filter: `Top 10` & `Bottom 10` | Which specific SKUs drive 80% of category volume? |
| **Visual 15** | Discount & Return Margin Erosion | Waterfall Chart | Category: Gross Sales -> Discounts -> Cost of Goods -> Net Profit -> Returns | Exactly how much potential margin is lost to promotional discounting and customer returns? |

---

## Page 4: Customer Trends & Time Intelligence

| Visual # | Visual Name | Visual Type | Primary Measures & Fields | Business Question Answered |
| :--- | :--- | :--- | :--- | :--- |
| **Visual 16** | Day-of-Week Sales Heatmap | Matrix Heatmap | Rows: `DimStore[StoreName]`<br>Columns: `DimDate[DayName]`<br>Values: `[Total Sales]` | When do store locations experience their peak weekend vs weekday footfall? |
| **Visual 17** | Customer Segment Revenue Distribution | 100% Stacked Bar Chart | Y-Axis: `DimProduct[ProductLine]`<br>X-Axis: `[Total Sales]`<br>Legend: `DimCustomer[Segment]` | Which customer tiers (VIP vs Corporate vs Regular) purchase which product lines? |

---

## Stakeholder Impact & ROI
- **25% Reduction in Manual Reporting Effort**: Consolidated disjointed store-level spreadsheets into an automated, single-source-of-truth semantic model.
- **Cross-Filtering**: Clicking any store location or product category cross-filters all other 16 visuals instantaneously.
