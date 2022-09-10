Django-Dynamic-model
====================

This package is used to connect two independent django projects together
via rest apis while providing the same interface that a normal django
model class will have.

Dependencies
------------

The script uses Django REST framework. You can install it by following
this `tutorial <https://www.django-rest-framework.org/#installation>`__

Installation
------------

.. code:: bash

   pip install django_remote_model

Usage
-----

They say a good example is worth 100 pages of API documentation. so
let’s get started with an example

We will have two projects: - The provider - The consumer

we will assume that the provider has a model that the consumer need to
access, let’s say this model is called ‘Product’.

so to create the apis to make it available to the consumer to connect to
the provider we will use the ``ProviderViewGenerator`` and
``ModelViewSetGenerator`` methods from the package

.. code:: python

   # provider urls
   from django_remote_model.provider.provider_view_set import ProviderViewGenerator, ModelViewSetGenerator


   provider_view = ProviderViewGenerator(<model_class>, 'Remote-Model-Api-Key', 'KEY_Value')
   model_view_set = ModelViewSetGenerator(<model_class>,'Remote-Model-Api-Key', 'KEY_Value')

   router = SimpleRouter()
   router.register('api/model', model_view_set)


   urlpatterns =[
       path('api/<model>/provider/', provider_view),

   ] + router.urls

Now that we half the apis ready, it’s the consumer turn to connect to it

.. code:: python

   remote_model = DynamicRemote('<model_name>',<provider_url>,<view_set_url>,'Remote-Model-Api-Key', 'KEY_Value')

Now if you want to access the model

.. code:: py

   remote_model.model.objects.all()

It’s better to have only one remote_model instance per api and to import
it wherever you want ti

The ``remote_model`` instance will update the model inside of it if any
update happens in the fields from the provider but if you want to force
update it you can run ``remote_model.update()``

Usage with the Admin
--------------------

The model can be registered normally like this

.. code:: python

   from django.contrib import admin
   from .models import remote_model

   admin.site.register(remote_model.model)
