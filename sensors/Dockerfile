# Stage 1: Building the dependencies
FROM python:3.10-slim AS builder

WORKDIR /app

# Copy the poetry.lock and pyproject.toml files
COPY ./poetry.lock ./pyproject.toml ./

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Stage 2: Running the shell script
FROM python:3.10-slim

WORKDIR /app

# Copy the shell script
COPY ./sensors/launch.sh ./sensors/joystick.py ./sensors/humidity_temp_pressure.py ./sensors/accelerator.py ./
COPY ./RTIMULib ./RTIMULib

# Copy the installed dependencies from the previous stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
# Install dependencies including sense-hat
RUN apt-get update && apt-get install -y python3-dev
RUN cd RTIMULib/Linux/python && \
    python3 setup.py build && \
    python3 setup.py install && \
    apt-get install -y libopenjp2-7 install sense-hat

# Run the shell script
CMD ["bash", "launch.sh"]
