from rest_framework import serializers 
from .models import profile

class p_s(serializers.ModelSerializer):

    class Meta:
        model=profile
        fields = "__all__"
    
    def update(self, instance, validated_data):
        
        instance.img = validated_data.get('img',instance.img)
        
        instance.save()
        return instance
 
    