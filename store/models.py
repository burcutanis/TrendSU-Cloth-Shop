from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Distributor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductManagersAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    distributor = models.ForeignKey(Distributor, on_delete = models.SET_NULL, null = True, blank=True)


    def __str__(self):
        return self.user.username +  " --- distributor: " + self.distributor.name

class SalesManagersAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    distributor = models.ForeignKey(Distributor, on_delete = models.SET_NULL, null = True, blank=True)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
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
    others = models.CharField(max_length=10 )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    gender = models.ForeignKey(Gender, on_delete = models.SET_NULL, null = True)
    price = models.FloatField( null = True,  blank=True)
    discountRate = models.IntegerField(default=0, null=True, blank=True)
    sellingPrice = models.FloatField(default=0, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True,  blank=True)
    Primaryimage = models.ImageField(upload_to="images/",default="", null = True,  blank=True)
    Secondimage = models.ImageField(upload_to="images/",default="",null = True,  blank=True)
    Thirdimage = models.ImageField(upload_to="images/",default="", null = True,  blank=True)
    description = models.CharField(max_length=2000,default="", null = True)
    model = models.CharField(max_length=200, default="", null = True)
    warrantyStatus = models.CharField(max_length=200, default="",null = True )
    distributor = models.ForeignKey(Distributor, on_delete = models.SET_NULL, null = True, blank=True)
    color = models.CharField(max_length=200, default="", null = True)
    slug = models.SlugField(default="")
    size = models.CharField(max_length=10, default ="Standart")
    quantity = models.IntegerField(default=0, null=True, blank=True)
    popularity = models.IntegerField(default=0, null=True, blank=True)
    purchase_price = models.IntegerField(default=50)



    def __str__(self):
        return self.name  + " --- distributor: " + str(self.distributor)

    def get_absolute_url(self):
        return reverse("store:productDetail", kwargs = {
        'slug': self.slug
        })


REVIEW_STATUS = (
    ("Not Approved", "Not Approved"),
    ("Approved", "Approved"),
)

class WishList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "WishList: " + str(self.id)

class WishItem(models.Model):
    wish_list = models.ForeignKey(WishList, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "WishList: " + str(self.wish_list.id) + " WishItem: " + str(self.id)



class ReviewList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "ReviewList: " + str(self.id)

class ReviewItem(models.Model):
    review_list = models.ForeignKey(ReviewList, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.PositiveIntegerField(null=True, blank=True )
    distributor = models.ForeignKey(Distributor, on_delete = models.SET_NULL, null = True, blank=True)
    comment = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    approved = models.BooleanField(
            default=False, null=True, blank=True)
    review_status = models.CharField(max_length=50, choices=REVIEW_STATUS, null=True, blank=True)


    def __str__(self):
        return "ReviewList: " + str(self.review_list.id) + " ReviewItem: " + str(self.id)




class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
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
    discount =  models.FloatField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.FloatField( default=0, null = True,  blank=True)
    discountRate = models.PositiveIntegerField(default=0,null=True, blank=True)
    discountTotal =  models.FloatField(default=0, null=True, blank=True)
    sellingPrice = models.FloatField(default=0, null=True, blank=True)
    subtotal = models.FloatField(default=0, null=True, blank=True)
    distributor = models.ForeignKey(Distributor, on_delete = models.SET_NULL, null = True, blank=True)

    rate = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)





ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("Order In Transit", "Order In Transit"),
    ("Order Delivered", "Order Delivered"),
    ("Order Cancelled", "Order Cancelled"),
    ("Order Returned", "Order Returned"),
)

METHOD = (
    ("Visa", "Visa"),
    ("Mastercard", "Mastercard"),
)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)
    ordered_by = models.CharField(max_length=200,null=True, blank=True)
    shipping_address = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    distributor = models.ForeignKey(Distributor, on_delete = models.SET_NULL, null = True, blank=True)
    discount =  models.FloatField(default=0, null=True, blank=True)
    total = models.FloatField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Visa", null=True, blank=True)
    delivery_completed = models.BooleanField(
        default=False, null=True, blank=True)
    all_received = models.BooleanField(
        default=False, null=True, blank=True)
    processing = models.BooleanField(
        default=False, null=True, blank=True)
    inTransit = models.BooleanField(
        default=False, null=True, blank=True)
    delivered = models.BooleanField(
        default=False, null=True, blank=True)

    # subtotal = models.PositiveIntegerField(null=True, blank=True)


    def checkIfAllDelivered(self):
        orderProductSet = self.orderproduct_set.all()
        check = True
        for op in orderProductSet:

            if op.order_status != "Order Delivered" or op.order_status != "Order delivered":
                check = False
                self.delivery_completed = False
        if check == True:
            self.delivery_completed = True
        self.save()
        return check

    def checkIfAllReceived(self):
        orderProductSet = self.orderproduct_set.all()
        check = True
        for op in orderProductSet:
            if op.order_status != "Order Received":
                check = False
        if check == True:
            self.all_received = True
        self.save()
        return check

    def IfAllDelivered(self):
        orderProductSet = self.orderproduct_set.all()
        check = True
        for op in orderProductSet:
            if op.order_status != "Order Delivered":
                check = False
        if check == True:
            self.delivered = True
        self.save()
        return check


    def checkIfProcessing(self):
        orderProductSet = self.orderproduct_set.all()
        check = True
        for op in orderProductSet:
            if op.order_status == "Order Processing":
                check = False
        if check == False:
            self.processing = True
        self.save()
        return not check

    def checkIfinTransit(self):
        orderProductSet = self.orderproduct_set.all()
        check = True
        for op in orderProductSet:
            if op.order_status == "Order In Transit":
                check = False
                print("check is false")
        if check == False:
            self.inTransit = True
            print("in transit true")
        self.save()
        print(check)
        return not check

    def checkCanceled(self):
        orders = OrderProduct.objects.filter(order_id = self.pk)
        check = True
        for ord in orders:
            if ord.order_status == "Order Canceled" or ord.order_status == "Order canceled":
                check = False
        return not check

    def __str__(self):
        return "Order: " + str(self.id)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, null=True, blank=True)
    distributor = models.ForeignKey(Distributor, on_delete = models.SET_NULL, null = True, blank=True)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    price = models.FloatField( null = True,  blank=True)
    discountRate = models.PositiveIntegerField(default=0,null=True, blank=True)
    discountTotal =  models.FloatField(default=0, null=True, blank=True)
    sellingPrice = models.FloatField(default=0, null=True, blank=True)
    subtotal = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.order.id) + " OrderProduct: " + str(self.id)

# class Payment(models.Model):
# 	customer = models.ForeignKey( Customer, on_delete=models.SET_NULL, null=True, blank=True)
# 	amount = models.FloatField(null=True, blank=True)
# 	timestamp = models.DateTimeField(auto_now_add=True)
# 	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
# 	def __str__(self):
# 		return self.customer.name
