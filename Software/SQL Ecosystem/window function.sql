-- Aggregate as window (keeps row detail)
SELECT
    emp_name,
    dept_id,
    salary,
    AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM employees;

-- Ranking
SELECT
    emp_name,
    dept_id,
    salary,
    ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn,
    RANK()       OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rnk
FROM employees;

-- Top-N per group
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT emp_name, dept_id, salary FROM ranked WHERE rn = 1;

-- Offset functions
SELECT
    emp_name,
    salary,
    LAG(salary)  OVER (ORDER BY salary) AS prev_salary,
    LEAD(salary) OVER (ORDER BY salary) AS next_salary
FROM employees;

-- Running total with explicit frame
SELECT
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders;

-- Moving average
SELECT
    order_date,
    amount,
    AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS ma_3
FROM orders;

-- Distribution
SELECT
    emp_name,
    salary,
    NTILE(4)     OVER (ORDER BY salary) AS quartile,
    PERCENT_RANK() OVER (ORDER BY salary) AS pct_rank
FROM employees;

-- Named WINDOW clause
SELECT
    emp_name,
    salary,
    RANK() OVER w AS rnk,
    SUM(salary) OVER w AS dept_total
FROM employees
WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC);
