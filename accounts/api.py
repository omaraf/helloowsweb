from django.db import models
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization,DjangoAuthorization
from accounts.models import MyProfile
from django.contrib.auth.models import User
from tastypie.resources import ModelResource

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name= 'user_info'
        list_allowed_methods = ['get', 'post']
        fields = ['email','first_name','last_name']
        include_resource_uri = False
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'username':[ 'exact', ]
        }

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(username=bundle.request.user)
