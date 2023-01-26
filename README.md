# Flaskr

In this repository you will find the source code of **flaskr**, the
application developed during the official tutorial of flask documentation,
so below you will find some instructions to run and test it.


## Instructions

To run this application you need to:

1 - Create the python virtual environment and activate it:

```sh
python -m venv venv
```

2 - Activate the virtual environment

```sh
source venv/bin/activate
```

3 - Install the packages in the `requirements.txt`:

```sh
pip install -r requirements.txt
```

4 - Initialise the sqlite3 database

```sh
flask --app flaskr init-db
```

5 - Start the development server

```sh
flask --app flaskr run
```
