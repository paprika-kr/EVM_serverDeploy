from rest_framework import serializers

from rest_framework.serializers import (
      ModelSerializer,
)

from generator.models import *


class imageSerializer(ModelSerializer):
   class Meta:
      model = problem
      fields = [
         'ID',
         'type',
         'answer',
         'image',
         'blank_num'
      ]


class imgTotextSerializer(serializers.ModelSerializer):
    class Meta:
        model = problem
        fields = ['text']