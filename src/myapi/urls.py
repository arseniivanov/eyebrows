# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from rest_framework import routers
from myapi.viewsets import ShowImageViewSet

router = routers.DefaultRouter()
router.register(r'images', ShowImageViewSet)

urlpatterns = [
        url(r'^', include(router.urls))
]