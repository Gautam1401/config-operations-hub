# 📊 Data Mapping Guide - Config Operations Hub

## ARC Configuration Dashboard

### **Excel File:** `ARC Configuration.xlsx`

### **Sheet Structure:**
- August Go Live
- SEPT Go -Live
- OCT Go Live
- NOV Go Live

### **Excel Columns (Wide Format):**
```
1. Assignee
2. Go Live Date
3. Type of Implementation
4. SIM
5. Dealership
6. Region
7. Parts (Status)
8. Service (Status)
9. Accounting (Status)
10. CP LINK Created
11. Comments
12. Missing DOCS
13. Communication Templates
14. Go Live date changed
```

### **Transformation Logic:**

**BEFORE (Wide Format - 1 row per dealership):**
```
Dealership      | Region | Parts      | Service | Accounting
─────────────────────────────────────────────────────────────
Downtown Toyota | NAM    | Completed  | WIP     | Not Configured
```

**AFTER (Long Format - 3 rows per dealership):**
```
Dealership      | Region | Module      | Status
──────────────────────────────────────────────────
Downtown Toyota | NAM    | Parts       | Completed
Downtown Toyota | NAM    | Service     | WIP
Downtown Toyota | NAM    | Accounting  | Not Configured
```

### **Column Mapping:**
```
Excel Column              →  Dashboard Column
────────────────────────────────────────────────
Dealership                →  Dealership Name
Go Live Date              →  Go Live Date
Type of Implementation    →  Type of Implementation
Assignee                  →  Assigned To
Region                    →  Region
Parts (value)             →  Status (when Module = Parts)
Service (value)           →  Status (when Module = Service)
Accounting (value)        →  Status (when Module = Accounting)
```

### **Status Standardization:**
```
Excel Value        →  Dashboard Status
─────────────────────────────────────
Completed          →  Completed
Complete           →  Completed
Done               →  Completed
WIP                →  WIP
In Progress        →  WIP
Not Configured     →  Not Configured
Not Started        →  Not Configured
NA / N/A / blank   →  Not Configured
```

### **Month/YTD Logic:**

**Current Month (October 2025):**
- Loads: "OCT Go Live" sheet only
- Filters: Go Live Date in October 2025

**Next Month (November 2025):**
- Loads: "NOV Go Live" sheet only
- Filters: Go Live Date in November 2025

**YTD (Year to Date):**
- Loads: ALL sheets (August, SEPT, OCT, NOV)
- Filters: Go Live Date from Jan 1, 2025 to Dec 31, 2025

### **Drill-Down Flow:**
```
1. KPI Card (e.g., "Completed")
   ↓
2. Region Breakdown (NAM: 50, EMEA: 30, APAC: 20)
   ↓
3. Module Breakdown (Parts: 20, Service: 18, Accounting: 12)
   ↓
4. Data Table (List of dealerships for selected KPI + Region + Module)
```

---

## CRM Configuration Dashboard

### **Excel File:** `CRM Data.xlsx`

### **Sheet Structure:**
- Aug 2025
- Sep 2025
- Oct 2025

### **Excel Columns:**
```
1. Dealer ID
2. Dealer Name
3. Type of Implementation
4. Region
5. Configuration - Assigned
6. Go Live
7. Date of Completion
8. Configuration - User List
9. Configuration - BP
10. Configuration - Comments
11. Configuration - Status
12. Pre Go Live - Assigned to
13. Pre Go Live - Domain Updated
14. Pre Go Live - Set Up Check
15. Pre Go Live - Comments
16. Go Live Testing - Assigned To
17. Go Live Testing - Sample ADF
18. Go Live Testing - Inbound Email Test
19. Go Live Testing - Outbound Mail Test
20. Go Live Testing - Data Migration Test
21. Go Live Testing - Comments
22. Config team didn't work on the store
```

### **Column Mapping:**
```
Excel Column                          →  Dashboard Column
──────────────────────────────────────────────────────────────
Dealer Name                           →  Dealership Name
Dealer ID                             →  Dealer ID
Go Live                               →  Go Live Date
Region                                →  Region
Type of Implementation                →  Type of Implementation
Configuration - Status                →  Configuration Status
Pre Go Live - Assigned to             →  Pre Go Live Assigned
Pre Go Live - Domain Updated          →  Domain Updated
Pre Go Live - Set Up Check            →  Set Up Check
Go Live Testing - Assigned To         →  Go Live Testing Assigned
Go Live Testing - Sample ADF          →  Sample ADF
Go Live Testing - Inbound Email Test  →  Inbound Email
Go Live Testing - Outbound Mail Test  →  Outbound Email
Go Live Testing - Data Migration Test →  Data Migration
```

### **Month/YTD Logic:**
- Same as ARC (combines all month sheets for YTD)

---

## Integration Dashboard

### **Excel File:** `Integration Access Board.xlsx`

### **Sheet Structure:**
- Single sheet (first sheet)

### **Excel Columns:**
```
1. Dealer Name
2. Dealer ID
3. Go Live Date
4. Days to Go Live
5. PEM
6. Director
7. Type of Implementation
8. Region
9. POD Leader
10. Assigned to
11. Vendor List Updated
12. OEM ID
13. Vendor Email Count
14. Email Sent
15. OEM Tasks Completed
16. Integration to Be Launched
17. Count of Launch
18. Comments
```

### **Column Mapping:**
```
Excel Column              →  Dashboard Column
────────────────────────────────────────────────
Dealer Name               →  Dealership Name
Dealer ID                 →  Dealer ID
Go Live Date              →  Go Live Date
Days to Go Live           →  Days to Go Live
PEM                       →  PEM
Director                  →  Director
Type of Implementation    →  Type of Implementation
Region                    →  Region
Assigned to               →  Assigned To
Vendor List Updated       →  Vendor List Updated
```

---

## Regression Testing Dashboard

### **Excel File:** `E2E Testing Check.xlsx`

### **Sheet Structure:**
- Stores Checklist

### **Excel Columns:**
```
1. Dealership Name
2. Go-Live Date
3. Region
4. Size
5. Type of Implementation
6. SIM Start Date
7. Week Count
8. Config Check
9. Signoffs Check
10. Assignee
11. Testing Status
12. Comments
```

### **Column Mapping:**
```
Excel Column              →  Dashboard Column
────────────────────────────────────────────────
Dealership Name           →  Dealership Name
Go-Live Date              →  Go Live Date
Region                    →  Region
Type of Implementation    →  Type of Implementation
SIM Start Date            →  SIM Start Date
Assignee                  →  Assigned To
Testing Status            →  Status
```

---

## General Notes

### **Date Handling:**
- All date columns are parsed as datetime
- Month filters use calendar month logic (1st to last day of month)
- YTD includes all data from Jan 1 to Dec 31 of current year

### **Region Standardization:**
- NAM (North America)
- EMEA (Europe, Middle East, Africa)
- APAC (Asia Pacific)
- LATAM (Latin America)

### **Status Values:**
- Standardized to: Completed, WIP, Not Configured
- Case-insensitive matching
- Blank/NA/N/A treated as "Not Configured"

---

**Last Updated:** October 2025

