#!/usr/bin/env bash
psql postgresql://airflow:airflow@postgres:5432/airflow <<- EOSQL
UPDATE public.connection
SET host     = 'db',
    schema   = 'test',
    login    = 'test',
    password = 'test123',
    is_encrypted=false,
    is_extra_encrypted=false,
    port     = 3306
WHERE id = 12;

UPDATE public.connection
SET conn_id = 'fs_no_default',
    extra   = '{"path":"/home/airflow/monitor"}',
    is_encrypted=false,
    is_extra_encrypted=false
WHERE id = 22;
EOSQL
streamlit run /usr/local/airflow/app/app.py