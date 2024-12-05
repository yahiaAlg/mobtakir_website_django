FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app


# Install system dependencies including Brotli
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    brotli \
    && rm -rf /var/lib/apt/lists/*
# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Make port 8000 available for the app
EXPOSE 8000

# Create and switch to non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
# Before switching to appuser, add:
RUN mkdir -p /app/data
RUN chown -R appuser:appuser /app/data
USER appuser

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mobtakir_website_django.wsgi:application"]