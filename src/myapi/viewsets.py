# -*- coding: utf-8 -*-
from rest_framework import viewsets
from myapi.serializers import ShowImageSerializer
from pages.models import ShowImage

class ShowImageViewSet(viewsets.ModelViewSet):
    queryset = ShowImage.objects.all()
    serializer_class = ShowImageSerializer
