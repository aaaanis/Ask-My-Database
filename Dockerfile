# Use a base image with Python
FROM python:3.10.13-slim-bookworm

# Copy the requirements.txt file and your application code into the image
COPY requirements.txt /requirements.txt
COPY DBA_PI.py /app/DBA_PI.py
COPY LLM_DB.py /app/LLM_DB.py
COPY LLM_DISCORDBOT.py /app/LLM_DISCORDBOT.py
COPY LLM_AGENT.py /app/LLM_AGENT.py

# Install the required packages
RUN pip install --no-cache-dir -r /requirements.txt

# Set the working directory
WORKDIR /app

# Specify the command to run your application
#CMD ["python", "LLM_AGENT.py"]
