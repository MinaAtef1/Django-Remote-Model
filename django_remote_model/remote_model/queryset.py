from django.db.models.query import QuerySet

class RemoteModelQuerySet():

    def queryset_factory(dynamic_instance, model, provider_dict_api_url, model_base_url, api_name, api_key):
        class model_query_set(QuerySet):


            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.__values_list = None
                self.__values_list_flat = False 
                self.__distinct = False
                self.__order_by_lambda = None
                self.__order_by_args = None
                self.__filter_kwargs = None


            ########################################
            ##### Remote Model Special Funtion #####
            ########################################
            
            def __iterable_factory(self, data):
                def iterable(self):
                    return list(data)
                return iterable

            def __check_model_update(self,data):
                model_fields = [field.name for field in dynamic_instance.model._meta.fields if field.name not in ['_state', '_meta']]
                number_of_model_fields = len(model_fields)
                number_of_given_fields = len(data)
                if number_of_given_fields != number_of_model_fields:
                    dynamic_instance.update()

            def __dict_to_model(self, data):
                self.__check_model_update(data)
                return dynamic_instance.model(**data)

            #######################################
            ##### overriding QuerySet methods #####
            #######################################


            def get(self, *args, **kwargs):
                data, status = dynamic_instance.make_query_request(
                    'get', f"{model_base_url}{kwargs['id']}/", dynamic_instance.api_name, dynamic_instance.api_key)

                return self.__dict_to_model(data)


            def filter(self, *args, **kwargs):
                if kwargs:
                    self.__filter_kwargs = kwargs
               
                return self

            def values_list(self, *args, **kwargs):
                self.__values_list = args
                self.__values_list_flat = kwargs.get('flat', False)
                return self

            def distinct(self, *args, **kwargs):
                self.__distinct = True
                return self                

            def order_by(self, *args, **kwargs):
                self.__order_by_lambda = lambda obj: [getattr(obj, field.replace('-','')) if field.startswith('-') else getattr(obj, field)*-1 for field in args]
                self.__order_by_args = args
                return self

            def _clone(self):
                qs = super()._clone()
                qs.__values_list = self.__values_list
                qs.__values_list_flat = self.__values_list_flat
                qs.__distinct = self.__distinct
                qs.__order_by = self.__order_by_lambda
                qs.__filter_kwargs = self.__filter_kwargs
                return qs

            def count(self):
                if self._result_cache:
                    return len(self._result_cache)
                return list(self).__len__()

            def ordered(self):
                return self.__order_by_lambda != None

            ####################################
            ########## Magic Method ############
            ####################################


            def __iter__(self):
                if not self._result_cache:
                    qs = model.objects.none()
                    data, status = dynamic_instance.make_query_request('get', model_base_url, dynamic_instance.api_name, dynamic_instance.api_key,params=self.__filter_kwargs)
                
                if self.__values_list:
                    if self.__values_list_flat:
                        models = [row[self.__values_list[0]] for row in data]
                    else:
                        models = [{field: row[field] for field in self.__values_list} for row in data]
                else:
                    models = [self.__dict_to_model(row) for row in data]
    

                if self.__distinct:
                    models = list(set(models))


                if self.__order_by_lambda:
                    if self.__values_list_flat:
                        sign = -1 if self.__order_by_args[0].startswith('-') else 1
                        models = sorted(models, key=lambda x: x*sign)
                    else:
                        models.sort(key=self.__order_by_lambda)

                qs._iterable_class = self.__iterable_factory(models)
                self._result_cache = list(qs)
                return super().__iter__()

            def __len__(self):
                if self._result_cache:
                    return len(self._result_cache)
                return 0

        return model_query_set(model=model)
