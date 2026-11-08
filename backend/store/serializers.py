from rest_framework import serializers
from .models import Brand, BusinessSettings, CustomerEnquiry, Product, ProductCategory, ProductImage, RepairBooking, Service

class CategorySerializer(serializers.ModelSerializer):
    class Meta: model=ProductCategory; fields=['id','name','slug']
class BrandSerializer(serializers.ModelSerializer):
    class Meta: model=Brand; fields=['id','name']
class ProductSerializer(serializers.ModelSerializer):
    brand_name=serializers.CharField(source='brand.name',read_only=True,default='')
    category_name=serializers.CharField(source='category.name',read_only=True)
    image=serializers.SerializerMethodField()
    images=serializers.SerializerMethodField()
    def get_images(self,obj):
        request=self.context.get('request')
        return [
            {
                'url': request.build_absolute_uri(item.image.url) if request else item.image.url,
                'alt_text': item.alt_text or f'{obj.name} product image',
            }
            for item in obj.images.all()
        ]
    def get_image(self,obj):
        item=obj.images.first()
        request=self.context.get('request')
        if item:
            return request.build_absolute_uri(item.image.url) if request else item.image.url
        category_art={
            'smartphones':'/catalog/catalog-reference-phone.jpg',
            'mobile-accessories':'/catalog/demo-cover.svg',
            'earphones-headphones':'/catalog/demo-earbuds.svg',
            'chargers-cables':'/catalog/demo-charger.svg',
        }
        return category_art.get(obj.category.slug, '/catalog/demo-phone.svg')
    class Meta: model=Product; fields=['id','name','model_name','slug','brand','brand_name','category','category_name','description','ram','storage','colour','price','original_price','availability_status','is_demo','is_featured','image','images','created_at','updated_at']
class ServiceSerializer(serializers.ModelSerializer):
    class Meta: model=Service; fields=['id','title','description','sort_order']
class BookingSerializer(serializers.ModelSerializer):
    reference=serializers.ReadOnlyField()
    class Meta:
        model=RepairBooking; fields=['id','reference','customer_name','phone','email','brand','model','service','problem_description','preferred_date','preferred_time','status','created_at']
        read_only_fields=['id','reference','status','created_at']
class PublicBookingLookupSerializer(serializers.ModelSerializer):
    class Meta: model=RepairBooking; fields=['reference','service','status','created_at']
class EnquirySerializer(serializers.ModelSerializer):
    class Meta: model=CustomerEnquiry; fields=['id','name','phone','email','subject','message','resolved','is_spam','created_at']; read_only_fields=['id','resolved','is_spam','created_at']
class BusinessSettingsSerializer(serializers.ModelSerializer):
    class Meta: model=BusinessSettings; fields=['name','phone','whatsapp_number','address','opening_hours','description']
