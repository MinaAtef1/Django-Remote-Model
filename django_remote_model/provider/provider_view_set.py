from dataclasses import field
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .provider_serializer import dynamic_model_dict_serializer, provider_model_generator
from .provider_fields_generator import dynamic_model_dict_generator
from rest_framework.viewsets import ModelViewSet


from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .provider_serializer import dynamic_model_dict_serializer
from .provider_fields_generator import dynamic_model_dict_generator
from rest_framework.permissions import BasePermission
from django_filters.rest_framework import DjangoFilterBackend

def ProviderViewGenerator(model,  api_key_name, api_key):

    class Check_API_KEY_Auth(BasePermission):
        def has_permission(self, request, view):
            # API_KEY should be in request headers to authenticate requests
            api_key_secret = request.headers.get(api_key_name)
            return api_key == api_key_secret

    fields = dynamic_model_dict_generator(model)

    class ProviderView(generics.GenericAPIView):
        serializer_class = dynamic_model_dict_serializer(model)
        permission_classes = [Check_API_KEY_Auth]

        def get(self, request):

            serializer = dynamic_model_dict_serializer(fields, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    return ProviderView.as_view()


def ModelViewSetGenerator(model, api_key_name, api_key):

    class Check_API_KEY_Auth(BasePermission):
        def has_permission(self, request, view):
            # API_KEY should be in request headers to authenticate requests
            api_key_secret = request.headers.get(api_key_name)
            return True

    class model_viewSet(ModelViewSet):
        serializer_class = provider_model_generator(model)
        permission_classes = [Check_API_KEY_Auth]
        queryset = model.objects.all()
        filter_backends = [DjangoFilterBackend]
        filterset_fields = [field.name for field in model._meta.fields if field.get_internal_type() not in ['FileField', 'ImageField']]

    return model_viewSet
