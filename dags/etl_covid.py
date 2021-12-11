from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.contrib.sensors.file_sensor import FileSensor
from structlog import get_logger
from airflow.contrib.hooks.fs_hook import FSHook
import pandas as pd
from airflow.hooks.mysql_hook import MySqlHook
import os

logger = get_logger()

cols = ['province_state','country_region','lat','lon','date','count']
file_path_confirmed = f"{FSHook('fs_no_default').get_path()}/time_series_covid19_confirmed_global.csv"
file_path_deaths = f"{FSHook('fs_no_default').get_path()}/time_series_covid19_deaths_global.csv"
file_path_recovered = f"{FSHook('fs_no_default').get_path()}/time_series_covid19_recovered_global.csv"

dag = DAG('db_update', description='Actualización base de datos COVID',
          default_args={
              'owner': 'grupo.x',
              'depends_on_past': False,
              'max_active_runs': 1,
              'start_date': days_ago(1),
              'is_paused_upon_creation': False
          },
          schedule_interval='0 0 * * *',
          catchup=False)

def transformation(file_path):
    df = pd.read_csv(file_path)
    df.set_index(['Province/State', 'Country/Region','Lat','Long'], inplace=True)
    df = df.diff(axis=1)
    df = df. iloc[:, 1:]
    df = df.stack()
    df = df.to_frame()
    df.reset_index(inplace=True)
    df.columns = cols
    df['date'] = pd.to_datetime(df['date'], format="%m/%d/%y")
    if file_path == file_path_confirmed:
        df['Category'] = 'Confirmed'
    elif file_path == file_path_deaths:
        df['Category'] = 'Deaths'
    elif file_path == file_path_recovered:
        df['Category'] = 'Recovered'
    return df

def process_file(**kwargs):
    execution_date = kwargs['execution_date']
    logger.info(execution_date)

    connection = MySqlHook('mysql_default').get_sqlalchemy_engine()
    
    df_confirmed = transformation(file_path_confirmed)
    df_deaths = transformation(file_path_deaths)
    df_recovered = transformation(file_path_recovered)

    with connection.begin() as transaction:
        transaction.execute('DELETE FROM test.covid WHERE 1=1')
        df_confirmed.to_sql('covid', con=transaction, schema='test', if_exists='append', index=False)
        df_deaths.to_sql('covid', con=transaction, schema='test', if_exists='append', index=False)
        df_recovered.to_sql('covid', con=transaction, schema='test', if_exists='append', index=False)

    logger.info(f"Records Inserted Confirmed: {len(df_confirmed.index)}")
    logger.info(f"Records Inserted Deaths: {len(df_deaths.index)}")
    logger.info(f"Records Inserted Recovered: {len(df_recovered.index)}")
    os.remove(file_path_confirmed)
    os.remove(file_path_deaths)
    os.remove(file_path_recovered)
    


sensor_confirmed = FileSensor(filepath='time_series_covid19_confirmed_global.csv', fs_conn_id='fs_no_default', task_id='check_for_confirmed_file', poke_interval=5, timeout=120, dag=dag)
sensor_deaths = FileSensor(filepath='time_series_covid19_deaths_global.csv', fs_conn_id='fs_no_default', task_id='check_for_deaths_file', poke_interval=5, timeout=120, dag=dag)
sensor_recovered = FileSensor(filepath='time_series_covid19_recovered_global.csv', fs_conn_id='fs_no_default', task_id='check_for_recovered_file', poke_interval=5, timeout=120, dag=dag)


operator = PythonOperator(task_id='process_file', dag=dag, python_callable=process_file, provide_context=True)


sensor_confirmed>>sensor_deaths>>sensor_recovered>>operator
