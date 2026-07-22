# HR Analytics System

End-to-end data analytics portfolio project. Demonstrates database design, SQL, data cleaning, analysis, and dashboarding skills — simulating how a Data Analyst transforms raw HR data into actionable insights.

## Background

HR departments manage data scattered across multiple sources: employee records, attendance, leave, performance, recruitment, and training. This fragmentation makes data-driven decision-making difficult.

This project simulates the full analytics workflow:

```
Raw CSV → Import → SQL Cleaning → Analysis → Dashboard
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Database | PostgreSQL / MySQL |
| Data Generation | Python + Faker + NumPy (seed=42) |
| Query Language | SQL (DDL, DML, JOIN, GROUP BY, Window Functions, Subqueries) |
| Dashboard | Spreadsheet (Pivot Table + Chart) |

## Project Structure

```
HR Analytics System/
├── dataset/                    # CSV data + generation scripts
│   ├── generate_dummy_data.py  # Python + Faker data generator
│   ├── export_analysis.py      # Export analysis CSVs for dashboard
│   ├── department.csv
│   ├── position.csv
│   ├── employee.csv            # 300 employees
│   ├── attendance.csv          # 28,200 records
│   ├── leave.csv               # 540 records
│   ├── performance.csv         # 1,200 records
│   ├── recruitment.csv         # 224 candidates
│   └── training.csv            # 603 enrollments
├── database/                   # SQL scripts
│   ├── create_table.sql        # Schema (8 tables + 8 raw staging)
│   ├── insert.sql              # CSV import via COPY
│   ├── cleaning.sql            # NULL, dupes, normalization, FK validation
│   └── analysis.sql            # 22 business analysis queries
├── dashboard/                  # Spreadsheet + analysis results
│   ├── HR Dashboard.xlsx       # Final dashboard
│   ├── DASHBOARD_GUIDE.md      # Layout instructions
│   └── analysis_results/       # 21 analysis CSV exports
├── documentation/
│   ├── data_dictionary.md      # Column-level documentation
│   ├── business_rules.md       # Business rule definitions
│   └── ERD.md                  # Entity Relationship Diagram (Mermaid)
├── PRD.md                      # Product Requirements Document
├── design.md                   # Design Document
├── task.md                     # Task Breakdown & Status
└── index.html                  # Project landing page
```

## Database Schema (8 Tables)

| Table | Type | Description |
|-------|------|-------------|
| `department` | Master | Department master data (8 depts) |
| `position` | Master | Job positions with grade G1–G5 (19 positions) |
| `employee` | Core | Employee records FK → department, position (300 rows) |
| `attendance` | Transaction | Daily attendance with check-in/out times (28,200 rows) |
| `leave_request` | Transaction | Leave applications with duration (540 rows) |
| `performance` | Transaction | Quarterly KPI & manager scores (1,200 rows) |
| `recruitment` | Independent | Candidate pipeline from application to hire (224 candidates) |
| `training` | Transaction | Course enrollment and completion scores (603 rows) |

See [ERD](documentation/ERD.md) for the full entity relationship diagram.

## How to Run

### Prerequisites

- PostgreSQL (or MySQL)
- Python 3.8+ with `pip install faker numpy pandas`

### Steps

```bash
# 1. Generate dummy data
cd dataset
python generate_dummy_data.py

# 2. Create database
createdb hr_analytics
psql -d hr_analytics -f database/create_table.sql

# 3. Import CSV data into staging tables
psql -d hr_analytics -f database/insert.sql

# 4. Clean and transform data
psql -d hr_analytics -f database/cleaning.sql

# 5. Run business analysis
psql -d hr_analytics -f database/analysis.sql

# 6. Export analysis results for dashboard
python dataset/export_analysis.py
```

## Sample Insights

| Metric | Value |
|--------|-------|
| Total Employees | 300 |
| Active | 262 (87.3%) |
| Resigned | 28 (9.3%) |
| Terminated | 10 (3.3%) |
| Turnover Rate | **12.67%** |
| Avg Salary (Active) | **Rp 13,080,107** |
| Attendance Rate (Present) | **78.6%** |
| Candidates | 224 |
| Hire Rate | **29.0%** |
| Avg KPI Score | **75.4 / 100** |
| Gender Ratio | 161 Male : 139 Female |

### Key Findings

1. **Payroll:** Salary distribution varies significantly by department — Legal and IT have the highest average compensation due to grade G5 positions and department multipliers.

2. **Turnover:** 12.67% overall turnover. Employees with 2–3 years of tenure show higher resignation probability, suggesting a critical retention window.

3. **Recruitment:** Referral source yields the highest hire rate (~40%), followed by LinkedIn. Time-to-hire averages 30–45 days.

4. **Attendance:** 78.6% present rate. Sick/leave rates spike on Mondays and Fridays — a pattern consistent with real workforce behavior.

5. **Performance:** Top performers consistently score above 85 KPI. A weak-positive correlation exists between training completion and KPI scores, supporting investment in employee development.

## SQL Techniques Used

- **Window Functions:** `RANK() OVER (PARTITION BY department ORDER BY salary DESC)` — salary ranking per dept
- **Subqueries:** Correlative subquery comparing individual training scores against employee's average KPI
- **Aggregation:** `GROUP BY`, `CASE WHEN`, `HAVING` across 7 analysis categories
- **Data Cleaning:** NULL handling, `DISTINCT ON` deduplication, category normalization, referential integrity validation
- **Derived Columns:** Leave duration calculated as `end_date - start_date`

## Business Questions Answered

See [analysis.sql](database/analysis.sql) for all 22 queries.

| Category | Questions |
|----------|-----------|
| Employee | Active vs inactive counts. Composition by dept, position, gender. |
| Payroll | Average salary. Top earners. Salary rank per department (window function). |
| Attendance | Status distribution. Monthly trends. Late check-in patterns. |
| Turnover | Turnover rate (%). Turnover by department. Status breakdown. |
| Recruitment | Funnel conversion. Best hiring sources. Average time-to-hire. |
| Performance | Top/bottom performers. KPI trends per quarter. |
| Training | Course effectiveness. Training completion vs KPI correlation. |

## Status

**Complete** — All 4 levels per roadmap.

## Future Development

- Star schema migration (fact & dimension tables) for data warehousing practice
- Python ETL automation with pandas to replace manual import
- Power BI interactive dashboard with direct DB connection
- Predictive analytics: turnover risk modeling using Python
