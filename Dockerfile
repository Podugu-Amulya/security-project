# ----------------------------------------------------------------------
# Stage 1: Builder Stage (To install dependencies securely)
# ----------------------------------------------------------------------
FROM python:3.11-slim-bookworm as builder

# Set environment variables for non-interactive commands
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------------------
# Stage 2: Runtime Stage (Minimal image for execution)
# ----------------------------------------------------------------------
FROM python:3.11-slim-bookworm as runtime

# Install cron daemon and tini
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tini && \
    rm -rf /var/lib/apt/lists/*

# Set UTC timezone as required
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set the working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application files (scripts and keys)
COPY app/ app/
COPY decrypt_seed.py .
COPY requirements.txt .
COPY student_private.pem .
COPY encrypted_seed.txt .

# Create volume mount points and data directory
RUN mkdir -p /app/data
VOLUME ["/app/data", "/app/cron"]

# --- CRON SETUP ---
# CRITICAL FIX: Explicitly use the full path to python3 for the cron job
RUN echo "* * * * * /usr/local/bin/python3 /app/app/cron_job.py >> /app/cron/cron_output.log 2>&1" > /etc/cron.d/crypto-job
RUN chmod 0644 /etc/cron.d/crypto-job
RUN crontab /etc/cron.d/crypto-job

# Expose the application port
EXPOSE 8080

# Use tini as the entrypoint
ENTRYPOINT ["/usr/bin/tini", "--"]

# FINAL CRITICAL FIX: Explicitly use the full path to python3 for the uvicorn server
CMD ["/bin/sh", "-c", "cron -f & /usr/local/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080"]