from django.contrib import admin
from .models import Brand, BusinessSettings, CustomerEnquiry, Product, ProductCategory, ProductImage, RepairBooking, Service

class ProductImageInline(admin.TabularInline): model=ProductImage; extra=1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): list_display=('name','model_name','brand','category','price','availability_status','is_demo','is_featured'); list_filter=('category','brand','availability_status','is_demo'); search_fields=('name','model_name','description'); prepopulated_fields={'slug':('name',)}; inlines=[ProductImageInline]; readonly_fields=('created_at','updated_at')
@admin.register(RepairBooking)
class BookingAdmin(admin.ModelAdmin): list_display=('reference','customer_name','phone','service','status','created_at'); list_filter=('status','created_at'); search_fields=('reference','customer_name','phone'); readonly_fields=('reference','created_at')
@admin.register(CustomerEnquiry)
class EnquiryAdmin(admin.ModelAdmin): list_display=('name','subject','phone','resolved','is_spam','created_at'); list_filter=('resolved','is_spam'); search_fields=('name','phone','subject')
admin.site.register([Brand,ProductCategory,Service,BusinessSettings])
