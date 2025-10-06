# Integration Dashboard - Complete Documentation

## ✅ Overview

The Integration Dashboard is a comprehensive LOB (Line of Business) dashboard integrated into the Config Operations Hub. It provides real-time visibility into integration go-lives, vendor list updates, and implementation tracking.

---

## 🎯 Business Requirements

### Main Tabs
1. **Data** - Interactive data exploration with KPIs and regional drilldown
2. **Analytics** - Placeholder for future analytics features

### Sub-tabs (Date Filters)
Based on Go Live month logic:
- **Current Month** - Go-lives in the current calendar month
- **Next Month** - Go-lives in the next calendar month
- **2 Months From Now** - Go-lives two months ahead
- **YTD (Year to Date)** - All go-lives from January 1st to latest data

---

## 📊 KPI Definitions

### 1. Total Go Lives
- **Definition**: Cumulative count of all go-lives in the selected period
- **Color**: Blue (Accent)
- **Calculation**: Count of all records

### 2. GTG (Good to Go)
- **Definition**: Vendor List Updated = 'Yes'
- **Color**: Green (Success)
- **Calculation**: Count where `Vendor List Updated = 'Yes'`

### 3. On Track
- **Definition**: Vendor List Updated = 'No' and within safe timeframe
- **Color**: Blue (Accent)
- **Calculation**:
  - **Conquest**: Days to Go Live > 60
  - **Buy/Sell or New Point**: Days to Go Live > 15

### 4. Critical
- **Definition**: Vendor List Updated = 'No' and approaching deadline
- **Color**: Orange (Warning)
- **Calculation**:
  - **Conquest**: Days to Go Live between 30 and 60 (inclusive)
  - **Buy/Sell or New Point**: Days to Go Live between 3 and 15 (inclusive)

### 5. Escalated
- **Definition**: Vendor List Updated = 'No' and past safe deadline
- **Color**: Red (Error)
- **Calculation**:
  - **Conquest**: Days to Go Live < 30
  - **Buy/Sell or New Point**: Days to Go Live < 3

### 6. Data Incomplete
- **Definition**: Missing key data fields required for go-live
- **Color**: Grey
- **Calculation**: Any of these fields are blank:
  - Dealer Name
  - Dealer ID
  - Go Live Date
  - Implementation Type
  - PEM
  - Director
  - Assignee

---

## 🎨 Status Logic Flow

```
For each go-live record:

1. Check Data Incomplete
   └─ If any required field is blank → Data Incomplete

2. Check GTG
   └─ If Vendor List Updated = 'Yes' → GTG

3. Check if Vendor List Updated = 'No'
   └─ If not 'No' → Data Incomplete

4. Get Implementation Type and Days to Go Live
   └─ If Implementation Type is blank → Data Incomplete

5. Apply threshold logic based on Implementation Type:
   
   Conquest:
   - Days < 30 → Escalated
   - Days 30-60 → Critical
   - Days > 60 → On Track
   
   Buy/Sell or New Point:
   - Days < 3 → Escalated
   - Days 3-15 → Critical
   - Days > 15 → On Track
```

---

## 🔄 Interactive Flow

### User Journey
1. **Select Time Period** → Choose from Current Month, Next Month, 2 Months, or YTD
2. **View KPI Cards** → See counts for all statuses
3. **Click KPI Card** → View regional breakdown for that status
4. **Click Region** → View detailed data table
5. **Download Data** → Export filtered data as CSV

### Session State Management
- `integration_date_filter` - Currently selected time period
- `integration_selected_kpi` - Currently selected KPI
- `integration_selected_region` - Currently selected region

### Reset Logic
- Changing date filter → Resets KPI and region selection
- Clicking new KPI → Resets region selection
- Clicking region → Shows filtered table

---

## 📁 File Structure

```
integration_dashboard/
├── __init__.py
├── app.py                          # Main application
├── components/
│   ├── __init__.py
│   └── data_table.py              # Data table component
├── config/
│   ├── __init__.py
│   └── settings.py                # Configuration settings
├── data/
│   ├── __init__.py
│   └── mock_data.py               # Mock data generator
└── utils/
    ├── __init__.py
    └── data_processor.py          # Data processing logic
```

---

## 🔧 Key Components

### 1. Data Processor (`data_processor.py`)
**Class**: `IntegrationDataProcessor`

**Methods**:
- `_prepare_data()` - Clean and prepare data
- `_calculate_status()` - Calculate status based on business rules
- `_is_data_incomplete()` - Check for missing required fields
- `filter_by_date_range()` - Filter by time period
- `get_kpis()` - Calculate KPI counts
- `get_regions()` - Get unique regions
- `get_region_counts()` - Get counts by region for a status
- `filter_by_region()` - Filter by region
- `get_display_dataframe()` - Format data for display

### 2. Data Table (`data_table.py`)
**Functions**:
- `render_data_table()` - Render table with color-coded status
- `render_status_breakdown()` - Show status summary

### 3. Mock Data (`mock_data.py`)
**Functions**:
- `generate_mock_integration_data()` - Generate test data
- `load_integration_data()` - Load from mock or SharePoint

### 4. Settings (`settings.py`)
**Constants**:
- `DATE_FILTERS` - Time period options
- `KPI_DEFINITIONS` - KPI descriptions
- `THRESHOLDS` - Days to Go Live thresholds
- `STATUS_COLORS` - Color mapping
- `REQUIRED_FIELDS` - Required data fields

---

## 📊 Data Table Columns

### Display Columns
1. **Dealership Name** - Format: "Dealer Name - Dealer ID"
2. **Go Live Date** - Format: DD-MMM-YYYY (e.g., 15-Jan-2025)
3. **Days to Go Live** - Calculated days; shows "Rolled Out" if negative
4. **Implementation Type** - Conquest, Buy/Sell, or New Point
5. **PEM** - Project Engagement Manager
6. **Director** - Director name
7. **Assignee** - Assigned to (person responsible)
8. **Status** - Color-coded status (GTG, On Track, Critical, Escalated, Data Incomplete)

---

## 🎨 Visual Design

### Black Theme
- Background: #18191A (Dark Black)
- Cards: #23272F (Charcoal)
- Text: #F5F5F7 (Off-White)

### KPI Card Colors
- Total Go Lives: Blue (#3874F2)
- GTG: Green (#29C46F)
- On Track: Blue (#3874F2)
- Critical: Orange (#FF9800)
- Escalated: Red (#F44336)
- Data Incomplete: Grey (#23272F)

### Interactive States
- Hover: Card lifts with enhanced shadow
- Selected: Gold border (#FFD700) with glow
- Region buttons: Dark charcoal, blue when selected

---

## 🔄 Data Flow

```
1. Load Data
   └─ load_integration_data()
   └─ IntegrationDataProcessor()

2. Prepare Data
   └─ Convert dates
   └─ Calculate Days to Go Live
   └─ Create Dealership Name
   └─ Calculate Status
   └─ Check Data Incomplete

3. Filter by Date
   └─ filter_by_date_range()
   └─ Current Month / Next Month / 2 Months / YTD

4. Calculate KPIs
   └─ get_kpis()
   └─ Count by status

5. User Interaction
   └─ Click KPI → Show regions
   └─ Click Region → Show table

6. Display Table
   └─ get_display_dataframe()
   └─ Format dates and values
   └─ Color-code status
```

---

## 📝 Business Rules

### Implementation Type Thresholds

**Conquest**:
- On Track: > 60 days
- Critical: 30-60 days
- Escalated: < 30 days

**Buy/Sell**:
- On Track: > 15 days
- Critical: 3-15 days
- Escalated: < 3 days

**New Point**:
- On Track: > 15 days
- Critical: 3-15 days
- Escalated: < 3 days

### Status Priority
1. Data Incomplete (highest priority)
2. GTG
3. Escalated
4. Critical
5. On Track

### Date Calculations
- **Days to Go Live** = Go Live Date - Today
- **Rolled Out** = Days to Go Live < 0
- **Current Month** = Same month and year as today
- **Next Month** = Month after current month
- **2 Months** = Two months from current month
- **YTD** = January 1st to latest data

---

## 🚀 Usage Examples

### Example 1: View Current Month GTG
1. Dashboard loads with "Current Month" selected
2. Click "GTG" KPI card
3. See regional breakdown (NAM: 5, EMEA: 3, etc.)
4. Click "NAM" region
5. View table of all GTG go-lives in NAM for current month
6. Download CSV if needed

### Example 2: Check Escalated Items
1. Select "Next Month" time period
2. Click "Escalated" KPI card
3. See which regions have escalated items
4. Click region with highest count
5. Review escalated go-lives
6. Identify PEM/Director for follow-up

### Example 3: YTD Analysis
1. Select "YTD (Year to Date)"
2. Click "Total Go Lives"
3. See all regions
4. Click each region to review
5. Download data for reporting

---

## 🔧 Configuration

### Mock Data Settings
```python
# In integration_dashboard/config/settings.py
USE_MOCK_DATA = True  # Set to False for SharePoint
```

### SharePoint Connection (Future)
```python
SHAREPOINT_SITE_URL = "https://your-site.sharepoint.com"
SHAREPOINT_LIST_NAME = "Integration Access Board"
```

### Threshold Customization
```python
# In integration_dashboard/config/settings.py
THRESHOLDS = {
    'Conquest': {
        'on_track': 60,
        'critical_min': 30,
        'critical_max': 60,
        'escalated': 30
    },
    # ... customize as needed
}
```

---

## 📊 Sample Data

The mock data generator creates 100 sample records with:
- 20 unique dealer names
- 4 regions (NAM, EMEA, APAC, LATAM)
- 3 implementation types
- Go-live dates from -60 to +120 days
- 10% data incomplete rate
- 30% GTG, 60% No, 10% blank vendor list

---

## ✅ Testing Checklist

- [ ] All KPI cards display correct counts
- [ ] Clicking KPI shows region breakdown
- [ ] Region counts match filtered data
- [ ] Clicking region shows correct table
- [ ] Table displays all required columns
- [ ] Status colors are correct
- [ ] Days to Go Live shows "Rolled Out" for negatives
- [ ] Date format is DD-MMM-YYYY
- [ ] CSV download works
- [ ] All time periods filter correctly
- [ ] Session state resets properly
- [ ] Black theme applied consistently

---

## 🎯 Future Enhancements

### Short Term
1. Connect to SharePoint data source
2. Add refresh button
3. Add filters (PEM, Director, Implementation Type)
4. Add search functionality

### Long Term
1. Build Analytics tab with charts
2. Add trend analysis
3. Add email notifications for escalated items
4. Add bulk update functionality
5. Add export to Excel with formatting
6. Add user authentication

---

## 📞 Support

For questions or issues:
1. Check this documentation
2. Review code comments
3. Check debug output in terminal
4. Verify data format matches expected structure

---

**Status**: ✅ Complete and Ready to Use  
**Dashboard URL**: http://localhost:8502 → Integration Tab  
**Last Updated**: 2025-10-06

