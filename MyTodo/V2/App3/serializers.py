from rest_framework import serializers 
from .models import td


class td_serializer(serializers.ModelSerializer):


    class Meta:
        model = td
        fields = ('task','is_pending')

    def create(self, validated_data):
        return td.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.task = validated_data.get('task',instance.task)
        
        instance.save()
        return instance
    
    