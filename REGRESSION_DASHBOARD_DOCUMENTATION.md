# Regression Testing Dashboard - Complete Documentation

## ✅ Dashboard Created Successfully!

### Overview

Created a new **Regression Testing Dashboard** as a main tab in the Config Operations Hub, following the same architecture and design patterns as the ARC Configuration and Integration dashboards.

**Location**: Config Operations Hub → 🧪 Regression Testing tab

---

## Dashboard Structure

### Main Tabs

1. **📊 Data** (Fully Implemented)
   - Interactive KPI cards
   - Implementation type filters
   - Region drilldown
   - Data tables with export

2. **📈 Analytics** (Stub - To be built later)
   - Placeholder with planned features
   - Will include trend analysis, performance metrics, etc.

---

### Sub-tabs in Data Tab

**Month Filter** (at the top):
- **Current Month** (e.g., "October 2025") - Shows only records where Go-Live Date is this month and year
- **Next Month** (e.g., "November 2025") - Shows only records where Go-Live Date is next calendar month and correct year
- **YTD (Year to Date)** - All records in current year up to today

**Filter Logic**:
```python
# Current Month
mask = (df['Go Live Month'] == today.month) & (df['Go Live Year'] == today.year)

# Next Month (with year rollover)
next_date = today + pd.DateOffset(months=1)
mask = (df['Go Live Month'] == next_date.month) & (df['Go Live Year'] == next_date.year)

# YTD (up to current date)
mask = (df['Go Live Year'] == today.year) & (df['Go Live Date'] <= today)
```

---

## Data Source

**Source File**: E2E Testing Check.xlsx  
**Sheet**: "Stores Checklist" (only this sheet is used)

**Column Mappings**:
```python
{
    'Dealership Name': 'Dealership Name',
    'Go-Live Date': 'Go Live Date',
    'SIM Start Date': 'SIM Start Date',
    'Assignee': 'Assignee',
    'Region': 'Region',
    'Testing Status': 'Status',
    'Type of Implementation': 'Type of Implementation'
}
```

---

## KPI Cards

### 1. Total Go Live
- **Definition**: Cumulative count of all rows in filtered data
- **Color**: Blue (kpi-accent)
- **Logic**: `len(df)`

### 2. Completed
- **Definition**: Testing Status = "Completed"
- **Color**: Green (kpi-success)
- **Logic**: `len(df[df['Status'] == 'Completed'])`

### 3. WIP
- **Definition**: Testing Status = "WIP"
- **Color**: Orange (kpi-warning)
- **Logic**: `len(df[df['Status'] == 'WIP'])`

### 4. Unable to Complete
- **Definition**: Testing Status = "Unable to Complete"
- **Color**: Red (kpi-error)
- **Logic**: `len(df[df['Status'] == 'Unable to Complete'])`

### 5. Upcoming Next Week
- **Definition**: SIM Start Date is within the next 7 days from today (always real time)
- **Color**: Teal (kpi-info)
- **Logic**: 
  ```python
  today = pd.Timestamp.now().normalize()
  next_week = today + pd.Timedelta(days=7)
  count = len(df[(df['SIM Start Date'] >= today) & (df['SIM Start Date'] <= next_week)])
  ```
- **Note**: Uses full dataset (not filtered by month), always real-time

### 6. Data Incomplete
- **Definition**: SIM Start Date before today but Status is blank
- **Color**: Grey (kpi-grey)
- **Logic**:
  ```python
  today = pd.Timestamp.now().normalize()
  count = len(df[(df['SIM Start Date'] < today) & (df['Status'].isna() | (df['Status'] == ''))])
  ```
- **Note**: Uses full dataset (not filtered by month)

---

## Implementation Type Filter

**Location**: Below KPI cards

**Options**:
- Conquest
- Buy/Sell
- Enterprise
- New Point
- All (no filter)

**UI**: Pill-style buttons (same as region buttons)

**Logic**:
```python
if impl_type == 'All':
    filtered_df = df.copy()
else:
    filtered_df = df[df['Type of Implementation'] == impl_type]
```

**Behavior**:
- Clicking a type filters all downstream data
- Resets region selection
- Updates region counts

---

## Region Drilldown

**Location**: Below Implementation Type filter

**Options**:
- All Regions (shows combined count)
- Individual regions (dynamically generated from data)

**UI**: Pill-style buttons with counts (e.g., "NAM (5)")

**Logic**:
```python
# Get unique regions
regions = df['Region'].dropna().unique().tolist()

# Count by region for selected KPI
for region in regions:
    region_df = df[df['Region'] == region]
    if kpi_name == 'Total Go Live':
        count = len(region_df)
    else:
        count = len(region_df[region_df['Status'] == kpi_name])
```

**Behavior**:
- Only shows regions with data > 0
- Clicking a region shows the data table
- "All Regions" shows combined data

---

## Data Table

**Display Condition**: Only shows when all three selections are made:
1. KPI selected
2. Implementation Type selected (default: "All")
3. Region selected

**Columns**:
1. Dealership Name
2. Go-Live Date (formatted as DD-MMM-YYYY)
3. SIM Start Date (formatted as DD-MMM-YYYY)
4. Assignee
5. Region
6. Status (Testing Status from Excel)

**Features**:
- Full-width display
- No index column
- CSV export button
- Formatted dates

---

## User Flow

### Step 1: Select Month
User selects "October 2025", "November 2025", or "YTD"

### Step 2: View KPIs
Dashboard shows 6 KPI cards with counts based on selected month

### Step 3: Select KPI
User clicks a KPI card (e.g., "Completed")

### Step 4: Select Implementation Type
User clicks a type (e.g., "Conquest") or keeps "All"

### Step 5: View Regions
Dashboard shows region buttons with counts for selected KPI + Type

### Step 6: Select Region
User clicks a region (e.g., "NAM")

### Step 7: View Table
Dashboard shows data table with filtered records

### Step 8: Export (Optional)
User clicks "Download CSV" to export data

---

## File Structure

```
regression_dashboard/
├── __init__.py
├── app.py                          # Main application
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration constants
├── data/
│   ├── __init__.py
│   └── mock_data.py                # Mock data generator
├── utils/
│   ├── __init__.py
│   └── data_processor.py           # Data processing logic
└── components/
    └── __init__.py
```

---

## Key Features

### ✅ Modern Dark Theme
- Consistent with ARC/Integration dashboards
- Teal background (#18191A)
- White text (#F5F5F7)
- Vibrant accent colors

### ✅ Interactive Drilldown
- Click KPI → Select Type → Select Region → View Table
- Same pattern as other dashboards
- Smooth user experience

### ✅ Real-Time Calculations
- "Upcoming Next Week" always shows next 7 days from today
- "Data Incomplete" always checks against current date
- Updates automatically each day

### ✅ Exact Month Filtering
- Current Month: Exact month and year match
- Next Month: Handles year rollover (Dec → Jan)
- YTD: All records in current year up to today

### ✅ Dynamic Filters
- Regions generated from data
- Implementation types from data
- Only shows options with data > 0

### ✅ Export Capability
- Download filtered data as CSV
- Filename includes date
- All columns included

---

## Code Highlights

### Data Processor

**File**: `regression_dashboard/utils/data_processor.py`

**Key Methods**:
- `filter_by_date_range()` - Exact calendar month filtering
- `get_kpis()` - Calculate all 6 KPIs
- `filter_by_implementation_type()` - Filter by type
- `get_region_counts()` - Count by region for KPI
- `filter_by_region()` - Filter by region
- `get_display_dataframe()` - Format for display

### Mock Data Generator

**File**: `regression_dashboard/data/mock_data.py`

**Features**:
- Generates 50 rows by default
- Realistic data distribution
- Dates spread across past/current/future months
- Status based on SIM Start Date logic
- Multiple regions, types, assignees

### Main App

**File**: `regression_dashboard/app.py`

**Components**:
- `render_kpi_cards()` - KPI card display
- `render_implementation_type_pills()` - Type filter pills
- `render_region_buttons()` - Region buttons
- `render_data_table()` - Data table with export
- `render_data_tab()` - Main data tab logic
- `render_analytics_tab()` - Analytics stub

---

## Integration with Config Operations Hub

**File**: `config_operations_hub.py`

**Changes**:
```python
# Added import
import regression_dashboard.app as regression_app

# Updated tab4
with tab4:
    # Render Regression Testing dashboard
    regression_app.render_regression_dashboard()
```

**Result**: Regression Testing dashboard now appears as 4th tab in main hub

---

## Testing Checklist

- [x] Dashboard appears in Config Operations Hub
- [x] Month filter works (Current, Next, YTD)
- [x] 6 KPI cards display correctly
- [x] KPI cards are clickable
- [x] Implementation type pills work
- [x] Region buttons appear with counts
- [x] Table shows when all selections made
- [x] Table columns are correct
- [x] Dates formatted as DD-MMM-YYYY
- [x] CSV export works
- [x] "Upcoming Next Week" is real-time
- [x] "Data Incomplete" logic correct
- [x] Year rollover handled (Dec → Jan)
- [x] Dark theme applied
- [x] Selection highlighting works

---

## Examples

### Example 1: View Completed Tests in October 2025 for Conquest in NAM

1. Select "October 2025"
2. Click "Completed" KPI
3. Click "Conquest" type
4. Click "NAM" region
5. View table with completed Conquest tests in NAM for October 2025

### Example 2: View Upcoming Next Week Tests

1. Select any month (doesn't affect this KPI)
2. Click "Upcoming Next Week" KPI
3. Click "All" type (or specific type)
4. Click "All Regions" (or specific region)
5. View table with tests starting in next 7 days

### Example 3: Export WIP Tests for Buy/Sell

1. Select "Current Month"
2. Click "WIP" KPI
3. Click "Buy/Sell" type
4. Click "All Regions"
5. Click "Download CSV" to export

---

## Future Enhancements (Analytics Tab)

**Planned Features**:
- Trend analysis (completion rate over time)
- Performance metrics (average time to complete)
- Regional comparisons (completion rate by region)
- Status distribution charts (pie/bar charts)
- Implementation type analysis
- Assignee performance metrics

---

## 🚀 Dashboard Status

**URL**: http://localhost:8502  
**Tab**: 🧪 Regression Testing  
**Status**: ✅ Fully Functional  

**Working Features**:
- ✅ Month filter (Current, Next, YTD)
- ✅ 6 KPI cards with correct logic
- ✅ Implementation type filter (5 options)
- ✅ Region drilldown (dynamic)
- ✅ Data table (6 columns)
- ✅ CSV export
- ✅ Real-time calculations
- ✅ Dark theme
- ✅ Interactive drilldown

**Stub Features** (to be built):
- ⏳ Analytics tab

---

**Last Updated**: 2025-10-06  
**Status**: ✅ Complete  
**Ready for Use**: ✅ Yes  
**Mock Data**: ✅ Working  
**SharePoint Integration**: ⏳ To be implemented

