sudo docker-compose exec -T web python manage.py makemigrations
sudo docker-compose exec -T web python manage.py migrate