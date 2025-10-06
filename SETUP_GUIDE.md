# ARC Dashboard Setup Guide 🚀

Step-by-step guide to get your ARC Configuration Dashboard up and running.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for installing packages)

## 🎯 Quick Setup (5 Minutes)

### Step 1: Install Python Packages

Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

This installs all necessary packages:
- Streamlit (dashboard framework)
- Pandas (data processing)
- Plotly (visualizations)
- And other dependencies

### Step 2: Launch the Dashboard

Simply run:

```bash
python launch_dashboard.py
```

That's it! The dashboard will open in your browser automatically.

## 🎨 What You'll See

When you first launch, you'll see:

1. **Header**: Dashboard title and refresh button
2. **Sidebar**: Date filters and quick stats
3. **Two Tabs**:
   - **Data Tab**: Interactive KPI cards and drill-down
   - **Analytics Tab**: Placeholder for future features

4. **Mock Data**: 100 sample records to explore

## 🔍 Testing the Dashboard

### Try These Interactions:

1. **Change Date Filter**:
   - Click sidebar → Select "Current Month", "Next Month", or "YTD"
   - Watch KPI cards update

2. **Drill Down**:
   - Click "Completed" KPI card
   - See breakdown by Service/Parts/Accounting
   - Click "Service" to filter further
   - Click a region banner
   - View filtered data table

3. **Export Data**:
   - After filtering, click "📥 Download CSV"
   - Open the downloaded file in Excel

4. **Reset Filters**:
   - Click "🔄 Reset Filters" in sidebar
   - Start fresh

## 📊 Understanding the Data Flow

```
Excel File (SharePoint)
    ↓
Data Loader (sharepoint_loader.py)
    ↓
Data Processor (data_processor.py)
    ↓
UI Components (kpi_cards.py, data_table.py)
    ↓
Dashboard Display (app.py)
```

## 🔧 Connecting to SharePoint (Advanced)

### Prerequisites

- Azure AD App Registration
- SharePoint site access
- Admin permissions to create app registrations

### Step-by-Step SharePoint Setup

#### 1. Create Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure Active Directory** → **App Registrations**
3. Click **"New registration"**
4. Fill in:
   - **Name**: "ARC Dashboard App"
   - **Supported account types**: "Accounts in this organizational directory only"
   - **Redirect URI**: Leave blank
5. Click **"Register"**

#### 2. Note Your Credentials

After registration, you'll see:
- **Application (client) ID**: Copy this
- **Directory (tenant) ID**: Copy this

#### 3. Create Client Secret

1. In your app registration, go to **"Certificates & secrets"**
2. Click **"New client secret"**
3. Add description: "ARC Dashboard Secret"
4. Set expiration: Choose appropriate duration
5. Click **"Add"**
6. **IMPORTANT**: Copy the secret **Value** immediately (you won't see it again!)

#### 4. Grant Permissions

1. Go to **"API permissions"**
2. Click **"Add a permission"**
3. Select **"Microsoft Graph"**
4. Choose **"Application permissions"**
5. Add these permissions:
   - `Sites.Read.All`
   - `Files.Read.All`
6. Click **"Add permissions"**
7. Click **"Grant admin consent"** (requires admin)

#### 5. Configure Dashboard

1. Copy the template file:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` file with your credentials:
   ```
   SHAREPOINT_CLIENT_ID=<your-client-id>
   SHAREPOINT_CLIENT_SECRET=<your-client-secret>
   SHAREPOINT_TENANT_ID=<your-tenant-id>
   SHAREPOINT_SITE_URL=https://yourtenant.sharepoint.com/sites/yoursite
   SHAREPOINT_FILE_PATH=/Shared Documents/ARC Configuration/data.xlsx
   USE_MOCK_DATA=False
   ```

3. Update `arc_dashboard/config/settings.py`:
   ```python
   USE_MOCK_DATA = False
   ```

#### 6. Prepare Your Excel File

Ensure your SharePoint Excel file has these columns:

| Column Name | Type | Required | Example |
|------------|------|----------|---------|
| Dealership Name | Text | Yes | "Downtown Toyota - Service" |
| Go Live Date | Date | Yes | 2024-10-15 |
| Type of Implementation | Text | Yes | "New Implementation" |
| Assigned To | Text | Yes | "John Smith" |
| Region | Text | Yes | "North America" |
| Line of Business | Text | Yes | "Service" |
| Status | Text | Yes | "Completed" |

**Status Values**: Must be exactly one of:
- `Completed`
- `WIP`
- `Not Configured`

**Line of Business Values**: Must be exactly one of:
- `Service`
- `Parts`
- `Accounting`

#### 7. Test Connection

1. Launch dashboard: `python launch_dashboard.py`
2. Check sidebar: Should show "Connected to SharePoint"
3. If errors appear, check:
   - Credentials in `.env`
   - File path is correct
   - Permissions granted in Azure
   - Excel file format matches requirements

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: Dashboard won't start

**Solution**:
```bash
# Try running Streamlit directly
streamlit run arc_dashboard/app.py
```

### Issue: SharePoint authentication fails

**Solutions**:
1. Verify credentials in `.env` file
2. Check Azure AD app permissions
3. Ensure admin consent was granted
4. Test with mock data first: `USE_MOCK_DATA=True`

### Issue: Data not displaying

**Solutions**:
1. Check Excel column names match exactly
2. Verify date format (YYYY-MM-DD)
3. Check for blank rows in Excel
4. Ensure Status values are exact matches

### Issue: Port 8501 already in use

**Solution**:
```bash
# Use a different port
streamlit run arc_dashboard/app.py --server.port=8502
```

## 📚 Next Steps

After setup:

1. **Explore Mock Data**: Get familiar with the interface
2. **Connect SharePoint**: Follow advanced setup above
3. **Customize**: Modify colors, add features
4. **Share**: Deploy for your team

## 🎓 Learning Resources

### Understanding the Code

Each file is heavily commented. Start here:

1. **`arc_dashboard/config/settings.py`**: All configuration
2. **`arc_dashboard/data/mock_data.py`**: See how data is structured
3. **`arc_dashboard/utils/data_processor.py`**: Learn data processing logic
4. **`arc_dashboard/app.py`**: Main application flow

### Streamlit Documentation

- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)

### Microsoft Graph API

- [Graph API Docs](https://docs.microsoft.com/en-us/graph/)
- [SharePoint API](https://docs.microsoft.com/en-us/graph/api/resources/sharepoint)

## 💡 Tips

1. **Start with Mock Data**: Test everything before connecting SharePoint
2. **Use Version Control**: Keep your `.env` file out of git (it's in `.gitignore`)
3. **Document Changes**: Add comments when you modify code
4. **Test Incrementally**: Make small changes and test frequently

## 🎯 Success Checklist

- [ ] Python installed and working
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Dashboard launches successfully
- [ ] Can interact with mock data
- [ ] Can filter by date range
- [ ] Can drill down through KPIs
- [ ] Can export CSV
- [ ] (Optional) SharePoint connected
- [ ] (Optional) Real data loading

## 📞 Getting Help

If you're stuck:

1. Check error messages carefully
2. Review this guide
3. Check code comments
4. Test with mock data to isolate issues
5. Verify Excel file format

---

**Happy Dashboarding! 🎉**

