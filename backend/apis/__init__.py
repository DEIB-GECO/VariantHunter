from sqlite3 import OperationalError

from flask import Blueprint, json
from flask_restplus import Api

from .startup import api as startup, version
from .explorer import api as explorer
from .lineage_specific import api as lineage_specific
from .lineage_independent import api as lineage_independent
from .locations import api as locations

api_blueprint = Blueprint('api', __name__)
api = Api(title='UFL API', version=version, description='Available APIs for the VariantHunter project')
api.init_app(api_blueprint, add_specs=True)


@api.errorhandler(OperationalError)
def handler(e):
    return {'message': 'Resource Unavailable: The server is temporarily unable to service your request due to maintenance downtime. Please try again later.'}, 423


api.add_namespace(startup)
api.add_namespace(lineage_specific)
api.add_namespace(lineage_independent)
api.add_namespace(locations)
api.add_namespace(explorer)
