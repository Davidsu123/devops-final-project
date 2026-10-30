FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what the app needs to run
COPY app.py db.py ./
COPY templates/ templates/

# Run as a regular user, not as root
RUN useradd --uid 10001 --no-create-home appuser
USER 10001

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

# gunicorn is a web server made for production (Flask's own server is only for development)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "app:app"]
