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
   pip install django-filter

Usage
-----

They say a good example is worth 100 pages of API documentation. so
let’s get started with an example

We will have two projects:

-  The provider
-  The consumer

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

Now that we half the apis ready, it’s the consumer turn to connect to
it, first let’s import the ``RemoteModel``

.. code:: python

   from django_remote_model.remote_model import RemoteModel
   remote_model = RemoteModel(model_name, provider_url,view_set_url, Remote_Model_Api_Key, KEY_Value, has_permission=false)

Explanation for the arguments: Argument \| Function — \| — model_name \|
The name of the model provider_url \| The url for the
``ProviderViewGenerator`` view_set_url \| The url for the
``ModelViewSetGenerator`` Remote_Model_Api_Key \| The api Key KEY_Value
\| The Key has_permission \| default ``False``, Whether the model has
permissions or not (useful when using the admin)

So far the following methods are tested

.. code:: py

   remote_model.model.objects.all()
   remote_model.model.objects.get()
   remote_model.model.objects.filter()
   remote_model.model.objects.order_by()
   remote_model.model.objects.distinct()
   remote_model.model.objects.count()
   remote_model.model.save()
   remote_model.model.delete()

Best Practices
--------------

It’s better to have only one remote_model instance per api and to import
it wherever you want it

The ``remote_model`` instance will update the model inside of it if any
update happens in the fields from the provider but if you want to force
update it you can run ``remote_model.update()``

Permission
----------

By default the remote model does not have permission of its own because
it’s not generated from a migration, but you can create a migration for
it by setting ``has_permission`` to ``True``

but bear in mind that you will need to delete those permission by hand
if you decided to change or remote the remote model

Usage with the Django Admin
---------------------------

The model can be used normally with the Django admin and it supports
most of the admin functionality

.. code:: python

   from django.contrib import admin
   from .models import remote_model

   admin.site.register(remote_model.model)
