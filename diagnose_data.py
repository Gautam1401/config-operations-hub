import os
import pandas as pd
import re

# --- 1. Central mapping for all dashboards ---
DASHBOARD_EXCELS = {
    "ARC":    "ARC Configurations.xlsx",
    "CRM":    "CRM Data.xlsx",
    "Integration": "Integration Access Board.xlsx",
    "Regression":  "E2E Testing Check .xlsx"
}
BASE_PATH = os.path.expanduser("~/Desktop/Operations Hub/Data Source")

# --- 2. Canonical dashboard mappings and their variants ---
CANONICAL_REQUIRED = {
    "ARC": [
        ["Dealership Name", "DEALERSHIP NAME"],
        ["Go Live Date", "GO LIVE DATE", "Go Live Data"],
        ["Region", "REGION"],
        ["Assigned To", "ASSIGNED TO", "Assignee"],
        ["Type of Implementation", "TYPE OF IMPLEMENTATION"]
    ],
    "CRM": [
        ["Dealership Name", "DEALERSHIP NAME"],
        ["Implementation Type", "IMPLEMENTATION TYPE"],
        ["Region", "REGION"],
        ["Configuration – Assigned", "CONFIGURATION – ASSIGNED"],
        ["Go Live Date", "GO LIVE DATE", "Go Live Data"],
        ["Configuration – Status","CONFIGURATION – STATUS"],
        ["Pre Go Live - Assigned to"],
        ["Pre Go Live - Domain Updated"],
        ["Pre Go Live - Set Up Check"],
        ["Go Live Testing - Assigned To"],
        ["Go Live Testing - Sample ADF"],
        ["Go Live Testing - Inbound Email Test"],
        ["Go Live Testing - Outbound Mail Test"],
        ["Go Live Testing - Data Migration Test"]
    ],
    "Integration": [
        ["Dealer Name - Dealer ID"],
        ["Go Live Date", "GO LIVE DATE"],
        ["PEM"],
        ["Director"],
        ["Type of Implementation", "TYPE OF IMPLEMENTATION"],
        ["Region"],
        ["Assigned To"],
        ["Vendor List Updated"]
    ],
    "Regression": [
        ["Dealership Name"],
        ["Go Live Date"],
        ["SIM Start", "SIM Start Date"],
        ["Assignee"],
        ["Region"],
        ["Testing Status"]
    ]
}

def flex_match(col, candidates):
    """Match ignoring case/spaces/punctuation."""
    norm_col = re.sub(r'[^a-z0-9]', '', col.lower())
    for can in candidates:
        norm_can = re.sub(r'[^a-z0-9]', '', can.lower())
        if norm_col == norm_can:
            return can
    return None

def get_sheet_df(excel_path, sheet):
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet)
        return df
    except Exception as e:
        print(f"  ⛔ Error reading sheet {sheet}: {e}")
        return None

print("\n=== DASHBOARD DATA DIAGNOSTICS REPORT ===")

for dash, fname in DASHBOARD_EXCELS.items():
    fpath = os.path.join(BASE_PATH, fname)
    print(f"\n[{dash}]: {fname}")
    if not os.path.exists(fpath):
        print(f"  ⛔ File not found: {fpath}")
        continue
    try:
        xls = pd.ExcelFile(fpath)
        print(f"  ✔ Found file. Sheets: {xls.sheet_names}")
        all_issues = []
        for sheet in xls.sheet_names:
            print(f"    → Checking sheet: {sheet}")
            df = get_sheet_df(fpath, sheet)
            if df is not None:
                issues = []
                headers = list(df.columns)
                print(f"      📋 Columns found ({len(headers)} total):")
                for i, h in enumerate(headers[:15]):
                    print(f"         {i+1}. {h}")
                if len(headers) > 15:
                    print(f"         ... and {len(headers)-15} more")
                
                missing = []
                for req_variants in CANONICAL_REQUIRED[dash]:
                    found = any(flex_match(h, req_variants) for h in headers)
                    if not found:
                        missing.append(req_variants[0])
                if missing:
                    issues.append(f"      ⚠️ MISSING columns: {missing}")
                
                # Check for columns with all NaN
                for req_variants in CANONICAL_REQUIRED[dash]:
                    col = next((h for h in headers if flex_match(h, req_variants)), None)
                    if col and df[col].isna().all():
                        issues.append(f"      ⚠️ EMPTY column: {col}")
                
                if not issues:
                    print(f"      ✔ All required columns found and populated.")
                else:
                    for issue in issues:
                        print(issue)
                
                print(f"      📊 Total rows: {len(df)}")
    except Exception as e:
        print(f"  ⛔ Error reading file: {e}")

print("\n=== END OF REPORT ===\n")
