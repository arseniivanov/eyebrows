# -*- coding: utf-8 -*-
from rest_framework import serializers
from pages.models import ShowImage

class ShowImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowImage
        fields = ('text', 'image')
