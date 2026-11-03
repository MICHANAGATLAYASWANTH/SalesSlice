# Power BI Data Model Architecture: SalesSlice

## 1. Architectural Philosophy: Pure Star Schema
The **SalesSlice** semantic model is designed following Ralph Kimball dimensional modeling principles. Normalization artifacts (snowflaking) were deliberately avoided to optimize Power BI's VertiPaq columnar in-memory compression engine, ensure deterministic filter propagation, and eliminate bidirectional relationship ambiguity.

```
                           +----------------------+
                           |       DimDate        |
                           |----------------------|
                           | DateKey (PK)         |
                           | FullDate             |
                           | MonthName, YearMonth |
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

## 2. Table Relationships & Cardinality

| From Table (Dimension) | From Column | To Table (Fact) | To Column | Cardinality | Cross Filter Direction | Security Filtering |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DimDate** | `DateKey` | **FactSales** | `DateKey` | 1 to Many (`1:*`) | Single (`DimDate` -> `FactSales`) | None |
| **DimStore** | `StoreKey` | **FactSales** | `StoreKey` | 1 to Many (`1:*`) | Single (`DimStore` -> `FactSales`) | None (RLS Optional) |
| **DimProduct** | `ProductKey` | **FactSales** | `ProductKey` | 1 to Many (`1:*`) | Single (`DimProduct` -> `FactSales`) | None |
| **DimCustomer** | `CustomerKey` | **FactSales** | `CustomerKey` | 1 to Many (`1:*`) | Single (`DimCustomer` -> `FactSales`) | None |
| **DimPromotion** | `PromotionKey` | **FactSales** | `PromotionKey` | 1 to Many (`1:*`) | Single (`DimPromotion` -> `FactSales`) | None |

---

## 3. VertiPaq Engine Optimization Guidelines

1. **Mark as Date Table**:
   - `DimDate` is designated as the official date table using `DimDate[FullDate]`.
   - Built-in automatic date hierarchies are disabled in Power BI Options (`Auto Date/Time = OFF`) to prevent bloated hidden local date tables, reducing model RAM size by 15-20%.

2. **Column Cardinality & Memory Footprint**:
   - High-cardinality keys like `SalesKey` (Surrogate Primary Key in `FactSales`) are hidden from report view and excluded from VertiPaq memory if not needed for row-level drill-through.
   - Surrogate keys (`DateKey`, `StoreKey`, `ProductKey`, `CustomerKey`) use fixed integer formats (`INT32`) enabling VertiPaq dictionary encoding and Bit-Packed Array compression.

3. **Separation of Measures and Attributes**:
   - All calculation metrics reside in a dedicated calculation group/empty table `_Measures`.
   - Naked numerical columns in `FactSales` (`SalesAmount`, `TotalCost`, `GrossProfit`) are hidden from end users to force consumption through validated DAX measures.

4. **Hierarchies Configured**:
   - **Calendar Hierarchy**: `Year` -> `Quarter` -> `MonthName` -> `FullDate`
   - **Store Hierarchy**: `Region` -> `State` -> `City` -> `StoreName`
   - **Product Hierarchy**: `ProductLine` -> `SubCategory` -> `ProductName`
