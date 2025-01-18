FROM python:3.13-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Set the working directory
WORKDIR /app

# Copy only dependencies files first
COPY pyproject.toml ./
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the files
COPY . .

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser
CMD ["python", "-m", "pohadkomat", "serve"]
