"""
HR Analytics System — Dummy Data Generator
Generates 8 CSV files with realistic distributions.
Design: design.md §4 (Salary Formula), §3 (Schema), task.md §1.1
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import date

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Config ──────────────────────────────────────────────────────────
N_EMPLOYEES = 300
N_MONTHS = 6
WORK_DAYS_PER_MONTH = 22
N_ATTENDANCE = N_EMPLOYEES * WORK_DAYS_PER_MONTH * N_MONTHS  # ~39,600

DEPARTMENTS = [
    "IT", "Finance", "Sales", "Marketing",
    "Operations", "HR", "Admin", "Legal"
]

POSITIONS = [
    ("Junior Developer",    "G1", "IT"),
    ("Senior Developer",    "G3", "IT"),
    ("IT Manager",          "G4", "IT"),
    ("Data Analyst",        "G2", "IT"),
    ("Accountant",          "G2", "Finance"),
    ("Finance Manager",     "G4", "Finance"),
    ("Financial Analyst",   "G3", "Finance"),
    ("Sales Representative","G2", "Sales"),
    ("Sales Manager",       "G4", "Sales"),
    ("Marketing Specialist","G2", "Marketing"),
    ("Marketing Manager",   "G4", "Marketing"),
    ("Operations Associate","G1", "Operations"),
    ("Operations Manager",  "G4", "Operations"),
    ("HR Staff",            "G1", "HR"),
    ("HR Manager",          "G4", "HR"),
    ("Admin Staff",         "G1", "Admin"),
    ("Admin Manager",       "G4", "Admin"),
    ("Legal Counsel",       "G3", "Legal"),
    ("Legal Manager",       "G5", "Legal"),
]

BASE_SALARY = {
    "G1": 5_000_000,
    "G2": 7_500_000,
    "G3": 11_000_000,
    "G4": 16_000_000,
    "G5": 25_000_000,
}

DEPT_MULTIPLIER = {
    "IT": 1.25, "Finance": 1.20, "Sales": 1.10,
    "Marketing": 1.05, "Operations": 1.00,
    "HR": 0.95, "Admin": 0.90, "Legal": 1.30,
}

GENDERS = ["Male", "Female"]
LEAVE_TYPES = ["Annual", "Sick", "Maternity", "Paternity", "Personal"]
RECRUITMENT_SOURCES = ["LinkedIn", "Job Portal", "Referral", "Company Website", "University"]
ATTENDANCE_STATUS = ["Present", "Present", "Present", "Present", "Present",
                     "Present", "Sick", "Leave", "Absent", "Absent"]  # ~70% present
COURSES = [
    "Leadership Essentials", "Data Literacy", "Communication Skills",
    "Project Management", "Cloud Computing", "Advanced Excel",
    "Public Speaking", "Time Management", "Conflict Resolution",
]

# ── Helpers ─────────────────────────────────────────────────────────
def generate_salary(grade, department):
    base = BASE_SALARY[grade]
    mult = DEPT_MULTIPLIER[department]
    noise = np.random.normal(loc=0, scale=0.08)
    salary = base * mult * (1 + noise)
    return round(salary, -3)



def random_date(start_year, end_year):
    return fake.date_between(
        start_date=date(start_year, 1, 1), 
        end_date=date(end_year, 12, 31)
    )


# ── 1. Department ───────────────────────────────────────────────────
def gen_department():
    df = pd.DataFrame({
        "department_id": range(1, len(DEPARTMENTS) + 1),
        "department_name": DEPARTMENTS,
    })
    df.to_csv(os.path.join(OUT_DIR, "department.csv"), index=False)
    print(f"department.csv — {len(df)} rows")
    return df


# ── 2. Position ─────────────────────────────────────────────────────
def gen_position():
    rows = []
    for i, (name, grade, dept) in enumerate(POSITIONS, 1):
        rows.append({"position_id": i, "position_name": name, "grade": grade, "department": dept})
    df = pd.DataFrame(rows)
    # Export only columns matching the schema (drop 'department' — used internally for generation only)
    df[["position_id", "position_name", "grade"]].to_csv(
        os.path.join(OUT_DIR, "position.csv"), index=False
    )
    print(f"position.csv — {len(df)} rows")
    return df


# ── 3. Employee ─────────────────────────────────────────────────────
def gen_employee(dept_df, pos_df):
    rows = []
    for emp_id in range(1, N_EMPLOYEES + 1):
        dept_id = random.choice(dept_df["department_id"].tolist())
        dept_name = dept_df.loc[dept_df["department_id"] == dept_id, "department_name"].iloc[0]

        # Pick a position matching the department
        dept_positions = pos_df[pos_df["department"] == dept_name]
        pos_row = dept_positions.sample(1).iloc[0]
        pos_id = pos_row["position_id"]
        grade = pos_row["grade"]

        hire_date = random_date(2015, 2025)
        tenure_years = (pd.Timestamp("2025-06-30") - pd.Timestamp(hire_date)).days / 365.25

        # Higher resignation probability at years 2-3
        if 2 <= tenure_years <= 3:
            status = np.random.choice(["Active", "Resigned", "Terminated"], p=[0.60, 0.30, 0.10])
        elif tenure_years < 1:
            status = np.random.choice(["Active", "Resigned"], p=[0.95, 0.05])
        else:
            status = np.random.choice(["Active", "Resigned", "Terminated"], p=[0.85, 0.10, 0.05])

        salary = generate_salary(grade, dept_name)
        gender = random.choice(GENDERS)
        birth_date = random_date(1970, 2000)
        full_name = fake.name_male() if gender == "Male" else fake.name_female()

        rows.append({
            "employee_id": emp_id,
            "full_name": full_name,
            "gender": gender,
            "birth_date": birth_date,
            "hire_date": hire_date,
            "department_id": dept_id,
            "position_id": pos_id,
            "salary": salary,
            "status": status,
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "employee.csv"), index=False)
    print(f"employee.csv — {len(df)} rows")
    return df


# ── 4. Attendance ───────────────────────────────────────────────────
def gen_attendance(emp_df):
    rows = []
    start = pd.Timestamp("2025-01-01")
    all_employees = emp_df["employee_id"].tolist()

    for day_offset in range(N_MONTHS * WORK_DAYS_PER_MONTH):
        date = start + pd.Timedelta(days=day_offset)
        if date.weekday() >= 5:
            continue
        # Higher sick/leave on Monday/Friday
        is_monday_friday = date.weekday() in (0, 4)
        for emp_id in all_employees:
            if is_monday_friday:
                status = np.random.choice(
                    ["Present", "Present", "Present", "Sick", "Sick", "Leave", "Absent"],
                    p=[0.50, 0.10, 0.10, 0.10, 0.05, 0.10, 0.05],
                )
            else:
                status = np.random.choice(
                    ["Present", "Present", "Present", "Present", "Present", "Sick", "Leave", "Absent"],
                    p=[0.60, 0.10, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
                )

            check_in = None
            check_out = None
            if status == "Present":
                hour_in = np.random.randint(7, 10)
                min_in = np.random.randint(0, 60)
                check_in = f"{hour_in:02d}:{min_in:02d}:00"
                hour_out = np.random.randint(16, 19)
                min_out = np.random.randint(0, 60)
                check_out = f"{hour_out:02d}:{min_out:02d}:00"

            rows.append({
                "employee_id": emp_id,
                "date": date.date(),
                "check_in": check_in,
                "check_out": check_out,
                "status": status,
            })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "attendance.csv"), index=False)
    print(f"attendance.csv — {len(df)} rows")
    return df


# ── 5. Leave ────────────────────────────────────────────────────────
def gen_leave(emp_df):
    rows = []
    all_employees = emp_df["employee_id"].tolist()
    target = np.random.randint(500, 801)
    leave_id = 1
    for emp_id in all_employees:
        n_leaves = np.random.poisson(2)  # avg 2 leaves per year
        for _ in range(n_leaves):
            if leave_id > target:
                break
            start = random_date(2024, 2025)
            duration = np.random.randint(1, 15)
            end = pd.Timestamp(start) + pd.Timedelta(days=duration)
            leave_type = np.random.choice(LEAVE_TYPES, p=[0.35, 0.30, 0.10, 0.05, 0.20])
            rows.append({
                "leave_id": leave_id,
                "employee_id": emp_id,
                "leave_type": leave_type,
                "start_date": start,
                "end_date": end.date(),
                "duration": duration,
            })
            leave_id += 1
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "leave.csv"), index=False)
    print(f"leave.csv — {len(df)} rows")
    return df


# ── 6. Performance ──────────────────────────────────────────────────
def gen_performance(emp_df):
    rows = []
    periods = [f"2025-Q{i}" for i in range(1, 5)]
    for emp_id in emp_df["employee_id"]:
        base_kpi = np.random.normal(75, 10)
        base_manager = np.random.normal(75, 10)
        for period in periods:
            kpi_score = max(0, min(100, round(np.random.normal(base_kpi, 5), 2)))
            manager_score = max(0, min(100, round(np.random.normal(base_manager, 5), 2)))
            rows.append({
                "employee_id": emp_id,
                "period": period,
                "kpi_score": kpi_score,
                "manager_score": manager_score,
            })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "performance.csv"), index=False)
    print(f"performance.csv — {len(df)} rows")
    return df


# ── 7. Recruitment ──────────────────────────────────────────────────
def gen_recruitment():
    rows = []
    n_candidates = np.random.randint(150, 251)
    for cid in range(1, n_candidates + 1):
        source = np.random.choice(RECRUITMENT_SOURCES, p=[0.30, 0.25, 0.20, 0.15, 0.10])
        # hire rate differs by source
        hire_probs = {
            "LinkedIn": 0.30, "Job Portal": 0.15, "Referral": 0.40,
            "Company Website": 0.25, "University": 0.20,
        }
        if np.random.random() < hire_probs[source]:
            status = "Hired"
        else:
            status = np.random.choice(
                ["Applied", "Interviewed", "Rejected"],
                p=[0.10, 0.20, 0.70],
            )
        apply_date = random_date(2024, 2025)
        hire_date = None
        if status == "Hired":
            hire_date = (pd.Timestamp(apply_date) + pd.Timedelta(days=np.random.randint(14, 60))).date()
        rows.append({
            "candidate_id": cid,
            "candidate_name": fake.name(),
            "position": np.random.choice([p[0] for p in POSITIONS]),
            "source": source,
            "status": status,
            "apply_date": apply_date,
            "hire_date": hire_date,
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "recruitment.csv"), index=False)
    print(f"recruitment.csv — {len(df)} rows")
    return df


# ── 8. Training ─────────────────────────────────────────────────────
def gen_training(emp_df, perf_df):
    rows = []
    train_id = 1
    for emp_id in emp_df["employee_id"]:
        n_courses = np.random.randint(1, 4)
        emp_courses = np.random.choice(COURSES, n_courses, replace=False)
        emp_avg_kpi = perf_df[perf_df["employee_id"] == emp_id]["kpi_score"].mean()
        for course in emp_courses:
            completion = np.random.choice(
                ["Completed", "Completed", "Completed", "In Progress", "Not Started"],
                p=[0.50, 0.15, 0.10, 0.15, 0.10],
            )
            score = None
            if completion == "Completed":
                base = emp_avg_kpi + np.random.normal(5, 8)
                score = max(0, min(100, round(base, 2)))
            rows.append({
                "training_id": train_id,
                "employee_id": emp_id,
                "course_name": course,
                "completion": completion,
                "score": score,
            })
            train_id += 1
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "training.csv"), index=False)
    print(f"training.csv — {len(df)} rows")
    return df


# ── Main ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating HR dummy data...")
    dept = gen_department()
    pos = gen_position()
    emp = gen_employee(dept, pos)
    att = gen_attendance(emp)
    lev = gen_leave(emp)
    perf = gen_performance(emp)
    rec = gen_recruitment()
    train = gen_training(emp, perf)
    print("\nAll CSV files generated in dataset/")
