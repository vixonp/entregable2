FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java y herramientas necesarias
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget curl && \
    apt-get clean

# Descargar e instalar Apache Pig
RUN wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xzf pig-0.17.0.tar.gz -C /opt && \
    mv /opt/pig-0.17.0 /opt/pig && \
    rm pig-0.17.0.tar.gz

# Variables de entorno necesarias
ENV PIG_HOME=/opt/pig
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PIG_HOME/bin:$JAVA_HOME/bin:$PATH

# Directorio de trabajo y montaje
RUN mkdir /data
WORKDIR /data

CMD ["/bin/bash"]
