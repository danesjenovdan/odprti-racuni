## odprti_racuni

### How to run?

```
docker-compose up
```

### SETUP

This will migrate and seed the database, collect static files, compile messages (translations), and createa a superuser with the username `admin`, email `admin@example.dev`, and password `changeme`.

```
docker-compose run odprti-racuni ./setup.sh
```

You can then start the app with `docker-compose up` if you haven't already.

Visit `http://localhost:8000/admin/nvo/organization/1/change/`, log in with `admin` and `changeme` and edit the organization in order to be able to see something rendered at one of the urls below. Make sure you set the `is_active` field to `True` on the bottom of the admin page (OrganizationFinancialYear inline).

### URLS

#### Admin
http://localhost:8000/admin/

#### Front end
http://localhost:8000/info/1/leto/2021/
http://localhost:8000/finance/1/leto/2021/
http://localhost:8000/projekti/1/leto/2021/
http://localhost:8000/donacije/1/leto/2021/
