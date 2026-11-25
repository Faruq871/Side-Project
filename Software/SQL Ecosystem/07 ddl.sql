-- CREATE with constraints
CREATE TABLE projects (
    project_id   SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL UNIQUE,
    owner_id     INT REFERENCES employees(emp_id) ON DELETE SET NULL,
    budget       NUMERIC(12, 2) CHECK (budget >= 0),
    status       VARCHAR(20) DEFAULT 'active',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ALTER
ALTER TABLE projects ADD COLUMN deadline DATE;
ALTER TABLE projects ALTER COLUMN status SET DEFAULT 'planned';
ALTER TABLE projects ALTER COLUMN project_name TYPE VARCHAR(150);
ALTER TABLE projects RENAME COLUMN deadline TO due_date;
ALTER TABLE projects DROP COLUMN due_date;

-- Composite constraint
ALTER TABLE projects ADD CONSTRAINT uq_owner_name UNIQUE (owner_id, project_name);

-- Indexes
CREATE INDEX idx_employees_dept ON employees(dept_id);
CREATE UNIQUE INDEX idx_orders_emp_date ON orders(emp_id, order_date);
CREATE INDEX idx_orders_amount_partial ON orders(amount) WHERE amount > 1000;

-- View
CREATE OR REPLACE VIEW dept_summary AS
SELECT d.dept_name, COUNT(e.emp_id) AS headcount, ROUND(AVG(e.salary), 2) AS avg_salary
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_name;

SELECT * FROM dept_summary;

-- Inspect plan
EXPLAIN ANALYZE
SELECT * FROM employees WHERE dept_id = 1;

-- Cleanup
DROP VIEW IF EXISTS dept_summary;
DROP TABLE IF EXISTS projects;
