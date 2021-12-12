from rest_framework import serializers, exceptions
from API.models import Account
from django.contrib.auth import get_user_model, authenticate

class AccountSerializer(serializers.Serializer):
    class Meta:
        model = Account 
        fields = ('id','username','auth_id')



class DataSerializer(serializers.Serializer):
    vars()['from']= serializers.CharField(min_length=6,max_length=16, required = True)
    to = serializers.CharField(min_length=6,max_length=16, required = True)
    text = serializers.CharField(min_length=1,max_length=120, required = True)

