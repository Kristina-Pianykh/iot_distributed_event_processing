FROM python:3.10

# Install jdk-8
RUN mkdir -p /etc/apt/keyrings
RUN wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc
RUN echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list
RUN apt update 
RUN apt install -y temurin-8-jdk

# Install old version of mavin to avoid http blocking - https://stackoverflow.com/questions/67001968/how-to-disable-maven-blocking-external-http-repositories
# TODO: Checksum validation
ARG MAVEN_VERSION=3.6.3
ARG USER_HOME_DIR="/root"
ARG DOWNLOAD_URL=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/${MAVEN_VERSION}/apache-maven-${MAVEN_VERSION}-bin.tar.gz
RUN mkdir -p /usr/share/maven /usr/share/maven/ref \
    && echo "Downlaoding maven" \
    && curl -fsSL -o /tmp/apache-maven.tar.gz ${DOWNLOAD_URL} \
    \
    && echo "Unziping maven" \
    && tar -xzf /tmp/apache-maven.tar.gz -C /usr/share/maven --strip-components=1 \
    \
    && echo "Cleaning and setting links" \
    && rm -f /tmp/apache-maven.tar.gz \
    && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn
ENV MAVEN_HOME /usr/share/maven
ENV MAVEN_CONFIG "$USER_HOME_DIR/.m2"
RUN mvn --version

# Most of this is probably not needed, but I'm not sure which parts are needed
RUN apt install -y libboost-python-dev build-essential g++ autotools-dev libicu-dev build-essential libbz2-dev libboost-all-dev

RUN git clone https://github.com/siddhi-io/PySiddhi.git \
    && cd PySiddhi \
    && pip install -r Requirements.txt \
    && export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:/bin/javac::") \
    && export CPATH=$CPATH:$JAVA_HOME/include:$JAVA_HOME/include/linux:/usr/local/include/python3.10 \
    && pip install Cython==0.29.36 \
    && python setup.py install

WORKDIR /app

# COPY test.py ./test.py

RUN pip install pydantic fastapi uvicorn httpx pyyaml


RUN wget https://github.com/siddhi-io/siddhi-sdk/releases/download/v5.1.2/siddhi-sdk-5.1.2.zip
RUN unzip siddhi-sdk-5.1.2.zip
ENV SIDDHISDK_HOME=/app/siddhi-sdk-5.1.2
RUN wget https://github.com/siddhi-io/PySiddhi/releases/download/v5.1.0/siddhi-python-api-proxy-5.1.0.jar
RUN cp siddhi-python-api-proxy-5.1.0.jar $SIDDHISDK_HOME/lib

ENV JAVA_HOME=/usr/lib/jvm/temurin-8-jdk-armhf
ENV JVM_PATH=/usr/lib/jvm/temurin-8-jdk-armhf/jre/lib/aarch32/client/libjvm.so

# Install dependencies including sense-hat
RUN apt upgrade -y && \
    apt install -y python3-dev libopenjp2-7 && \
    git clone https://github.com/RPi-Distro/RTIMULib.git && \
    cd RTIMULib/Linux/python && \
    python setup.py build && \
    python setup.py install && \
    pip install sense-hat && \
    cd /app
# CMD ["python", "test.py"]
COPY server/ .
COPY config.yaml ./

CMD python -m uvicorn http_server:app --reload --host 0.0.0.0 --port 8000
