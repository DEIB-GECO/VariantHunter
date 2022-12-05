"""

    SERVER INITIALIZER
    This init script is the first script to be executed on server execution

"""

from sqlite3 import OperationalError

from flask import Blueprint
from flask_restplus import Api

from .startup import api as startup, version

from .locations import api as locations
from .explorer import api as explorer
from .lineage_independent import api as lineage_independent
from .lineage_specific import api as lineage_specific

api_blueprint = Blueprint('api', __name__)
api = Api(ui=False)  # disable Swagger docs
api.init_app(api_blueprint)


@api.errorhandler(OperationalError)
def handler(e):
    """
    When the "OperationalError: database is locked" exception is thrown, it converts the error into a
    response with error code 423. This occurs when the database is locked due to a dataset update.
    """
    if str(e) == 'database is locked':
        return {'message': 'Resource Unavailable: The server is temporarily unable to service ' +
                           'your request due to maintenance downtime. Please try again later.'}, 423
    # Otherwise proceed as usual

# Import startup code
api.add_namespace(startup)

# Import APIs
api.add_namespace(locations)
api.add_namespace(explorer)
api.add_namespace(lineage_independent)
api.add_namespace(lineage_specific)
