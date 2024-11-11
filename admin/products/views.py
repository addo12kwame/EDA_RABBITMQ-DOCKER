from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
import random

from .models import Products,User
from .producer import publish
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
        publish('product_created',serializer.data)
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
        publish('product_updated',serializer.data)

        return Response(serializer.data,status=HTTP_202_ACCEPTED)



    def destroy(self,request,pk): #/api/products/<str:id>
        product = Products.objects.get(id=pk)
        product.delete()
        publish('product_deleted',pk)

        return Response(status=HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self,request):

        user_rand = random.Random().randint(1,100)   # getting a random number
        new_user = User(id=user_rand)
        new_user.save()
        users = User.objects.all()
        print(users)
        user = random.choice(users)
        return Response({
            'id':user.id
        })



