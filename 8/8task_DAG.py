from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='8task_dag',
    default_args=default_args,
    schedule_interval='45 12 * * *',
    catchup=False,
) as dag:

    start = DummyOperator(
        task_id='start'
    )

    task1 = BashOperator(
        task_id='echo_hi',
        bash_command='echo "Hello"',
    )

    task2 = BashOperator(
        task_id='echo_date',
        bash_command='date',
    )

    task3 = BashOperator(
        task_id='get_hostname',
        bash_command='hostname',
    )

    def process_data(ti):
        echo_hi_output = ti.xcom_pull(task_ids='echo_hi')
        echo_date_output = ti.xcom_pull(task_ids='echo_date')
        hostname_output = ti.xcom_pull(task_ids='get_hostname')
        return f"Processed data: {echo_hi_output}, {echo_date_output}, Hostname: {hostname_output}"

    # PythonOperator, который принимает результат и обрабатывает его
    process_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
    )

    # Фин
    end = DummyOperator(
        task_id='end'
    )

    # Задаем последовательность задач
    start >> [task1, task2, task3] >> process_task >> end
