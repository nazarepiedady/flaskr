import os
from flask import Flask


def create_app(test_config=None):
    ''' create and configure the application '''
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance configuration, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # load the test configuration if passed in
        application.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    from . import db as database
    database.init_application(application)

    from . import auth
    application.register_blueprint(auth.blueprint)

    from . import blog
    application.register_blueprint(blog.blueprint)

    # a simple page that says hello
    @application.route('/hello')
    def hello():
        return 'Hello, World!'

    return application
