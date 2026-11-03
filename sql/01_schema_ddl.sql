-- ============================================================================
-- Project: SalesSlice – Interactive Retail Analytics Dashboard
-- Script:  01_schema_ddl.sql
-- Engine:  Microsoft SQL Server (2019 / 2022 / Azure SQL)
-- Schema:  Star Schema Data Warehouse Architecture (SalesSliceDW)
-- Author:  Retail Analytics Engineering Team
-- ============================================================================

-- Create Database if not exists
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'SalesSliceDW')
BEGIN
    CREATE DATABASE SalesSliceDW;
END
GO

USE SalesSliceDW;
GO

-- Set ANSI standards for query optimization and indexed views
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

-- ----------------------------------------------------------------------------
-- Drop existing foreign keys and tables if recreating
-- ----------------------------------------------------------------------------
IF OBJECT_ID('dbo.FactSales', 'U') IS NOT NULL DROP TABLE dbo.FactSales;
IF OBJECT_ID('dbo.DimCustomer', 'U') IS NOT NULL DROP TABLE dbo.DimCustomer;
IF OBJECT_ID('dbo.DimProduct', 'U') IS NOT NULL DROP TABLE dbo.DimProduct;
IF OBJECT_ID('dbo.DimStore', 'U') IS NOT NULL DROP TABLE dbo.DimStore;
IF OBJECT_ID('dbo.DimPromotion', 'U') IS NOT NULL DROP TABLE dbo.DimPromotion;
IF OBJECT_ID('dbo.DimDate', 'U') IS NOT NULL DROP TABLE dbo.DimDate;
GO

-- ----------------------------------------------------------------------------
-- 1. Dimension: DimStore (8 Locations)
-- ----------------------------------------------------------------------------
CREATE TABLE dbo.DimStore (
    StoreKey            INT IDENTITY(1,1) NOT NULL,
    StoreID             VARCHAR(20)       NOT NULL,
    StoreName           VARCHAR(100)      NOT NULL,
    City                VARCHAR(50)       NOT NULL,
    State               VARCHAR(10)       NOT NULL,
    Region              VARCHAR(30)       NOT NULL,
    StoreType           VARCHAR(50)       NOT NULL,
    SquareFootage       INT               NOT NULL,
    ManagerName         VARCHAR(100)      NOT NULL,
    MonthlySalesTarget  DECIMAL(12,2)     NOT NULL,
    CreatedAt           DATETIME2         DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_DimStore PRIMARY KEY CLUSTERED (StoreKey),
    CONSTRAINT UQ_DimStore_StoreID UNIQUE (StoreID)
);
GO

-- ----------------------------------------------------------------------------
-- 2. Dimension: DimProduct (5 Product Lines, 40 Products)
-- ----------------------------------------------------------------------------
CREATE TABLE dbo.DimProduct (
    ProductKey          INT IDENTITY(1,1) NOT NULL,
    ProductID           VARCHAR(20)       NOT NULL,
    ProductName         VARCHAR(150)      NOT NULL,
    ProductLine         VARCHAR(50)       NOT NULL, -- 5 Core Lines
    SubCategory         VARCHAR(50)       NOT NULL,
    UnitCost            DECIMAL(10,2)     NOT NULL,
    UnitPrice           DECIMAL(10,2)     NOT NULL,
    MarginPercent       DECIMAL(5,2)      NOT NULL,
    CreatedAt           DATETIME2         DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_DimProduct PRIMARY KEY CLUSTERED (ProductKey),
    CONSTRAINT UQ_DimProduct_ProductID UNIQUE (ProductID)
);
GO

-- ----------------------------------------------------------------------------
-- 3. Dimension: DimCustomer (1,200 Customers)
-- ----------------------------------------------------------------------------
CREATE TABLE dbo.DimCustomer (
    CustomerKey         INT IDENTITY(1,1) NOT NULL,
    CustomerID          VARCHAR(20)       NOT NULL,
    CustomerName        VARCHAR(100)      NOT NULL,
    CustomerEmail       VARCHAR(120)      NOT NULL,
    Segment             VARCHAR(30)       NOT NULL, -- VIP, Regular, Corporate, Student
    City                VARCHAR(50)       NOT NULL,
    State               VARCHAR(10)       NOT NULL,
    SignupDate          DATE              NOT NULL,
    PreferredStoreKey   INT               NULL,
    CreatedAt           DATETIME2         DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_DimCustomer PRIMARY KEY CLUSTERED (CustomerKey),
    CONSTRAINT UQ_DimCustomer_CustomerID UNIQUE (CustomerID)
);
GO

-- ----------------------------------------------------------------------------
-- 4. Dimension: DimDate (366 Days: 2023-07-01 to 2024-06-30)
-- ----------------------------------------------------------------------------
CREATE TABLE dbo.DimDate (
    DateKey             INT               NOT NULL, -- Format: YYYYMMDD
    FullDate            DATE              NOT NULL,
    DayOfWeek           TINYINT           NOT NULL,
    DayName             VARCHAR(15)       NOT NULL,
    DayOfMonth          TINYINT           NOT NULL,
    MonthNumber         TINYINT           NOT NULL,
    MonthName           VARCHAR(15)       NOT NULL,
    YearMonth           VARCHAR(7)        NOT NULL, -- Format: YYYY-MM
    Quarter             VARCHAR(2)        NOT NULL, -- Q1, Q2, Q3, Q4
    [Year]              SMALLINT          NOT NULL,
    IsWeekend           BIT               NOT NULL,
    Season              VARCHAR(15)       NOT NULL,
    IsHolidaySeason     BIT               NOT NULL,
    CONSTRAINT PK_DimDate PRIMARY KEY CLUSTERED (DateKey),
    CONSTRAINT UQ_DimDate_FullDate UNIQUE (FullDate)
);
GO

-- ----------------------------------------------------------------------------
-- 5. Dimension: DimPromotion (Campaigns & Seasonal Events)
-- ----------------------------------------------------------------------------
CREATE TABLE dbo.DimPromotion (
    PromotionKey        INT IDENTITY(1,1) NOT NULL,
    PromotionName       VARCHAR(100)      NOT NULL,
    DiscountPct         DECIMAL(4,2)      NOT NULL,
    StartDate           DATE              NOT NULL,
    EndDate             DATE              NOT NULL,
    CONSTRAINT PK_DimPromotion PRIMARY KEY CLUSTERED (PromotionKey)
);
GO

-- ----------------------------------------------------------------------------
-- 6. Fact: FactSales (Consolidated 12 Months Retail Transactions)
-- ----------------------------------------------------------------------------
CREATE TABLE dbo.FactSales (
    SalesKey            BIGINT IDENTITY(1,1) NOT NULL,
    DateKey             INT                  NOT NULL,
    StoreKey            INT                  NOT NULL,
    ProductKey          INT                  NOT NULL,
    CustomerKey         INT                  NOT NULL,
    PromotionKey        INT                  NOT NULL,
    Quantity            INT                  NOT NULL CHECK (Quantity > 0),
    UnitPrice           DECIMAL(10,2)        NOT NULL,
    UnitCost            DECIMAL(10,2)        NOT NULL,
    DiscountAmount      DECIMAL(10,2)        NOT NULL DEFAULT 0.00,
    SalesAmount         DECIMAL(12,2)        NOT NULL,
    TotalCost           DECIMAL(12,2)        NOT NULL,
    GrossProfit         DECIMAL(12,2)        NOT NULL,
    ReturnFlag          BIT                  NOT NULL DEFAULT 0,
    PaymentMethod       VARCHAR(40)          NOT NULL,
    TransactionTime     DATETIME2            DEFAULT SYSUTCDATETIME(),
    
    -- Primary Key Constraint
    CONSTRAINT PK_FactSales PRIMARY KEY CLUSTERED (SalesKey),
    
    -- Foreign Key Relationships (Star Schema)
    CONSTRAINT FK_FactSales_DimDate      FOREIGN KEY (DateKey)      REFERENCES dbo.DimDate (DateKey),
    CONSTRAINT FK_FactSales_DimStore     FOREIGN KEY (StoreKey)     REFERENCES dbo.DimStore (StoreKey),
    CONSTRAINT FK_FactSales_DimProduct   FOREIGN KEY (ProductKey)   REFERENCES dbo.DimProduct (ProductKey),
    CONSTRAINT FK_FactSales_DimCustomer  FOREIGN KEY (CustomerKey)  REFERENCES dbo.DimCustomer (CustomerKey),
    CONSTRAINT FK_FactSales_DimPromotion FOREIGN KEY (PromotionKey) REFERENCES dbo.DimPromotion (PromotionKey)
);
GO

-- Optional foreign key for Customer preferred store
ALTER TABLE dbo.DimCustomer
ADD CONSTRAINT FK_DimCustomer_DimStore FOREIGN KEY (PreferredStoreKey) REFERENCES dbo.DimStore (StoreKey);
GO

PRINT 'SalesSliceDW Star Schema DDL created successfully.';
