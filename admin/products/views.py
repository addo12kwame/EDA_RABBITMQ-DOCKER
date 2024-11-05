from itertools import product

from django.core.serializers import serialize
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
import random

from .models import Products,User
from .serializers import ProductSerializer



class ProductViewSet(viewsets.ViewSet):
    def list(self, request):  #/api/products---> get
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    def create(self,request):  #/api/products----> post
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


    def retrieve(self,request,pk=None   ): #/api/products/<str:id>
        product = Products.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self,request,pk): #/api/products/<str:id>
        product = Products.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=HTTP_202_ACCEPTED)



    def destroy(self,request,pk): #/api/products/<str:id>
        product = Products.objects.get(id=pk)
        product.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self,request):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id':user.id
        })