from django.urls import include, path
from rest_framework import routers

from api.views import *

urlpatterns = [
    path('customers/', Customers.as_view()),
    path('customers/<int:user>', Customers_detail.as_view()),

    path('genders/', Genders.as_view()),
    path('big_category/', Big_Category.as_view()),
    path('category/', CategoryView.as_view()),

    path('product/',ProductView.as_view()),
    path('product/<int:category>', product_detail.as_view()),

    path('product/slug/<str:slug>', product_detail_slug.as_view()),



    path('reviewlist/',ReviewListView.as_view()),
    path('reviewlist/<int:customer>',reviewlist_detail.as_view()),

    path('reviewitem/',ReviewItemView.as_view()),

    path('address/',AddressView.as_view()),
    path('address/<int:user>',address_detail.as_view()),

    path('cart/',CartView.as_view()),
    path('cart/<int:customer>',cart_detail.as_view()),

    path('cartproduct/',CartProductView.as_view()),    

    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]