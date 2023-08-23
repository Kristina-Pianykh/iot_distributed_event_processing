#!/usr/bin/env bash


# This script is used to build docker images for sensor-reader and
# fastapi-siddhi services and upload them to a public repository.
# on docker hub.
# The reason is that the build time is faster on a machine
# with more power than a raspberry pi.

echo "Building and uploading docker images for sensor-reader..."
docker buildx build --platform linux/arm/v7 -t piankris/sensor-reader:armv7 -f sensors/Dockerfile .
docker push piankris/sensor-reader:armv7
echo "Uploade complete."

echo "Building and uploading docker images for fastapi-siddhi..."
docker buildx build --platform linux/arm/v7 -t piankris/fastapi-siddhi:armv7 -f server/Dockerfile .
docker push piankris/fastapi-siddhi:armv7
echo "Uploade complete."