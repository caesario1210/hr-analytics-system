-- ============================================================
-- HR Analytics System — Business Analysis Queries
-- Categories: Employee, Payroll, Attendance, Turnover,
--             Recruitment, Performance, Training
-- ============================================================

-- ── EMPLOYEE OVERVIEW ────────────────────────────────────────

-- 1. Total active vs non-active
SELECT
    status,
    COUNT(*) AS total
FROM employee
GROUP BY status
ORDER BY total DESC;

-- 2. Employees per department
SELECT
    d.department_name,
    COUNT(*) AS total_employees
FROM employee e
JOIN department d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY total_employees DESC;

-- 3. Employees per position
SELECT
    p.position_name,
    COUNT(*) AS total_employees
FROM employee e
JOIN position p ON e.position_id = p.position_id
GROUP BY p.position_name
ORDER BY total_employees DESC;

-- 4. Gender composition
SELECT
    gender,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM employee
WHERE status = 'Active'
GROUP BY gender;

-- ── PAYROLL ──────────────────────────────────────────────────

-- 5. Overall average salary
SELECT
    ROUND(AVG(salary), 2) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employee
WHERE status = 'Active';

-- 6. Average salary per department
SELECT
    d.department_name,
    ROUND(AVG(e.salary), 2) AS avg_salary,
    ROUND(MIN(e.salary), 2) AS min_salary,
    ROUND(MAX(e.salary), 2) AS max_salary
FROM employee e
JOIN department d ON e.department_id = d.department_id
WHERE e.status = 'Active'
GROUP BY d.department_name
ORDER BY avg_salary DESC;

-- 7. Top 10 highest salaries
SELECT
    full_name,
    d.department_name,
    p.position_name,
    salary
FROM employee e
JOIN department d ON e.department_id = d.department_id
JOIN position p ON e.position_id = p.position_id
WHERE e.status = 'Active'
ORDER BY salary DESC
LIMIT 10;

-- 8. Salary rank per department (window function)
SELECT
    full_name,
    d.department_name,
    salary,
    RANK() OVER (PARTITION BY d.department_name ORDER BY salary DESC) AS salary_rank
FROM employee e
JOIN department d ON e.department_id = d.department_id
WHERE e.status = 'Active'
ORDER BY d.department_name, salary_rank;

-- ── ATTENDANCE ───────────────────────────────────────────────

-- 9. Attendance status distribution
SELECT
    status,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM attendance
GROUP BY status
ORDER BY total DESC;

-- 10. Monthly attendance trend
SELECT
    TO_CHAR(date, 'YYYY-MM') AS month,
    status,
    COUNT(*) AS total
FROM attendance
GROUP BY TO_CHAR(date, 'YYYY-MM'), status
ORDER BY month, status;

-- 11. Late check-in count per employee (after 09:00)
SELECT
    e.employee_id,
    e.full_name,
    COUNT(*) AS late_days
FROM attendance a
JOIN employee e ON a.employee_id = e.employee_id
WHERE a.status = 'Present'
  AND a.check_in > '09:00:00'
GROUP BY e.employee_id, e.full_name
ORDER BY late_days DESC
LIMIT 10;

-- ── TURNOVER ─────────────────────────────────────────────────

-- 12. Turnover rate
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN status <> 'Active' THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS turnover_rate_percent
FROM employee;

-- 13. Turnover by department
SELECT
    d.department_name,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN e.status <> 'Active' THEN 1 ELSE 0 END) AS left_count,
    ROUND(
        100.0 * SUM(CASE WHEN e.status <> 'Active' THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS turnover_percent
FROM employee e
JOIN department d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY turnover_percent DESC;

-- ── RECRUITMENT ──────────────────────────────────────────────

-- 14. Recruitment funnel
SELECT
    status,
    COUNT(*) AS candidates
FROM recruitment
GROUP BY status
ORDER BY
    CASE status
        WHEN 'Applied' THEN 1
        WHEN 'Interviewed' THEN 2
        WHEN 'Hired' THEN 3
        WHEN 'Rejected' THEN 4
    END;

-- 15. Best candidate sources (by hire rate)
SELECT
    source,
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'Hired' THEN 1 ELSE 0 END) AS hired,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'Hired' THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS hire_rate_percent
FROM recruitment
GROUP BY source
ORDER BY hire_rate_percent DESC;

-- 16. Average time-to-hire (days)
SELECT
    ROUND(AVG(hire_date - apply_date), 0) AS avg_days_to_hire
FROM recruitment
WHERE status = 'Hired'
  AND hire_date IS NOT NULL;

-- ── PERFORMANCE ──────────────────────────────────────────────

-- 17. Average KPI per period
SELECT
    period,
    ROUND(AVG(kpi_score), 2) AS avg_kpi,
    ROUND(AVG(manager_score), 2) AS avg_manager_score
FROM performance
GROUP BY period
ORDER BY period;

-- 18. Top 10 performers (avg kpi highest)
SELECT
    e.full_name,
    d.department_name,
    ROUND(AVG(p.kpi_score), 2) AS avg_kpi,
    RANK() OVER (ORDER BY AVG(p.kpi_score) DESC) AS rank
FROM performance p
JOIN employee e ON p.employee_id = e.employee_id
JOIN department d ON e.department_id = d.department_id
WHERE e.status = 'Active'
GROUP BY e.full_name, d.department_name
ORDER BY avg_kpi DESC
LIMIT 10;

-- 19. Worst 10 performers
SELECT
    e.full_name,
    d.department_name,
    ROUND(AVG(p.kpi_score), 2) AS avg_kpi
FROM performance p
JOIN employee e ON p.employee_id = e.employee_id
JOIN department d ON e.department_id = d.department_id
WHERE e.status = 'Active'
GROUP BY e.full_name, d.department_name
ORDER BY avg_kpi ASC
LIMIT 10;

-- ── TRAINING ─────────────────────────────────────────────────

-- 20. Average training score per course
SELECT
    course_name,
    COUNT(*) AS participants,
    ROUND(AVG(score), 2) AS avg_score
FROM training
WHERE score IS NOT NULL
GROUP BY course_name
ORDER BY avg_score DESC;

-- 21. Training effectiveness: avg KPI by completion status
SELECT
    t.completion,
    COUNT(*) AS records,
    ROUND(AVG(p.kpi_score), 2) AS avg_kpi
FROM training t
JOIN performance p ON t.employee_id = p.employee_id
GROUP BY t.completion
ORDER BY avg_kpi DESC;

-- 22. Employees with Completed training vs overall avg KPI (correlative subquery)
SELECT
    e.full_name,
    t.course_name,
    t.score AS training_score,
    (SELECT ROUND(AVG(kpi_score), 2)
     FROM performance p2
     WHERE p2.employee_id = e.employee_id) AS employee_avg_kpi
FROM training t
JOIN employee e ON t.employee_id = e.employee_id
WHERE t.completion = 'Completed'
  AND t.score IS NOT NULL
ORDER BY employee_avg_kpi DESC
LIMIT 20;
