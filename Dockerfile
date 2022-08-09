# Pull base image
FROM python:3.8
# LABEL MAINTAINER=" https://giahino "
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
RUN mkdir /giahino
WORKDIR /giahino
# Install dependencies
# COPY Pipfile Pipfile.lock /code/
ADD requirements.txt /giahino

COPY . /giahino/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["celery -A config worker --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler","celery -A config beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler"]
# RUN python manage.py collectstatic --no-input
