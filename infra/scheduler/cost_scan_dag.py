from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def trigger_cost_scan():
    url = "http://localhost:8000/recommendation"
    sample_payload = {
        "resource_name": "staging-ec2-01",
        "resource_type": "EC2",
        "usage_data": "Average CPU usage: 5% over 14 days",
        "recommendation": "Downsize to t3.small"
    }

    try:
        response = requests.post(url, json=sample_payload)
        response.raise_for_status()
        print("Response:", response.json())
    except Exception as e:
        print("Failed to trigger recommendation:", str(e))

with DAG(
    'daily_cost_scan',
    default_args=default_args,
    description='Trigger cost scan and AI recommendation',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    scan_task = PythonOperator(
        task_id='trigger_ai_cost_summary',
        python_callable=trigger_cost_scan
    )
