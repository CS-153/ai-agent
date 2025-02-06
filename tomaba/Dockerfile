# Use a lightweight Python base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONPATH=/app

# Set a dedicated user (security best practice)
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set working directory
WORKDIR /app

# Install system dependencies required for Poetry
RUN apt-get update && apt-get install -y curl gcc g++ && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first (ensures caching)
COPY pyproject.toml poetry.lock ./

# Install only production dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy remaining source files
COPY . ./tomaba

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose the server port
EXPOSE 8080

# Start the bot & FastAPI server
CMD ["poetry", "run", "python", "tomaba/run.py"]
