#!/bin/bash
docker-compose.exe down

docker-compose.exe up -d

winpty docker-compose.exe exec builder bash