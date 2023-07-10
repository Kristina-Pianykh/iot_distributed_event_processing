# # Stage 1: Building the dependencies
# FROM python:3.10.12 AS builder

# WORKDIR /app

# # Copy the poetry.lock and pyproject.toml files
# COPY ./poetry.lock ./pyproject.toml ./

# # install Rust toolchain (needed to install poetry on raspberry pi)
# RUN curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh -s -- -y && \
#     export PATH="$HOME/.cargo/bin:$PATH" && \
#     rustc --version && \
#     source "$HOME/.cargo/env"

# RUN pip install --upgrade pip && \
#     pip install --upgrade setuptools && \
#     pip install --upgrade wheel && \
#     pip install poetry

# # Install Poetry
# # RUN pip -U pip setuptools && \
# #     pip install --only-binary cryptography poetry && \
# #     poetry export -f requirements.txt --without-hashes --no-interaction --no-ansi > requirements.txt

# # RUN curl -sSL https://install.python-poetry.org | python3 -

# # # Install project dependencies
# RUN ~/.local/share/pypoetry/venv/bin/poetry config virtualenvs.create false && \
#     ~/.local/share/pypoetry/venv/bin/poetry export -f requirements.txt --without-lshashes --no-interaction --no-ansi > requirements.txt

# Stage 2: Running the shell script
FROM python:3.7

WORKDIR /app
# COPY requirements.txt ./
COPY server/ ./

# Copy the installed dependencies from the previous stage
# COPY --from=builder /app/requirements.txt /app/requirements.txt

# RUN pip install --upgrade pip && \
#     # apt-get update && \
#     # apt-get install -y default-jdk && \
#     pip install -r requirements.txt

RUN pip install --upgrade pip && \
    apt-get update && \
    pip install httpx fastapi uvicorn pyyaml cython wheel && \
    apt-get install -y python3-dev libboost-python-dev build-essential g++ autotools-dev libicu-dev build-essential libbz2-dev libboost-all-dev maven default-jdk && \
    wget https://github.com/siddhi-io/siddhi-sdk/releases/download/v5.1.2/siddhi-sdk-5.1.2.zip && \
    unzip siddhi-sdk-5.1.2.zip && \
    export SIDDHISDK_HOME=/app/siddhi-sdk-5.1.2 && \
    pip install PySiddhi==5.1.0 && \
    wget https://github.com/siddhi-io/PySiddhi/releases/download/v5.1.0/siddhi-python-api-proxy-5.1.0.jar && \
    cp siddhi-python-api-proxy-5.1.0.jar $SIDDHISDK_HOME/lib && \
    
    # apt update
    # apt install software-properties-common -y && \
    # apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' -y && \
    # apt-get -y upgrade && \
    # apt install -y openjdk-8-jdk && \
    # pip install git+https://github.com/siddhi-io/PySiddhi.git


# ENTRYPOINT uvicorn --host 0.0.0.0 api:app
CMD python -m uvicorn http_server:app --reload --host 0.0.0.0 --port 8080
