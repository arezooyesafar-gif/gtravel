from import_export import resources
from .models import *

class visa_resource(resources.ModelResource):
    class Meta:
        model = visa_request_item