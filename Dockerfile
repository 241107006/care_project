FROM python:3.11.0

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

RUN mkdir -p /app/static

# RUN python manage.py collectstatic --noinput

RUN chmod -R 755 /app/static /app/staticfiles

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]