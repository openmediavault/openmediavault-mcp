FROM python:3.12-slim

# Prevents Python from writing .pyc files & forces unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY config.yaml .
COPY src/ .

EXPOSE 8511
CMD ["python3", "main.py"]
