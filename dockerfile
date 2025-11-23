# Use an official Python image as the base.
# Match your local Python version if possible (e.g. 3.13-slim).
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for building Python packages (Pillow etc.)
RUN apt-get update && apt-get install -y \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install uv (Python package/dependency manager)
RUN pip install --no-cache-dir uv

# Copy only dependency files first for better build caching
COPY pyproject.toml uv.lock ./ 

# Install Python dependencies (no dev dependencies)
RUN uv sync --no-dev

# Copy the rest of the project code into the container
COPY . .

# Collect static files into STATIC_ROOT (staticfiles/)
RUN python manage.py collectstatic --noinput

# Environment variable for the port (Railway usually injects PORT)
ENV PORT=8000

# Expose the port (for documentation; Railway maps it automatically)
EXPOSE 8000

# Run Django using gunicorn as the WSGI server
CMD ["uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
