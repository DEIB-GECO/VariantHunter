import os
from logging.config import dictConfig

import flask
from flask import Flask, redirect, Blueprint, url_for, render_template
from flask_cors import CORS
from flask_executor import Executor

from apis import api_blueprint

base_url = '/variant_hunter/'
api_url = base_url + 'api'
repo_static_url = base_url + 'repo_static'


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)



dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s:%(lineno)d: %(message)s',
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

my_app = Flask(__name__)
cors = CORS(my_app)

my_app.debug = False
my_app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = True
my_app.config['EXECUTOR_MAX_WORKERS'] = 20

executor_inner = Executor(my_app)

simple_page = Blueprint('root_pages', __name__,
                        static_folder='../frontend/dist/static',
                        template_folder='../frontend/dist')

graph_pages = Blueprint('static', __name__,
                        # static_url_path='/',
                        static_folder='./repo_static/',
                        # template_folder='../frontend/dist'
                        )


# base url defined in apis init
@simple_page.route('/')
def index():
    flask.current_app.logger.info("serve index")
    return render_template('index.html')


# base url defined in apis init
@simple_page.route('/epitope/')
def index_epitope():
    flask.current_app.logger.info("serve index")
    return render_template('index.html')


# Make a "catch all route" so all requests match our index.html file.
# This lets us use the new history APIs in the browser.
@simple_page.route('/', defaults={'path': ''})
@simple_page.route('/<path:path>')
def redirect_all(path):
    if path.startswith("epi"):
        return redirect(url_for('.index_epitope'))
    else:
        return redirect(url_for('.index'))


# register blueprints
my_app.register_blueprint(api_blueprint, url_prefix=api_url)
my_app.register_blueprint(graph_pages, url_prefix=repo_static_url)
my_app.register_blueprint(simple_page, url_prefix=base_url)
my_app.app_context().push()


# redirect all to base url
@my_app.route('/', defaults={'path': ''})
@my_app.route('/<path:path>')
def index_all(path):
    return redirect(base_url)


if __name__ == '__main__':
   my_app.run(host="0.0.0.0", port=5000, use_reloader=False, debug=False)

# if __name__ == '__main__':
#     my_app.run()


# prevent cached responses
@my_app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    if "Cache-Control" not in r.headers:
        r.cache_control.max_age = 1  # 1 seconds # 5 min
        # r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        # r.headers["Pragma"] = "no-cache"
        # r.headers["Expires"] = "0"
        # r.headers['Cache-Control'] = 'public, max-age=0'
    return r
