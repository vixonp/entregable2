#!/bin/bash

# Script para iniciar Hadoop (NameNode, DataNode, YARN) y Pig
echo "Starting Hadoop services..."

# Formatear HDFS NameNode si no está formateado
# Solo hacer la primera vez o si quieres resetear HDFS
if [ ! -d "/tmp/hadoop-hdfs/dfs/name/current" ]; then
  echo "Formating HDFS NameNode..."
  hdfs namenode -format -force
else
  echo "HDFS NameNode already formatted."
fi

# Iniciar HDFS
echo "Starting HDFS..."
start-dfs.sh

# Iniciar YARN
echo "Starting YARN..."
start-yarn.sh

# Mantener el contenedor en ejecución
# Esto es importante para que el contenedor no se detenga después de iniciar los servicios
echo "Hadoop services started. Keeping container alive..."
tail -f /dev/null