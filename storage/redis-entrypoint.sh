#!/bin/sh
set -e

if [ -n "$R_PSWRD" ]; then
    exec redis-server --requirepass "$R_PSWRD" --appendonly yes
fi

exec "$@"