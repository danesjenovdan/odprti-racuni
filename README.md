## odprti_racuni

```
docker-compose up -d
docker-compose exec odprti-racuni python manage.py migrate
docker-compose exec odprti-racuni python manage.py collectstatic
docker-compose exec odprti-racuni python manage.py compilemessages
docker-compose exec odprti-racuni python manage.py seed
docker-compose exec odprti-racuni python manage.py createsuperuser
```
