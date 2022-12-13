"""

    OVERALL APP CONFIG
    Route configurations for the application

"""

import logging
import os
from logging.config import dictConfig

from flask import Flask, Blueprint, render_template, send_from_directory
from flask_cors import CORS
from flask_executor import Executor

from apis import api_blueprint

base_url = '/variant_hunter/'  # webapp base url
api_url = base_url + 'api'  # api base url

my_app = Flask(__name__)
cors = CORS(my_app)

my_app.debug = False
my_app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = False
my_app.config['PROPAGATE_EXCEPTIONS'] = False
my_app.config['EXECUTOR_MAX_WORKERS'] = 20

executor_inner = Executor(my_app)

simple_page = Blueprint('root_pages', __name__,
                        static_folder='../frontend/dist/static',
                        template_folder='../frontend/dist')


@simple_page.route('/')
def index():
    """
    Catch the route to the main url
    """
    return render_template('index.html')


@my_app.route(base_url + 'favicon.ico')
def favicon():
    """
    Catch the route to the favicon
    """
    return send_from_directory(os.path.join(my_app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@my_app.route(base_url + 'appicon.png')
def appicon():
    """
    Catch the route to the app icon
    """
    return send_from_directory(os.path.join(my_app.root_path, 'static'), 'appicon.png', mimetype='image/png')


@my_app.route('/', defaults={'path': ''})
@my_app.route('/<path:path>')
def index_all(path):
    """
    Catch all routes so all requests match index.html file
    """
    return render_template('index.html')


# Log format
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '> %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

# Register blueprints
my_app.register_blueprint(api_blueprint, url_prefix=api_url)
my_app.register_blueprint(simple_page, url_prefix=base_url)
my_app.app_context().push()

# Prevent logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

if __name__ == '__main__':
    my_app.run(host="0.0.0.0", port=5000)
