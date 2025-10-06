# Regression Testing Dashboard - Quick Reference

## 🚀 Quick Start

**URL**: http://localhost:8502  
**Tab**: 🧪 Regression Testing → 📊 Data

---

## KPI Cards (6 Total)

| KPI | Definition | Color | Logic |
|-----|------------|-------|-------|
| **Total Go Live** | All rows in filtered data | Blue | Count all |
| **Completed** | Testing Status = "Completed" | Green | Status match |
| **WIP** | Testing Status = "WIP" | Orange | Status match |
| **Unable to Complete** | Testing Status = "Unable to Complete" | Red | Status match |
| **Upcoming Next Week** | SIM Start Date in next 7 days | Teal | Real-time |
| **Data Incomplete** | SIM Start Date < today, Status blank | Grey | Real-time |

---

## Month Filters

| Filter | Shows |
|--------|-------|
| **Current Month** | Go-Live Date in current month/year |
| **Next Month** | Go-Live Date in next month/year |
| **YTD** | Go-Live Date in current year up to today |

---

## Implementation Types

- Conquest
- Buy/Sell
- Enterprise
- New Point
- **All** (no filter)

---

## User Flow

1. **Select Month** → October 2025 / November 2025 / YTD
2. **Click KPI** → Total Go Live / Completed / WIP / etc.
3. **Select Type** → Conquest / Buy/Sell / Enterprise / New Point / All
4. **Click Region** → NAM / EMEA / APAC / LATAM / All Regions
5. **View Table** → Filtered data with 6 columns
6. **Export** → Download CSV (optional)

---

## Table Columns

1. Dealership Name
2. Go-Live Date (DD-MMM-YYYY)
3. SIM Start Date (DD-MMM-YYYY)
4. Assignee
5. Region
6. Status

---

## Special KPIs

### Upcoming Next Week
- **Always real-time** (not affected by month filter)
- Shows SIM Start Dates in next 7 days from today
- Updates automatically each day

### Data Incomplete
- **Always real-time** (not affected by month filter)
- Shows records where SIM Start Date < today but Status is blank
- Helps identify missing data

---

## File Structure

```
regression_dashboard/
├── app.py                    # Main app
├── config/settings.py        # Settings
├── data/mock_data.py         # Mock data
└── utils/data_processor.py   # Data logic
```

---

## Key Functions

### Data Processor

```python
# Filter by month
filtered_df = processor.filter_by_date_range('current_month')

# Get KPIs
kpis = processor.get_kpis(filtered_df)

# Filter by type
impl_filtered = processor.filter_by_implementation_type('Conquest', filtered_df)

# Get region counts
region_counts = processor.get_region_counts('Completed', impl_filtered)

# Filter by region
region_df = processor.filter_by_region('NAM', impl_filtered)

# Get display dataframe
display_df = processor.get_display_dataframe(region_df)
```

---

## Common Tasks

### View Completed Tests in Current Month
1. Select "October 2025" (or current month)
2. Click "Completed"
3. Click "All"
4. Click "All Regions"

### View Upcoming Tests
1. Select any month
2. Click "Upcoming Next Week"
3. Click "All"
4. Click "All Regions"

### Export WIP Tests for Conquest in NAM
1. Select desired month
2. Click "WIP"
3. Click "Conquest"
4. Click "NAM"
5. Click "Download CSV"

---

## Debug Output

Check terminal for debug messages:
```
[DEBUG Regression Processor] Data prepared: 50 records
[DEBUG Regression Processor] Current Month: 10/2025, Records: 15
[DEBUG Regression Processor] KPIs: {'Total Go Live': 15, 'Completed': 8, ...}
[DEBUG Regression Processor] Filtered by Conquest: 12 records
```

---

## Troubleshooting

**No data showing?**
- Check month filter selection
- Verify mock data has records in that month
- Check debug output in terminal

**Table not appearing?**
- Make sure KPI is selected
- Make sure region is selected
- Implementation type defaults to "All"

**Wrong counts?**
- Check if using "Upcoming Next Week" or "Data Incomplete" (these use full dataset)
- Verify date filtering logic in debug output

---

## Next Steps

**To implement SharePoint integration**:
1. Update `USE_MOCK_DATA = False` in settings.py
2. Add SharePoint file path
3. Implement data loading in data_processor.py

**To build Analytics tab**:
1. Create charts for trend analysis
2. Add performance metrics
3. Implement regional comparisons

---

**Last Updated**: 2025-10-06  
**Status**: ✅ Ready for Use

