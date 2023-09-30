# # Stage 1: Building the dependencies
# FROM python:3.10-slim AS builder

# WORKDIR /app

# # Copy the poetry.lock and pyproject.toml files
# COPY ./poetry.lock ./pyproject.toml ./

# # Install Poetry
# RUN pip install poetry==1.1.14

# # Install project dependencies
# RUN poetry config virtualenvs.create false && \
#     poetry install --no-root --no-interaction --no-ansi --no-dev

# Stage 2: Running the shell script
FROM python:3.10.12

WORKDIR /app

# Copy the installed dependencies from the previous stage
# COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
# Install dependencies including sense-hat
RUN apt update && \
    apt upgrade -y && \
    apt install -y python3-dev libopenjp2-7 && \
    git clone https://github.com/RPi-Distro/RTIMULib.git && \
    cd RTIMULib/Linux/python && \
    python setup.py build && \
    python setup.py install && \
    pip install sense-hat && \
    cd /app

# Install project dependencies
RUN pip install httpx pyyaml RPi.GPIO

# COPY sensors/ ./
# COPY config.yaml ./

# ENV DEVICE_ID=${DEVICE_ID}

# Run the shell script
# ENTRYPOINT bash /app/launch.sh ${DEVICE_ID}
# CMD ["bash", "/app/launch.sh"]
