#!/usr/bin/env bash

echo "wait mongo db";
python3 "src/utils/wait_mongo_db.py";

echo "run fastapi project";
gunicorn src.main:app -w 4 -b :$PORT_TO_RUN -k uvicorn.workers.UvicornWorker;