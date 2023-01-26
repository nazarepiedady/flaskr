import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_database, init_database


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as file:
    __data_sql = file.read().decode('utf-8')
