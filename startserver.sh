#!/usr/bin/sh

# start the server
if [ "$VIRTUAL_ENV" ]
then flask --app flaskr --debug run
else
  source "venv/bin/activate"
  flask --app flaskr --debug run
fi
