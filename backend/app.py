import logging
import os
from logging.config import dictConfig

from flask import Flask, Blueprint, render_template, send_from_directory
from flask_cors import CORS
from flask_executor import Executor

from apis import api_blueprint

base_url = '/variant_hunter/'
api_url = base_url + 'api'

my_app = Flask(__name__)
cors = CORS(my_app)

my_app.debug = False
my_app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = True
my_app.config['EXECUTOR_MAX_WORKERS'] = 20

executor_inner = Executor(my_app)

simple_page = Blueprint('root_pages', __name__,
                        static_folder='../frontend/dist/static',
                        template_folder='../frontend/dist')


# Catch the index route
@simple_page.route('/')
def index():
    return render_template('index.html')


@my_app.route(base_url + 'favicon.ico')
def favicon():
    return send_from_directory(os.path.join(my_app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@my_app.route(base_url + '/appicon.png')
def appicon():
    return send_from_directory(os.path.join(my_app.root_path, 'static'), 'appicon.png', mimetype='image/png')


# Catch all routes so all requests match index.html file.
@my_app.route('/', defaults={'path': ''})
@my_app.route('/<path:path>')
def index_all(path):
    return render_template('index.html')


# prevent cached responses
@my_app.after_request
def add_header(r):
    if "Cache-Control" not in r.headers:
        r.cache_control.max_age = 300  # 5 minutes
    return r


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

# register blueprints
my_app.register_blueprint(api_blueprint, url_prefix=api_url)
my_app.register_blueprint(simple_page, url_prefix=base_url)
my_app.app_context().push()

# prevent logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    print("\n\n\033[01m\033[32m> * STARTUP COMPLETED:\033[0m\033[32m The application is now accessible from your browser at http://0.0.0.0:"
          + str(port) + " (PRESS CTRL+C to stop)\033[0m\n")
    my_app.run(host="0.0.0.0", port=5000)
