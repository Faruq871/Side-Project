-- INSERT
INSERT INTO departments (dept_id, dept_name) VALUES (5, 'Operations');

-- Multi-row INSERT
INSERT INTO departments VALUES (6, 'Support'), (7, 'Research');

-- INSERT ... SELECT
CREATE TEMP TABLE high_earners AS
SELECT emp_id, emp_name, salary FROM employees WHERE salary >= 85000;

-- UPDATE
UPDATE employees SET salary = salary * 1.05 WHERE dept_id = 1;

-- UPDATE ... FROM (PostgreSQL join-update)
UPDATE employees e
SET salary = e.salary + 1000
FROM departments d
WHERE e.dept_id = d.dept_id AND d.dept_name = 'Sales';

-- DELETE
DELETE FROM departments WHERE dept_id IN (6, 7);

-- UPSERT
INSERT INTO departments (dept_id, dept_name) VALUES (5, 'Operations Updated')
ON CONFLICT (dept_id) DO UPDATE SET dept_name = EXCLUDED.dept_name;

-- RETURNING
UPDATE employees SET salary = salary + 500 WHERE emp_id = 8 RETURNING emp_id, salary;

-- Transaction
BEGIN;
UPDATE employees SET salary = salary - 1000 WHERE emp_id = 1;
UPDATE employees SET salary = salary + 1000 WHERE emp_id = 2;
COMMIT;

-- Savepoint / ROLLBACK
BEGIN;
DELETE FROM orders WHERE emp_id = 4;
SAVEPOINT before_second_delete;
DELETE FROM orders WHERE emp_id = 5;
ROLLBACK TO SAVEPOINT before_second_delete;
COMMIT;
