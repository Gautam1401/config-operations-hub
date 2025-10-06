# CRM Configuration Dashboard - Quick Reference

## 🚀 Launch Dashboard

```bash
cd /Users/gautam/PyCharmMiscProject
streamlit run config_operations_hub.py --server.port=8502
```

Then click the **📞 CRM Configuration** tab.

---

## 📊 Dashboard Navigation

### 1. Select Time Period
- **Current Month** - This month's go-lives only
- **Next Month** - Next month's go-lives only  
- **YTD** - All go-lives this year

### 2. Select Category
- **Configuration** - Track configuration status
- **Pre Go Live Checks** - Monitor readiness checks
- **Go Live Testing** - Track testing and blockers

### 3. Click KPI Card
- Shows regional breakdown
- Only regions with data appear

### 4. Click Region
- Shows detailed data table
- Export to CSV available

---

## 🎯 KPI Definitions

### Configuration
| KPI | Definition |
|-----|------------|
| **Go Lives** | Total go-lives in selected period |
| **Standard** | Configuration Type = Standard |
| **Copy** | Configuration Type = Copy or Implementation |
| **Not Configured** | Configuration Type is blank |
| **Data Incorrect** | Go Live Status = 'Rolled out' but Configuration Type is blank |

### Pre Go Live Checks
| KPI | Definition |
|-----|------------|
| **Checks Completed** | Pre Go Live Assignee is not blank |
| **GTG** | Both Domain Updated and Set Up Check = Yes |
| **Partial** | One check Yes, one No/blank |
| **Fail** | Both checks = No |
| **Data Incorrect** | Go Live Status = 'Rolled out' but both checks are blank |

### Go Live Testing
| KPI | Definition |
|-----|------------|
| **Tests Completed** | Go Live Testing Assignee not blank AND not future go-live |
| **GTG** | All 4 tests = Yes or No Issues |
| **Go Live Blocker** | Sample ADF or Data Migration = Issues Found |
| **Non-Blocker** | Inbound or Outbound Email = Issues Found |
| **Fail** | All tests = Issues Found |
| **Data Incorrect** | Go Live Status = 'Rolled out' but all tests are blank |

---

## 📋 Table Columns

| Column | Description |
|--------|-------------|
| **Dealership Name** | Dealer Name + Dealer ID (e.g., "AutoNation Toyota (D1001)") |
| **Go Live Date** | Formatted as DD-MMM-YYYY (e.g., "15-Dec-2025") |
| **Days to Go Live** | Days remaining, or "Rolled Out" if negative |
| **Implementation Type** | Conquest, Buy-Sell, or New Point |
| **Region** | NAM, EMEA, APAC, or LATAM |
| **Assignee** | Person assigned (varies by sub-tab) |
| **Status** | Color-coded status |

---

## 🎨 Status Colors

| Status | Color | Meaning |
|--------|-------|---------|
| **Standard** | Green | Standard configuration |
| **Copy** | Blue | Copy or Implementation |
| **GTG** | Green | Good to go |
| **Partial** | Yellow | Partially complete |
| **Fail** | Red | Failed checks |
| **Go Live Blocker** | Red | Critical blocker |
| **Non-Blocker** | Yellow | Non-critical issue |
| **Not Configured** | Yellow | Not yet configured |
| **Data Incorrect** | Red | Data quality issue |

---

## ⚠️ Special Features

### Upcoming Week Alert
- Yellow banner appears when go-lives are scheduled in next 7 days
- Shows count of upcoming go-lives
- Visible in all sub-tabs

### Data Incorrect Logic
Automatically flags records where:
- Go Live Status = 'Rolled out' BUT
- Required fields are blank/missing

This helps identify data quality issues.

---

## 💾 Export Data

1. Select KPI and Region to view table
2. Click **📥 Download CSV** button
3. File downloads with timestamp
4. Opens in Excel or any CSV viewer

---

## 🔍 Filtering Logic

### Configuration
- **Go Lives**: All records (no status filter)
- **Other KPIs**: Filtered by Configuration Status

### Pre Go Live
- **Checks Completed**: Pre Go Live Assignee not blank
- **Other KPIs**: Filtered by Pre Go Live Status

### Go Live Testing
- **Tests Completed**: Go Live Testing Assignee not blank AND Days to Go Live ≤ 0
- **Other KPIs**: Filtered by Go Live Testing Status
- **Note**: Future go-lives excluded from testing metrics

---

## 🐛 Troubleshooting

### No Data Showing
- Check date filter (Current/Next Month/YTD)
- Verify mock data is enabled: `USE_MOCK_DATA = True` in settings.py
- Refresh browser

### KPI Shows 0
- Normal if no records match criteria
- Try different date filter
- Check if data exists for that status

### Region Not Appearing
- Region only shows if count > 0
- Try different KPI
- Check date filter

### Table Not Showing
- Must select both KPI and Region
- Look for instruction message
- Click region banner after selecting KPI

---

## 📁 File Locations

### Main Files
- **Dashboard**: `crm_dashboard/app.py`
- **Data Logic**: `crm_dashboard/utils/data_processor.py`
- **Settings**: `crm_dashboard/config/settings.py`
- **Mock Data**: `crm_dashboard/data/mock_data.py`

### Components
- **KPI Cards**: `crm_dashboard/components/kpi_cards.py`
- **Data Table**: `crm_dashboard/components/data_table.py`

### Documentation
- **Full Docs**: `CRM_DASHBOARD_DOCUMENTATION.md`
- **Summary**: `CRM_IMPLEMENTATION_SUMMARY.md`
- **Quick Ref**: `CRM_QUICK_REFERENCE.md` (this file)

---

## 🔧 Configuration

### Change Mock Data Size
```python
# In crm_dashboard/config/settings.py
MOCK_DATA_ROWS = 100  # Change to desired number
```

### Change Upcoming Week Threshold
```python
# In crm_dashboard/config/settings.py
UPCOMING_WEEK_DAYS = 7  # Change to desired days
```

### Change Regions
```python
# In crm_dashboard/config/settings.py
REGIONS = ['NAM', 'EMEA', 'APAC', 'LATAM']  # Add/remove regions
```

---

## 🎯 Common Tasks

### View All Current Month Go-Lives
1. Select **Current Month**
2. Select **Configuration** tab
3. Click **Go Lives** KPI
4. Click any region

### Find Go Live Blockers
1. Select desired time period
2. Select **Go Live Testing** tab
3. Click **Go Live Blocker** KPI
4. Click region to see details

### Check Pre Go Live Readiness
1. Select **Current Month**
2. Select **Pre Go Live Checks** tab
3. Click **GTG** to see ready stores
4. Click **Fail** to see issues

### Export All Data for Region
1. Select **YTD** for all data
2. Select any sub-tab
3. Click **Go Lives** or **Checks Completed** or **Tests Completed**
4. Click desired region
5. Click **📥 Download CSV**

---

## 📞 Support

For issues or questions:
1. Check this Quick Reference
2. Review `CRM_DASHBOARD_DOCUMENTATION.md`
3. Check terminal output for debug messages
4. Contact development team

---

## ✅ Quick Checklist

Before using dashboard:
- [ ] Dashboard running at http://localhost:8502
- [ ] CRM Configuration tab visible
- [ ] Date filter working
- [ ] Sub-tabs switching correctly
- [ ] KPI cards clickable
- [ ] Region banners appearing
- [ ] Tables displaying
- [ ] CSV export working

---

**Dashboard URL:** http://localhost:8502  
**Tab:** 📞 CRM Configuration  
**Status:** ✅ Ready to Use

**Last Updated:** 2025-10-06

