from flask import Blueprint
from flask_restplus import Api

from .create_database import api as create_database
from .automatic_analysis import api as automatic_analysis
from .analyse_mutations import api as analyse_mutations
from .analyse_mutations_without_lineages import api as analyse_mutations_without_lineages

enable_doc = True

api_blueprint = Blueprint('api', __name__)

if enable_doc:
    api = Api(title='UFL API', version='1.0', description='TODO', )
else:
    api = Api(title='UFL API', version='1.0', description='TODO', doc=False)


api.init_app(api_blueprint, add_specs=enable_doc)

api.add_namespace(create_database)
api.add_namespace(automatic_analysis)
api.add_namespace(analyse_mutations)
api.add_namespace(analyse_mutations_without_lineages)
