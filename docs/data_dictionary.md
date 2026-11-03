# SalesSlice Data Warehouse: Data Dictionary

This document details the entity structures, column definitions, data types, nullability, and business rules across the **SalesSliceDW** relational star schema.

---

## 1. Dimension Tables

### `dbo.DimStore`
Captures commercial metadata, physical geography, and monthly revenue targets across all 8 brick-and-mortar retail locations.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `StoreKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate primary key. |
| `StoreID` | `VARCHAR(20)` | No | Unique | Natural business key (e.g., `STR-001`). |
| `StoreName` | `VARCHAR(100)` | No | None | Commercial store designation (e.g., Manhattan Flagship). |
| `City` | `VARCHAR(50)` | No | None | Municipality where store is located. |
| `State` | `VARCHAR(10)` | No | None | 2-letter US State postal code. |
| `Region` | `VARCHAR(30)` | No | None | Corporate territory: `East`, `West`, `South`, `Midwest`. |
| `StoreType` | `VARCHAR(50)` | No | None | Classification: `Flagship`, `Urban Metro`, `Suburban Mall`, etc. |
| `SquareFootage` | `INT` | No | None | Usable retail floor area in square feet (used for spatial metrics). |
| `ManagerName` | `VARCHAR(100)` | No | None | General store manager on record. |
| `MonthlySalesTarget`| `DECIMAL(12,2)` | No | None | Monthly financial revenue quota set by retail leadership. |
| `CreatedAt` | `DATETIME2` | No | None | Record ingestion timestamp (UTC). |

---

### `dbo.DimProduct`
Maintains SKU hierarchy, category mappings, supplier costs, and retail catalog pricing across 5 product lines.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `ProductKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate primary key. |
| `ProductID` | `VARCHAR(20)` | No | Unique | Stock keeping unit identifier (e.g., `PRD-001`). |
| `ProductName` | `VARCHAR(150)` | No | None | Full commercial title of retail SKU. |
| `ProductLine` | `VARCHAR(50)` | No | None | One of 5 core categories (`Electronics & Gadgets`, `Apparel & Accessories`, `Home & Kitchen`, `Beauty & Personal Care`, `Sports & Outdoors`). |
| `SubCategory` | `VARCHAR(50)` | No | None | Specific departmental taxonomy (e.g., `Wearables`, `Audio`, `Cookware`). |
| `UnitCost` | `DECIMAL(10,2)` | No | None | Inbound supplier purchase cost per unit. |
| `UnitPrice` | `DECIMAL(10,2)` | No | None | Recommended retail catalog list price before promotions. |
| `MarginPercent` | `DECIMAL(5,2)` | No | None | Standard margin percentage: `((UnitPrice - UnitCost) / UnitPrice) * 100`. |
| `CreatedAt` | `DATETIME2` | No | None | Audit timestamp. |

---

### `dbo.DimCustomer`
Captures shopper demographics, loyalty segmentation, and geographic residence for 1,200 unique retail customers.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `CustomerKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate primary key. |
| `CustomerID` | `VARCHAR(20)` | No | Unique | Customer loyalty ID (e.g., `CUST-00001`). |
| `CustomerName` | `VARCHAR(100)` | No | None | Customer full name. |
| `CustomerEmail` | `VARCHAR(120)` | No | None | Contact email address. |
| `Segment` | `VARCHAR(30)` | No | None | Loyalty classification: `Retail VIP` (15%), `Regular` (55%), `Corporate` (18%), `Student` (12%). |
| `City` | `VARCHAR(50)` | No | None | Customer billing municipality. |
| `State` | `VARCHAR(10)` | No | None | Customer billing state. |
| `SignupDate` | `DATE` | No | None | Date customer entered loyalty program. |
| `PreferredStoreKey`| `INT` | Yes | FK -> `DimStore` | Store location where customer registers most frequent visits. |

---

### `dbo.DimDate`
Comprehensive corporate calendar dimension covering all 366 days in the reporting window (2023-07-01 to 2024-06-30).

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `DateKey` | `INT` | No | PK | Integer key in `YYYYMMDD` format (enables partition pruning). |
| `FullDate` | `DATE` | No | Unique | ISO standard calendar date. |
| `DayOfWeek` | `TINYINT` | No | None | Day index: 1 (Monday) to 7 (Sunday). |
| `DayName` | `VARCHAR(15)` | No | None | Text day of week (e.g., `Saturday`). |
| `DayOfMonth` | `TINYINT` | No | None | Calendar day (1 to 31). |
| `MonthNumber` | `TINYINT` | No | None | Calendar month (1 to 12). |
| `MonthName` | `VARCHAR(15)` | No | None | English month title (e.g., `November`). |
| `YearMonth` | `VARCHAR(7)` | No | None | ISO month string (`YYYY-MM`). |
| `Quarter` | `VARCHAR(2)` | No | None | Fiscal / Calendar quarter (`Q1`, `Q2`, `Q3`, `Q4`). |
| `Year` | `SMALLINT` | No | None | 4-digit calendar year (`2023`, `2024`). |
| `IsWeekend` | `BIT` | No | None | `1` if Saturday or Sunday, `0` otherwise. |
| `Season` | `VARCHAR(15)` | No | None | Climatological season: `Fall`, `Winter`, `Spring`, `Summer`. |
| `IsHolidaySeason` | `BIT` | No | None | `1` during Black Friday, Cyber Week, Christmas, Memorial Day, July 4th. |

---

### `dbo.DimPromotion`
Tracks active marketing campaigns and price markdown concessions.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `PromotionKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate primary key. |
| `PromotionName` | `VARCHAR(100)` | No | None | Campaign title (e.g., `Black Friday Mega Savings`). |
| `DiscountPct` | `DECIMAL(4,2)` | No | None | Promotional markdown percentage (e.g., `0.25` for 25%). |
| `StartDate` | `DATE` | No | None | Campaign activation date. |
| `EndDate` | `DATE` | No | None | Campaign termination date. |

---

## 2. Fact Table

### `dbo.FactSales`
Central transaction grain capturing itemized POS retail transactions across the 12-month reporting horizon.

| Column Name | Data Type | Nullable | Primary/Foreign Key | Description & Business Rules |
| :--- | :--- | :--- | :--- | :--- |
| `SalesKey` | `BIGINT IDENTITY(1,1)` | No | PK | Unique POS line item identifier. |
| `DateKey` | `INT` | No | FK -> `DimDate` | Transaction date surrogate integer. |
| `StoreKey` | `INT` | No | FK -> `DimStore` | Physical store location. |
| `ProductKey` | `INT` | No | FK -> `DimProduct` | Purchased SKU. |
| `CustomerKey` | `INT` | No | FK -> `DimCustomer` | Purchasing customer account. |
| `PromotionKey` | `INT` | No | FK -> `DimPromotion` | Applied promotional campaign. |
| `Quantity` | `INT` | No | None | Units purchased (strictly `> 0`). |
| `UnitPrice` | `DECIMAL(10,2)` | No | None | Catalog sticker price at time of sale. |
| `UnitCost` | `DECIMAL(10,2)` | No | None | Supplier product unit cost at time of sale. |
| `DiscountAmount` | `DECIMAL(10,2)` | No | None | `(Quantity * UnitPrice) * DiscountPct`. |
| `SalesAmount` | `DECIMAL(12,2)` | No | None | Net realization: `(Quantity * UnitPrice) - DiscountAmount`. |
| `TotalCost` | `DECIMAL(12,2)` | No | None | `Quantity * UnitCost`. |
| `GrossProfit` | `DECIMAL(12,2)` | No | None | `SalesAmount - TotalCost`. |
| `ReturnFlag` | `BIT` | No | None | `1` if item was returned for refund; `0` if sale kept. |
| `PaymentMethod` | `VARCHAR(40)` | No | None | Tender type: `Credit Card`, `Apple Pay / Digital Wallet`, `Debit Card`, `Store Credit`. |
| `TransactionTime`| `DATETIME2` | No | None | POS transaction timestamp. |
