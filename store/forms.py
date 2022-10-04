from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import Order, OrderProduct
from .models import ReviewItem
from .models import Product
from .models import Category
from django.core.files.uploadedfile import SimpleUploadedFile

# from django_countries.fields import CountryField
# from django_countries.widgets import CountrySelectWidget


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address",
                  "email", "payment_method"]


class ProductManagersLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    distributor = forms.Select()

class SalesManagersLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class PriceChangeForm(forms.Form):

    discount = forms.IntegerField(label='Discount rate')




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class ReviewItemForm(forms.ModelForm):
	class Meta:
		model = ReviewItem
		fields = ["comment", "rate"]

class ContactForm(forms.Form):
    name= forms.CharField(max_length=500, label="Name")
    email= forms.EmailField(max_length=500, label="Email")
    comment= forms.CharField(label='',widget=forms.Textarea(
                        attrs={'placeholder': 'Enter your comment here'}))


class StockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ "quantity"]
        widgets = {
            "quantity": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the new quantity in stock..."
            }),

        }


class PriceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ "price"]
        widgets = {
            "price": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the new price..."
            }),

        }


class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Product
        fields = ["name", "gender",  "slug", "category", "Primaryimage", "Secondimage", "Thirdimage", "model", "warrantyStatus",
                   "color", "quantity", "popularity", "price", "description"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the unique slug here..."
            }),
            "gender": forms.Select(attrs={
                "class": "form-control",
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
             "Primaryimage": forms.FileInput(attrs={
                 "class": "form-control"
             }),
             "Secondimage": forms.ClearableFileInput(attrs={
                 "class": "form-control"
             }),
            "Thirdimage": forms.ClearableFileInput(attrs={
                 "class": "form-control"
             }),
             "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Marked price of the product..."
             }),
            "model": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "warrantyStatus": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product warranty here..."
            }),
            "color": forms.TextInput(attrs={
                "class": "form-control",

            }),
            "quantity": forms.TextInput(attrs={
                "class": "form-control",

            }),
            "popularity": forms.TextInput(attrs={
                "class": "form-control",

            }),



         }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "bigcategory" ]
        widgets = {
            "bigcategory": forms.Select(attrs={
                "class": "form-control",
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the unique slug here..."
            }),

         }

class DateForm(forms.ModelForm):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    class Meta:
        model = Order
        fields = []


# class UserProfileInfoForm(forms.ModelForm):
#     class Meta():
#         model = Customer
#         fields = ('adress1','adress2')
