-- ============================================================
-- HR Analytics System — Import CSV to staging (*_raw) tables
-- ============================================================
-- \copy is client-side — run from project root directory.
-- Run: cd "D:\RIO\PORTOFOLIO\HR Analyst System"
--      psql -U postgres -d hr_analytics -f database\insert.sql

\copy department_raw(department_id, department_name) FROM 'dataset/department.csv' DELIMITER ',' CSV HEADER;
\copy position_raw(position_id, position_name, grade) FROM 'dataset/position.csv' DELIMITER ',' CSV HEADER;
\copy employee_raw(employee_id, full_name, gender, birth_date, hire_date, department_id, position_id, salary, status) FROM 'dataset/employee.csv' DELIMITER ',' CSV HEADER;
\copy attendance_raw(employee_id, date, check_in, check_out, status) FROM 'dataset/attendance.csv' DELIMITER ',' CSV HEADER;
\copy leave_request_raw(leave_id, employee_id, leave_type, start_date, end_date, duration) FROM 'dataset/leave.csv' DELIMITER ',' CSV HEADER;
\copy performance_raw(employee_id, period, kpi_score, manager_score) FROM 'dataset/performance.csv' DELIMITER ',' CSV HEADER;
\copy recruitment_raw(candidate_id, candidate_name, position, source, status, apply_date, hire_date) FROM 'dataset/recruitment.csv' DELIMITER ',' CSV HEADER;
\copy training_raw(training_id, employee_id, course_name, completion, score) FROM 'dataset/training.csv' DELIMITER ',' CSV HEADER;
