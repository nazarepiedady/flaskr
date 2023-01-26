#!/usr/bin/sh

# activate the virtual environment
source venv/bin/activate

# execute the development server
flask --app flaskr --debug run
