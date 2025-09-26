#!/bin/bash 


# For build applicatio;
docker-compose up --build 


# Inspect into kafka;
# Shows partitions, offsets, consumer lag;
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic my-topic


# Simulate scale
# Run other consumer container
docker-compose scale consumer=2


# Stop
docker-compose down