from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_api_admin')
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE,related_name='user_api_cust')
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	# adress1 = models.CharField(max_lenght=1000, null = True, blank=true)
	# adress2 = models.CharField(max_lenght=1000, null = True, blank=true)

	def __str__(self):
		return self.user.username




class Gender(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name



class BigCategory(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Big Categories"

class Category(models.Model):
	name = models.CharField(max_length=50)
	bigcategory = models.ForeignKey(BigCategory, on_delete = models.SET_NULL, null = True)
	slug = models.SlugField(default="")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Categories"



class Product(models.Model):
	name = models.CharField(max_length=200)
	gender = models.ForeignKey(Gender, on_delete = models.SET_NULL, null = True)
	price = models.FloatField()
	category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
	Primaryimage = models.ImageField(upload_to="images/",default="")
	Secondimage = models.ImageField(upload_to="images/",default="",null = True)
	Thirdimage = models.ImageField(upload_to="images/",default="", null = True)
	description = models.CharField(max_length=2000,default="", null = True )
	model = models.CharField(max_length=200, default="", null = True)
	warrantyStatus = models.CharField(max_length=200, default="",null = True )
	distributor = models.CharField(max_length=200, default="", null = True)
	color = models.CharField(max_length=200, default="", null = True)
	slug = models.SlugField(default="")
	size = models.CharField(max_length=10, null = True, default ="Standart")
	quantity = models.IntegerField(default=0, null=True, blank=True)
	popularity = models.IntegerField(default=0, null=True, blank=True)


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("store:productDetail", kwargs = {
		'slug': self.slug
		})




class ReviewList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "ReviewList: " + str(self.id)

class ReviewItem(models.Model):
    review_list = models.ForeignKey(ReviewList, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.PositiveIntegerField(null=True, blank=True )
    comment = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "ReviewList: " + str(self.review_list.id) + " ReviewItem: " + str(self.id)




class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,related_name='user_api_address')
	district = models.CharField(max_length=200, blank=True, null=True)
	city = models.CharField(max_length=200, blank=True, null=True)
	street = models.CharField(max_length=200, blank=True, null=True)
	apartment = models.CharField(max_length=200,blank=True, null=True)
	zipcode = models.CharField(max_length=200, blank=True, null=True)
	# date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username



class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    subtotal = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("Order in transit", "Order in transit"),
    ("Order delivered", "Order Delivered"),

)

METHOD = (
    ("Visa", "Visa"),
    ("Mastercard", "Mastercard"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)
    ordered_by = models.CharField(max_length=200,null=True, blank=True)
    shipping_address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField(null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Visa", null=True, blank=True)
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)

# class Payment(models.Model):
# 	customer = models.ForeignKey( Customer, on_delete=models.SET_NULL, null=True, blank=True)
# 	amount = models.FloatField(null=True, blank=True)
# 	timestamp = models.DateTimeField(auto_now_add=True)
# 	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
# 	def __str__(self):
# 		return self.customer.name
