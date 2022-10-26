#!/usr/bin/sh

# start the virtual environment
source venv/bin/activate

# setup the environment variables
export FLASK_APP=flaskr
export FLASK_ENV=development

# and run the development server
flask run
