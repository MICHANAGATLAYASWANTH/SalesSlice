#!/usr/bin/env python3
"""
SalesSlice - Retail Analytics Data Generator
Generates 12 months (July 1, 2023 - June 30, 2024) of realistic retail sales data
spanning 8 store locations and 5 product lines.
"""

import os
import csv
import random
from datetime import datetime, timedelta

# Set deterministic random seed for reproducible datasets
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SQL_DIR = os.path.join(BASE_DIR, "sql")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. DimStore: 8 Store Locations
# -------------------------------------------------------------
STORES = [
    {
        "StoreKey": 1,
        "StoreID": "STR-001",
        "StoreName": "Manhattan Flagship",
        "City": "New York",
        "State": "NY",
        "Region": "East",
        "StoreType": "Flagship",
        "SquareFootage": 18500,
        "ManagerName": "Elena Rostova",
        "MonthlySalesTarget": 450000.00,
        "TrafficMultiplier": 1.45,
    },
    {
        "StoreKey": 2,
        "StoreID": "STR-002",
        "StoreName": "Beverly Hills Metro",
        "City": "Los Angeles",
        "State": "CA",
        "Region": "West",
        "StoreType": "Urban Metro",
        "SquareFootage": 14200,
        "ManagerName": "Marcus Vance",
        "MonthlySalesTarget": 380000.00,
        "TrafficMultiplier": 1.25,
    },
    {
        "StoreKey": 3,
        "StoreID": "STR-003",
        "StoreName": "Michigan Ave Downtown",
        "City": "Chicago",
        "State": "IL",
        "Region": "Midwest",
        "StoreType": "Downtown",
        "SquareFootage": 12000,
        "ManagerName": "Sarah Jenkins",
        "MonthlySalesTarget": 310000.00,
        "TrafficMultiplier": 1.05,
    },
    {
        "StoreKey": 4,
        "StoreID": "STR-004",
        "StoreName": "Galleria Pavilion",
        "City": "Houston",
        "State": "TX",
        "Region": "South",
        "StoreType": "Suburban Mall",
        "SquareFootage": 16000,
        "ManagerName": "David Chen",
        "MonthlySalesTarget": 340000.00,
        "TrafficMultiplier": 1.15,
    },
    {
        "StoreKey": 5,
        "StoreID": "STR-005",
        "StoreName": "Lincoln Road Center",
        "City": "Miami",
        "State": "FL",
        "Region": "South",
        "StoreType": "Tourist Destination",
        "SquareFootage": 9800,
        "ManagerName": "Sofia Morales",
        "MonthlySalesTarget": 290000.00,
        "TrafficMultiplier": 0.95,
    },
    {
        "StoreKey": 6,
        "StoreID": "STR-006",
        "StoreName": "Westlake Promenade",
        "City": "Seattle",
        "State": "WA",
        "Region": "West",
        "StoreType": "Urban Commercial",
        "SquareFootage": 11500,
        "ManagerName": "James Thorne",
        "MonthlySalesTarget": 280000.00,
        "TrafficMultiplier": 0.92,
    },
    {
        "StoreKey": 7,
        "StoreID": "STR-007",
        "StoreName": "NorthPark Center",
        "City": "Dallas",
        "State": "TX",
        "Region": "South",
        "StoreType": "Suburban Mall",
        "SquareFootage": 15000,
        "ManagerName": "Amanda Lewis",
        "MonthlySalesTarget": 320000.00,
        "TrafficMultiplier": 1.10,
    },
    {
        "StoreKey": 8,
        "StoreID": "STR-008",
        "StoreName": "Back Bay Boutique",
        "City": "Boston",
        "State": "MA",
        "Region": "East",
        "StoreType": "Historic Boutique",
        "SquareFootage": 8200,
        "ManagerName": "Robert O'Connor",
        "MonthlySalesTarget": 230000.00,
        "TrafficMultiplier": 0.78,
    },
]

# -------------------------------------------------------------
# 2. DimProduct: 5 Product Lines, 40 distinct items
# -------------------------------------------------------------
PRODUCT_LINES = {
    "Electronics & Gadgets": [
        ("AcousticMax ANC Headphones", "Audio", 110.00, 249.99),
        ("SoundPulse Portable Speaker", "Audio", 35.00, 79.99),
        ("PulseFit Smartwatch V3", "Wearables", 85.00, 199.99),
        ("AuraGlow Smart Desk Lamp", "Smart Home", 28.00, 69.99),
        ("NovaPower 25K Power Bank", "Accessories", 18.00, 44.99),
        ("HyperView 4K Ultra Webcam", "Peripherals", 45.00, 119.99),
        ("OmniCharge 3-in-1 Wireless Pad", "Accessories", 22.00, 59.99),
        ("VibeEar Wireless Earbuds", "Audio", 40.00, 99.99),
    ],
    "Apparel & Accessories": [
        ("Merino Wool Thermal Crew", "Tops", 32.00, 89.99),
        ("All-Weather Tech Trenchcoat", "Outerwear", 75.00, 219.99),
        ("AirFlex Running Jogger", "Activewear", 24.00, 64.99),
        ("Artisan Vegetable Tanned Belt", "Leather Goods", 18.00, 49.99),
        ("Urban Commuter Backpack 22L", "Bags", 38.00, 110.00),
        ("Classic Tailored Oxford Shirt", "Tops", 22.00, 68.00),
        ("Raw Selvedge Slim Denim", "Bottoms", 42.00, 128.00),
        ("BreezeKnit Performance Polo", "Tops", 19.00, 54.99),
    ],
    "Home & Kitchen": [
        ("Cast Iron Dutch Oven 6-Qt", "Cookware", 45.00, 129.99),
        ("Precision Conical Burr Grinder", "Coffee", 55.00, 149.99),
        ("Damascus Steel Chef's Knife 8in", "Cutlery", 36.00, 99.99),
        ("HEPA PureAir Room Filter", "Appliances", 60.00, 169.99),
        ("ThermoSmart Insulated Carafe", "Drinkware", 16.00, 42.99),
        ("Bamboo Organic Cutting Board Set", "Accessories", 12.00, 34.99),
        ("Microfiber Ultra Chef Apron", "Textiles", 9.00, 26.99),
        ("Nordic Ceramic Dinnerware 16-Pc", "Tableware", 52.00, 139.99),
    ],
    "Beauty & Personal Care": [
        ("Radiance Botanical Serum 50ml", "Skincare", 21.00, 68.00),
        ("Hyaluronic Moisture Cream", "Skincare", 16.00, 48.00),
        ("Ultrasonic Facial Cleansing Wand", "Devices", 28.00, 85.00),
        ("Velvet Cedar Eau De Parfum", "Fragrance", 38.00, 115.00),
        ("Mineral Broad Spectrum SPF 50", "Suncare", 11.00, 32.00),
        ("BioKeratin Repair Hair Mask", "Haircare", 14.00, 38.00),
        ("Rose Quartz Gua Sha Sculptor", "Tools", 7.00, 24.00),
        ("Overnight Recovery Peptide Oil", "Skincare", 25.00, 78.00),
    ],
    "Sports & Outdoors": [
        ("Summit Pro 2-Person Backpacking Tent", "Camping", 115.00, 289.99),
        ("Carbon Fiber Trekking Poles", "Hiking", 28.00, 79.99),
        ("AeroGrip Pro Yoga Mat 6mm", "Fitness", 22.00, 64.99),
        ("HydroShield 32oz Insulated Flask", "Hydration", 12.00, 34.99),
        ("SpeedStream Road Cycling Helmet", "Cycling", 48.00, 129.99),
        ("Adjustable Cast Iron Kettlebell 40lb", "Fitness", 42.00, 99.99),
        ("QuickDry Microfiber Camp Towel", "Accessories", 6.50, 18.99),
        ("Trailblazer Waterproof Daypack", "Bags", 34.00, 89.99),
    ],
}

PRODUCTS = []
p_key = 1
for line, items in PRODUCT_LINES.items():
    for name, subcat, cost, price in items:
        p_id = f"PRD-{p_key:03d}"
        PRODUCTS.append({
            "ProductKey": p_key,
            "ProductID": p_id,
            "ProductName": name,
            "ProductLine": line,
            "SubCategory": subcat,
            "UnitCost": cost,
            "UnitPrice": price,
            "MarginPercent": round((price - cost) / price * 100, 2)
        })
        p_key += 1

# -------------------------------------------------------------
# 3. DimCustomer: 1,200 Customers
# -------------------------------------------------------------
FIRST_NAMES = ["James", "Emma", "Liam", "Olivia", "Noah", "Sophia", "Lucas", "Mia", "Alexander", "Isabella", "William", "Harper", "Benjamin", "Evelyn", "Elijah", "Charlotte", "Oliver", "Amelia", "Daniel", "Emily", "Henry", "Abigail", "Sebastian", "Ella", "Jack", "Scarlett", "Mateo", "Grace", "Samuel", "Chloe"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"]
SEGMENTS = ["Retail VIP", "Regular", "Corporate", "Student"]
SEGMENT_WEIGHTS = [0.15, 0.55, 0.18, 0.12]

CUSTOMERS = []
for c_key in range(1, 1201):
    c_id = f"CUST-{c_key:05d}"
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    seg = random.choices(SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
    store = random.choice(STORES)
    CUSTOMERS.append({
        "CustomerKey": c_key,
        "CustomerID": c_id,
        "CustomerName": f"{first} {last}",
        "CustomerEmail": f"{first.lower()}.{last.lower()}{c_key}@example.com",
        "Segment": seg,
        "City": store["City"],
        "State": store["State"],
        "SignupDate": (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 500))).strftime("%Y-%m-%d"),
        "PreferredStoreKey": store["StoreKey"]
    })

# -------------------------------------------------------------
# 4. DimDate: 366 Days (July 1, 2023 - June 30, 2024)
# -------------------------------------------------------------
START_DATE = datetime(2023, 7, 1)
END_DATE = datetime(2024, 6, 30)

DATES = []
curr = START_DATE
while curr <= END_DATE:
    d_key = int(curr.strftime("%Y%m%d"))
    day_of_week = curr.weekday() + 1 # 1=Mon, 7=Sun
    is_weekend = 1 if day_of_week in [6, 7] else 0
    month = curr.month
    year = curr.year
    quarter = (month - 1) // 3 + 1
    
    # Seasonality identification
    if month in [12, 1, 2]:
        season = "Winter"
    elif month in [3, 4, 5]:
        season = "Spring"
    elif month in [6, 7, 8]:
        season = "Summer"
    else:
        season = "Fall"
        
    # Holiday surge flag
    is_holiday_season = 0
    if (month == 11 and curr.day >= 20) or (month == 12 and curr.day <= 26):
        is_holiday_season = 1
    elif (month == 7 and curr.day in [1, 2, 3, 4]): # 4th July
        is_holiday_season = 1
    elif (month == 5 and curr.day >= 24 and curr.day <= 30): # Memorial Day
        is_holiday_season = 1
        
    DATES.append({
        "DateKey": d_key,
        "FullDate": curr.strftime("%Y-%m-%d"),
        "DayOfWeek": day_of_week,
        "DayName": curr.strftime("%A"),
        "DayOfMonth": curr.day,
        "MonthNumber": month,
        "MonthName": curr.strftime("%B"),
        "YearMonth": curr.strftime("%Y-%m"),
        "Quarter": f"Q{quarter}",
        "Year": year,
        "IsWeekend": is_weekend,
        "Season": season,
        "IsHolidaySeason": is_holiday_season
    })
    curr += timedelta(days=1)

# -------------------------------------------------------------
# 5. DimPromotion: 6 campaigns
# -------------------------------------------------------------
PROMOTIONS = [
    {"PromotionKey": 1, "PromotionName": "No Promotion", "DiscountPct": 0.00, "StartDate": "2023-07-01", "EndDate": "2024-06-30"},
    {"PromotionKey": 2, "PromotionName": "Summer Splash Deals", "DiscountPct": 0.10, "StartDate": "2023-07-01", "EndDate": "2023-07-31"},
    {"PromotionKey": 3, "PromotionName": "Back to Campus Sprint", "DiscountPct": 0.15, "StartDate": "2023-08-15", "EndDate": "2023-09-10"},
    {"PromotionKey": 4, "PromotionName": "Black Friday Mega Savings", "DiscountPct": 0.25, "StartDate": "2023-11-20", "EndDate": "2023-11-30"},
    {"PromotionKey": 5, "PromotionName": "Winter Holiday Warmup", "DiscountPct": 0.15, "StartDate": "2023-12-10", "EndDate": "2023-12-25"},
    {"PromotionKey": 6, "PromotionName": "Spring Refresh Sale", "DiscountPct": 0.10, "StartDate": "2024-04-01", "EndDate": "2024-04-20"},
]

# -------------------------------------------------------------
# 6. FactSales Generation
# -------------------------------------------------------------
SALES = []
sales_key = 1
payment_methods = ["Credit Card", "Apple Pay / Digital Wallet", "Debit Card", "Store Credit / Gift Card"]
pm_weights = [0.55, 0.25, 0.15, 0.05]

print(f"Generating realistic retail sales transactions across {len(DATES)} days...")

for date_row in DATES:
    d_key = date_row["DateKey"]
    is_weekend = date_row["IsWeekend"]
    is_holiday = date_row["IsHolidaySeason"]
    full_date = date_row["FullDate"]
    month_num = date_row["MonthNumber"]
    
    # Active promotion
    active_promo = PROMOTIONS[0] # Default none
    for p in PROMOTIONS[1:]:
        if p["StartDate"] <= full_date <= p["EndDate"]:
            active_promo = p
            break
            
    # Base daily traffic: weekend lift (1.35x), holiday lift (1.75x)
    base_factor = 1.0
    if is_weekend:
        base_factor *= 1.35
    if is_holiday:
        base_factor *= 1.75
        
    for store in STORES:
        store_key = store["StoreKey"]
        t_mult = store["TrafficMultiplier"]
        
        # Transaction count per day per store
        num_transactions = int(random.uniform(16, 25) * base_factor * t_mult)
        
        for _ in range(num_transactions):
            cust = random.choice(CUSTOMERS)
            
            line_affinity = {
                "Electronics & Gadgets": 1.4 if (is_holiday or month_num in [11, 12, 1]) else 1.0,
                "Apparel & Accessories": 1.3 if (month_num in [8, 9, 11, 12, 4]) else 1.0,
                "Home & Kitchen": 1.4 if (month_num in [10, 11, 12, 5]) else 0.95,
                "Beauty & Personal Care": 1.2 if (month_num in [2, 5, 12]) else 1.0,
                "Sports & Outdoors": 1.5 if (month_num in [5, 6, 7, 8, 1]) else 0.85,
            }
            
            prod = random.choice(PRODUCTS)
            if random.random() > (line_affinity[prod["ProductLine"]] / 1.5):
                prod = random.choice(PRODUCTS)
                
            qty = random.choices([1, 2, 3, 4, 5], weights=[0.68, 0.20, 0.08, 0.03, 0.01])[0]
            
            unit_price = prod["UnitPrice"]
            unit_cost = prod["UnitCost"]
            
            discount_pct = active_promo["DiscountPct"]
            if cust["Segment"] == "Retail VIP":
                discount_pct = min(0.35, discount_pct + 0.05)
            elif cust["Segment"] == "Student" and active_promo["PromotionKey"] == 3:
                discount_pct = min(0.35, discount_pct + 0.10)
                
            gross_amount = round(qty * unit_price, 2)
            discount_amount = round(gross_amount * discount_pct, 2)
            sales_amount = round(gross_amount - discount_amount, 2)
            total_cost = round(qty * unit_cost, 2)
            gross_profit = round(sales_amount - total_cost, 2)
            
            return_flag = 1 if random.random() < 0.035 else 0
            payment = random.choices(payment_methods, weights=pm_weights)[0]
            
            SALES.append({
                "SalesKey": sales_key,
                "DateKey": d_key,
                "StoreKey": store_key,
                "ProductKey": prod["ProductKey"],
                "CustomerKey": cust["CustomerKey"],
                "PromotionKey": active_promo["PromotionKey"],
                "Quantity": qty,
                "UnitPrice": unit_price,
                "UnitCost": unit_cost,
                "DiscountAmount": discount_amount,
                "SalesAmount": sales_amount,
                "TotalCost": total_cost,
                "GrossProfit": gross_profit,
                "ReturnFlag": return_flag,
                "PaymentMethod": payment
            })
            sales_key += 1

print(f"Generated {len(SALES):,} sales records across 12 months.")

def write_csv(filepath, fieldnames, data):
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Written: {filepath} ({len(data):,} rows)")

write_csv(os.path.join(DATA_DIR, "dim_store.csv"), STORES[0].keys(), STORES)
write_csv(os.path.join(DATA_DIR, "dim_product.csv"), PRODUCTS[0].keys(), PRODUCTS)
write_csv(os.path.join(DATA_DIR, "dim_customer.csv"), CUSTOMERS[0].keys(), CUSTOMERS)
write_csv(os.path.join(DATA_DIR, "dim_date.csv"), DATES[0].keys(), DATES)
write_csv(os.path.join(DATA_DIR, "dim_promotion.csv"), PROMOTIONS[0].keys(), PROMOTIONS)
write_csv(os.path.join(DATA_DIR, "fact_sales.csv"), SALES[0].keys(), SALES)

# SQL Seed Script
sql_seed_path = os.path.join(SQL_DIR, "02_seed_data.sql")
with open(sql_seed_path, "w", encoding="utf-8") as f:
    f.write("""-- =============================================================
-- SalesSlice Retail Analytics - Seed Data Script
-- Populates Dimension tables and FactSales sample records
-- =============================================================
USE SalesSliceDW;
GO

SET NOCOUNT ON;
PRINT 'Beginning seed data insertion into SalesSliceDW...';

-- -------------------------------------------------------------
-- 1. Populate DimPromotion
-- -------------------------------------------------------------
PRINT 'Populating DimPromotion...';
SET IDENTITY_INSERT dbo.DimPromotion ON;
""")
    for p in PROMOTIONS:
        f.write(f"INSERT INTO dbo.DimPromotion (PromotionKey, PromotionName, DiscountPct, StartDate, EndDate) "
                f"VALUES ({p['PromotionKey']}, '{p['PromotionName']}', {p['DiscountPct']}, '{p['StartDate']}', '{p['EndDate']}');\n")
    f.write("SET IDENTITY_INSERT dbo.DimPromotion OFF;\nGO\n\n")

    f.write("""-- -------------------------------------------------------------
-- 2. Populate DimStore (8 Store Locations)
-- -------------------------------------------------------------
PRINT 'Populating DimStore...';
SET IDENTITY_INSERT dbo.DimStore ON;
""")
    for s in STORES:
        f.write(f"INSERT INTO dbo.DimStore (StoreKey, StoreID, StoreName, City, State, Region, StoreType, SquareFootage, ManagerName, MonthlySalesTarget) "
                f"VALUES ({s['StoreKey']}, '{s['StoreID']}', '{s['StoreName']}', '{s['City']}', '{s['State']}', '{s['Region']}', '{s['StoreType']}', {s['SquareFootage']}, '{s['ManagerName']}', {s['MonthlySalesTarget']});\n")
    f.write("SET IDENTITY_INSERT dbo.DimStore OFF;\nGO\n\n")

    f.write("""-- -------------------------------------------------------------
-- 3. Populate DimProduct (5 Product Lines, 40 Products)
-- -------------------------------------------------------------
PRINT 'Populating DimProduct...';
SET IDENTITY_INSERT dbo.DimProduct ON;
""")
    for prd in PRODUCTS:
        name_esc = prd['ProductName'].replace("'", "''")
        f.write(f"INSERT INTO dbo.DimProduct (ProductKey, ProductID, ProductName, ProductLine, SubCategory, UnitCost, UnitPrice, MarginPercent) "
                f"VALUES ({prd['ProductKey']}, '{prd['ProductID']}', '{name_esc}', '{prd['ProductLine']}', '{prd['SubCategory']}', {prd['UnitCost']}, {prd['UnitPrice']}, {prd['MarginPercent']});\n")
    f.write("SET IDENTITY_INSERT dbo.DimProduct OFF;\nGO\n\n")

    f.write("""-- -------------------------------------------------------------
-- 4. Populate DimDate (366 Days: 2023-07-01 to 2024-06-30)
-- -------------------------------------------------------------
PRINT 'Populating DimDate...';
""")
    for d in DATES:
        f.write(f"INSERT INTO dbo.DimDate (DateKey, FullDate, DayOfWeek, DayName, DayOfMonth, MonthNumber, MonthName, YearMonth, Quarter, [Year], IsWeekend, Season, IsHolidaySeason) "
                f"VALUES ({d['DateKey']}, '{d['FullDate']}', {d['DayOfWeek']}, '{d['DayName']}', {d['DayOfMonth']}, {d['MonthNumber']}, '{d['MonthName']}', '{d['YearMonth']}', '{d['Quarter']}', {d['Year']}, {d['IsWeekend']}, '{d['Season']}', {d['IsHolidaySeason']});\n")
    f.write("GO\n\n")

    f.write("""-- -------------------------------------------------------------
-- 5. Populate DimCustomer (Representative initial sample)
-- (For full 1,200 records, import data/dim_customer.csv)
-- -------------------------------------------------------------
PRINT 'Populating DimCustomer...';
SET IDENTITY_INSERT dbo.DimCustomer ON;
""")
    for c in CUSTOMERS[:150]:
        cname_esc = c['CustomerName'].replace("'", "''")
        f.write(f"INSERT INTO dbo.DimCustomer (CustomerKey, CustomerID, CustomerName, CustomerEmail, Segment, City, State, SignupDate, PreferredStoreKey) "
                f"VALUES ({c['CustomerKey']}, '{c['CustomerID']}', '{cname_esc}', '{c['CustomerEmail']}', '{c['Segment']}', '{c['City']}', '{c['State']}', '{c['SignupDate']}', {c['PreferredStoreKey']});\n")
    f.write("SET IDENTITY_INSERT dbo.DimCustomer OFF;\nGO\n\n")

    f.write(f"""-- -------------------------------------------------------------
-- 6. Populate FactSales
-- To load all {len(SALES):,} records into SSMS, run BULK INSERT:
-- BULK INSERT dbo.FactSales
-- FROM 'C:\\SalesSlice\\data\\fact_sales.csv'
-- WITH (FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR = '\\n', TABLOCK);
-- -------------------------------------------------------------
PRINT 'Seeding initial representative batch of FactSales...';
SET IDENTITY_INSERT dbo.FactSales ON;
""")
    for s in SALES[:250]:
        f.write(f"INSERT INTO dbo.FactSales (SalesKey, DateKey, StoreKey, ProductKey, CustomerKey, PromotionKey, Quantity, UnitPrice, UnitCost, DiscountAmount, SalesAmount, TotalCost, GrossProfit, ReturnFlag, PaymentMethod) "
                f"VALUES ({s['SalesKey']}, {s['DateKey']}, {s['StoreKey']}, {s['ProductKey']}, {s['CustomerKey']}, {s['PromotionKey']}, {s['Quantity']}, {s['UnitPrice']}, {s['UnitCost']}, {s['DiscountAmount']}, {s['SalesAmount']}, {s['TotalCost']}, {s['GrossProfit']}, {s['ReturnFlag']}, '{s['PaymentMethod']}');\n")
    f.write("""SET IDENTITY_INSERT dbo.FactSales OFF;
GO

PRINT 'Seed data population completed successfully.';
""")

print(f"Written: {sql_seed_path}")

total_rev = sum(s["SalesAmount"] for s in SALES if s["ReturnFlag"] == 0)
total_profit = sum(s["GrossProfit"] for s in SALES if s["ReturnFlag"] == 0)
total_orders = len(SALES)
total_units = sum(s["Quantity"] for s in SALES if s["ReturnFlag"] == 0)
overall_margin = (total_profit / total_rev) * 100

print("\n--- DATASET SUMMARY METRICS ---")
print(f"Total Sales Revenue:  ${total_rev:,.2f}")
print(f"Total Gross Profit:   ${total_profit:,.2f}")
print(f"Overall Gross Margin: {overall_margin:.2f}%")
print(f"Total Transactions:   {total_orders:,}")
print(f"Total Units Sold:     {total_units:,}")
print(f"Average Order Value:  ${total_rev / total_orders:.2f}")
print("-------------------------------\n")
