# Stage 1: Builder
FROM python:3.12-slim-bullseye as builder

# Install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Set the working directory
WORKDIR /tmp

# Copy dependency management files
COPY ./pyproject.toml ./poetry.lock* /tmp/

# Export all dependencies (including dev) to requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev 


# Stage 2: Development environment
FROM python:3.12-slim-bullseye as dev

# Set the working directory
WORKDIR /app

# Copy requirements.txt from builder stage
COPY --from=builder /tmp/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the source code and entrypoint script into the container
COPY ./src/ /app/src/
COPY ./web.entrypoint.sh /app/web.entrypoint.sh



# Make the entrypoint script executable
RUN chmod +x /app/web.entrypoint.sh

# Define the entrypoint
ENTRYPOINT ["/app/web.entrypoint.sh"]