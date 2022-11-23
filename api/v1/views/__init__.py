from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states.index import *
#from api.v1.views.amenities.index import *
#from api.v1.views.users.index import *
#from api.v1.views.places.index import *
