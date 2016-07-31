from django.contrib.auth.models import *
from rest_framework import serializers
from tech.models import *

class TodolistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Question
        fields=('questions',)


class TodoitemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Answer
        fields=('question_id','answers')


