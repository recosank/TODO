from rest_framework import serializers 
from .models import profile

class p_s(serializers.ModelSerializer):

    class Meta:
        model=profile
        fields = "__all__"
    
    def update(self, instance, validated_data):
        instance.img = validated_data.get('img',instance.img)
        instance.bio = validated_data.get('bio',instance.bio)
        instance.date_of_birth = validated_data.get('date_of_birth',instance.date_of_birth)
        instance.country = validated_data.get('country',instance.country)
        instance.address = validated_data.get('address',instance.address)
        instance.save()
        return instance
 
    