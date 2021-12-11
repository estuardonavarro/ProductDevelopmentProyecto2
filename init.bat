docker compose up -d
pause "Por favor, espere que se construya Airflow..."
docker exec airflow-main-streamlit-1 /bin/bash -c /loadconfig.sh
pause