from .models import td
from .serializers import td_serializer
from V1.App2.models import profile
from django.core.exceptions import ValidationError
from V1.App2.models import profile
from rest_framework.response import Response
from rest_framework.views import APIView

class todo_view(APIView):
    
    def get(self,req,*args, **kwargs):
        p=profile.objects.get(user=req.user)
        qryst = td.objects.filter(user=p)
        sr = td_serializer(qryst,many=True)
        return Response(
            {'data': sr.data},
        )
        
    def post(self,req,*args, **kwargs):
        p=profile.objects.get(user=req.user)
        sr = td_serializer(data = req.data)
        if sr.is_valid():
            sr.save(user=p)
            return Response(
                {'data': sr.data},
            )
        return Response(
            {'data': sr.errors},
        )
        
    def put(self,req,pk,*args, **kwargs):
        try: 
            tdd=td.objects.get(id=pk)
        except td.DoesNotExist: 
            return Response(
                {'message': 'does not exist'}
            ) 
        
        sr = td_serializer(tdd,data = req.data,partial=True)
        if sr.is_valid():
            sr.save()
            return Response(
                {'data': sr.data},
            )    
        return Response(
            {'data': sr.errors},
        )
    def delete(self,req,pk,*args, **kwargs):
        try: 
            tdd=td.objects.get(id=pk).delete()
        except td.DoesNotExist: 
            return Response(
                {'message': 'does not exist'}
            ) 
       
        return Response(
            {'data':"deleted"},
        )
