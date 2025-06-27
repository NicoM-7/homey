#!/bin/sh
MAX_WAIT_TIME=120
elapsed_time=0

while [ "$elapsed_time" -lt 120 ]; do
  if nc -z "$DB_HOST" "$DB_PORT"; then
    echo "MySQL is ready. Starting Flask server..."
    exec "$@" 
  else
    echo "Waiting for the MySQL to be ready before starting the Flask server..."
    sleep 10
    elapsed_time=$((elapsed_time + 10))
  fi
done

echo "Error: MySQL is not ready after ${MAX_WAIT_TIME} seconds."
exit 1 