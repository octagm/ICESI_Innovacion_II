FROM python:3.12-slim

ENV PYTHONPATH=/app
ENV DATA_DIR=/storage
ENV MLMODELS_DIR=/mlmodels
ENV STORAGE_DIR=/storage

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src/ .
CMD ["sh", "-c", "fastapi run /app/app.py --port ${PORT:-8000}"]
