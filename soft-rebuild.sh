#!/bin/bash
docker-compose build web
docker-compose -f production.yml up -d
echo "Done!"