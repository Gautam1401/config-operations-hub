# CRM Configuration Dashboard - Complete Documentation

## Overview

The CRM Configuration Dashboard is a comprehensive Line of Business (LOB) dashboard integrated into the Config Operations Hub. It provides real-time tracking and analytics for CRM configuration, pre-go-live checks, and go-live testing across all regions.

---

## Architecture

### File Structure

```
crm_dashboard/
├── __init__.py
├── app.py                          # Main application file
├── components/
│   ├── __init__.py
│   ├── kpi_cards.py               # KPI card components
│   └── data_table.py              # Data table components
├── config/
│   ├── __init__.py
│   └── settings.py                # Configuration and constants
├── data/
│   ├── __init__.py
│   └── mock_data.py               # Mock data generator
└── utils/
    ├── __init__.py
    └── data_processor.py          # Data processing logic
```

---

## Features

### 1. Main Tabs
- **Data Tab**: Interactive data exploration with KPIs, regions, and tables
- **Analytics Tab**: Placeholder for future analytics features

### 2. Sub-Tabs (Under Data Tab)
1. **Configuration**: Track configuration status (Standard, Copy, Not Configured)
2. **Pre Go Live Checks**: Monitor pre-go-live readiness (GTG, Partial, Fail)
3. **Go Live Testing**: Track testing completion and blockers

### 3. Date Filters
- **Current Month**: Shows data for current month only
- **Next Month**: Shows data for next month only
- **YTD (Year to Date)**: Shows cumulative data for current year

### 4. Interactive KPI Cards
Each sub-tab has specific KPIs:

**Configuration KPIs:**
- Go Lives (total)
- Standard
- Copy
- Not Configured
- Data Incorrect

**Pre Go Live KPIs:**
- Checks Completed
- GTG (Good to Go)
- Partial
- Fail
- Data Incorrect

**Go Live Testing KPIs:**
- Tests Completed
- GTG
- Go Live Blocker
- Non-Blocker
- Fail
- Data Incorrect

### 5. Regional Breakdown
- Click any KPI to see region-wise breakdown
- Regions: NAM, EMEA, APAC, LATAM
- Only regions with data are shown

### 6. Data Tables
- Displayed after selecting both KPI and region
- Columns:
  - Dealership Name (Dealer Name + Dealer ID)
  - Go Live Date (DD-MMM-YYYY format)
  - Days to Go Live (shows "Rolled Out" for negative values)
  - Implementation Type
  - Region
  - Assignee (context-specific)
  - Status (color-coded)
- CSV export functionality

### 7. Upcoming Week Alert
- Highlights go-lives scheduled in next 7 days
- Yellow banner with count

---

## Business Logic

### Configuration Status Logic

```python
def calculate_configuration_status(row):
    # Data Incorrect: Go Live Status = 'Rolled out' but Configuration Type is blank
    if row['Go Live Status'] == 'Rolled out' and row['Configuration Type'] is blank:
        return 'Data Incorrect'
    
    # Not Configured
    if row['Configuration Type'] is blank:
        return 'Not Configured'
    
    # Standard or Copy
    if row['Configuration Type'] in ['Standard', 'Copy']:
        return row['Configuration Type']
    
    # Implementation -> treat as Copy
    if row['Configuration Type'] == 'Implementation':
        return 'Copy'
    
    return 'Not Configured'
```

### Pre Go Live Status Logic

```python
def calculate_pre_go_live_status(row):
    # Data Incorrect: Go Live Status = 'Rolled out' but both checks are blank
    if row['Go Live Status'] == 'Rolled out' and both checks are blank:
        return 'Data Incorrect'
    
    domain = row['Domain Updated']
    setup = row['Set Up Check']
    
    # Both blank -> Not started (None)
    if both are blank:
        return None
    
    # Both Yes -> GTG
    if domain == 'Yes' and setup == 'Yes':
        return 'GTG'
    
    # Both No -> Fail
    if domain == 'No' and setup == 'No':
        return 'Fail'
    
    # One Yes, one No/blank -> Partial
    # One No, one blank -> Partial
    return 'Partial'
```

### Go Live Testing Status Logic

```python
def calculate_go_live_testing_status(row):
    # Skip if future go-live
    if row['Days to Go Live'] > 0:
        return None
    
    # Data Incorrect: Go Live Status = 'Rolled out' but all tests are blank
    if row['Go Live Status'] == 'Rolled out' and all tests are blank:
        return 'Data Incorrect'
    
    # All blank -> Not tested (None)
    if all tests are blank:
        return None
    
    # All Yes or No Issues -> GTG
    if all tests in ['Yes', 'No Issues']:
        return 'GTG'
    
    # Check for blockers
    has_blocker = (Sample ADF == 'Issues Found' or Data Migration == 'Issues Found')
    has_non_blocker = (Inbound Email == 'Issues Found' or Outbound Email == 'Issues Found')
    
    if has_blocker and has_non_blocker:
        return 'Go Live Blocker & Non-Blocker'
    elif has_blocker:
        return 'Go Live Blocker'
    elif has_non_blocker:
        return 'Non-Blocker'
    
    # All failed
    if all tests == 'Issues Found':
        return 'Fail'
    
    return None
```

### Weighted Scoring (Go Live Testing)
- Sample ADF: 40%
- Inbound Email: 12.5%
- Outbound Email: 12.5%
- Data Migration: 35%

---

## Key Files and Functions

### 1. `crm_dashboard/app.py`

**Main Functions:**
- `initialize_session_state()`: Initialize CRM-specific session state
- `load_data()`: Load and process CRM data
- `on_kpi_click(kpi_name)`: Handle KPI card clicks
- `on_region_click(region)`: Handle region banner clicks
- `render_header(processor)`: Render dashboard header
- `render_date_filter()`: Render date filter radio buttons
- `render_sub_tab_selector()`: Render sub-tab selector
- `render_configuration_tab(processor, filtered_df)`: Render Configuration sub-tab
- `render_pre_go_live_tab(processor, filtered_df)`: Render Pre Go Live sub-tab
- `render_go_live_testing_tab(processor, filtered_df)`: Render Go Live Testing sub-tab
- `render_data_tab(processor)`: Render main Data tab
- `render_analytics_tab()`: Render Analytics tab (placeholder)
- `render_crm_dashboard()`: Main entry point

### 2. `crm_dashboard/utils/data_processor.py`

**CRMDataProcessor Class Methods:**
- `__init__(df)`: Initialize with raw data
- `_prepare_data()`: Prepare data (dates, calculations, statuses)
- `_calculate_configuration_status()`: Calculate Configuration status
- `_calculate_pre_go_live_status()`: Calculate Pre Go Live status
- `_calculate_go_live_testing_status()`: Calculate Go Live Testing status
- `filter_by_date_range(filter_type)`: Filter by current month/next month/YTD
- `filter_by_region(region, df)`: Filter by region
- `get_regions(df)`: Get unique regions
- `get_configuration_kpis(df)`: Get Configuration KPI counts
- `get_pre_go_live_kpis(df)`: Get Pre Go Live KPI counts
- `get_go_live_testing_kpis(df)`: Get Go Live Testing KPI counts
- `get_region_counts(status_field, status_value, df)`: Get counts by region for status
- `get_display_dataframe(sub_tab, df)`: Format data for table display

### 3. `crm_dashboard/components/kpi_cards.py`

**Functions:**
- `render_kpi_grid(kpis, on_kpi_click, selected_kpi)`: Render KPI cards in grid
- `render_region_banners(region_counts, on_region_click, selected_region)`: Render region banners
- `render_upcoming_week_banner(count)`: Render upcoming week alert

### 4. `crm_dashboard/components/data_table.py`

**Functions:**
- `render_data_table(df, title, key_suffix)`: Render data table with styling and export
- `render_summary_stats(df)`: Render summary statistics

### 5. `crm_dashboard/config/settings.py`

**Constants:**
- `DASHBOARD_TITLE`: Dashboard title
- `USE_MOCK_DATA`: Flag for mock vs real data
- `REGIONS`: List of regions
- `SUB_TABS`: Sub-tab definitions
- `DATE_FILTERS`: Date filter options
- `KPI_COLORS`: Color mapping for KPIs
- `STATUS_COLORS`: Color mapping for statuses
- `UPCOMING_WEEK_DAYS`: Threshold for upcoming week (7 days)
- `DISPLAY_COLUMNS`: Table column definitions
- `COLUMN_MAPPINGS`: Source to standard column mappings

### 6. `crm_dashboard/data/mock_data.py`

**Functions:**
- `generate_mock_crm_data(num_rows)`: Generate mock CRM data
- `load_crm_data()`: Load data from source (mock or SharePoint)

---

## Session State Variables

All CRM dashboard session state variables are prefixed with `crm_` to avoid conflicts:

- `crm_date_filter`: Current date filter ('current_month', 'next_month', 'ytd')
- `crm_sub_tab`: Current sub-tab ('configuration', 'pre_go_live', 'go_live_testing')
- `crm_selected_kpi`: Currently selected KPI name
- `crm_selected_region`: Currently selected region

---

## Integration with Config Operations Hub

The CRM dashboard is integrated as the second tab in the main Config Operations Hub:

```python
# In config_operations_hub.py
import crm_dashboard.app as crm_app

tab1, tab2, tab3, tab4 = st.tabs([
    "🔧 ARC Configuration",
    "📞 CRM Configuration",  # CRM tab
    "🔗 Integration",
    "🧪 Regression Testing"
])

with tab2:
    crm_app.render_crm_dashboard()
```

---

## Testing

To test the CRM dashboard standalone:

```bash
cd /Users/gautam/PyCharmMiscProject
streamlit run crm_dashboard/app.py --server.port=8503
```

To test within Config Operations Hub:

```bash
streamlit run config_operations_hub.py --server.port=8502
```

---

## Future Enhancements

1. **Analytics Tab Implementation**
   - Configuration trends over time
   - Pre Go Live completion rates
   - Go Live Testing success metrics
   - Regional performance comparison
   - Assignee workload distribution

2. **SharePoint Integration**
   - Replace mock data with real SharePoint data
   - Implement authentication
   - Real-time data refresh

3. **Advanced Filtering**
   - Filter by assignee
   - Filter by implementation type
   - Multi-region selection

4. **Notifications**
   - Email alerts for upcoming go-lives
   - Slack integration for blockers
   - Dashboard notifications

5. **Export Enhancements**
   - PDF reports
   - Excel export with formatting
   - Scheduled reports

---

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all `__init__.py` files exist
   - Check Python path includes project root

2. **Data Not Loading**
   - Verify `USE_MOCK_DATA = True` in settings.py
   - Check mock data generator

3. **Session State Conflicts**
   - All CRM variables prefixed with `crm_`
   - Clear browser cache if issues persist

4. **Styling Issues**
   - Check STATUS_COLORS and KPI_COLORS in settings.py
   - Verify CSS in app.py

---

## Contact & Support

For questions or issues with the CRM Configuration Dashboard, please contact the development team.

**Last Updated:** 2025-10-06

