FROM python:3.11.0

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . /app/

EXPOSE 8000

RUN mkdir -p /app/static
RUN mkdir -p /app/media

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]