# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc musl-dev sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure SQLite database file exists and has proper permissions
RUN touch words.db && chmod 777 words.db

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Default command to check and initialize the database before running Flask
CMD ["sh", "-c", "invoke init-db && flask run --host=0.0.0.0 --port=5000"]
