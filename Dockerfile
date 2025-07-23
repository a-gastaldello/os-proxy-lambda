FROM docker.io/library/python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
	pip install --no-cache-dir gunicorn

COPY *.py .

ENV OPENSEARCH_HOST=http://localhost:9200
EXPOSE 8000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]