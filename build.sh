#!/bin/bash
echo "Updating source files"
pipenv lock --requirements > requirements.txt
echo "Building image"
docker build -t registry.beappia.com/alvistar/manta-telegram --build-arg SSH_KEY="$(cat ~/.ssh/github_rsa)" -f docker/Dockerfile .
