from django.contrib.auth import authenticate, login
from tastypie import fields
from tastypie.resources import ModelResource,ALL_WITH_RELATIONS,ALL
from tastypie.models import ApiKey
from tastypie.authentication import BasicAuthentication,ApiKeyAuthentication
from tastypie.serializers import Serializer
import simplejson as json
from django.contrib.auth.models import User

class CustomAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        jsondata = json.loads(request.body)
        username = jsondata.get('username','')
        password = jsondata.get('pass','')

        if not username or not password:
            return self._unauthorized()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                request.META['TOKENN'] = user.api_key.key
                request.user = user
                print request
                return super(CustomAuthentication, self).is_authenticated(request,**kwargs)
            else:
                return self._unauthorized()
        else:
            return self._unauthorized()

class LoginResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'login'
        allowed_methods = ['post']
        serializer = Serializer(formats=['json',])
        authentication = CustomAuthentication()
        filtering = {
            'user' :   ALL_WITH_RELATIONS  
        }
#def get_object_list(self, request):
#    return super(LoginResource, self).get_object_list(request)
