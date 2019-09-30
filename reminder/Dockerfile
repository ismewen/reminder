FROM python:3.7
RUN mkdir /code
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
COPY . /code
EXPOSE 8000
RUN mkdir static && python manage.py collectstatic --no-input
CMD gunicorn reminder.wsgi:application --bind 0.0.0.0:8000
