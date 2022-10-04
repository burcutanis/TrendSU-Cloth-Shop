from django.contrib import admin

# Register your models here.


from .models import *


# class ProductImageAdmin(admin.StackedInline):
#     model = ProductImage


# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductImageAdmin]
#
#     class Meta:
#        model = Product
#
#
# class ProductImageAdmin(admin.ModelAdmin):
#     pass

admin.site.register(Customer)
admin.site.register(BigCategory)
admin.site.register(Category)
admin.site.register(Product)

admin.site.register(ReviewItem)
admin.site.register(ReviewList)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Address)
admin.site.register(Gender)
admin.site.register(OrderProduct)
admin.site.register(Distributor)
admin.site.register(WishList)
admin.site.register(WishItem)


admin.site.register(SalesManagersAdmin)
admin.site.register(ProductManagersAdmin)
# admin.site.register(Payment)


