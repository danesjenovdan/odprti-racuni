## odprti_racuni

### SETUP

```
docker-compose up -d
docker-compose exec odprti-racuni python manage.py migrate
docker-compose exec odprti-racuni python manage.py collectstatic
docker-compose exec odprti-racuni python manage.py compilemessages
docker-compose exec odprti-racuni python manage.py seed
docker-compose exec odprti-racuni python manage.py createsuperuser
```


### URLS

http://localhost:8000/admin/
http://localhost:8000/info/1/leto/2021/
http://localhost:8000/finance/1/leto/2021/
http://localhost:8000/projekti/1/leto/2021/
http://localhost:8000/donacije/1/leto/2021/
