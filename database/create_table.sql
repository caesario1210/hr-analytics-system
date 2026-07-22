-- ============================================================
-- HR Analytics System — Create Tables (8 tables)
-- Order: department → position → employee → attendance →
--        leave → performance → recruitment → training
-- ============================================================

-- 1. Department
CREATE TABLE IF NOT EXISTS department (
    department_id   INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

-- 2. Position
CREATE TABLE IF NOT EXISTS position (
    position_id   INT PRIMARY KEY,
    position_name VARCHAR(100) NOT NULL,
    grade         VARCHAR(10)  NOT NULL
);

-- 3. Employee
CREATE TABLE IF NOT EXISTS employee (
    employee_id   INT PRIMARY KEY,
    full_name     VARCHAR(150) NOT NULL,
    gender        VARCHAR(10)  NOT NULL,
    birth_date    DATE         NOT NULL,
    hire_date     DATE         NOT NULL,
    department_id INT          NOT NULL,
    position_id   INT          NOT NULL,
    salary        NUMERIC(12,2) NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'Active',
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (position_id)   REFERENCES position(position_id)
);

-- 4. Attendance
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id   INT          NOT NULL,
    date          DATE         NOT NULL,
    check_in      TIME,
    check_out     TIME,
    status        VARCHAR(20)  NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
    UNIQUE (employee_id, date)
);

-- 5. Leave
CREATE TABLE IF NOT EXISTS leave_request (
    leave_id    INT PRIMARY KEY,
    employee_id INT          NOT NULL,
    leave_type  VARCHAR(50)  NOT NULL,
    start_date  DATE         NOT NULL,
    end_date    DATE         NOT NULL,
    duration    INT,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- 6. Performance
CREATE TABLE IF NOT EXISTS performance (
    performance_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id    INT          NOT NULL,
    period         VARCHAR(10)  NOT NULL,
    kpi_score      NUMERIC(5,2),
    manager_score  NUMERIC(5,2),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- 7. Recruitment
CREATE TABLE IF NOT EXISTS recruitment (
    candidate_id   INT PRIMARY KEY,
    candidate_name VARCHAR(150) NOT NULL,
    position       VARCHAR(100) NOT NULL,
    source         VARCHAR(50)  NOT NULL,
    status         VARCHAR(30)  NOT NULL,
    apply_date     DATE         NOT NULL,
    hire_date      DATE,
    CHECK (status IN ('Applied', 'Interviewed', 'Hired', 'Rejected'))
);

-- 8. Training
CREATE TABLE IF NOT EXISTS training (
    training_id  INT PRIMARY KEY,
    employee_id  INT          NOT NULL,
    course_name  VARCHAR(150) NOT NULL,
    completion   VARCHAR(20)  NOT NULL,
    score        NUMERIC(5,2),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- Staging tables for raw CSV import (before cleaning)
-- No FK/UNIQUE constraints on raw tables — raw data may be invalid before cleaning
CREATE TABLE IF NOT EXISTS employee_raw (
    employee_id   INT,
    full_name     VARCHAR(150),
    gender        VARCHAR(10),
    birth_date    TEXT,
    hire_date     TEXT,
    department_id INT,
    position_id   INT,
    salary        NUMERIC(12,2),
    status        VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS attendance_raw (
    attendance_id INT GENERATED ALWAYS AS IDENTITY,
    employee_id   INT,
    date          TEXT,
    check_in      TEXT,
    check_out     TEXT,
    status        VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS leave_request_raw (
    leave_id    INT,
    employee_id INT,
    leave_type  VARCHAR(50),
    start_date  TEXT,
    end_date    TEXT,
    duration    INT
);
CREATE TABLE IF NOT EXISTS performance_raw (
    performance_id INT GENERATED ALWAYS AS IDENTITY,
    employee_id    INT,
    period         VARCHAR(10),
    kpi_score      NUMERIC(5,2),
    manager_score  NUMERIC(5,2)
);
CREATE TABLE IF NOT EXISTS recruitment_raw (
    candidate_id   INT,
    candidate_name VARCHAR(150),
    position       VARCHAR(100),
    source         VARCHAR(50),
    status         VARCHAR(30),
    apply_date     TEXT,
    hire_date      TEXT
);
CREATE TABLE IF NOT EXISTS training_raw (
    training_id  INT,
    employee_id  INT,
    course_name  VARCHAR(150),
    completion   VARCHAR(20),
    score        NUMERIC(5,2)
);
-- department and position typically clean from source
CREATE TABLE IF NOT EXISTS department_raw (LIKE department INCLUDING ALL);
CREATE TABLE IF NOT EXISTS position_raw (LIKE position INCLUDING ALL);
