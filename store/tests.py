from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse
from .models import Distributor
from .models import Gender
from .models import BigCategory
from .models import SalesManagersAdmin
from .models import ProductManagersAdmin
from .models import Customer
from .models import Product
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class HomepageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "store/womenPage.html")

    def test_template_content(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Shop Dresses")
        self.assertNotContains(response, "Not on the page")


class ProdadminLoginTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/admin-login")
        self.assertEqual(response.status_code, 301)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("adminlogin"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("adminlogin"))
        self.assertTemplateUsed(response, "productmanagers/adminlogin.html")

    # def test_template_content(self):
    #     response = self.client.get(reverse("adminlogin"))
    #     self.assertContains(response, "Admin Login")
    #     self.assertNotContains(response, "Not on the page")

# class SalesadminLoginTests(TestCase):
#
#     def test_url_exists_at_correct_location(self):
#         response = self.client.get("/sales-admin-login")
#         self.assertEqual(response.status_code, 301)
#
#     def test_url_available_by_name(self):
#         response = self.client.get(reverse("SalesAdminLoginView"))
#         self.assertEqual(response.status_code, 200)
#
#     def test_template_name_correct(self):
#         response = self.client.get(reverse("adminlogin"))
#         self.assertTemplateUsed(response, "salesmanagers/adminlogin.html")
#
#     def test_template_content(self):
#         response = self.client.get(reverse("adminlogin"))
#         self.assertContains(response, "Admin Login")
#         self.assertNotContains(response, "Not on the page")

class adminPanelTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 301)

    def test_url_available_by_name(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 301)


class myOrdersTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/store/myOrders/")
        self.assertEqual(response.status_code, 302)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("store:myOrders"))
        self.assertEqual(response.status_code, 302)



class myBasketTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/store/myBasket")
        self.assertEqual(response.status_code, 301)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("store:myBasket"))
        self.assertEqual(response.status_code, 200)


class login(TestCase):
    def setUp(self):
            self.user = User.objects.create_user(username='test', password='12test12', email='test@example.com')
            self.user.save()

    def login(self):
        user = authenticate(username='test', password='12test12')
        if user is not None and user.is_authenticated:
            login(self.request, user)

    def tearDown(self):
        self.user.delete()


class myWishlistTests(TestCase):

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/store/myWishList")
        self.assertEqual(response.status_code, 301)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("store:myWishList"))
        self.assertEqual(response.status_code, 302)




class DistributorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.distributor = Distributor.objects.create(name="Dummy Distributor")

    def test_model_content(self):
        self.assertEqual(self.distributor.name, "Dummy Distributor")

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/store/productDetail/dress2")
        self.assertEqual(response.status_code, 301)


class GenderTest(TestCase):

    def create_gender(self, name="female"):
        return Gender.objects.create(name=name)

    def test_gender_creation(self):
        w = self.create_gender()
        self.assertTrue(isinstance(w, Gender))
        self.assertEqual(w.__str__(), w.name)

class SigninTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

class ProductTest(TestCase):

    def create_product(self,name="testproduct"):
        return Product.objects.create(name=name,gender=None,price=123,discountRate=000,sellingPrice=123,category=None,Primaryimage="pr1",Secondimage="pr2",Thirdimage="pr3",description="descc",model="modelss",warrantyStatus="warrant",distributor=None,color="colorr",slug="slugg",size="size",quantity=123,popularity=123)
    
    def test_isproductadded(self):
        w = self.create_product()
        self.assertTrue(isinstance(w, Product))
        self.assertEqual(w.__str__(), w.name  + " --- distributor: " + str(w.distributor))
    
    def test_productview(self):
        response = self.client.get("/store/allProducts")
        self.assertEqual(response.status_code, 301)

class FormTest(TestCase):

    def test_set_price_form(self):
        form = PriceChangeForm(data={
            'discount':100
        })
        self.assertTrue(form.is_valid(),True)

    def test_checkout_form(self):
        form = CheckoutForm(data={
            'ordered_by':1,
            'shipping_address':1,
            'email':1,
            'payment_method':1
        }) 
        self.assertTrue(not form.is_valid())