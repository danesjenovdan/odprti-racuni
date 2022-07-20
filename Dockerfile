FROM python:3.9

RUN apt-get update && \
    apt-get upgrade -y

RUN apt-get update && apt-get install --yes python3-pip \
                        gettext

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

RUN python3 manage.py compilemessages

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=odprti_racuni.settings

CMD exec python manage.py runserver 0.0.0.0:8000
