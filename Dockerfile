FROM python:3.9-slim

# Install cron and clean up
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory for persistence
RUN mkdir -p /app/data

# Give execution rights to the cron script
RUN chmod +x /app/cron_script.py

# Run the application
CMD ["python", "app.py"]