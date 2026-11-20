from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_project_files_exist():
    required = [
        "README.md",
        "sql/schema.sql",
        "docker-compose.yml",
        "airflow/dags/olist_pipeline.py",
        "dbt/olist/dbt_project.yml",
        "src/ingestion/load_olist.py",
    ]
    for relative_path in required:
        assert (ROOT / relative_path).is_file(), relative_path
