#!/usr/bin/env bash

echo "wait redis";
python3 "utils/wait_redis.py";

echo "run fastapi project";
gunicorn main:app -w 4 -b :8003 -k uvicorn.workers.UvicornWorker;