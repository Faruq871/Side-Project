-- Projection
SELECT emp_name, salary FROM employees;

-- WHERE + ORDER BY + LIMIT
SELECT emp_name, salary
FROM employees
WHERE salary > 70000
ORDER BY salary DESC
LIMIT 5;

-- Operators
SELECT emp_name FROM employees WHERE dept_id IN (1, 2);
SELECT emp_name FROM employees WHERE salary BETWEEN 60000 AND 80000;
SELECT emp_name FROM employees WHERE emp_name LIKE 'A%';
SELECT emp_name FROM employees WHERE dept_id IS NULL;

-- DISTINCT
SELECT DISTINCT dept_id FROM employees;

-- CASE
SELECT
    emp_name,
    salary,
    CASE
        WHEN salary >= 85000 THEN 'Senior'
        WHEN salary >= 70000 THEN 'Mid'
        ELSE 'Junior'
    END AS band
FROM employees;

-- NULL handling
SELECT emp_name, COALESCE(dept_id, 0) AS dept_id FROM employees;

-- Alias + expression
SELECT emp_name, salary, ROUND(salary / 12, 2) AS monthly FROM employees;
