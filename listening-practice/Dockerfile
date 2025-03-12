# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (including ffmpeg which provides ffprobe)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install app dependencies
RUN pip install --no-cache-dir streamlit boto3 pydub

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port for the Streamlit app
EXPOSE 7861

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false", "--server.address", "0.0.0.0", "--server.port", "7861"]
