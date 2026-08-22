FROM apache/airflow:2.10.5-python3.12

USER root

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    openjdk-17-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

RUN mkdir -p /opt/airflow/jdbc \
    && curl -fL \
    https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.13/postgresql-42.7.13.jar \
    -o /opt/airflow/jdbc/postgresql-42.7.13.jar

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt \
    && pip install --no-cache-dir pyspark==4.1.2