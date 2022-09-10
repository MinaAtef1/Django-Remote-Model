from dataclasses import field
from django.db import models
from django.db.models.query import QuerySet
import requests
from types import new_class, FunctionType, MethodType

from django.apps import apps

import inspect


class DynamicRemote():
    @staticmethod
    def make_query_request( method_type, url, payload, api_name, api_key):
        method = getattr(requests, method_type)

        response = method(url, json=payload, headers={api_name: api_key})
        try:
            return response.json(), response.status_code
        except Exception as e:
            return response.text, response.status_code


    def queryset_factory(dynamic_instance, model,provider_dict_api_url, model_base_url, api_name, api_key):

        class model_query_set(QuerySet):


            def __iterable_factory(self, data):
                def iterable(self):
                    return iter(data)
                return iterable

            def __dict_to_model(self, data):
                model_fields = [field.name for field in dynamic_instance.model._meta.fields if field.name not in ['_state', '_meta']]
                number_of_model_fields = len(model_fields)
                number_of_given_fields = len(data)
                if number_of_given_fields != number_of_model_fields:
                    dynamic_instance.update()

                return dynamic_instance.model(**data)
               

            def get(self, *args, **kwargs):
                data,status = DynamicRemote.make_query_request('get', f"{model_base_url}{kwargs['id']}/", {'id': kwargs['id']}, dynamic_instance.api_name, dynamic_instance.api_key)
                if status != 200:
                    return None
                return self.__dict_to_model(data)


            def create(self, **kwargs):
                raise NotImplementedError('create is not implemented')


            def _fetch_all(self):
                qs = model.objects.none()
                data, status = DynamicRemote.make_query_request('get', model_base_url,{}, dynamic_instance.api_name, dynamic_instance.api_key)
                models = [self.__dict_to_model(row) for row in data]
                qs._iterable_class = self.__iterable_factory(models)
                return qs

            def __len__(self):
                return 0

            def count(self):
                return 0

            def filter(self, *args, **kwargs):
                return self._fetch_all()


            def save():
                raise NotImplementedError('save is not implemented')

        return model_query_set(model=model)


    def get_model_manager(dynamic_instance, model, ):
        
        class model_manager(models.Manager):

            def get_queryset(self):
                return dynamic_instance.queryset_factory(model,dynamic_instance.provider_dict_api_url, dynamic_instance.model_base_url, dynamic_instance.api_name, dynamic_instance.api_key)

        return model_manager()


    @staticmethod
    def get_field(**kwargs):
        type = getattr(models, kwargs.pop('type'))
        return type(**kwargs)


    def get_model_fields(self):
        response = requests.get(self.provider_dict_api_url, headers={self.api_name: self.api_key})
        model_data = response.json()
        model_fields = {
            field['name']: DynamicRemote.get_field(**field) for field in model_data
        }
        model_fields['__module__'] = f'{self.app_name}.models.{self.model_name}'
        
        return model_fields


    def get_shallow_model_fields(self):
        model_fields = {}
        model_fields['__module__'] = '{self.app_name}.models.shallow_model'
        
        return model_fields

    def __get_app_name(self):
        stack_trace = inspect.stack()
        file_path = stack_trace[1].filename
        module = inspect.getmodule(inspect.stack()[2][0])
        return apps.get_containing_app_config(module.__name__).name
    
    def __init__(self, model_name, provider_dict_api_url, model_base_url, api_name, api_key, app_name=None, shallow=False):
        self.model_name = model_name
        self.provider_dict_api_url = provider_dict_api_url
        self.model_base_url = model_base_url
        self.api_name = api_name
        self.api_key = api_key
        self.shallow = shallow
        self.app_name = app_name or self.__get_app_name()


    def generate_model(dyanmic_instance):

        def save(self, *args, **kwargs):
            id = getattr(self, 'id', None)
            model_data = {field.name: getattr(self, field.name) for field in self._meta.fields if field.name not in ['id','_state']}
            if id is None:
                DynamicRemote.make_query_request('post', f"{dyanmic_instance.model_base_url}", model_data, dyanmic_instance.api_name, dyanmic_instance.api_key)
            else:
                DynamicRemote.make_query_request('put', f"{dyanmic_instance.model_base_url}{id}/", model_data, dyanmic_instance.api_name, dyanmic_instance.api_key)

        def delete(self, *args, **kwargs):
            id = getattr(self, 'id', None)
            if id is not None:
                DynamicRemote.make_query_request('delete', f"{dyanmic_instance.model_base_url}{id}/", {} , dyanmic_instance.api_name, dyanmic_instance.api_key)
            
            
        attrs = dyanmic_instance.get_model_fields()
        model_for_manger = type(dyanmic_instance.model_name, (models.Model,), attrs)
        model_for_manger.save = save
        model_for_manger.delete = delete
        manger = dyanmic_instance.get_model_manager(model_for_manger)

        attrs1 = dyanmic_instance.get_model_fields()
        attrs1['objects'] = manger
        model = type(dyanmic_instance.model_name, (models.Model,), attrs1)    
        model.save = save 
        model.delete = delete
        dyanmic_instance.model = model
        return dyanmic_instance


    def __getattr__(self, name):
        if name == 'model':
            self.generate_model()
            return self.model
        else:
            raise AttributeError(f'{name} is not defined')
            
    def update(self):
        self.model = self.generate_model().model