#! /bin/bash

# This shell script quickly deploys your project to your
# DigitalOcean Droplet

# generate TAR file from git
git archive --format tar --output ./project.tar master

echo 'Uploading project...'
rsync ./project.tar root@$DIGITAL_OCEAN_IP_ADDRESS:/tmp/project.tar
echo 'Uploaded complete.'

echo 'Building image...'
ssh -o StrictHostKeyChecking=no root@$DIGITAL_OCEAN_IP_ADDRESS << 'ENDSSH'
    mkdir -p /app
    rm -rf /app/* && tar -xf /tmp/project.tar -C /app
    docker-compose -f /app/docker-compose.prod.yml build
    supervisorctl restart fastapi-celery-app
ENDSSH
echo 'Build complete.'
