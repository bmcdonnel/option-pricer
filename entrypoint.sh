#!/bin/bash

set -e

WAIT_SECONDS=300

wait_for_db() {
  if [[ -n "$PG_HOST" && -n "$PG_PORT" ]]; then

    printf "Waiting for database at $PG_HOST:$PG_PORT"
    for i in $(seq 1 $WAIT_SECONDS); do
      if echo 'SELECT 1' | psql -U $PG_USER -h $PG_HOST -p $PG_PORT &>> /tmp/wait_for_db.log; then
        printf "\n\e[32mfound\e[39m"
        break
      fi
      printf "."
      sleep 1
    done
    echo

    if [ "$i" = $WAIT_SECONDS ]; then
      printf "\e[31mNOT FOUND\e[39m\n"
      printf "psql log while trying to connect to database container:\n"
      printf "%0.1s" "-"{1..60}
      printf "\n"
      cat /tmp/wait_for_db.log
      printf "%0.1s" "-"{2..60}
      printf "\n"
      exit 1
    fi
  fi
}

wait_for_db

python manage.py flush --noinput && python manage.py migrate

exec "$@"
