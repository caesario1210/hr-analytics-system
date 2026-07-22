-- ============================================================
-- HR Analytics System — Data Cleaning
-- Transform *_raw staging tables into clean final tables.
-- ============================================================

-- ── Department ────────────────────────────────────────────────
INSERT INTO department (department_id, department_name)
SELECT DISTINCT department_id, department_name
FROM department_raw
WHERE department_id IS NOT NULL
  AND department_name IS NOT NULL
ON CONFLICT (department_id) DO NOTHING;

-- ── Position ──────────────────────────────────────────────────
INSERT INTO position (position_id, position_name, grade)
SELECT DISTINCT position_id, position_name, grade
FROM position_raw
WHERE position_id IS NOT NULL
  AND position_name IS NOT NULL;

-- ── Employee ──────────────────────────────────────────────────
INSERT INTO employee (employee_id, full_name, gender, birth_date,
                      hire_date, department_id, position_id, salary, status)
SELECT
    e.employee_id,
    e.full_name,
    CASE
        WHEN UPPER(TRIM(e.gender)) IN ('M', 'MALE') THEN 'Male'
        WHEN UPPER(TRIM(e.gender)) IN ('F', 'FEMALE') THEN 'Female'
        ELSE e.gender
    END AS gender,
    e.birth_date::DATE,
    e.hire_date::DATE,
    e.department_id,
    e.position_id,
    e.salary,
    CASE
        WHEN UPPER(TRIM(e.status)) IN ('ACTIVE', 'A') THEN 'Active'
        WHEN UPPER(TRIM(e.status)) IN ('RESIGNED', 'RESIGN', 'R') THEN 'Resigned'
        WHEN UPPER(TRIM(e.status)) IN ('TERMINATED', 'TERM', 'T') THEN 'Terminated'
        ELSE 'Active'
    END AS status
FROM employee_raw e
WHERE e.employee_id IS NOT NULL
  AND e.full_name IS NOT NULL
  AND e.department_id IN (SELECT department_id FROM department)
  AND e.position_id IN (SELECT position_id FROM position);

-- ── Attendance ────────────────────────────────────────────────
INSERT INTO attendance (employee_id, date, check_in, check_out, status)
SELECT DISTINCT ON (a.employee_id, a.date)
    a.employee_id,
    a.date::DATE,
    NULLIF(TRIM(a.check_in::text), '')::TIME,
    NULLIF(TRIM(a.check_out::text), '')::TIME,
    CASE
        WHEN UPPER(TRIM(a.status)) IN ('PRESENT', 'P') THEN 'Present'
        WHEN UPPER(TRIM(a.status)) IN ('SICK', 'S')  THEN 'Sick'
        WHEN UPPER(TRIM(a.status)) IN ('LEAVE', 'L')  THEN 'Leave'
        WHEN UPPER(TRIM(a.status)) IN ('ABSENT', 'A') THEN 'Absent'
        ELSE 'Absent'
    END AS status
FROM attendance_raw a
JOIN employee e ON a.employee_id = e.employee_id
WHERE a.employee_id IS NOT NULL
  AND a.date IS NOT NULL
ORDER BY a.employee_id, a.date, a.attendance_id;

-- ── Leave ─────────────────────────────────────────────────────
INSERT INTO leave_request (leave_id, employee_id, leave_type, start_date, end_date, duration)
SELECT
    l.leave_id,
    l.employee_id,
    INITCAP(TRIM(l.leave_type)),
    l.start_date::DATE,
    l.end_date::DATE,
    COALESCE(l.duration, (l.end_date::DATE - l.start_date::DATE))
FROM leave_request_raw l
JOIN employee e ON l.employee_id = e.employee_id
WHERE l.leave_id IS NOT NULL
  AND l.employee_id IS NOT NULL
  AND l.start_date IS NOT NULL
  AND l.end_date IS NOT NULL;

-- ── Performance ───────────────────────────────────────────────
INSERT INTO performance (employee_id, period, kpi_score, manager_score)
SELECT DISTINCT
    p.employee_id,
    p.period,
    p.kpi_score,
    p.manager_score
FROM performance_raw p
JOIN employee e ON p.employee_id = e.employee_id
WHERE p.employee_id IS NOT NULL
  AND p.period IS NOT NULL;

-- ── Recruitment ───────────────────────────────────────────────
INSERT INTO recruitment (candidate_id, candidate_name, position, source, status, apply_date, hire_date)
SELECT
    r.candidate_id,
    r.candidate_name,
    r.position,
    INITCAP(TRIM(r.source)),
    INITCAP(TRIM(r.status)),
    r.apply_date::DATE,
    NULLIF(TRIM(r.hire_date::text), '')::DATE
FROM recruitment_raw r
WHERE r.candidate_id IS NOT NULL
  AND r.candidate_name IS NOT NULL;

-- ── Training ──────────────────────────────────────────────────
INSERT INTO training (training_id, employee_id, course_name, completion, score)
SELECT
    t.training_id,
    t.employee_id,
    t.course_name,
    CASE
        WHEN UPPER(TRIM(t.completion)) IN ('COMPLETED', 'C')  THEN 'Completed'
        WHEN UPPER(TRIM(t.completion)) IN ('IN PROGRESS', 'IP') THEN 'In Progress'
        WHEN UPPER(TRIM(t.completion)) IN ('NOT STARTED', 'NS') THEN 'Not Started'
        ELSE t.completion
    END AS completion,
    t.score
FROM training_raw t
JOIN employee e ON t.employee_id = e.employee_id
WHERE t.training_id IS NOT NULL
  AND t.employee_id IS NOT NULL
  AND t.course_name IS NOT NULL;
