#!/bin/bash
export FLASK_APP=main.py
export FLASK_RUN_PORT=5000
export GOOGLE_KEY=your_api_key
export HOSTNAME=localhost
export DBUSER=root
export DBPASS=db_password
export DBNAME=servi_votacion
export DBPORT=3306

flask run
