#!/usr/bin/env bash

echo "Generate fake data in auth DB";
python3 "src/generate_fake_data_in_auth_db.py";

echo "Generate fake data in movies DB";
python3 "src/generate_fake_data_in_movies_db.py";

echo "Generate fake data in watching history DB";
python3 "src/generate_fake_data_in_watching_history_db.py";

echo "DONE"