#!/usr/bin/env sh

echo "Wait redis"
# TODO Add redis waiter

echo "run fastapi project";
gunicorn src.main:app -w 4 -b :8003 -k uvicorn.workers.UvicornWorker;