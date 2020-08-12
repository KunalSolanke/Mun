from rest_framework import serializers
from accounts.models import Country 
from chits.models import Chit



class CountrySerializer(serializers.ModelSerializer) :
    class Meta :
        model = Country
        fields = ['name','country_id']



class ChitSerializer(serializers.ModelSerializer) :
    chit_from = CountrySerializer() 
    chit_to = CountrySerializer()
    reply_to_country = serializers.CharField(source='reply_to_chit.chit_from.country_id',required=False) 
    class Meta :
        model= Chit
        fields = ['id','chit_from','chit_to','timestamp','status','chit','reply_to_country']

