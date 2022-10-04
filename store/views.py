#from urllib import response
import io
from tracemalloc import start
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.http import HttpResponse


from .forms import DateForm, PriceChangeForm, SalesManagersLoginForm, UserForm, ProductManagersLoginForm, ReviewItemForm, ContactForm, ProductForm, CategoryForm, StockForm,  PriceForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
from django.db.models import Q
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from cloth_shop.settings import EMAIL_HOST_USER
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required


import requests
from .models import *

def home(request):
    return render(request, 'store/womenPage.html')

def store(request):
    return render(request, 'store/store.html')
def payment(request):
    return render(request, 'store/payment.html')
def wishlist(request):
    return render(request, 'store/wishlist.html')

def sendemail(request):
    return render(request, 'store/send-email.html')


class RequestRefundView(TemplateView):
    template_name = "store/request_refund.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        order_id = self.kwargs['ord_id']
        print(order_id)
        # get product
        order_obj = OrderProduct.objects.get(id=order_id)
        print(order_obj.subtotal)
        print(order_obj.refund_requested)
        order_obj.refund_requested = True
        print(order_obj.refund_requested)
        order_obj.save()


        return context


class AddToWishList(TemplateView):
    template_name = "store/add_to_wishlist.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user:
            cust_obj, created = Customer.objects.get_or_create(user=self.request.user)
            cust_obj.name = self.request.user.first_name + " " + self.request.user.last_name
            cust_obj.email = self.request.user.email
            cust_obj.save()
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)
        if product_obj is None:
            print("--- add to wish list error, product not found for id: ----")
            print(product_id)
        else:
            cust_obj, created = Customer.objects.get_or_create(user=self.request.user)
            wishlist_obj , created = WishList.objects.get_or_create(customer=cust_obj)

            wishitem, created = WishItem.objects.get_or_create(
                wish_list=wishlist_obj, product=product_obj)

        return context

class myWishRemoveView(View):
    def get(self, request, *args, **kwargs):
        wishitem_id = self.kwargs["obj_id"]
        wishitem_obj =WishItem.objects.get(id=wishitem_id)
        if wishitem_obj is None:
            print("---- myWishRemoveView error, wishitem not found for id: ----")
            print(wishitem_id )
        else:
            wishitem_obj.delete()
        return redirect("store:myWishList")


class AddToCart(TemplateView):
    template_name = "store/add_to_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        print(product_id)
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                print(product_obj.name)
                print(product_obj.quantity)
                if product_obj.quantity > 0: #if product is in the stock
                    cartproduct.quantity += 1
                    cartproduct.subtotal += product_obj.price
                    cartproduct.save()

                    cart_obj.total += product_obj.price
                    cart_obj.save()
                else:
                    print("else")
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
                print(product_obj.name)
                print(product_obj.quantity)
                if product_obj.quantity > 0: #if product is in the stock

                    cartproduct.quantity = 1
                    cartproduct.subtotal = product_obj.price
                    cartproduct.save()

                    cart_obj.total += product_obj.price
                    cart_obj.save()
                else:
                    cartproduct.delete()

        else:
            if self.request.user.is_authenticated and self.request.user:
                cust_obj, created = Customer.objects.get_or_create(user=self.request.user)
                cart_obj , created = Cart.objects.get_or_create(customer=cust_obj)
                self.request.session['cart_id'] = cart_obj.id
            else:
                cart_obj = Cart.objects.create(total=0)
                self.request.session['cart_id'] = cart_obj.id

            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()

        return context


class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("store:myBasket")


class CheckoutView(CreateView):
    template_name = "store/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("store:home")

    def dispatch(self, request, *args, **kwargs):
        print("hey")
        if request.user.is_authenticated and request.user:
            pass
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        # print(self.request.user.username)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if cart_obj is None:
                return HttpResponse("error: cart object with id:",cart_id,"does not exist")

            cart_obj = Cart.objects.get(id=cart_id)
            cp_set = cart_obj.cartproduct_set.all()
            for cp in cp_set:
                product_obj = cp.product
                if product_obj.quantity < cp.quantity:
                    cp.quantity = product_obj.quantity
                    if cp.quantity == 0:
                        cp.delete()
                    return HttpResponse("Product is not in stock. My basket is updated")

            user_obj = self.request.user
            cust_obj, created = Customer.objects.get_or_create(user=self.request.user)
            order_obj = Order.objects.create(
                    customer=cust_obj, total = cart_obj.total, discount = 0)
            for cp in cp_set:
                orderproduct = OrderProduct.objects.create(
                    order=order_obj, product=cp.product, price=cp.product.price, quantity=cp.quantity, subtotal=cp.product.price*cp.quantity, distributor = cp.product.distributor, order_status = "Order Received")
                if cp.product.quantity < cp.quantity:
                    print("Error")
                    cp.quantity = cp.product.quantity
                    cp.product.quantity = 0
                    cp.product.save()
                    cp.save()
                else:
                    cp.product.quantity = cp.product.quantity - cp.quantity
                    cp.product.save()

            # order_obj.order_status = "Order Received"
            order_obj.shipping_address = form.cleaned_data.get("shipping_address")
            order_obj.ordered_by = form.cleaned_data.get("ordered_by")
            order_obj.payment_method = form.cleaned_data.get("payment_method")
            order_obj.email = form.cleaned_data.get("email")
            order_obj.save()
            del self.request.session['cart_id']
            cart_obj.delete()
            self.request.session['order_id'] = order_obj.id
            # if order_obj.payment_method == "Visa":
            #     return redirect(reverse("store:payment") + "?o_id=" + str(order_obj.id))
            # elif order_obj.payment_method == "Mastercard":
            #     return redirect(reverse("store:payment") + "?o_id=" + str(order_obj.id))

        else:
            return redirect("store:home")
        return super().form_valid(form)

def SendEmail(request, id):
    object = Order.objects.get(id=id)

    subject = "Your checkout - thanks for choosing us!"
    mylist = [object.ordered_by,object.total,object.created_at,object.shipping_address]
    start_msg = "You can find your order details which are customer name, total checkout price, date and shipping address subsequently.\n --------------------------------"
    message = start_msg + "\n" +",  ".join(str(obj) for obj in mylist) + '\n' + "Have a good one!"
    from_email = object.email
    #breakpoint()
    if subject and message and from_email:
        try:
            send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list = [from_email])
            messages.info(request, 'Email sent successfully!')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/store/myOrders')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Something went wrong :(')

class myWishListView(TemplateView):
    template_name = "store/myWishList.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            #print("my wish list view 0-------")
            pass
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        print("my wish list view 1-------")
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and self.request.user:
            cust_obj, created = Customer.objects.get_or_create(user=self.request.user)
            wishlist_obj , created = WishList.objects.get_or_create(customer=cust_obj)
            print(wishlist_obj)
            context['wishlist'] = wishlist_obj
            #print("my wish list view 2-------")
            #print(wishlist_obj.id)
        return context

class myBasketView(TemplateView):
    template_name = "store/myBasket.html"
    #print("hey2")

    def get_context_data(self, **kwargs):
        #print("hey")
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated and self.request.user:
            cust_obj, created = Customer.objects.get_or_create(user=self.request.user)
            cart_obj , created = Cart.objects.get_or_create(customer=cust_obj)
            self.request.session['cart_id'] = cart_obj.id

        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
                cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

class CustomerPaymentView(TemplateView):
    template_name = "store/payment.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        order_id = self.request.session['order_id']
        order_obj = Order.objects.get(id=order_id)
        print(order_id)
        print(order_obj.id)
        context["order_obj"] = order_obj
        return context


class CustomerReceiptView(TemplateView):
    template_name = "store/receipt.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            ord_obj = Order.objects.get(id=order_id)
            print(order_id)
            print(request.user.customer)
            if request.user.customer != ord_obj.customer:
                return redirect("store:receipt")
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        order_id = self.kwargs["pk"]
        ord_obj = Order.objects.get(id=order_id)
        print("-------------------------")
        print(order_id)
        print(ord_obj.total)
        context['customer'] = customer
        context["ord_obj"] = ord_obj
        return context



class CustomerOrdersView(TemplateView):
    template_name = "store/myOrders.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(customer=customer).order_by("-id")
        context["orders"] = orders
        return context

class CustomerCancelOrdersView(TemplateView):
    template_name = "store/myOrders.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            orderProducts = OrderProduct.objects.filter(order_id=order_id)
            for orderProduct in orderProducts:
                if orderProduct.order_status != "Order canceled" and orderProduct.order_status != "Order Canceled":
                    product = Product.objects.get(id=orderProduct.product_id)
                    product.quantity += orderProduct.quantity
                    product.save()
                    orderProduct.order_status = "Order Canceled"
                    orderProduct.save()
            return redirect("store:myOrders")
        else:
            return redirect("store:user_login")





class CustomerProfileView(TemplateView):
    template_name = "store/myProfile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context

class CustomerOrderDetailView(DetailView):
    template_name = "store/orderDetails.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.customer:
                return redirect("store:myOrders")
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)


def womenPage(request):
    return render(request, 'store/womenPage.html')
def menPage(request):
    return render(request, 'store/menPage.html')
def payment(request):
    return render(request, 'store/payment.html')


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/productDetail.html"



class OrderByPriceAs(ListView):
    model = Product
    template_name = "store/results.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        # results=Product.objects.filter(name__icontains=kw)
        results = Product.objects.order_by("price")
        print(results)
        context["results"] = results
        return context

class OrderByPriceDes(ListView):
    model = Product
    template_name = "store/results.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        # results=Product.objects.filter(name__icontains=kw)
        results = Product.objects.order_by("-price")
        print(results)
        context["results"] = results
        return context

class OrderByPopularityAs(ListView):
    model = Product
    template_name = "store/results.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        # results=Product.objects.filter(name__icontains=kw)
        results = Product.objects.order_by("popularity")
        print(results)
        context["results"] = results
        return context

class OrderByPopularityDes(ListView):
    model = Product
    template_name = "store/results.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        # results=Product.objects.filter(name__icontains=kw)
        results = Product.objects.order_by("-popularity")
        print(results)
        context["results"] = results
        return context


class SearchView(TemplateView):
    template_name = "store/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        # results=Product.objects.filter(name__icontains=kw)
        results = Product.objects.filter(
             Q(name__icontains=kw) | Q(description__icontains=kw) )
        print(results)
        context["results"] = results
        return context

class AddToReviewList(CreateView):
    template_name = "store/rate.html"
    form_class = ReviewItemForm
    success_url = reverse_lazy("store:home")

    def dispatch(self, request, *args, **kwargs):
        print("hey")
        if request.user.is_authenticated and request.user:
            pass
        else:
            return redirect("store:user_login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)
        self.request.session['product_id'] = product_obj.id
        cust_obj, created = Customer.objects.get_or_create(user=self.request.user)
        reviewlist_obj , created = ReviewList.objects.get_or_create(customer=cust_obj)
        self.request.session['reviewlist_id'] = reviewlist_obj.id

        review_obj, created = ReviewItem.objects.get_or_create(
                review_list=reviewlist_obj, product=product_obj)
        self.request.session['review_id'] = review_obj.id
        return context

    def form_valid(self, form):
        reviewlist_id = self.request.session.get("reviewlist_id")
        review_id = self.request.session.get("review_id")
        product_id = self.request.session['product_id']
        product_obj = Product.objects.get(id=product_id)
        print(reviewlist_id)
        print(review_id)
        print(product_id)
        if review_id:
            reviewlist_obj = ReviewList.objects.get(id=reviewlist_id)
            review = ReviewItem.objects.get(id=review_id)
            review.review_status = "Not Approved"
            dis = product_obj.distributor
            review.distributor = dis
            cm = form.cleaned_data.get("comment")
            rt = form.cleaned_data.get("rate")
            review.approved = False
            review.comment = cm
            if rt > 10:
                review.delete()
                return HttpResponse("Invalid rate value. You have to write an integer between 0 and 10")
            else:
                review.rate = rt
                review.save()
                return redirect("store:myRatingsEvaluated")
        else:
            print("review list id not found")
            return redirect("store:home")


class CustomerReviewView(TemplateView):
    template_name = "store/myRatingsEvaluated.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user:
            cust_obj, created = Customer.objects.get_or_create(user=self.request.user)
            reviewlist_obj , created = ReviewList.objects.get_or_create(customer=cust_obj)
            reviewlist_id = reviewlist_obj.id
            if reviewlist_id:
                reviewlist = ReviewList.objects.get(id=reviewlist_id)
            else:
                reviewlist = None
        context['reviewlist'] = reviewlist
        return context

class ProductReviewView(TemplateView):
    template_name = "store/productcomments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs["pk"]
        product_obj = Product.objects.get(id=product_id)
        if self.request.user.is_authenticated and self.request.user:
            review_set  = ReviewItem.objects.filter(product=product_obj, review_status ="Approved")
            context['reviews'] = review_set
        return context






class AllListView(ListView):
    model = Product
    template_name = 'store/allProducts.html'
    def query_set(self):
        return Product.objects.all()

    # template = "store/allProducts.html"
    # def get(self,request):
    #     response = requests.get('http://127.0.0.1:8000/api/product/3').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/4').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/6').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/7').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/8').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/9').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/10').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/11').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/15').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/12').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/13').json()
    #     return render(request,self.template,{'response':response})


class OtherCategoryListView(TemplateView):
    template_name = "store/OtherCategories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        prod_set = Product.objects.filter(category__others__contains = "others")

        context['prod_set'] = prod_set
        return context

    # model = Product
    # template_name = 'store/OtherCategories.html'
    # def query_set(self):
    #     return Product.objects.filter(category__others = 'others')


class DressListView(ListView):

    template = 'store/womenDressPage.html'

    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/3').json()
        return render(request,self.template,{'response':response})

class SkirtListView(ListView):

    template = "store/womenSkirtPage.html"

    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/4').json()
        return render(request,self.template,{'response':response})

class SweatshirtListView(ListView):

    template = "store/womenSweatshirtPage.html"

    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/6').json()
        return render(request,self.template,{'response':response})
class BlousesListView(ListView):

    template = "store/womenBlousesPage.html"

    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/7').json()
        return render(request,self.template,{'response':response})
class SweaterListView(ListView):

    template = "store/womenSweaterPage.html"

    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/8').json()
        return render(request,self.template,{'response':response})
class TshirtListView(ListView):

    template = "store/womenTshirtPage.html"

    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/9').json()
        return render(request,self.template,{'response':response})
class CoatListView(ListView):

    template = "store/womenCoatPage.html"
    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/10').json()
        return render(request,self.template,{'response':response})

class SleepListView(ListView):

    template = "store/womenSleepPage.html"
    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/11').json()
        return render(request,self.template,{'response':response})

class ShortListView(ListView):

    template = "store/womenShortPage.html"
    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/15').json()
        return render(request,self.template,{'response':response})

class PantListView(ListView):

    template = "store/womenJeanPage.html"
    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/12').json()
        return render(request,self.template,{'response':response})
class SweatsuitListView(ListView):

    template = "store/womenSweatsuitPage.html"
    def get(self,request):
        response = requests.get('http://127.0.0.1:8000/api/product/13').json()
        return render(request,self.template,{'response':response})




def myOrders(request):
    return render(request, 'store/myOrders.html')
def myRatings(request):
    return render(request, 'store/myRatings.html')
def myRatingsEvaluated(request):
    return render(request, 'store/myRatingsEvaluated.html')
def orderDetails(request):
    return render(request, 'store/orderDetails.html')
def receipt(request):
    return render(request, 'store/receipt.html')






# LOGIN
# Create your views here.


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('store:womenPage'))


def register(request):
    registered = False
    if request.method == 'POST':
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()
            # Now save model

            # Registration Successful!
            registered = True
            return HttpResponseRedirect(reverse('store:user_login'))
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'store/register.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('store:womenPage')) #kullanıcıyı index page'ine atıyor.
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'store/login.html', {})


#PRODUCTS MANAGERS PAGES

def productmanagersHome(request):
    return render(request, 'productmanagers/adminHome.html')

class ProdAdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and ProductManagersAdmin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("../admin-login/")
        return super().dispatch(request, *args, **kwargs)

class AdminLoginView(FormView):
    template_name = "productmanagers/adminlogin.html"
    form_class = ProductManagersLoginForm
    success_url = reverse_lazy("store:productmanagersHome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and ProductManagersAdmin.objects.filter(user=usr).exists():
            login(self.request, usr)
            return HttpResponseRedirect(reverse('store:productmanagersHome'))
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

@login_required
def product_managers_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('store:productmanagersHome'))

# class AdminRequiredMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and ProductManagersAdmin.objects.filter(user=request.user).exists():
#             pass
#         else:
#             return redirect("/admin-login/")
#         return super().dispatch(request, *args, **kwargs)

class AdminPendingOrdersView(ProdAdminRequiredMixin,TemplateView):
    template_name = "productmanagers/adminPendingOrders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        context["distributor"] = dis
        context["pendingorders"] = OrderProduct.objects.filter(
            order_status="Order Received" , distributor=dis).order_by("-id")
        return context

class AdminPendingRefundRequestsView(ProdAdminRequiredMixin,TemplateView):
    template_name = "productmanagers/adminPendingRefundRequests.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        context["distributor"] = dis
        context["pendingrefundrequests"] = OrderProduct.objects.filter(
            refund_requested=True ,refund_granted = False, distributor=dis).order_by("-id")
        return context

class AdminAllRefundRequestsView(ProdAdminRequiredMixin,TemplateView):
    template_name = "productmanagers/adminAllRefundRequests.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        context["distributor"] = dis
        context["allrefundrequests"] = OrderProduct.objects.filter(
            refund_requested=True , distributor=dis).order_by("-id")
        return context


class GrantRefundView(ProdAdminRequiredMixin,TemplateView):
    template_name = "productmanagers/grant_refund.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        context["distributor"] = dis
        # get product id from requested url
        order_id = self.kwargs['orderP_id']
        print(order_id)
        # get product
        order_obj = OrderProduct.objects.get(id=order_id)
        print(order_obj.subtotal)
        print(order_obj.refund_requested)
        order_obj.refund_granted = True
        order_obj.order_status = "Order Returned"
        order_obj.product.quantity += order_obj.quantity
        print(order_obj.refund_requested)
        order_obj.product.save()
        order_obj.save()

class AdminOrderDetailView(ProdAdminRequiredMixin,DetailView):
    template_name = "productmanagers/adminorderdetail.html"
    model = OrderProduct
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        context["distributor"] = dis
        context["allstatus"] = ORDER_STATUS
        return context

class AdminOrderListView(ProdAdminRequiredMixin,ListView):
    model = OrderProduct
    template_name = "productmanagers/adminorderlist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        context["distributor"] = dis
        results = OrderProduct.objects.filter(distributor=dis).order_by("-id")
        print(results)
        context["allorders"] = results
        return context



class AdminOrderStatusChangeView(ProdAdminRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = OrderProduct.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("store:adminorderdetail", kwargs={"pk": order_id}))

class PendingReviewView(ProdAdminRequiredMixin,TemplateView):
    template_name = "productmanagers/pendingComment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        context["distributor"] = dis
        context["pendingreviews"] = ReviewItem.objects.filter(
            review_status="Not Approved" , distributor=dis).order_by("-id")
        return context

class AdminReviewListView(ProdAdminRequiredMixin,ListView):
    model = ReviewItem
    template_name = "productmanagers/adminreviewlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        results = ReviewItem.objects.filter(distributor=dis).order_by("-id")
        print(results)
        context["allreviews"] = results
        context["distributor"] = dis
        return context


class AdminReviewDetailView(ProdAdminRequiredMixin, DetailView):
    template_name = "productmanagers/admincommentdetail.html"
    model = ReviewItem
    context_object_name = "review_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        context["distributor"] = dis
        context["allstatus"] = REVIEW_STATUS
        return context

class AdminReviewStatusChangeView(ProdAdminRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        reviewitem_id = self.kwargs["pk"]
        reviewitem_obj = ReviewItem.objects.get(id=reviewitem_id)
        new_status = request.POST.get("status")
        reviewitem_obj.review_status = new_status
        reviewitem_obj.save()
        return redirect(reverse_lazy("store:admindetailComment", kwargs={"pk": reviewitem_id}))




class AdminProductListView(ProdAdminRequiredMixin,ListView):
    model = Product
    template_name =  "productmanagers/adminproductlist.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.productmanagersadmin.distributor
        results = Product.objects.filter(distributor=dis).order_by("-id")
        print(results)
        context["results"] = results
        context["distributor"] = dis
        return context



    # def get(self,request, **kwargs):
    #     response = requests.get('http://127.0.0.1:8000/api/product/3').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/4').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/6').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/7').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/8').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/9').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/10').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/11').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/15').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/12').json()
    #     response += requests.get('http://127.0.0.1:8000/api/product/13').json()
    #     return render(request,self.template,{'response':response})


class AdminProductCreateView(ProdAdminRequiredMixin,CreateView):
    template_name = "productmanagers/adminproductadd.html"
    form_class = ProductForm
    success_url = reverse_lazy("store:adminproductlist")

    def form_valid(self, form):
        product_obj = Product.objects.create()
        product_obj.distributor = self.request.user.productmanagersadmin.distributor
        product_obj.name = form.cleaned_data.get("name")
        product_obj.gender = form.cleaned_data.get("gender")
        product_obj.slug = form.cleaned_data.get("slug")
        product_obj.category = form.cleaned_data.get("category")
        Primaryimage = self.request.FILES.get("Primaryimage")
        product_obj.Primaryimage = Primaryimage
        Secondimage = self.request.FILES.get("Secondimage")
        product_obj.Secondimage = Secondimage
        Thirdimage = self.request.FILES.get("Thirdimage")
        product_obj.Thirdimage = Thirdimage
        product_obj.model = form.cleaned_data.get("model")
        product_obj.warrantyStatus = form.cleaned_data.get("warrantyStatus")
        product_obj.color = form.cleaned_data.get("color")
        # product_obj.size = form.cleaned_data.get("size")
        product_obj.quantity = form.cleaned_data.get("quantity")
        product_obj.popularity = form.cleaned_data.get("popularity")
        product_obj.price = form.cleaned_data.get("price")
        product_obj.description = form.cleaned_data.get("description")
        product_obj.save()
        return redirect("store:adminproductlist")



class AdminProductDeleteView(ProdAdminRequiredMixin,CreateView):
    template_name = "productmanagers/adminproductlist.html"
    context_object_name = "product_obj"
    success_url = reverse_lazy("store:adminproductlist")

    def get(self, request, *args, **kwargs):
        pr_id = self.kwargs["pr_id"]
        action = request.GET.get("action")
        pr_obj = Product.objects.get(id=pr_id)
        print(pr_obj.name)
        if action == "delete":
            pr_obj.delete()
        else:
            pass

        return redirect("store:adminproductlist")

class AdminProductStockChangeView(ProdAdminRequiredMixin,CreateView):
    template_name = "productmanagers/adminProductStock.html"
    form_class = StockForm
    success_url = reverse_lazy("store:adminproductlist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pk']
        self.request.session['product_id'] = product_id
        return context

    def form_valid(self, form):
        pr_id = self.request.session.get("product_id")
        print(pr_id)
        pr_obj = Product.objects.get(id=pr_id)
        pr_obj.quantity = form.cleaned_data.get("quantity")
        pr_obj.save()
        return redirect("store:adminproductlist")




class AdminCategoryListView(ProdAdminRequiredMixin,ListView):
    model = Category
    template_name =  "productmanagers/admincategorylist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = Category.objects.all().order_by("-id")
        print(results)
        context["results"] = results
        return context

class AdminCategoryCreateView(ProdAdminRequiredMixin,CreateView):
    template_name = "productmanagers/admincategoryadd.html"
    form_class = CategoryForm
    success_url = reverse_lazy("store:admincategorylist")

    def form_valid(self, form):
        category_obj = Category.objects.create()
        category_obj.bigcategory = form.cleaned_data.get("bigcategory")
        category_obj.name = form.cleaned_data.get("name")
        category_obj.slug = form.cleaned_data.get("slug")
        category_obj.others = "others"

        category_obj.save()
        return redirect("store:admincategorylist")

class AdminCategoryDeleteView(ProdAdminRequiredMixin,CreateView):
    template_name = "productmanagers/admincategorylist.html"
    context_object_name = "category_obj"
    success_url = reverse_lazy("store:admincategorylist")

    def get(self, request, *args, **kwargs):
        c_id = self.kwargs["c_id"]
        action = request.GET.get("action")
        c_obj = Category.objects.get(id=c_id)
        print(c_obj.name)
        if action == "delete":
            c_obj.delete()
        else:
            pass

        return redirect("store:admincategorylist")





# END OF THE PRODUCTS MANAGERS PAGES


#SALES MANAGERS PAGES

def salesmanagersHome(request):
    return render(request, 'salesmanagers/adminHome.html')

class SalesAdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and SalesManagersAdmin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("../sales-admin-login/")
        return super().dispatch(request, *args, **kwargs)

class SalesAdminLoginView(FormView):
    template_name = "salesmanagers/adminlogin.html"
    form_class = SalesManagersLoginForm
    success_url = reverse_lazy("store:salesmanagersHome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and SalesManagersAdmin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

@login_required
def sales_managers_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('store:salesmanagersHome'))

class SalesAdminProductListView(SalesAdminRequiredMixin, ListView):
    model = Product
    template_name =  "salesmanagers/adminproductlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.salesmanagersadmin.distributor
        context["distributor"] = dis
        if dis is None:
            results = Product.objects.all()
        else:
            results = Product.objects.filter(distributor=dis)

        context["results"] = results
        return context

class AdminProductPriceChangeView(SalesAdminRequiredMixin,CreateView):
    template_name = "salesmanagers/salesAdminprice.html"
    form_class = PriceForm
    success_url = reverse_lazy("store:SalesAdminProductListView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pk']
        self.request.session['product_id'] = product_id
        return context

    def form_valid(self, form):
        pr_id = self.request.session.get("product_id")
        print(pr_id)
        pr_obj = Product.objects.get(id=pr_id)
        pr_obj.price = form.cleaned_data.get("price")
        pr_obj.save()
        return redirect("store:SalesAdminProductListView")

class PriceUpdatedView(SalesAdminRequiredMixin, View):
    def get(self,request):

        return render(request,
                    'salesmanagers/priceupdated.html')

def SalesAdminChangePrice(request, id):

    object = Product.objects.get(id=id)
    wish_object = WishItem.objects.filter(product=id)
    #print(wish_object)
    mail_group = []
    for i in wish_object:
        mail_group.append(i.wish_list.customer.email)
    #print(mail_group)

    if request.method == 'POST':
        form = PriceChangeForm(request.POST or None)
        if form.is_valid():
            discount = form.cleaned_data['discount']
            object.discountRate = discount
            xxx = object.price - (object.price*(discount/100))
            object.price = round(xxx,2)
            object.save()
            #Send e-mail to users who hold the product in their wishlist.
            subject = "Discount notification!!"
            message = "The price of " + object.name + " has been discounted by " + str(discount) + "%" + "\n"*2 + "You get this message because you hold the item in your wishlist. Have good one:)" + "\n" + "trendsu"
            try:
                send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list = mail_group)
            except Exception:
                return HttpResponse('There is a problem in mail addresses check this once again.')
            return redirect('store:PriceUpdatedView')
    else:
        form = PriceChangeForm(request.POST or None)
    return render(request, 'salesmanagers/adminpricechange.html', {'form': form, 'object':object})

class SalesShowInvoices(SalesAdminRequiredMixin, ListView):
    model = OrderProduct
    template_name =  "salesmanagers/showorders.html"

    def post(self,request):
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            objects_order = Order.objects.filter(created_at__range=[fromdate,todate])
            objects = OrderProduct.objects.filter(order__in=objects_order)
            return render(request,"salesmanagers/showorders.html",{'results':objects})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.salesmanagersadmin.distributor
        context["distributor"] = dis
        if dis is None:
            results = OrderProduct.objects.all()
        else:
            results = OrderProduct.objects.filter(distributor=dis)

        context["results"] = results
        return context

def ShowPDFold(request, id):

    object = OrderProduct.objects.get(id=id)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    mylist = [object.product,object.order.customer,object.order.total,object.order.created_at]
    detail_string = ",  ".join(str(obj) for obj in mylist)
    p.drawString(20, 750,"TRENDSU INVOICE AS PDF")
    p.drawString(20, 650,"Name ------, Customer ------, Price ------, Order Date ------")
    p.drawString(20, 600,detail_string)

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='invoice.pdf')

def ShowPDF(request, id):

    object = OrderProduct.objects.get(id=id)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    mylist = [object.product,object.order.customer,object.subtotal,object.order.created_at]
    detail_string = ",  ".join(str(obj) for obj in mylist)

    p.drawString(120, 780,"TRENDSU INVOICE AS PDF")


    date1 = object.order.created_at
    date1str = date1.strftime("%d %B %Y, %H:%M")
    p.drawString(20, 700,"Order Date:   " + date1str )

    p.drawString(20, 680,"OrderProduct ID:   " + str(object.id))
    p.drawString(20, 660,"Customer Name:   " + str(object.order.customer.user.username))

    p.drawString(20, 600,"Product ID:   " + str(object.product.id))
    p.drawString(20, 580,"Product Name:   " + str(object.product.name))
    p.drawString(20, 560,"Quantity:   " + str(object.quantity))
    p.drawString(20, 540,"Total Price:   " + str(object.subtotal))


    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='invoice.pdf')

class SalesShowProfit(SalesAdminRequiredMixin, ListView):
    model = OrderProduct
    template_name =  "salesmanagers/showprofit.html"

    def post(self,request):
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            objects_order = Order.objects.filter(created_at__range=[fromdate,todate])
            objects = OrderProduct.objects.filter(order__in=objects_order)

            dis = self.request.user.salesmanagersadmin.distributor

            if dis is None:
                objects = OrderProduct.objects.filter(order__in=objects_order)
            else:
                objects = OrderProduct.objects.filter(order__in=objects_order,distributor=dis)

            total = 0
            subtotal  = 0
            for i in objects:
                subtotal = i.subtotal - i.product.purchase_price
                total += subtotal

            return render(request,"salesmanagers/showprofit.html",{'results':objects,'total':total,'fromdate':fromdate,'todate':todate})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = self.request.user.salesmanagersadmin.distributor
        context["distributor"] = dis
        if dis is None:
            results = OrderProduct.objects.all()
        else:
            results = OrderProduct.objects.filter(distributor=dis)
        context["results"] = results
        return context


#END OF THE SALES MANAGERS PAGES
