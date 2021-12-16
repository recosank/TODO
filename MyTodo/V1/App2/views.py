from .models import profile
from .serializers import p_s
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class p_v(APIView):
   
    def get(self, req,*args, **kwargs):
        p = profile.objects.get(user=req.user)
        serializer = p_s(p)
        return Response(serializer.data)
    
    def patch(self,req,*args, **kwargs):
        p = profile.objects.get(user=req.user)
        serializer = p_s(p, data=req.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
            )
        return Response(
            {'data': serializer.errors},
        )
   
       
        

        


    

  
        

   