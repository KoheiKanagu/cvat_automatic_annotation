#!/bin/bash
set -euxo pipefail

cat <<EOF
********
Run it in the lima shell with sudo
********
EOF

if [ "$(whoami)" != "root" ]; then
    exit 1
fi

sleep 10

cp -r ./* ~

cd ~

CVAT_TAG=2.1.0
wget --no-clobber https://github.com/openvinotoolkit/cvat/archive/refs/tags/v$CVAT_TAG.tar.gz
rm -rf cvat-$CVAT_TAG
tar zxvf v$CVAT_TAG.tar.gz cvat-$CVAT_TAG/cvat/apps/iam/rules
rm -rf cvat
mv cvat-$CVAT_TAG/cvat cvat

docker compose up --build --detach

docker run \
    --detach \
    --publish 8000:8000 \
    --publish 9000:9000 \
    --name portainer \
    --restart=always \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume portainer_data:/data portainer/portainer-ce:latest

cat <<EOF
********
Set up portainer.
http://localhost:9000
********
EOF

sleep 30

wget -O nuctl https://github.com/nuclio/nuclio/releases/download/1.5.16/nuctl-1.5.16-linux-amd64
chmod +x nuctl

./nuctl create project cvat
./nuctl deploy --project-name cvat \
    --path yolox \
    --platform local

docker exec \
    -it cvat bash \
    -ic 'python3 ~/manage.py createsuperuser --username admin --email admin@example.com'
