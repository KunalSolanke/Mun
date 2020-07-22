from rest_framework import serializers
from .models import Country 
from chits.models import Chit



class CountrySerializer(serializers.ModelSerializer) :
    class Meta :
        model = Country 
        fields  = ('__all__')



class ChitSerializer(serializers.ModelSerializer) :
    chit_from = CountrySerializer() 
    chit_to = CountrySerializer() 
    class Meta :
        model= Chit
        fields = ['chit_from','chit_to','timestamp','status','chit','reply_to_chit']
    
