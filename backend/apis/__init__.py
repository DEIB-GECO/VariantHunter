from flask import Blueprint
from flask_restplus import Api

# from .create_database import api as create_database
from .lineage_specific import api as lineage_specific
from .lineage_independent import api as lineage_independent
from .locations import api as locations
from .explorer import api as explorer

api_blueprint = Blueprint('api', __name__)
api = Api(title='UFL API', version='1.0', description='Available APIs for the VariantHunter project')
api.init_app(api_blueprint, add_specs=True)

api.add_namespace(create_database)
api.add_namespace(analyse_mutations)
api.add_namespace(analyse_mutations_without_lineages)
api.add_namespace(locations)
api.add_namespace(explorer)
