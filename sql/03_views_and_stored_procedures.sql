-- ============================================================================
-- Project: SalesSlice – Interactive Retail Analytics Dashboard
-- Script:  03_views_and_stored_procedures.sql
-- Engine:  Microsoft SQL Server
-- Purpose: Analytical Views and Stored Procedures for Power BI & Reporting
-- ============================================================================

USE SalesSliceDW;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

-- ----------------------------------------------------------------------------
-- View 1: vw_ExecutiveSalesSummary
-- Consolidates monthly sales, cost, profit, and order volumes across stores & lines
-- ----------------------------------------------------------------------------
IF OBJECT_ID('dbo.vw_ExecutiveSalesSummary', 'V') IS NOT NULL 
    DROP VIEW dbo.vw_ExecutiveSalesSummary;
GO

CREATE VIEW dbo.vw_ExecutiveSalesSummary
AS
SELECT 
    d.YearMonth,
    d.[Year],
    d.Quarter,
    d.MonthNumber,
    d.MonthName,
    s.StoreKey,
    s.StoreID,
    s.StoreName,
    s.Region,
    s.City,
    p.ProductLine,
    COUNT(f.SalesKey)                          AS TotalTransactions,
    SUM(f.Quantity)                            AS TotalUnitsSold,
    SUM(f.SalesAmount)                         AS GrossSalesRevenue,
    SUM(f.DiscountAmount)                      AS TotalDiscounts,
    SUM(f.TotalCost)                           AS TotalCostOfGoodsSold,
    SUM(f.GrossProfit)                         AS TotalGrossProfit,
    ROUND(
        CASE 
            WHEN SUM(f.SalesAmount) > 0 
            THEN (SUM(f.GrossProfit) / SUM(f.SalesAmount)) * 100 
            ELSE 0 
        END, 2
    )                                          AS GrossMarginPercent,
    ROUND(
        CASE 
            WHEN COUNT(f.SalesKey) > 0 
            THEN SUM(f.SalesAmount) / COUNT(f.SalesKey) 
            ELSE 0 
        END, 2
    )                                          AS AverageOrderValue
FROM dbo.FactSales f
INNER JOIN dbo.DimDate d    ON f.DateKey = d.DateKey
INNER JOIN dbo.DimStore s   ON f.StoreKey = s.StoreKey
INNER JOIN dbo.DimProduct p ON f.ProductKey = p.ProductKey
WHERE f.ReturnFlag = 0
GROUP BY 
    d.YearMonth,
    d.[Year],
    d.Quarter,
    d.MonthNumber,
    d.MonthName,
    s.StoreKey,
    s.StoreID,
    s.StoreName,
    s.Region,
    s.City,
    p.ProductLine;
GO

-- ----------------------------------------------------------------------------
-- View 2: vw_ProductLineProfitability
-- Granular product performance, category share, and discount erosion analysis
-- ----------------------------------------------------------------------------
IF OBJECT_ID('dbo.vw_ProductLineProfitability', 'V') IS NOT NULL 
    DROP VIEW dbo.vw_ProductLineProfitability;
GO

CREATE VIEW dbo.vw_ProductLineProfitability
AS
SELECT 
    p.ProductKey,
    p.ProductID,
    p.ProductName,
    p.ProductLine,
    p.SubCategory,
    p.UnitCost,
    p.UnitPrice,
    p.MarginPercent                            AS CatalogMarginPercent,
    COUNT(f.SalesKey)                          AS TotalOrders,
    SUM(f.Quantity)                            AS UnitsSold,
    SUM(f.SalesAmount)                         AS RealizedRevenue,
    SUM(f.DiscountAmount)                      AS TotalDiscountsAwarded,
    SUM(f.GrossProfit)                         AS TotalProfit,
    ROUND(
        CASE 
            WHEN SUM(f.SalesAmount) > 0 
            THEN (SUM(f.GrossProfit) / SUM(f.SalesAmount)) * 100 
            ELSE 0 
        END, 2
    )                                          AS RealizedMarginPercent,
    SUM(CASE WHEN f.ReturnFlag = 1 THEN 1 ELSE 0 END) AS ReturnedUnitsCount
FROM dbo.DimProduct p
LEFT JOIN dbo.FactSales f ON p.ProductKey = f.ProductKey
GROUP BY 
    p.ProductKey,
    p.ProductID,
    p.ProductName,
    p.ProductLine,
    p.SubCategory,
    p.UnitCost,
    p.UnitPrice,
    p.MarginPercent;
GO

-- ----------------------------------------------------------------------------
-- View 3: vw_StoreSpatialEfficiency
-- Measures Revenue per Square Foot and Monthly Budget Attainment
-- ----------------------------------------------------------------------------
IF OBJECT_ID('dbo.vw_StoreSpatialEfficiency', 'V') IS NOT NULL 
    DROP VIEW dbo.vw_StoreSpatialEfficiency;
GO

CREATE VIEW dbo.vw_StoreSpatialEfficiency
AS
SELECT 
    s.StoreKey,
    s.StoreID,
    s.StoreName,
    s.City,
    s.State,
    s.Region,
    s.StoreType,
    s.SquareFootage,
    s.MonthlySalesTarget,
    SUM(f.SalesAmount)                         AS TotalAnnualRevenue,
    ROUND(SUM(f.SalesAmount) / s.SquareFootage, 2) AS RevenuePerSquareFoot,
    ROUND(SUM(f.SalesAmount) / 12.0, 2)        AS AverageMonthlyRevenue,
    ROUND(
        ((SUM(f.SalesAmount) / 12.0) / s.MonthlySalesTarget) * 100, 2
    )                                          AS MonthlyTargetAttainmentPct,
    COUNT(DISTINCT f.CustomerKey)              AS UniqueShoppersCount,
    COUNT(f.SalesKey)                          AS TotalTransactions
FROM dbo.DimStore s
LEFT JOIN dbo.FactSales f ON s.StoreKey = f.StoreKey AND f.ReturnFlag = 0
GROUP BY 
    s.StoreKey,
    s.StoreID,
    s.StoreName,
    s.City,
    s.State,
    s.Region,
    s.StoreType,
    s.SquareFootage,
    s.MonthlySalesTarget;
GO

-- ----------------------------------------------------------------------------
-- Stored Procedure: sp_GetStoreMoMGrowth
-- Calculates Month-over-Month Revenue Growth % across stores using Window Functions
-- ----------------------------------------------------------------------------
IF OBJECT_ID('dbo.sp_GetStoreMoMGrowth', 'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_GetStoreMoMGrowth;
GO

CREATE PROCEDURE dbo.sp_GetStoreMoMGrowth
    @StoreKey INT = NULL -- Pass NULL for all stores
AS
BEGIN
    SET NOCOUNT ON;

    WITH MonthlyStoreTotals AS (
        SELECT 
            s.StoreKey,
            s.StoreName,
            d.YearMonth,
            MIN(d.FullDate) AS MonthStartDate,
            SUM(f.SalesAmount) AS MonthlyRevenue,
            COUNT(f.SalesKey) AS MonthlyOrders
        FROM dbo.FactSales f
        INNER JOIN dbo.DimDate d  ON f.DateKey = d.DateKey
        INNER JOIN dbo.DimStore s ON f.StoreKey = s.StoreKey
        WHERE f.ReturnFlag = 0
          AND (@StoreKey IS NULL OR s.StoreKey = @StoreKey)
        GROUP BY 
            s.StoreKey,
            s.StoreName,
            d.YearMonth
    ),
    LaggedTotals AS (
        SELECT 
            StoreKey,
            StoreName,
            YearMonth,
            MonthStartDate,
            MonthlyRevenue,
            MonthlyOrders,
            LAG(MonthlyRevenue, 1) OVER (
                PARTITION BY StoreKey 
                ORDER BY MonthStartDate
            ) AS PriorMonthRevenue
        FROM MonthlyStoreTotals
    )
    SELECT 
        StoreKey,
        StoreName,
        YearMonth,
        MonthlyRevenue,
        PriorMonthRevenue,
        ROUND(MonthlyRevenue - ISNULL(PriorMonthRevenue, MonthlyRevenue), 2) AS RevenueVariance,
        ROUND(
            CASE 
                WHEN PriorMonthRevenue IS NOT NULL AND PriorMonthRevenue > 0
                THEN ((MonthlyRevenue - PriorMonthRevenue) / PriorMonthRevenue) * 100.0
                ELSE 0.0
            END, 2
        ) AS MoMGrowthPercent,
        MonthlyOrders
    FROM LaggedTotals
    ORDER BY StoreKey, MonthStartDate;
END;
GO

-- ----------------------------------------------------------------------------
-- Stored Procedure: sp_GetCustomerSegmentMetrics
-- Aggregates customer behavior, spending power, and loyalty breakdown
-- ----------------------------------------------------------------------------
IF OBJECT_ID('dbo.sp_GetCustomerSegmentMetrics', 'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_GetCustomerSegmentMetrics;
GO

CREATE PROCEDURE dbo.sp_GetCustomerSegmentMetrics
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        c.Segment,
        COUNT(DISTINCT c.CustomerKey)          AS TotalCustomers,
        COUNT(f.SalesKey)                      AS TotalTransactions,
        SUM(f.SalesAmount)                     AS SegmentRevenue,
        ROUND(
            CASE 
                WHEN COUNT(f.SalesKey) > 0 
                THEN SUM(f.SalesAmount) / COUNT(f.SalesKey) 
                ELSE 0 
            END, 2
        )                                      AS SegmentAOV,
        ROUND(
            CASE 
                WHEN COUNT(DISTINCT c.CustomerKey) > 0 
                THEN SUM(f.SalesAmount) / COUNT(DISTINCT c.CustomerKey) 
                ELSE 0 
            END, 2
        )                                      AS RevenuePerCustomer,
        ROUND(
            (SUM(f.SalesAmount) * 100.0) / 
            SUM(SUM(f.SalesAmount)) OVER(), 2
        )                                      AS RevenueSharePercent
    FROM dbo.DimCustomer c
    LEFT JOIN dbo.FactSales f ON c.CustomerKey = f.CustomerKey AND f.ReturnFlag = 0
    GROUP BY c.Segment
    ORDER BY SegmentRevenue DESC;
END;
GO

PRINT 'SalesSliceDW analytical views and stored procedures created successfully.';
