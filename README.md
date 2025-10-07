# ARC Configuration Dashboard 📊

Interactive dashboard for visualizing and managing ARC Configuration KPIs across multiple Lines of Business (LOBs) at Tekion.

## 🎯 Features

### Data Tab
- **Interactive KPI Cards**: Click to drill down into specific metrics
  - Total Go Live
  - Completed
  - WIP (Work In Progress)
  - Not Configured

- **LOB Breakdown**: View metrics by Line of Business
  - Service
  - Parts
  - Accounting

- **Region Filtering**: Filter data by geographic region
  - Dynamic region detection from data
  - "All" option to view combined data

- **Data Table**: View filtered records with:
  - Dealership Name
  - Go Live Date (DD-MMM-YYYY format)
  - Type of Implementation
  - Days to Go Live (auto-calculated daily)
  - Assigned To
  - Region
  - Line of Business
  - Status

- **CSV Export**: Download filtered data for offline analysis

### Analytics Tab
- Placeholder for future visual analytics
- Planned features: trend analysis, geographic distribution, performance metrics

### Date Filters
- **Current Month**: View current month's go-lives
- **Next Month**: View next month's go-lives
- **YTD (Year to Date)**: View all go-lives from Jan 1 to today

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch Dashboard

```bash
python launch_dashboard.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
arc_dashboard/
├── app.py                      # Main dashboard application
├── config/
│   └── settings.py            # Configuration and constants
├── data/
│   ├── mock_data.py           # Mock data generator
│   └── sharepoint_loader.py   # SharePoint integration
├── utils/
│   └── data_processor.py      # Data processing utilities
└── components/
    ├── kpi_cards.py           # KPI card components
    └── data_table.py          # Data table components
```

## 🔧 Configuration

### Using Mock Data (Default)

The dashboard comes pre-configured with mock data for immediate testing. No setup required!

### Connecting to SharePoint

To connect to your SharePoint data source:

1. **Set up Azure AD App Registration**:
   - Go to Azure Portal → Azure Active Directory → App Registrations
   - Create a new app registration
   - Note the Client ID, Tenant ID
   - Create a client secret and note it down
   - Grant permissions: `Sites.Read.All`, `Files.Read.All`

2. **Configure Environment Variables**:
   ```bash
   cp .env.template .env
   ```
   
   Edit `.env` and fill in your credentials:
   ```
   SHAREPOINT_CLIENT_ID=your_client_id
   SHAREPOINT_CLIENT_SECRET=your_client_secret
   SHAREPOINT_TENANT_ID=your_tenant_id
   SHAREPOINT_SITE_URL=https://yourtenant.sharepoint.com/sites/yoursite
   SHAREPOINT_FILE_PATH=/Shared Documents/ARC Configuration/data.xlsx
   USE_MOCK_DATA=False
   ```

3. **Update settings.py**:
   - Open `arc_dashboard/config/settings.py`
   - Set `USE_MOCK_DATA = False`

### Excel File Format

Your SharePoint Excel file should have these columns:

| Column Name | Description | Example |
|------------|-------------|---------|
| Dealership Name | Name of the dealership | "Downtown Toyota - Service" |
| Go Live Date | Target go-live date | "2024-10-15" |
| Type of Implementation | Implementation type | "New Implementation" |
| Assigned To | Team member assigned | "John Smith" |
| Region | Geographic region | "North America" |
| Line of Business | LOB category | "Service" / "Parts" / "Accounting" |
| Status | Current status | "Completed" / "WIP" / "Not Configured" |

## 🎨 Customization

### Colors

Edit `arc_dashboard/config/settings.py` to customize colors:

```python
COLORS = {
    'primary': '#008080',      # Teal (Tekion brand)
    'success': '#28a745',      # Green
    'warning': '#ffc107',      # Yellow
    'danger': '#dc3545',       # Red
}
```

### KPI Logic

Modify `arc_dashboard/utils/data_processor.py` to customize KPI calculations and filtering logic.

### UI Components

Customize UI components in `arc_dashboard/components/` to match your design preferences.

## 📊 How to Use

### Basic Workflow

1. **Select Date Range**: Use sidebar to choose Current Month, Next Month, or YTD
2. **Click KPI Card**: Click any KPI card to drill down
3. **View Breakdown**: See LOB breakdown for Completed/WIP statuses
4. **Select Region**: Click a region banner to filter data
5. **View Data**: See filtered data table with all details
6. **Export**: Click "Download CSV" to export filtered data

### Example Use Cases

**Scenario 1: View all completed implementations in North America for current month**
1. Select "Current Month" in sidebar
2. Click "Completed" KPI card
3. Click "North America" region banner
4. View and export the filtered data

**Scenario 2: Check WIP Service implementations**
1. Click "WIP" KPI card
2. Click "Service" breakdown card
3. Click "All" to see all regions or select specific region
4. Review the data table

## 🔄 Data Refresh

- **Automatic**: Data is cached for 1 hour
- **Manual**: Click "🔄 Refresh Data" button in the header
- **SharePoint**: Data is fetched fresh from SharePoint on each refresh

## 🛠️ Troubleshooting

### Dashboard won't start
```bash
# Check if Streamlit is installed
pip install streamlit

# Try running directly
streamlit run arc_dashboard/app.py
```

### SharePoint connection fails
- Verify Azure AD credentials in `.env`
- Check app permissions in Azure Portal
- Ensure SharePoint site URL and file path are correct
- Test with mock data first: set `USE_MOCK_DATA=True`

### Data not displaying correctly
- Check Excel file column names match expected format
- Verify date format in Excel (YYYY-MM-DD or Excel date)
- Check for blank/null values in required columns

## 📝 Development

### Adding New Features

1. **New KPI**: Add to `data_processor.py` → `get_kpi_counts()`
2. **New Filter**: Add to `settings.py` and update `data_processor.py`
3. **New Component**: Create in `components/` directory
4. **New Analytics**: Add to `render_analytics_tab()` in `app.py`

### Testing

```bash
# Test mock data generator
python arc_dashboard/data/mock_data.py

# Test data processor
python arc_dashboard/utils/data_processor.py
```

## 📞 Support

For questions or issues:
- Check this README
- Review code comments (extensively documented)
- Test with mock data to isolate issues

## 🎯 Roadmap

- [ ] Advanced analytics visualizations
- [ ] Trend analysis charts
- [ ] Team performance metrics
- [ ] Email notifications for upcoming go-lives
- [ ] Multi-user authentication
- [ ] Custom report builder

## 📄 License

Internal use at Tekion only.

---

**Built with ❤️ using Streamlit**

# Last updated: Tue Oct  7 17:32:53 IST 2025
