# ARC Dashboard - Quick Start Guide ⚡

## Launch in 3 Steps

### 1️⃣ Install (First Time Only)
```bash
pip3 install -r requirements.txt
```

### 2️⃣ Test
```bash
python3 test_setup.py
```

### 3️⃣ Launch
```bash
python3 launch_dashboard.py
```

Dashboard opens at: **http://localhost:8501**

---

## Using the Dashboard

### Basic Workflow
1. **Select Date** → Sidebar: Current Month / Next Month / YTD
2. **Click KPI** → Choose: Total / Completed / WIP / Not Configured
3. **Click LOB** → Filter by: Service / Parts / Accounting
4. **Click Region** → Select region or "All"
5. **View Table** → See filtered data
6. **Export** → Click "Download CSV"

### Reset
Click **"Reset Filters"** in sidebar to start over

---

## File Structure

```
arc_dashboard/
├── app.py                    # Main app (run this)
├── config/settings.py        # Change colors/settings here
├── data/
│   ├── mock_data.py         # Test data generator
│   └── sharepoint_loader.py # SharePoint connection
├── utils/data_processor.py  # KPI calculations
└── components/              # UI components
```

---

## Quick Commands

```bash
# Launch dashboard
python3 launch_dashboard.py

# Test setup
python3 test_setup.py

# Generate mock data
python3 arc_dashboard/data/mock_data.py

# Test data processor
python3 arc_dashboard/utils/data_processor.py

# Run directly with Streamlit
streamlit run arc_dashboard/app.py
```

---

## Customization Quick Tips

### Change Colors
Edit `arc_dashboard/config/settings.py`:
```python
COLORS = {
    'primary': '#008080',  # Your color here
}
```

### Change Mock Data Size
Edit `arc_dashboard/config/settings.py`:
```python
MOCK_DATA_ROWS = 200  # Change from 100
```

### Add New KPI
Edit `arc_dashboard/utils/data_processor.py`:
```python
def get_kpi_counts(self, df=None):
    kpis = {
        'Your New KPI': len(df[df['column'] == 'value'])
    }
```

---

## Troubleshooting

### Won't Start?
```bash
streamlit run arc_dashboard/app.py
```

### Import Errors?
```bash
pip3 install -r requirements.txt
```

### Port Busy?
```bash
streamlit run arc_dashboard/app.py --server.port=8502
```

---

## SharePoint Setup (Optional)

1. Create Azure AD App
2. Copy `.env.template` to `.env`
3. Fill in credentials
4. Set `USE_MOCK_DATA = False` in `settings.py`

See **SETUP_GUIDE.md** for details.

---

## Key Files

- **README.md** - Full documentation
- **SETUP_GUIDE.md** - Detailed setup
- **PROJECT_SUMMARY.md** - Project overview
- **QUICK_START.md** - This file

---

## Support

Check these in order:
1. This quick start
2. README.md
3. SETUP_GUIDE.md
4. Code comments

---

**Ready? Launch now:**
```bash
python3 launch_dashboard.py
```

🚀 **Happy Dashboarding!**

