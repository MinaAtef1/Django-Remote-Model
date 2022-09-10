from django.db import models
from django.db.models.query import QuerySet
import requests


def dynamic_model_dict_generator(model):


    fields = [{ 'name': field.name,
                'type': field.get_internal_type(),
                'null': field.null,
                'blank': field.blank,
                'default': None if field.default== models.fields.NOT_PROVIDED else field.default,
                'editable': field.editable,
                'choices': field.choices,
                'help_text': field.help_text,
                'verbose_name': field.verbose_name,
                'primary_key': field.primary_key,
                'max_length': field.max_length,
                
               } for field in model._meta.get_fields()]
    
    return fields
