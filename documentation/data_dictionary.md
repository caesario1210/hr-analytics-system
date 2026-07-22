# Data Dictionary — HR Analytics System

## Table: `department`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| department_id | INT (PK) | Unique identifier | 1 |
| department_name | VARCHAR(100) | Department name | IT |

## Table: `position`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| position_id | INT (PK) | Unique identifier | 1 |
| position_name | VARCHAR(100) | Job title | Senior Developer |
| grade | VARCHAR(10) | Grade level (G1–G5) | G3 |

## Table: `employee`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| employee_id | INT (PK) | Unique identifier | 101 |
| full_name | VARCHAR(150) | Employee full name | John Doe |
| gender | VARCHAR(10) | Gender (Male/Female) | Male |
| birth_date | DATE | Date of birth | 1988-03-15 |
| hire_date | DATE | Hire date | 2020-06-01 |
| department_id | INT (FK) | Refers to department | 2 |
| position_id | INT (FK) | Refers to position | 5 |
| salary | NUMERIC(12,2) | Monthly salary | 12500000.00 |
| status | VARCHAR(20) | Active / Resigned / Terminated | Active |

## Table: `attendance`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| attendance_id | INT (PK) | Auto-generated | 1 |
| employee_id | INT (FK) | Refers to employee | 101 |
| date | DATE | Attendance date | 2025-03-10 |
| check_in | TIME | Clock-in time | 08:15:00 |
| check_out | TIME | Clock-out time | 17:30:00 |
| status | VARCHAR(20) | Present / Sick / Leave / Absent | Present |

## Table: `leave_request`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| leave_id | INT (PK) | Unique identifier | 501 |
| employee_id | INT (FK) | Refers to employee | 101 |
| leave_type | VARCHAR(50) | Annual / Sick / Maternity / Paternity / Personal | Annual |
| start_date | DATE | Leave start date | 2025-04-10 |
| end_date | DATE | Leave end date | 2025-04-14 |
| duration | INT | Number of days (derived) | 5 |

## Table: `performance`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| performance_id | INT (PK) | Auto-generated | 1 |
| employee_id | INT (FK) | Refers to employee | 101 |
| period | VARCHAR(10) | Quarter (e.g. 2025-Q1) | 2025-Q1 |
| kpi_score | NUMERIC(5,2) | KPI score (0–100) | 82.50 |
| manager_score | NUMERIC(5,2) | Manager evaluation score | 78.00 |

## Table: `recruitment`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| candidate_id | INT (PK) | Unique identifier | 1001 |
| candidate_name | VARCHAR(150) | Candidate full name | Jane Smith |
| position | VARCHAR(100) | Position applied | Data Analyst |
| source | VARCHAR(50) | Recruitment channel | LinkedIn |
| status | VARCHAR(30) | Applied / Interviewed / Hired / Rejected | Hired |
| apply_date | DATE | Application date | 2025-02-01 |
| hire_date | DATE | Hire date (nullable) | 2025-03-15 |

## Table: `training`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| training_id | INT (PK) | Unique identifier | 2001 |
| employee_id | INT (FK) | Refers to employee | 101 |
| course_name | VARCHAR(150) | Course name | Leadership Essentials |
| completion | VARCHAR(20) | Completed / In Progress / Not Started | Completed |
| score | NUMERIC(5,2) | Training score (nullable) | 85.00 |

---

## Data Generation Rules

| Rule | Detail |
|------|--------|
| Seed | `random.seed(42)`, `np.random.seed(42)`, `Faker.seed(42)` |
| Salary | `base_salary_per_grade × department_multiplier × (1 + noise)` where `noise ~ N(0, 0.08)` |
| Employees | 300 rows, ~70% Active, ~15% Resigned, ~5% Terminated |
| Resignation spike | Higher probability at 2–3 year tenure range |
| Attendance | ~39,600 rows (300 emp × 22 days × 6 months); higher Sick/Leave on Mon/Fri |
| Performance | Base KPI ~ N(75, 10), per-period variation ~ N(base, 5) |
| Recruitment | 150–250 candidates; hire rate varies by source (Referral highest, Job Portal lowest) |
| Training | 1–3 courses per employee; weak-positive correlation between completion and KPI score |
