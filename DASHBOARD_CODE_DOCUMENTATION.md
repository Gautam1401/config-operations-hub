# ARC Configuration Dashboard - Complete Code Documentation

## Project Structure

```
PyCharmMiscProject/
├── config_operations_hub.py          # Main hub with tabs for all LOBs
├── arc_dashboard/                     # ARC Configuration Dashboard
│   ├── app.py                        # Main application entry point
│   ├── components/                   # UI components
│   │   ├── kpi_cards.py             # KPI cards and region banners
│   │   └── data_table.py            # Data table display
│   ├── config/                       # Configuration settings
│   │   └── settings.py              # Dashboard settings and constants
│   ├── data/                         # Data loading modules
│   │   ├── mock_data.py             # Mock data generator
│   │   └── sharepoint_loader.py     # SharePoint data loader
│   └── utils/                        # Utility functions
│       └── data_processor.py        # Data processing and filtering
```

---

## File Details

### 1. **config_operations_hub.py** (Main Hub)
**Purpose**: Main landing page with tabs for all LOB dashboards

**Key Features**:
- Tekion logo placeholder
- 4 tabs: ARC Configuration, ARC Regression Testing, CRM Configuration, Integration
- Loads ARC Configuration dashboard in first tab
- Placeholder content for other tabs

**Main Components**:
```python
- Page configuration (wide layout)
- Custom CSS styling
- Tab-based navigation
- Dynamic imports for each LOB dashboard
```

---

### 2. **arc_dashboard/app.py** (Main Application)
**Purpose**: Core application logic for ARC Configuration dashboard

**Key Functions**:

#### `initialize_session_state()`
- Initializes Streamlit session state variables
- Sets default values for filters and selections

#### `load_data(use_mock=True)`
- Loads data from SharePoint or mock data
- Returns ARCDataProcessor instance
- Handles fallback to mock data if SharePoint fails

#### `render_arc_dashboard()`
- Main rendering function for embedding in hub
- Initializes session state
- Loads data
- Renders sidebar and main content tabs

#### `render_sidebar(processor)`
- Displays filters (Region, Date Range)
- Shows data source information
- Provides reset filters button

#### `render_data_tab(processor)`
- Displays KPI cards (Total Go Live, Completed, WIP, Not Configured)
- Shows region banners with counts
- Displays module breakdown (Service, Parts, Accounting)
- Shows filtered data table

#### `render_analytics_tab()`
- Placeholder for future analytics features

**Callback Functions**:
- `on_kpi_click(kpi_name)`: Handles KPI card clicks
- `on_region_click(region)`: Handles region banner clicks
- `on_breakdown_click(category)`: Handles module breakdown clicks
- `reset_filters()`: Resets all filters

---

### 3. **arc_dashboard/components/kpi_cards.py**
**Purpose**: Reusable UI components for KPI display

**Functions**:

#### `render_kpi_grid(kpis, selected_kpi=None)`
- Displays KPI cards in a grid layout
- Shows Total Go Live, Completed, WIP, Not Configured
- Highlights selected KPI
- Returns clicked KPI name

#### `render_region_banners(regions, counts, selected_region=None)`
- Displays region cards (NAM, EMEA, APAC, LATAM)
- Shows count for each region
- Highlights selected region
- Returns clicked region

#### `render_breakdown_cards(breakdown, selected_lob=None)`
- Displays module breakdown (Service, Parts, Accounting)
- Shows count for each module
- Highlights selected module
- Returns clicked module

**Styling**:
- Teal background (#008080)
- White text
- Hover effects
- Click interactions

---

### 4. **arc_dashboard/components/data_table.py**
**Purpose**: Data table display and summary statistics

**Functions**:

#### `render_data_table(df, title="Data Table")`
- Displays filtered data in table format
- Shows columns: Dealership Name, Region, Module, Status, Go Live Date, Days to Go Live
- Provides download button for CSV export
- Sortable columns

#### `render_summary_stats(df)`
- Shows summary statistics
- Displays total records, date range, status distribution

---

### 5. **arc_dashboard/config/settings.py**
**Purpose**: Configuration settings and constants

**Key Settings**:

```python
# Dashboard Info
DASHBOARD_TITLE = "ARC Configuration Dashboard"
PAGE_ICON = "📊"

# Data Source
USE_MOCK_DATA = True  # Set to False for SharePoint
SHAREPOINT_CONFIG = {
    'site_url': 'your_sharepoint_site',
    'list_name': 'ARC Configuration',
    'credentials': {...}
}

# Mock Data
MOCK_DATA_ROWS = 100

# Regions
REGIONS = ['NAM', 'EMEA', 'APAC', 'LATAM']

# Status Options
STATUS_OPTIONS = ['Completed', 'WIP', 'Not Configured']

# Modules (Line of Business)
LOB_OPTIONS = ['Service', 'Parts', 'Accounting']

# Date Filters (Dynamic)
_current_month = datetime.now().strftime('%B %Y')
_next_month = (datetime.now() + relativedelta(months=1)).strftime('%B %Y')
DATE_FILTERS = {
    'current_month': _current_month,
    'next_month': _next_month,
    'ytd': 'YTD (Year to Date)',
}

# Colors
PRIMARY_COLOR = "#008080"  # Teal
SECONDARY_COLOR = "#FFFFFF"  # White
```

---

### 6. **arc_dashboard/data/mock_data.py**
**Purpose**: Generate realistic mock data for testing

**Function**:

#### `generate_mock_data(num_rows=100)`
- Generates random ARC configuration data
- Creates realistic dealership names
- Assigns random regions, modules, statuses
- Generates go-live dates (past, current, future)
- Returns pandas DataFrame

**Generated Columns**:
- Dealership ID
- Dealership Name
- Region
- Line of Business (Module)
- Status
- Go Live Date
- Configuration Type
- Assigned To

---

### 7. **arc_dashboard/data/sharepoint_loader.py**
**Purpose**: Load data from SharePoint

**Function**:

#### `load_data_from_sharepoint(config)`
- Connects to SharePoint site
- Retrieves data from specified list
- Handles authentication
- Returns pandas DataFrame
- Error handling and logging

**Configuration Required**:
```python
{
    'site_url': 'https://your-tenant.sharepoint.com/sites/your-site',
    'list_name': 'ARC Configuration',
    'credentials': {
        'username': 'user@domain.com',
        'password': 'password'
    }
}
```

---

### 8. **arc_dashboard/utils/data_processor.py**
**Purpose**: Data processing, filtering, and calculations

**Class**: `ARCDataProcessor`

**Methods**:

#### `__init__(self, df: pd.DataFrame)`
- Initializes processor with DataFrame
- Validates input type (defensive coding)
- Prepares data (converts dates, calculates days to go live)

#### `_prepare_data(self)`
- Converts Go Live Date to datetime
- Calculates Days to Go Live
- Handles missing values

#### `filter_by_date_range(self, filter_type: str) -> pd.DataFrame`
- Filters data by date range
- Options: 'current_month', 'next_month', 'ytd'
- Returns filtered DataFrame

#### `get_kpi_counts(self, df=None) -> Dict[str, int]`
- Calculates KPI counts
- Returns: {'Total Go Live': X, 'Completed': Y, 'WIP': Z, 'Not Configured': W}

#### `get_lob_breakdown(self, status: str, df=None) -> Dict[str, int]`
- Gets module breakdown for a specific status
- Returns: {'Service': X, 'Parts': Y, 'Accounting': Z, 'Any': Total}

#### `get_regions(self, df=None) -> List[str]`
- Returns list of unique regions in data

#### `filter_by_status(self, status: str, df=None) -> pd.DataFrame`
- Filters data by status
- Returns filtered DataFrame

#### `filter_by_lob(self, lob: str, df=None) -> pd.DataFrame`
- Filters data by module
- Returns filtered DataFrame

#### `filter_by_region(self, region: str, df=None) -> pd.DataFrame`
- Filters data by region
- Returns filtered DataFrame

#### `get_display_dataframe(self, df=None) -> pd.DataFrame`
- Prepares DataFrame for display
- Selects relevant columns
- Renames "Line of Business" to "Module"
- Formats dates as DD-MMM-YYYY
- Sorts by Go Live Date

**Helper Function**:

#### `calculate_days_to_go_live(go_live_date: datetime) -> int`
- Calculates days until go-live
- Returns negative if past, positive if future

---

## Data Flow

```
1. User opens Config Operations Hub
   ↓
2. Clicks "ARC Configuration" tab
   ↓
3. render_arc_dashboard() is called
   ↓
4. initialize_session_state() sets up filters
   ↓
5. load_data() fetches data (SharePoint or mock)
   ↓
6. ARCDataProcessor wraps the DataFrame
   ↓
7. render_sidebar() shows filters
   ↓
8. render_data_tab() displays:
   - KPI cards (via render_kpi_grid)
   - Region banners (via render_region_banners)
   - Module breakdown (via render_breakdown_cards)
   - Data table (via render_data_table)
   ↓
9. User interactions trigger callbacks:
   - Click KPI → filter by status
   - Click Region → filter by region
   - Click Module → filter by module
   ↓
10. Filtered data updates in real-time
```

---

## Key Features

### Interactive Filtering
- Click KPI cards to filter by status
- Click region banners to filter by region
- Click module cards to filter by module
- Drill-down shows breakdown by module
- Reset filters button

### Dynamic Date Filters
- Current Month (auto-updates: "October 2025")
- Next Month (auto-updates: "November 2025")
- YTD (Year to Date)

### Data Display
- Formatted dates: DD-MMM-YYYY
- Sortable columns
- Download to CSV
- Real-time count updates

### Responsive Design
- Wide layout
- Grid-based KPI cards
- Teal and white color scheme
- Hover effects
- Click interactions

---

## Session State Variables

```python
st.session_state.selected_kpi       # Currently selected KPI
st.session_state.selected_region    # Currently selected region
st.session_state.selected_lob       # Currently selected module
st.session_state.date_filter        # Current date filter
st.session_state.data_loaded        # Data load status
```

---

## Future Enhancements

### Planned Features
1. **Analytics Tab**: Advanced analytics and visualizations
2. **Other LOB Dashboards**: 
   - ARC Regression Testing
   - CRM Configuration
   - Integration
3. **User Authentication**: Login system with role-based access
4. **Real-time SharePoint Integration**: Live data refresh
5. **Export Options**: PDF, Excel reports
6. **Advanced Filters**: Multi-select, date range picker
7. **Notifications**: Alerts for critical items

---

## Dependencies

```python
streamlit              # Web framework
pandas                 # Data manipulation
datetime               # Date handling
python-dateutil        # Relative date calculations
openpyxl              # Excel file handling (for SharePoint)
```

---

## Running the Dashboard

### Local Development
```bash
streamlit run config_operations_hub.py --server.port=8502
```

### Standalone ARC Dashboard
```bash
streamlit run arc_dashboard/app.py --server.port=8501
```

---

## Configuration

### Switch to SharePoint Data
In `arc_dashboard/config/settings.py`:
```python
USE_MOCK_DATA = False

SHAREPOINT_CONFIG = {
    'site_url': 'https://your-tenant.sharepoint.com/sites/your-site',
    'list_name': 'ARC Configuration',
    'credentials': {
        'username': 'user@domain.com',
        'password': 'password'
    }
}
```

### Customize Colors
In `arc_dashboard/config/settings.py`:
```python
PRIMARY_COLOR = "#008080"    # Change teal color
SECONDARY_COLOR = "#FFFFFF"  # Change text color
```

---

## Error Handling

### Defensive Coding
- Type checking in ARCDataProcessor.__init__
- Fallback to mock data if SharePoint fails
- Graceful handling of missing data
- Clear error messages

### Common Issues
1. **Double-wrapping ARCDataProcessor**: Fixed with type assertion
2. **Indentation errors**: Fixed with proper Python syntax
3. **Import errors**: Fixed with correct module paths

---

## Best Practices

1. **Modular Design**: Separate components, data, config, utils
2. **Reusable Components**: KPI cards, region banners, data tables
3. **Type Hints**: Function signatures with type annotations
4. **Documentation**: Docstrings for all functions
5. **Error Handling**: Try-except blocks with fallbacks
6. **Session State**: Proper state management
7. **Caching**: @st.cache_data for data loading

---

## Contact & Support

For questions or issues, refer to:
- USER_GUIDE.docx
- ADMIN_GUIDE.docx
- REMINDER.docx

---

**Last Updated**: October 6, 2025
**Version**: 1.0
**Author**: Tekion Config Operations Team

