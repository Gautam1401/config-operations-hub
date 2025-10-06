"""
Quick test script to verify the dashboard setup
"""

import sys
from pathlib import Path

print("=" * 60)
print("ARC Dashboard Setup Test")
print("=" * 60)

# Test imports
print("\n1. Testing imports...")
try:
    import streamlit as st
    print("   ✓ Streamlit imported successfully")
except ImportError as e:
    print(f"   ✗ Streamlit import failed: {e}")
    sys.exit(1)

try:
    import pandas as pd
    print("   ✓ Pandas imported successfully")
except ImportError as e:
    print(f"   ✗ Pandas import failed: {e}")
    sys.exit(1)

try:
    import plotly
    print("   ✓ Plotly imported successfully")
except ImportError as e:
    print(f"   ✗ Plotly import failed: {e}")
    sys.exit(1)

# Test mock data generation
print("\n2. Testing mock data generation...")
try:
    from arc_dashboard.data.mock_data import generate_mock_data
    df = generate_mock_data(10)
    print(f"   ✓ Generated {len(df)} mock records")
    print(f"   ✓ Columns: {', '.join(df.columns.tolist())}")
except Exception as e:
    print(f"   ✗ Mock data generation failed: {e}")
    sys.exit(1)

# Test data processor
print("\n3. Testing data processor...")
try:
    from arc_dashboard.utils.data_processor import ARCDataProcessor
    processor = ARCDataProcessor(df)
    kpis = processor.get_kpi_counts()
    print(f"   ✓ Data processor initialized")
    print(f"   ✓ KPIs calculated: {kpis}")
except Exception as e:
    print(f"   ✗ Data processor failed: {e}")
    sys.exit(1)

# Test configuration
print("\n4. Testing configuration...")
try:
    from arc_dashboard.config.settings import DASHBOARD_TITLE, COLORS
    print(f"   ✓ Dashboard title: {DASHBOARD_TITLE}")
    print(f"   ✓ Color scheme loaded")
except Exception as e:
    print(f"   ✗ Configuration failed: {e}")
    sys.exit(1)

# Check file structure
print("\n5. Checking file structure...")
required_files = [
    "arc_dashboard/app.py",
    "arc_dashboard/config/settings.py",
    "arc_dashboard/data/mock_data.py",
    "arc_dashboard/data/sharepoint_loader.py",
    "arc_dashboard/utils/data_processor.py",
    "arc_dashboard/components/kpi_cards.py",
    "arc_dashboard/components/data_table.py",
    "launch_dashboard.py",
    "README.md",
    "SETUP_GUIDE.md",
]

all_exist = True
for file_path in required_files:
    if Path(file_path).exists():
        print(f"   ✓ {file_path}")
    else:
        print(f"   ✗ {file_path} - MISSING")
        all_exist = False

if not all_exist:
    print("\n⚠️  Some files are missing!")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed!")
print("=" * 60)
print("\nYou're ready to launch the dashboard!")
print("\nRun: python launch_dashboard.py")
print("=" * 60)

