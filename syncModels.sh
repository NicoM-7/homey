#!/bin/bash

set -e

cleanup() {
    echo "Cleaning up Docker containers and images..."

    rm -rf ./backend/docker/mysql-data

    docker ps -aq | xargs -r docker rm -f
    docker images -q | xargs -r docker rmi -f

    echo "Cleanup complete."
    exit 0
}

dos2unix ./backend/docker/scripts/wait-for-db.sh

rm -rf ./backend/docker/mysql-data

export SYNC=true
docker compose -f ./backend/docker/docker-compose.yml up --build -d

trap cleanup SIGINT SIGTERM EXIT

timeout=60
elapsed=0
interval=2

mysql_container=$(docker compose -f ./backend/docker/docker-compose.yml ps -q mysql)
backend_container=$(docker compose -f ./backend/docker/docker-compose.yml ps -q flask || docker compose -f ./backend/docker/docker-compose.yml ps -q flask)

# Wait for MySQL to be ready
while true; do
  if docker logs "$mysql_container" 2>&1 | grep "ready for connections"; then
    echo "MySQL is ready"
    sleep 5
    break
  fi

  elapsed=$((elapsed + interval))
  if [ "$elapsed" -ge "$timeout" ]; then
    echo "Timeout reached: MySQL did not start on time"
    exit 1
  fi
  sleep "$interval"
done

# Dump schema
docker exec -i "$mysql_container" sh -c 'mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --no-data --no-tablespaces "$MYSQL_DATABASE"' > ./backend/docker/dumps/init.sql

perl ./summarizeSchema.pl

cleanup