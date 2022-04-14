from flask import Blueprint
from flask_restplus import Api

from .startup import api as startup
from .explorer import api as explorer
from .lineage_specific import api as lineage_specific
from .lineage_independent import api as lineage_independent
from .locations import api as locations

api_blueprint = Blueprint('api', __name__)
api = Api(title='UFL API', version='1.0', description='Available APIs for the VariantHunter project')
api.init_app(api_blueprint, add_specs=True)

api.add_namespace(startup)
api.add_namespace(lineage_specific)
api.add_namespace(lineage_independent)
api.add_namespace(locations)
api.add_namespace(explorer)
