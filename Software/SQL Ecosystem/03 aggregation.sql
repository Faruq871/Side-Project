-- Basic aggregates
SELECT COUNT(*) AS n, AVG(salary) AS avg_sal, MIN(salary) AS min_sal, MAX(salary) AS max_sal
FROM employees;

-- GROUP BY
SELECT dept_id, COUNT(*) AS headcount, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept_id
ORDER BY dept_id;

-- HAVING
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 2;

-- Aggregate over joined data
SELECT e.emp_name, COUNT(o.order_id) AS n_orders, COALESCE(SUM(o.amount), 0) AS total
FROM employees e
LEFT JOIN orders o ON o.emp_id = e.emp_id
GROUP BY e.emp_id, e.emp_name
ORDER BY total DESC;

-- FILTER (PostgreSQL only)
SELECT
    COUNT(*) FILTER (WHERE salary >= 80000) AS high_earners,
    COUNT(*) FILTER (WHERE salary <  80000) AS other_earners
FROM employees;

-- GROUPING SETS / ROLLUP
SELECT dept_id, COUNT(*), SUM(salary)
FROM employees
GROUP BY ROLLUP (dept_id);

-- String aggregate
SELECT dept_id, STRING_AGG(emp_name, ', ' ORDER BY emp_name) AS members
FROM employees
GROUP BY dept_id;
