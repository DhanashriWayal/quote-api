FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and static files
COPY app.py .
COPY static/ ./static/

EXPOSE 8000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]