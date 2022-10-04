
from django.urls import include, path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name = "home"),
    path('store/', views.store, name = "store"),
    path('womenPage/', views.womenPage, name ="womenPage"),



    path('search/', views.SearchView.as_view(), name = "search"),
    path('price-low-to-high/', views.OrderByPriceAs.as_view(), name ="price"),
    path('price-high-to-low/', views.OrderByPriceDes.as_view(), name ="priceDes"),
    path('popularity-low-to-high/', views.OrderByPopularityAs.as_view(), name ="popularityAs"),
    path('popularity-high-to-low/', views.OrderByPopularityDes.as_view(), name ="popularityDes"),
    # path("rate-<int:pro_id>/'", views.CommentView.as_view(), name="rate"),



    path('add_to_cart-<int:pro_id>/', views.AddToCart.as_view(), name = "AddToCart"),
    path('myBasket/', views.myBasketView.as_view(), name ="myBasket"),
    path("manage-cart/<int:cp_id>/", views.ManageCartView.as_view(), name = "managecart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path('myOrders/', views.CustomerOrdersView.as_view(), name ="myOrders"),
    path('cancelOrder<int:pk>', views.CustomerCancelOrdersView.as_view(), name ="cancelOrder"),
    path('myProfile/', views.CustomerProfileView.as_view(), name ="myProfile"),
    path("orderDetails/order-<int:pk>/", views.CustomerOrderDetailView.as_view(),name="customerorderdetail"),
    path('rate-<int:pro_id>/', views.AddToReviewList.as_view(), name ="rate"),
    path("receipt/order-<int:pk>/", views.CustomerReceiptView.as_view(),name="receipt"),
    path("receipt/sendmail/<int:id>", views.SendEmail, name="SendEmail"),
    path('payment/', views.CustomerPaymentView.as_view(), name ="payment"),
    path('myRatingsEvaluated/', views.CustomerReviewView.as_view(), name ="myRatingsEvaluated"),
    path('productReviews/-<int:pk>/', views.ProductReviewView.as_view(), name ="productReviews"),
    path('add_to_wishlist-<int:pro_id>/', views.AddToWishList.as_view(), name = "AddToWishList"),
    path('myWishList/', views.myWishListView.as_view(), name ="myWishList"),
    path('myWishRemove-<int:obj_id>//', views.myWishRemoveView.as_view(), name ="myWishRemove"),



    # PRODUCT MANAGERS URLS
    path("admin-home/", views.productmanagersHome, name="productmanagersHome"),
    path("admin-login/", views.AdminLoginView.as_view(), name="adminlogin"),
    path("admin-PendingOrders/", views.AdminPendingOrdersView.as_view(), name="adminPendingOrders"),
    path("admin-order/<int:pk>/", views.AdminOrderDetailView.as_view(), name="adminorderdetail"),
    path("admin-all-orders/", views.AdminOrderListView.as_view(), name="adminorderlist"),
    path("admin-order-<int:pk>-change/",views.AdminOrderStatusChangeView.as_view(), name="adminorderstatuschange"),
    path("admin-pendingComment/", views.PendingReviewView.as_view(), name="adminpendingComment"),
    path("admin-all-reviews/", views.AdminReviewListView.as_view(), name="adminreviewlist"),
    path("admin-detailComment/<int:pk>/", views.AdminReviewDetailView.as_view(), name="admindetailComment"),
    path("admin-review-<int:pk>-change/",views.AdminReviewStatusChangeView.as_view(), name="adminreviewstatuschange"),
    path("admin-product-list/", views.AdminProductListView.as_view(), name="adminproductlist"),
    path("admin-product-add/", views.AdminProductCreateView.as_view(), name="adminproductcreate"),
    path("admin-productdelete/<int:pr_id>/", views.AdminProductDeleteView.as_view(), name = "adminproductdelete"),
    path("admin-category-list/", views.AdminCategoryListView.as_view(), name="admincategorylist"),
    path("admin-category-add/", views.AdminCategoryCreateView.as_view(), name="admincategorycreate"),
    path("admin-categorydelete/<int:c_id>/", views.AdminCategoryDeleteView.as_view(), name = "admincategorydelete"),
    path("admin-PendingRefundRequests/", views.AdminPendingRefundRequestsView.as_view(), name="adminRefundRequests"),
    path("admin-AllRefundRequests/", views.AdminAllRefundRequestsView.as_view(), name="adminAllRefundRequests"),
    path('product_managers_logout/', views.product_managers_logout, name='product_managers_logout'),
    path('product_managers_stock/<int:pk>/', views.AdminProductStockChangeView.as_view(), name='product_managers_stock'),
    # END OF PRODUCT MANAGERS URLS

    #  SALES MANAGERS URLS
    path("sales-admin-home/", views.salesmanagersHome, name="salesmanagersHome"),
    path("sales-admin-login/", views.SalesAdminLoginView.as_view(), name="SalesAdminLoginView"),
    path("sales-admin-products/", views.SalesAdminProductListView.as_view(), name="SalesAdminProductListView"),
    path("sales-price-update/<int:id>/change", views.SalesAdminChangePrice, name="SalesAdminChangePrice"),
    path("price_updated/", views.PriceUpdatedView.as_view(), name="PriceUpdatedView"),
    path("sales-show-invoices/", views.SalesShowInvoices.as_view(), name="SalesShowInvoices"),
    path("invoice-pdf/<int:id>", views.ShowPDF, name="ShowPDF"),
    path("sales-show-profit/", views.SalesShowProfit.as_view(), name="SalesShowProfit"),
    path('sales_managers_logout/', views.sales_managers_logout, name='sales_managers_logout'),
    path('sales_managers_price/<int:pk>/', views.AdminProductPriceChangeView.as_view(), name='sales_managers_price'),

    # END OF SALES MANAGERS URLS


    path('otherCategories/', views.OtherCategoryListView.as_view(), name ="OtherCategoryListView"),
    path('allProducts/', views.AllListView.as_view(), name ="AllListView"),
    path('womenDressPage/', views.DressListView.as_view(), name ="DressListView"),
    path('productDetail/<slug>/', views.ProductDetailView.as_view(), name ="productDetail"),
    path('womenSkirtPage/', views.SkirtListView.as_view(), name ="SkirtListView"),
    path('womenSweatshirtPage/', views.SweatshirtListView.as_view(), name ="SweatshirtListView"),
    path('womenBlousesPage/', views.BlousesListView.as_view(), name ="BlousesListView"),
    path('womenSweaterPage/', views.SweaterListView.as_view(), name ="SweaterListView"),
    path('womenTshirtPage/', views.TshirtListView.as_view(), name ="TshirtListView"),
    path('womenCoatPage/', views.CoatListView.as_view(), name ="CoatListView"),
    path('womenSleepPage/', views.SleepListView.as_view(), name ="SleepListView"),
    path('womenShortPage/', views.ShortListView.as_view(), name ="ShortListView"),
    path('womenPantPage/', views.PantListView.as_view(), name ="PantListView"),
    path('womenSweatsuitPage/', views.SweatsuitListView.as_view(), name ="SweatsuitListView"),



    path('user_login/',views.user_login,name='user_login'),
    path('register/', views.register, name ="register"),
    path('myRatings/', views.myRatings, name ="myRatings"),
    path('wishlist/', views.wishlist, name ="wishlist"),


    path('request-refund/order-<int:ord_id>/', views.RequestRefundView.as_view(), name='request-refund'),
    path('grant-refund/orderProduct-<int:orderP_id>/', views.GrantRefundView.as_view(), name='grant-refund')
]
