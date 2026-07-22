"""
HR Analytics System — Export Analysis Results to CSV
Reads clean CSV files, runs analysis queries in pandas,
exports results to dashboard/analysis_results/ for spreadsheet import.

Run: python dataset/export_analysis.py
Output: dashboard/analysis_results/*.csv
"""

import os
import sys
import pandas as pd
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "dataset")
OUT_DIR = os.path.join(BASE, "dashboard", "analysis_results")
os.makedirs(OUT_DIR, exist_ok=True)


def load():
    dept = pd.read_csv(os.path.join(DATA_DIR, "department.csv"))
    pos = pd.read_csv(os.path.join(DATA_DIR, "position.csv"))
    emp = pd.read_csv(os.path.join(DATA_DIR, "employee.csv"))
    att = pd.read_csv(os.path.join(DATA_DIR, "attendance.csv"))
    lev = pd.read_csv(os.path.join(DATA_DIR, "leave.csv"))
    perf = pd.read_csv(os.path.join(DATA_DIR, "performance.csv"))
    rec = pd.read_csv(os.path.join(DATA_DIR, "recruitment.csv"))
    train = pd.read_csv(os.path.join(DATA_DIR, "training.csv"))
    return dept, pos, emp, att, lev, perf, rec, train


# ── Employee Overview ──────────────────────────────────────────

def emp_overview(emp, dept, pos):
    em = emp.merge(dept, on="department_id").merge(pos, on="position_id")

    # 1. Status breakdown
    status_counts = em["status"].value_counts().reset_index()
    status_counts.columns = ["status", "total"]

    # 2. Per department
    dept_counts = em.groupby("department_name").size().reset_index(name="total_employees")
    dept_counts = dept_counts.sort_values("total_employees", ascending=False)

    # 3. Per position
    pos_counts = em.groupby("position_name").size().reset_index(name="total_employees")
    pos_counts = pos_counts.sort_values("total_employees", ascending=False)

    # 4. Gender composition (active only)
    active = em[em["status"] == "Active"]
    gender_counts = active["gender"].value_counts().reset_index()
    gender_counts.columns = ["gender", "total"]
    gender_counts["percentage"] = (100 * gender_counts["total"] / gender_counts["total"].sum()).round(2)

    # 5. Active employees per dept
    active_dept = active.groupby("department_name").size().reset_index(name="active_employees")

    status_counts.to_csv(os.path.join(OUT_DIR, "emp_status.csv"), index=False)
    dept_counts.to_csv(os.path.join(OUT_DIR, "emp_department.csv"), index=False)
    pos_counts.to_csv(os.path.join(OUT_DIR, "emp_position.csv"), index=False)
    gender_counts.to_csv(os.path.join(OUT_DIR, "emp_gender.csv"), index=False)
    active_dept.to_csv(os.path.join(OUT_DIR, "emp_active_dept.csv"), index=False)
    print("  emp_status.csv, emp_department.csv, emp_position.csv, emp_gender.csv")


# ── Payroll ────────────────────────────────────────────────────

def payroll(emp, dept):
    em = emp.merge(dept, on="department_id")

    # Overall
    active = em[em["status"] == "Active"]
    overall = active["salary"].agg(["mean", "min", "max"]).round(2).reset_index()
    overall.columns = ["metric", "value"]

    # Per department
    dept_payroll = active.groupby("department_name")["salary"].agg(["mean", "min", "max"]).round(2).reset_index()
    dept_payroll = dept_payroll.sort_values("mean", ascending=False)

    # Top 10
    top10 = active.nlargest(10, "salary")[["full_name", "department_name", "salary"]]

    # Salary rank per dept
    active["salary_rank"] = active.groupby("department_name")["salary"].rank(method="dense", ascending=False)
    rank = active.sort_values(["department_name", "salary_rank"])[
        ["full_name", "department_name", "salary", "salary_rank"]
    ]

    overall.to_csv(os.path.join(OUT_DIR, "payroll_overall.csv"), index=False)
    dept_payroll.to_csv(os.path.join(OUT_DIR, "payroll_department.csv"), index=False)
    top10.to_csv(os.path.join(OUT_DIR, "payroll_top10.csv"), index=False)
    rank.to_csv(os.path.join(OUT_DIR, "payroll_rank.csv"), index=False)
    print("  payroll_overall.csv, payroll_department.csv, payroll_top10.csv, payroll_rank.csv")


# ── Attendance ─────────────────────────────────────────────────

def attendance(att, emp):
    a = att.copy()
    a["month"] = pd.to_datetime(a["date"]).dt.to_period("M").astype(str)

    # Distribution
    status_dist = a["status"].value_counts().reset_index()
    status_dist.columns = ["status", "total"]
    status_dist["percentage"] = (100 * status_dist["total"] / status_dist["total"].sum()).round(2)

    # Monthly trend
    monthly = a.groupby(["month", "status"]).size().reset_index(name="total")
    monthly = monthly.sort_values(["month", "status"])

    # Late check-in
    a["check_in_dt"] = pd.to_datetime(a["check_in"], format="%H:%M:%S", errors="coerce")
    late = a[(a["status"] == "Present") & (a["check_in_dt"].dt.hour >= 9)]
    late_counts = late.groupby("employee_id").size().reset_index(name="late_days")
    late_top = late_counts.merge(emp[["employee_id", "full_name"]], on="employee_id")
    late_top = late_top.sort_values("late_days", ascending=False).head(10)

    status_dist.to_csv(os.path.join(OUT_DIR, "attendance_status.csv"), index=False)
    monthly.to_csv(os.path.join(OUT_DIR, "attendance_monthly.csv"), index=False)
    late_top.to_csv(os.path.join(OUT_DIR, "attendance_late.csv"), index=False)
    print("  attendance_status.csv, attendance_monthly.csv, attendance_late.csv")


# ── Turnover ───────────────────────────────────────────────────

def turnover(emp, dept):
    em = emp.merge(dept, on="department_id")
    total = len(em)
    turnover_rate = round(100 * em["status"].ne("Active").sum() / total, 2)

    # Per dept
    dept_turn = em.groupby("department_name").agg(
        total_employees=("employee_id", "count"),
        left_count=("status", lambda x: (x != "Active").sum()),
    ).reset_index()
    dept_turn["turnover_percent"] = (100 * dept_turn["left_count"] / dept_turn["total_employees"]).round(2)
    dept_turn = dept_turn.sort_values("turnover_percent", ascending=False)

    rate_df = pd.DataFrame({"metric": ["turnover_rate_percent"], "value": [turnover_rate]})
    rate_df.to_csv(os.path.join(OUT_DIR, "turnover_rate.csv"), index=False)
    dept_turn.to_csv(os.path.join(OUT_DIR, "turnover_department.csv"), index=False)
    print("  turnover_rate.csv, turnover_department.csv")


# ── Recruitment ────────────────────────────────────────────────

def recruitment(rec):
    # Funnel
    funnel_order = {"Applied": 1, "Interviewed": 2, "Hired": 3, "Rejected": 4}
    funnel = rec["status"].value_counts().reset_index()
    funnel.columns = ["status", "candidates"]
    funnel["order"] = funnel["status"].map(funnel_order)
    funnel = funnel.sort_values("order").drop(columns="order")

    # Source performance
    source = rec.groupby("source").agg(
        total=("candidate_id", "count"),
        hired=("status", lambda x: (x == "Hired").sum()),
    ).reset_index()
    source["hire_rate_percent"] = (100 * source["hired"] / source["total"]).round(2)
    source = source.sort_values("hire_rate_percent", ascending=False)

    # Time to hire
    hired = rec[rec["status"] == "Hired"].copy()
    hired["apply_date"] = pd.to_datetime(hired["apply_date"])
    hired["hire_date"] = pd.to_datetime(hired["hire_date"])
    hired["days_to_hire"] = (hired["hire_date"] - hired["apply_date"]).dt.days
    avg_days = round(hired["days_to_hire"].mean(), 0)
    tth = pd.DataFrame({"metric": ["avg_days_to_hire"], "value": [avg_days]})

    funnel.to_csv(os.path.join(OUT_DIR, "recruitment_funnel.csv"), index=False)
    source.to_csv(os.path.join(OUT_DIR, "recruitment_source.csv"), index=False)
    tth.to_csv(os.path.join(OUT_DIR, "recruitment_timetohire.csv"), index=False)
    print("  recruitment_funnel.csv, recruitment_source.csv, recruitment_timetohire.csv")


# ── Performance ────────────────────────────────────────────────

def performance(perf, emp, dept):
    p = perf.merge(emp, on="employee_id").merge(dept, on="department_id")

    # Avg per period
    period_avg = p.groupby("period")[["kpi_score", "manager_score"]].mean().round(2).reset_index()

    # Top 10 performers
    emp_avg = p[p["status"] == "Active"].groupby(["employee_id", "full_name", "department_name"])["kpi_score"].mean().round(2).reset_index()
    emp_avg.columns = ["employee_id", "full_name", "department_name", "avg_kpi"]
    emp_avg["rank"] = emp_avg["avg_kpi"].rank(method="dense", ascending=False)
    top10 = emp_avg.sort_values("avg_kpi", ascending=False).head(10)
    bottom10 = emp_avg.sort_values("avg_kpi", ascending=True).head(10)

    period_avg.to_csv(os.path.join(OUT_DIR, "performance_period.csv"), index=False)
    top10.to_csv(os.path.join(OUT_DIR, "performance_top10.csv"), index=False)
    bottom10.to_csv(os.path.join(OUT_DIR, "performance_bottom10.csv"), index=False)
    print("  performance_period.csv, performance_top10.csv, performance_bottom10.csv")


# ── Training ───────────────────────────────────────────────────

def training(train, perf, emp):
    t = train.merge(perf, on="employee_id").merge(emp[["employee_id", "full_name"]], on="employee_id")

    # Avg score per course
    course_avg = t[t["score"].notna()].groupby("course_name").agg(
        participants=("employee_id", "count"),
        avg_score=("score", "mean"),
    ).round(2).reset_index().sort_values("avg_score", ascending=False)

    # Avg KPI by completion
    completion_kpi = t.groupby("completion").agg(
        records=("employee_id", "count"),
        avg_kpi=("kpi_score", "mean"),
    ).round(2).reset_index().sort_values("avg_kpi", ascending=False)

    # Training score vs avg KPI
    completed = t[t["completion"] == "Completed"].copy()
    emp_avg_kpi = perf.groupby("employee_id")["kpi_score"].mean().round(2).reset_index()
    emp_avg_kpi.columns = ["employee_id", "employee_avg_kpi"]
    correlation = completed.merge(emp_avg_kpi, on="employee_id")[
        ["full_name", "course_name", "score", "employee_avg_kpi"]
    ].drop_duplicates().sort_values("employee_avg_kpi", ascending=False).head(20)

    course_avg.to_csv(os.path.join(OUT_DIR, "training_course_avg.csv"), index=False)
    completion_kpi.to_csv(os.path.join(OUT_DIR, "training_completion_kpi.csv"), index=False)
    correlation.to_csv(os.path.join(OUT_DIR, "training_correlation.csv"), index=False)
    print("  training_course_avg.csv, training_completion_kpi.csv, training_correlation.csv")


# ── Main ───────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading CSVs...")
    dept, pos, emp, att, lev, perf, rec, train = load()
    print("Exporting analysis results...")
    emp_overview(emp, dept, pos)
    payroll(emp, dept)
    attendance(att, emp)
    turnover(emp, dept)
    recruitment(rec)
    performance(perf, emp, dept)
    training(train, perf, emp)
    print(f"\nAll exported to {OUT_DIR}/")
