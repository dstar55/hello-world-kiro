FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so this layer is cached across code-only changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY app.py .
COPY templates/ templates/

EXPOSE 8000

# Production server; the debug dev server in app.py's __main__ block is for local use only
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "app:app"]
