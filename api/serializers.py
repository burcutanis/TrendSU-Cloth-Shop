from rest_framework import serializers
from api.models import Product
from store.models import ProductManagersAdmin,Customer,Gender,BigCategory,Category,ReviewList,ReviewItem,Address,Cart,CartProduct,Order, Product


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user','full_name','image','mobile']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user','name','email']

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['name']

class BigCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BigCategory
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['bigcategory','slug']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','gender','price','category','Primaryimage','Secondimage',
        'Thirdimage','description','model','warrantyStatus','distributor','color','slug', 'quantity', 'size', 'id']


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewList
        fields = ['customer','created_at']

class ReviewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewItem
        fields = ['review_list','product','rate','comment','date_added']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['user','district','city','street','apartment','zipcode']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['customer','total','created_at']

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['cart','product','rate','quantity','subtotal']
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['cart','ordered_by','shipping_address','email','subtotal','discount','total','order_status','created_at','payment_method','payment_completed']
