from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.models import ApiKey
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

class ApiTokenResource(ModelResource):
    class Meta:
        queryset = ApiKey.objects.all()
        resource_name = "token"
        include_resource_uri = False
        fields = ["key"]
        list_allowed_methods = []
        detail_allowed_methods = ["get"]
        authentication = BasicAuthentication()
 
    def get_detail(self, request, **kwargs):
        if kwargs["pk"] != "auth":
            raise NotImplementedError("Resource not found")
        
        obj = ApiKey.objects.get(user=request.user)
        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)
