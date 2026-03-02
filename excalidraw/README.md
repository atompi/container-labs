## Excalidraw

### build docker image

```
mkdir docker
cd docker

git clone https://github.com/alswl/excalidraw.git
git clone https://github.com/excalidraw/excalidraw-room.git
git clone https://github.com/alswl/excalidraw-storage-backend.git

cd excalidraw
docker build --build-arg CHINA_MIRROR=true -f dynamic-env.Dockerfile -t atompi/excalidraw:v0.18.0-fork-b3 .

cd ../excalidraw-room
docker build -t atompi/excalidraw-room:latest .

cd ../excalidraw-storage-backend
docker build --build-arg CHINA_MIRROR=true -t atompi/excalidraw-storage-backend:v2023.11.11 .
```

### create persistent storage

```
mkdir -p ./data/mongodb
```

### modify .env

```
APP_HOST=draw.atompi.com    # main domain
ROOM_HOST=draw.atompi.com    # room domain
STORAGE_BACKEND_HOST=draw.atompi.com/storage    # storage backend host

DB_USER=excalidraw    # mongodb user
DB_PASS=excalidraw    # mongodb password
DB_VOLUME_PATH=./data/mongodb    # mongodb volume path
```

### startup

```
docker compose up -d
```
