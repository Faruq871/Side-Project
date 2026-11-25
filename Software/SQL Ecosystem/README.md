# SQL Libraries Documentation

Runnable SQL examples organized by topic. Dialect: PostgreSQL.

## Topics Covered

| File | Topic |
|---|---|
| `00_setup` | Sample schema and seed data |
| `01_basics` | SELECT, WHERE, ORDER BY, LIMIT, CASE |
| `02_joins` | INNER, LEFT, FULL, CROSS, SELF, anti-join |
| `03_aggregation` | GROUP BY, HAVING, FILTER, GROUPING SETS |
| `04_subqueries_ctes` | Scalar/derived subqueries, EXISTS, CTE, recursive CTE |
| `05_window_functions` | Ranking, offset, frames, running totals |
| `06_dml` | INSERT, UPDATE, DELETE, upsert, transaction |
| `07_ddl` | CREATE, ALTER, constraints, indexes, views |

## Sample Schema

- `departments(dept_id, dept_name)`
- `employees(emp_id, emp_name, dept_id, salary, hired_on)`
- `orders(order_id, emp_id, amount, order_date)`

## Guidelines

- Run `00 setup.sql` before any other script; it drops and recreates the tables.
- Comments are limited to section headers. Each statement is self-explanatory and independently executable.
- All data is synthetic and deterministic, so results are reproducible across runs.
