FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
        libpango1.0-dev \
        libglib2.0-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

RUN python manage.py collectstatic --no-input --clear

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000" ]
