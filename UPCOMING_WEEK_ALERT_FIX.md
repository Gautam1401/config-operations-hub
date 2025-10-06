# Integration Dashboard - Upcoming Week Alert Fix

## ✅ Issue Fixed: TypeError with render_upcoming_week_alert()

### Problem
```
TypeError: render_upcoming_week_alert() got an unexpected keyword argument 'alert_data'
```

**Root Cause**:
The `render_upcoming_week_alert()` function in `shared/styles.py` only accepts a `count` parameter, but the Integration dashboard was trying to pass `alert_data`, `title`, and `key_suffix` parameters.

**Function Definition** (shared/styles.py):
```python
def render_upcoming_week_alert(count: int):
    """Render upcoming week alert banner"""
    if count > 0:
        st.markdown(
            f'<div class="alert">⚠️ <b>Upcoming Week Alert</b><br>'
            f'{count} Go-Live(s) scheduled in the next 7 days</div>',
            unsafe_allow_html=True
        )
```

**Incorrect Call** (integration_dashboard/app.py):
```python
render_upcoming_week_alert(
    alert_data=alert_data,  # ❌ Not a valid parameter
    title="⚠️ Upcoming Week Go Live Alert",  # ❌ Not a valid parameter
    key_suffix="integration"  # ❌ Not a valid parameter
)
```

---

### Solution Applied

Created a custom alert function for the Integration dashboard that:
1. Shows an alert banner with count
2. Displays a detailed table with dealership information

**New Function** (integration_dashboard/app.py):
```python
def render_upcoming_week_alert_integration(processor: IntegrationDataProcessor):
    """
    Render Upcoming Week Go Live alert
    Shows dealerships with Go Live in next 7 days from today (real-time)
    """
    
    # Get upcoming week data (next 7 days from today)
    upcoming_df = processor.get_upcoming_week_data()
    
    if len(upcoming_df) > 0:
        # Show alert banner
        st.markdown(
            f'<div class="alert">⚠️ <b>Upcoming Week Go Live Alert</b><br>'
            f'{len(upcoming_df)} Go-Live(s) scheduled in the next 7 days</div>',
            unsafe_allow_html=True
        )
        
        # Show table with details
        st.markdown("#### 📋 Upcoming Week Go Live Details")
        
        # Prepare display dataframe
        display_df = upcoming_df[['Dealer Name', 'Dealer ID', 'Go Live Date', 'PEM', 'Director']].copy()
        
        # Format Go Live Date
        display_df['Go Live Date'] = pd.to_datetime(display_df['Go Live Date']).dt.strftime('%d-%b-%Y')
        
        # Display table
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
```

---

### Changes Made

**File**: `integration_dashboard/app.py`

**1. Removed Import**:
```python
# Before
from shared.styles import (
    apply_modern_styles,
    render_modern_header,
    render_upcoming_week_alert  # ❌ Removed
)

# After
from shared.styles import (
    apply_modern_styles,
    render_modern_header
)
```

**2. Rewrote Alert Function**:
- Removed incorrect function call to `render_upcoming_week_alert()`
- Created custom alert with banner + table
- Shows count in banner
- Shows detailed table with all required fields

---

### Alert Features

**Alert Banner**:
- Shows count of upcoming go lives
- Displays: "⚠️ Upcoming Week Go Live Alert"
- Shows: "X Go-Live(s) scheduled in the next 7 days"

**Details Table**:
- Title: "📋 Upcoming Week Go Live Details"
- Columns:
  - Dealer Name
  - Dealer ID
  - Go Live Date (formatted as DD-MMM-YYYY)
  - PEM
  - Director
- Full-width table
- No index column

**Display Logic**:
- Only shows if there are upcoming go lives (next 7 days)
- Real-time calculation from today
- Updates automatically each day

---

### Example Output

**When there are upcoming go lives**:

```
┌─────────────────────────────────────────────────┐
│ ⚠️ Upcoming Week Go Live Alert                  │
│ 3 Go-Live(s) scheduled in the next 7 days      │
└─────────────────────────────────────────────────┘

#### 📋 Upcoming Week Go Live Details

┌──────────────────┬───────────┬──────────────┬──────────┬───────────┐
│ Dealer Name      │ Dealer ID │ Go Live Date │ PEM      │ Director  │
├──────────────────┼───────────┼──────────────┼──────────┼───────────┤
│ ABC Motors       │ 12345     │ 08-Oct-2025  │ John Doe │ Jane Smith│
│ XYZ Auto         │ 67890     │ 10-Oct-2025  │ Bob Lee  │ Mary Jones│
│ 123 Dealership   │ 11111     │ 12-Oct-2025  │ Tom Brown│ Sue White │
└──────────────────┴───────────┴──────────────┴──────────┴───────────┘
```

**When there are no upcoming go lives**:
- Alert does not appear
- Dashboard shows normal KPI cards

---

### Comparison with CRM Dashboard

**CRM Dashboard**:
- Uses `render_upcoming_week_alert(count)` from shared/styles.py
- Only shows count in banner
- No detailed table

**Integration Dashboard**:
- Uses custom `render_upcoming_week_alert_integration(processor)`
- Shows count in banner
- Shows detailed table with dealership information
- More comprehensive for Integration needs

---

### Testing

**Test 1: No Upcoming Go Lives**
- Date: October 6, 2025
- Go Lives: October 20, November 5
- Expected: No alert shown
- Result: ✅ Pass

**Test 2: Some Upcoming Go Lives**
- Date: October 6, 2025
- Go Lives: October 8, October 10, October 12
- Expected: Alert with 3 go lives, table with 3 rows
- Result: ✅ Pass

**Test 3: Go Live Today**
- Date: October 6, 2025
- Go Lives: October 6
- Expected: Alert with 1 go live (today counts)
- Result: ✅ Pass

**Test 4: Go Live Exactly 7 Days Away**
- Date: October 6, 2025
- Go Lives: October 13
- Expected: Alert with 1 go live (7 days counts)
- Result: ✅ Pass

**Test 5: Go Live 8 Days Away**
- Date: October 6, 2025
- Go Lives: October 14
- Expected: No alert (8 days is outside range)
- Result: ✅ Pass

---

### Date Formatting

**Go Live Date Display**:
- Format: `DD-MMM-YYYY`
- Example: `08-Oct-2025`
- Consistent with other dashboards

**Code**:
```python
display_df['Go Live Date'] = pd.to_datetime(display_df['Go Live Date']).dt.strftime('%d-%b-%Y')
```

---

### Complete Fix Summary

**Files Modified**:
1. `integration_dashboard/app.py`
   - Removed import of `render_upcoming_week_alert`
   - Rewrote `render_upcoming_week_alert_integration()` function
   - Added custom alert banner + table

**Files Unchanged**:
- `shared/styles.py` - No changes needed
- `integration_dashboard/utils/data_processor.py` - Already has `get_upcoming_week_data()`

---

### Verification Checklist

- [x] TypeError fixed
- [x] Alert banner shows correctly
- [x] Table displays with all required columns
- [x] Date formatted as DD-MMM-YYYY
- [x] Only shows when there are upcoming go lives
- [x] Real-time calculation (next 7 days from today)
- [x] Full-width table
- [x] No index column
- [x] Separator line after alert

---

## 🚀 Dashboard Status

**URL**: http://localhost:8502  
**Tab**: 🔗 Integration  
**Status**: ✅ TypeError fixed  

**Working Features**:
- ✅ Upcoming Week Go Live alert (banner + table)
- ✅ Exact calendar month filtering
- ✅ KPI cards render properly
- ✅ Region buttons render properly
- ✅ Selection highlighting
- ✅ Regional drilldown
- ✅ Data tables
- ✅ CSV export
- ✅ Black theme

---

**Last Updated**: 2025-10-06  
**Status**: ✅ Complete  
**TypeError**: ✅ Fixed  
**Alert Working**: ✅ Yes

