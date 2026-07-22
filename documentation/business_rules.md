# Business Rules — HR Analytics System

## Employee Rules

| Rule | Definition |
|------|-----------|
| **Employee Status** | `Active` = currently employed. `Resigned` = voluntarily left. `Terminated` = involuntarily dismissed. |
| **Active Employee** | An employee whose `status = 'Active'` on the current date. |
| **Turnover** | Percentage of non-active employees (Resigned + Terminated) against total headcount. |
| **Tenure** | Calculated as `CURRENT_DATE - hire_date`. Used to model resignation probability. |

## Salary Rules

| Rule | Definition |
|------|-----------|
| **Base Salary** | Determined by position `grade` (G1–G5). Higher grade = higher base. |
| **Department Multiplier** | Adjusts base salary by department. IT/Legal have higher multipliers; Admin/HR have lower. |
| **Final Salary** | `base_salary × department_multiplier × (1 + noise)` where noise ~ Normal(0, 0.08). |
| **Rounding** | All salaries rounded to nearest thousand. |

### Grade Levels

| Grade | Base Salary | Typical Positions |
|-------|------------|-------------------|
| G1 | Rp 5,000,000 | Junior Developer, Operations Associate, HR Staff, Admin Staff |
| G2 | Rp 7,500,000 | Data Analyst, Accountant, Sales Representative, Marketing Specialist |
| G3 | Rp 11,000,000 | Senior Developer, Financial Analyst, Legal Counsel |
| G4 | Rp 16,000,000 | IT Manager, Finance Manager, Sales Manager, Marketing Manager, etc. |
| G5 | Rp 25,000,000 | Legal Manager (senior leadership) |

### Department Multipliers

| Department | Multiplier |
|-----------|-----------|
| Legal | 1.30 |
| IT | 1.25 |
| Finance | 1.20 |
| Sales | 1.10 |
| Marketing | 1.05 |
| Operations | 1.00 |
| HR | 0.95 |
| Admin | 0.90 |

## Attendance Rules

| Rule | Definition |
|------|-----------|
| **Present** | Employee clocked in and out on a working day. `check_in` ≤ 09:00 is on-time. |
| **Late** | `check_in > 09:00` while status is Present. |
| **Sick** | Employee reported sick (higher probability on Mondays/Fridays). |
| **Leave** | Employee on approved leave (higher probability on Mondays/Fridays). |
| **Absent** | No check-in record without prior notification. |
| **Working Days** | Monday–Friday only. Weekends excluded from attendance. |

## Leave Rules

| Rule | Definition |
|------|-----------|
| **Leave Types** | Annual, Sick, Maternity, Paternity, Personal. |
| **Duration** | Derived column: `end_date - start_date`. Default to 1 if null. |
| **Annual Leave** | Typically 5–12 days per request. |
| **Sick Leave** | Typically 1–5 days per request. |

## Performance Rules

| Rule | Definition |
|------|-----------|
| **KPI Score** | Numeric 0–100. Employee-level key performance indicator. |
| **Manager Score** | Numeric 0–100. Manager evaluation (may differ from KPI). |
| **Period** | Quarterly format: `YYYY-Q#` (e.g., 2025-Q1). |
| **Top Performer** | Employee with highest average KPI score across all periods. |
| **Bottom Performer** | Employee with lowest average KPI score across all periods. |

## Recruitment Rules

| Rule | Definition |
|------|-----------|
| **Funnel Stages** | Applied → Interviewed → Hired → Rejected. |
| **Hired** | Candidate who received and accepted an offer. Requires `hire_date`. |
| **Time-to-Hire** | Days between `apply_date` and `hire_date` for hired candidates. |
| **Source** | Recruitment channel: LinkedIn, Job Portal, Referral, Company Website, University. |
| **Referral Priority** | Referral source has the highest expected hire rate (~40%). |

## Training Rules

| Rule | Definition |
|------|-----------|
| **Completion Status** | `Completed`, `In Progress`, or `Not Started`. |
| **Training Score** | Numeric 0–100. Only available for completed courses. |
| **Effectiveness** | Measured by comparing avg KPI of employees who completed training vs those who didn't. |
| **Correlation** | A weak-positive correlation exists between training completion and KPI scores. |

## Data Quality Rules

| Rule | Standard |
|------|---------|
| **Naming Convention** | All tables and columns use `snake_case`, singular form (e.g., `employee` not `employees`). |
| **Raw Tables** | Suffixed with `_raw` (e.g., `employee_raw`). No FK constraints — allows invalid data before cleaning. |
| **Date Format** | Standardized to ISO 8601 (`YYYY-MM-DD`) in final tables. Raw tables accept TEXT. |
| **Gender Values** | Normalized to `Male` / `Female` during cleaning. Raw may contain `M`/`F`. |
| **Reproducibility** | All data generation uses `seed=42` for deterministic output. |
