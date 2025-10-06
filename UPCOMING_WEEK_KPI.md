# Integration Dashboard - Upcoming Week as KPI

## ✅ Feature Added: "Upcoming Week" KPI Card

### Overview

Added "Upcoming Week" as a KPI card (before "Data Incomplete") that shows dealerships with Go Live dates in the next 7 days from today (real-time).

**Benefits**:
- ✅ **Easier** - No separate alert function needed
- ✅ **More Consistent** - Matches existing KPI card pattern
- ✅ **Better UX** - Users can click to see regional breakdown
- ✅ **Cleaner Code** - Reuses existing KPI infrastructure
- ✅ **Interactive** - Can drill down by region like other KPIs

---

### KPI Card Layout

**New Order**:
```
┌─────────────┬─────────┬──────────┬──────────┬────────────┬─────────────────┬─────────────────┐
│ Total Go    │   GTG   │ On Track │ Critical │ Escalated  │ Upcoming Week   │ Data Incomplete │
│ Lives       │         │          │          │            │                 │                 │
│     25      │    4    │    6     │    6     │     2      │       3         │        4        │
└─────────────┴─────────┴──────────┴──────────┴────────────┴─────────────────┴─────────────────┘
```

**Color**: Teal/Cyan (`kpi-info` class)

---

### Implementation Details

#### 1. Updated `get_kpis()` Function

**File**: `integration_dashboard/utils/data_processor.py`

**Code**:
```python
def get_kpis(self, df: pd.DataFrame) -> Dict[str, int]:
    """Calculate KPIs from filtered data"""
    
    # Calculate Upcoming Week count (next 7 days from today)
    today = pd.Timestamp.now().normalize()
    next_week = today + pd.Timedelta(days=7)
    upcoming_week_count = len(self.df[
        (self.df['Go Live Date'] >= today) &
        (self.df['Go Live Date'] <= next_week)
    ])
    
    kpis = {
        'Total Go Lives': len(df),
        'GTG': len(df[df['Status'] == 'GTG']),
        'On Track': len(df[df['Status'] == 'On Track']),
        'Critical': len(df[df['Status'] == 'Critical']),
        'Escalated': len(df[df['Status'] == 'Escalated']),
        'Upcoming Week': upcoming_week_count,  # NEW
        'Data Incomplete': len(df[df['Status'] == 'Data Incomplete'])
    }
    
    return kpis
```

**Key Points**:
- Uses `self.df` (full dataset) not `df` (filtered dataset)
- Real-time calculation from today
- Counts records where Go Live Date is between today and today + 7 days

---

#### 2. Added KPI Color

**File**: `integration_dashboard/config/settings.py`

**Code**:
```python
KPI_COLORS = {
    'Total Go Lives': 'kpi-accent',
    'GTG': 'kpi-success',
    'On Track': 'kpi-accent',
    'Critical': 'kpi-warning',
    'Escalated': 'kpi-error',
    'Upcoming Week': 'kpi-info',  # NEW - Teal/Cyan color
    'Data Incomplete': 'kpi-grey'
}
```

---

#### 3. Updated Region Counts Logic

**File**: `integration_dashboard/app.py`

**Code**:
```python
# Get region counts
if st.session_state.integration_selected_kpi == 'Total Go Lives':
    region_counts = {region: len(filtered_df[filtered_df['Region'] == region]) 
                   for region in processor.get_regions(filtered_df)}
elif st.session_state.integration_selected_kpi == 'Upcoming Week':
    # Get upcoming week data and count by region
    upcoming_df = processor.get_upcoming_week_data()
    region_counts = {region: len(upcoming_df[upcoming_df['Region'] == region]) 
                   for region in processor.get_regions(processor.df)}
else:
    region_counts = processor.get_region_counts(
        st.session_state.integration_selected_kpi,
        filtered_df
    )
```

**Key Points**:
- Special handling for "Upcoming Week" KPI
- Uses `get_upcoming_week_data()` to get next 7 days data
- Counts by region from upcoming week data

---

#### 4. Updated Table Filtering Logic

**File**: `integration_dashboard/app.py`

**Code**:
```python
# Filter by region
if st.session_state.integration_selected_kpi == 'Upcoming Week':
    # Use upcoming week data
    upcoming_df = processor.get_upcoming_week_data()
    region_filtered_df = processor.filter_by_region(st.session_state.integration_selected_region, upcoming_df)
else:
    region_filtered_df = processor.filter_by_region(st.session_state.integration_selected_region, filtered_df)
    
    if st.session_state.integration_selected_kpi != 'Total Go Lives':
        region_filtered_df = region_filtered_df[
            region_filtered_df['Status'] == st.session_state.integration_selected_kpi
        ]
```

**Key Points**:
- When "Upcoming Week" is selected, uses upcoming week data
- Filters by selected region
- Shows table with dealerships in that region with upcoming go lives

---

#### 5. Removed Old Alert Function

**Removed**:
- `render_upcoming_week_alert_integration()` function
- Call to the alert function in `render_data_tab()`

**Reason**: No longer needed - "Upcoming Week" is now a KPI card

---

### User Flow

**Step 1**: User sees "Upcoming Week" KPI card with count (e.g., 3)

**Step 2**: User clicks "Upcoming Week" KPI card

**Step 3**: Regional breakdown appears:
```
┌─────────┬─────────┬─────────┬─────────┐
│   NAM   │  EMEA   │  APAC   │ LATAM   │
│   (2)   │   (1)   │   (0)   │   (0)   │
└─────────┴─────────┴─────────┴─────────┘
```

**Step 4**: User clicks a region (e.g., "NAM")

**Step 5**: Table appears with dealerships in NAM with upcoming go lives:
```
┌──────────────────┬───────────┬──────────────┬──────────┬───────────┐
│ Dealership Name  │ Go Live   │ Days to Go   │ PEM      │ Director  │
│                  │ Date      │ Live         │          │           │
├──────────────────┼───────────┼──────────────┼──────────┼───────────┤
│ ABC Motors - 123 │ 08-Oct-25 │ 2            │ John Doe │ Jane Smith│
│ XYZ Auto - 456   │ 10-Oct-25 │ 4            │ Bob Lee  │ Mary Jones│
└──────────────────┴───────────┴──────────────┴──────────┴───────────┘
```

---

### Features

✅ **Real-Time Calculation**:
- Calculates from current date every time
- Updates automatically each day
- Always shows next 7 days from today

✅ **Interactive Drilldown**:
- Click KPI → See regions
- Click region → See table
- Same flow as other KPIs

✅ **Consistent UX**:
- Matches existing KPI card design
- Same hover effects
- Same selection highlighting (gold border)

✅ **Independent of Date Filter**:
- Always shows next 7 days from today
- Not affected by "Current Month", "Next Month", etc. filters
- Provides real-time visibility

---

### Examples

**Example 1: Today = October 6, 2025**
- Upcoming Week shows: Go Lives from Oct 6 to Oct 13, 2025
- Count: 3 dealerships

**Example 2: Tomorrow = October 7, 2025**
- Upcoming Week shows: Go Lives from Oct 7 to Oct 14, 2025
- Count: 2 dealerships (auto-updates)

**Example 3: No Upcoming Go Lives**
- Upcoming Week shows: 0
- Card still appears but with count 0
- Clicking it shows "No data" message

---

### Comparison: Before vs After

**Before** (Alert Banner):
```
┌─────────────────────────────────────────────────┐
│ ⚠️ Upcoming Week Go Live Alert                  │
│ 3 Go-Live(s) scheduled in the next 7 days      │
└─────────────────────────────────────────────────┘

📋 Upcoming Week Go Live Details
[Table with all upcoming go lives]
```

**After** (KPI Card):
```
┌─────────────────┐
│ Upcoming Week   │
│       3         │
└─────────────────┘

Click → See regions → Click region → See table
```

**Advantages**:
- ✅ More compact
- ✅ Interactive drilldown
- ✅ Consistent with other KPIs
- ✅ Cleaner code
- ✅ Better UX

---

### Files Modified

1. **`integration_dashboard/utils/data_processor.py`**
   - Updated `get_kpis()` to include "Upcoming Week" count

2. **`integration_dashboard/config/settings.py`**
   - Added "Upcoming Week" to `KPI_COLORS`

3. **`integration_dashboard/app.py`**
   - Removed `render_upcoming_week_alert_integration()` function
   - Removed call to alert function
   - Updated region counts logic for "Upcoming Week"
   - Updated table filtering logic for "Upcoming Week"

---

### Testing Checklist

- [x] "Upcoming Week" KPI card appears
- [x] Shows correct count (next 7 days from today)
- [x] Teal/cyan color applied
- [x] Clicking KPI shows regional breakdown
- [x] Regional counts are correct
- [x] Clicking region shows table
- [x] Table shows only upcoming week data for that region
- [x] Date filter doesn't affect "Upcoming Week" count
- [x] Real-time calculation works
- [x] Selection highlighting works (gold border)

---

## 🚀 Dashboard Status

**URL**: http://localhost:8502  
**Tab**: 🔗 Integration  
**Status**: ✅ "Upcoming Week" KPI added  

**KPI Cards** (in order):
1. Total Go Lives
2. GTG
3. On Track
4. Critical
5. Escalated
6. **Upcoming Week** ⬅️ NEW
7. Data Incomplete

**Working Features**:
- ✅ "Upcoming Week" KPI card (teal color)
- ✅ Real-time calculation (next 7 days from today)
- ✅ Interactive drilldown (KPI → Region → Table)
- ✅ Exact calendar month filtering
- ✅ All other KPIs working
- ✅ Selection highlighting
- ✅ Black theme

---

**Last Updated**: 2025-10-06  
**Status**: ✅ Complete  
**"Upcoming Week" KPI**: ✅ Added  
**Ready for Use**: ✅ Yes

