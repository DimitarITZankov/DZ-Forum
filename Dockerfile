FROM python:3.11-slim
LABEL maintainer="dimitarzankovit"

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY ./requirements.txt /tmp/requirements.txt
EXPOSE 8000

# Create virtualenv and install Python packages
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp 

# Copy app code
COPY ./app /app
WORKDIR /app

# Create non-root user and set ownership
RUN adduser --disabled-password --no-create-home django-user && \
    chown -R django-user /app

# Expose port
EXPOSE 8000

# Switch to non-root user
USER django-user

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]