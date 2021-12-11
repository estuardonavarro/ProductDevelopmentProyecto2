read -p "Press enter to continue..."
sudo docker-compose up 
read -p "Press enter to continue..."
sudo docker exec -it airflow-main-streamlit-1 /bin/bash -c /loadconfig.sh
read -p "Press enter to continue..."