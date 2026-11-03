# SalesSlice: KPI & Metrics Business Catalog

This catalog outlines the formal definitions, mathematical formulas, business rationales, and target benchmarks for metrics implemented within the **SalesSlice** analytics platform.

---

## 1. Top-Line Financial & Profitability Metrics

### 1.1 Total Net Sales Revenue
- **Business Definition**: Total gross realized revenue from retail POS checkouts minus promotional discounts and returns.
- **Mathematical Formula**:
  $$\text{Net Sales} = \sum (\text{Quantity} \times \text{UnitPrice}) - \sum \text{DiscountAmount} \quad [\text{where ReturnFlag} = 0]$$
- **Power BI DAX**: `[Total Sales]`
- **Reporting Frequency**: Real-time / Daily
- **Stakeholders**: Chief Commercial Officer, VP of Retail Operations, Regional Directors

### 1.2 Gross Profit & Gross Margin %
- **Business Definition**: Dollar profit remaining after subtracting total Cost of Goods Sold (COGS) from net sales, and the percentage margin realized.
- **Mathematical Formula**:
  $$\text{Gross Profit} = \text{Net Sales} - \text{Total Cost of Goods Sold}$$
  $$\text{Gross Margin \%} = \frac{\text{Gross Profit}}{\text{Net Sales}} \times 100$$
- **Benchmark Target**: $\ge 58.0\%$ across blended retail product mix.
- **Actual Achieved**: $60.91\%$ ($6.10M gross profit on $10.02M revenue).
- **Stakeholders**: Finance Team, Merchandising Leads

### 1.3 Average Order Value (AOV)
- **Business Definition**: Mean dollar expenditure per retail checkout transaction.
- **Mathematical Formula**:
  $$\text{AOV} = \frac{\text{Total Net Sales}}{\text{Total Completed Transactions}}$$
- **Baseline / Target**: $\$125.00$
- **Actual Achieved**: $\$130.01$ across 77,033 completed orders.

---

## 2. Time Intelligence & Growth Metrics

### 2.1 Month-over-Month (MoM) Sales Growth %
- **Business Definition**: Percentage acceleration or deceleration in sales relative to the immediate preceding month.
- **Mathematical Formula**:
  $$\text{MoM Growth \%} = \frac{\text{Sales}_{t} - \text{Sales}_{t-1}}{\text{Sales}_{t-1}} \times 100$$
- **T-SQL Implementation**: `LAG(MonthlyRevenue, 1) OVER (PARTITION BY StoreKey ORDER BY MonthStartDate)`
- **Power BI DAX**: `[MoM Sales Growth %]`

### 2.2 Year-over-Year (YoY) Sales Growth %
- **Business Definition**: Revenue pace compared to the identical calendar interval in the preceding fiscal cycle.
- **Mathematical Formula**:
  $$\text{YoY Growth \%} = \frac{\text{Sales}_{\text{Current}} - \text{Sales}_{\text{Prior Year}}}{\text{Sales}_{\text{Prior Year}}} \times 100$$
- **Target Benchmark**: $+10.0\%$ to $+15.0\%$ annual retail growth.

### 2.3 3-Month Trailing Moving Average
- **Business Definition**: Smoothing metric calculating the unweighted average sales over a rolling 90-day window to isolate underlying momentum from seasonal spikes (e.g. Black Friday or post-holiday lulls).

---

## 3. Commercial Spatial Efficiency & Quota Attainment

### 3.1 Sales per Square Foot
- **Business Definition**: Prime commercial metric measuring dollar revenue generated per unit of physical store floor space.
- **Mathematical Formula**:
  $$\text{Sales per Sq Ft} = \frac{\text{Store Annual Sales}}{\text{Store Square Footage}}$$
- **Top Store Performer**: **Lincoln Road Center** ($\$112$ / sq ft) and **Manhattan Flagship** ($\$90$ / sq ft).
- **Stakeholders**: Real Estate Strategy, Store Layout Architects

### 3.2 Monthly Sales Target Attainment %
- **Business Definition**: Cumulative actual store revenue expressed as a percentage of the assigned corporate quota.
- **Mathematical Formula**:
  $$\text{Target Attainment \%} = \frac{\text{Realized Store Sales}}{\text{Assigned Budget Target}} \times 100$$
- **Thresholds**:
  - Exceeding: $\ge 105\%$
  - On Track: $95\% - 104\%$
  - Action Required: $< 95\%$

---

## 4. Product Portfolio & Category Economics

### 4.1 Category Contribution Share %
- **Business Definition**: Percentage share of aggregate business volume captured by each of the 5 product lines:
  1. **Electronics & Gadgets**: 24.8% ($2.49M)
  2. **Sports & Outdoors**: 21.2% ($2.12M)
  3. **Home & Kitchen**: 21.0% ($2.11M)
  4. **Apparel & Accessories**: 20.6% ($2.06M)
  5. **Beauty & Personal Care**: 12.4% ($1.24M)

### 4.2 Margin Erosion Rate
- **Business Definition**: Quantifies the percentage of potential gross sticker revenue sacrificed to promotional discounts and return write-offs:
  $$\text{Discount Concession \%} = \frac{\text{Total Discounts}}{\text{Gross Revenue}} \times 100 \approx 5.96\%$$
  $$\text{Return Rate \%} = \frac{\text{Refund Transactions}}{\text{Total Transactions}} \times 100 \approx 3.52\%$$
