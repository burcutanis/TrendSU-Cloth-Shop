from os import stat
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.views import View

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from requests import request

from api.models import Product
from store.models import ProductManagersAdmin,Customer,Gender,BigCategory,Category,ReviewList,ReviewItem,Address,Cart,CartProduct,Order, Product
from api.serializers import *


class Customers(APIView):

    def get(self,request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({'customers':serializer.data})
    def post(self,request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class Customers_detail(APIView):

    def get(self,request,user):
        customers = Customer.objects.get(user=user)
        serializer = CustomerSerializer(customers)
        return Response(serializer.data)

class Genders(APIView):

    def get(self,request):
        genders = Gender.objects.all()
        serializer = GenderSerializer(genders, many=True)
        return Response({'genders':serializer.data})
    def post(self,request):
        serializer = GenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class Big_Category(APIView):

    def get(self,request):
        big_categories = BigCategory.objects.all()
        serializer = BigCategorySerializer(big_categories, many=True)
        return Response({'big_categories':serializer.data})
    def post(self,request):
        serializer = BigCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class CategoryView(APIView):

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'categories':serializer.data})
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class ProductView(APIView):

    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products':serializer.data})
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class product_detail(APIView):

    def get(self,request,category):
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class product_detail_slug(APIView):

    def get(self,request,slug):
        products = Product.objects.filter(slug=slug)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ReviewListView(APIView):

    def get(self,request):
        reviews = ReviewList.objects.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response({'reviews':serializer.data})
    def post(self,request):
        serializer = ReviewListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class reviewlist_detail(APIView):

    def get(self,request,customer):
        reviews = ReviewList.objects.filter(customer=customer)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewItemView(APIView):

    def get(self,request):
        reviews = ReviewItem.objects.all()
        serializer = ReviewItemSerializer(reviews, many=True)
        return Response({'reviews':serializer.data})
    def post(self,request):
        serializer = ReviewItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class OrderView(APIView):

    def get(self,request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({'orders':serializer.data})
    def post(self,request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class AddressView(APIView):

    def get(self,request):
        address = Address.objects.all()
        serializer = AddressSerializer(address, many=True)
        return Response({'addresses':serializer.data})
    def post(self,request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class address_detail(APIView):

    def get(self,request,user):
        adress = Address.objects.filter(user=user)
        serializer = AddressSerializer(adress, many=True)
        return Response(serializer.data)


class CartView(APIView):

    def get(self,request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response({'carts':serializer.data})
    def post(self,request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class cart_detail(APIView):

    def get(self,request,customer):
        carts = Cart.objects.filter(customer=customer)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)


class CartProductView(APIView):

    def get(self,request):
        cartproducts = CartProduct.objects.all()
        serializer = CartProductSerializer(cartproducts, many=True)
        return Response({'cartProducts':serializer.data})
    def post(self,request):
        serializer = CartProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


class OrderView(APIView):

    def get(self,request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({'orders':serializer.data})
    def post(self,request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
