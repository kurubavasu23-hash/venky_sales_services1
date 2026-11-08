from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Brand, BusinessSettings, CustomerEnquiry, Product, ProductCategory, RepairBooking, Service
from .permissions import PublicReadStaffWrite
from .serializers import (BookingSerializer, BrandSerializer, BusinessSettingsSerializer, CategorySerializer, EnquirySerializer, ProductSerializer, PublicBookingLookupSerializer, ServiceSerializer)

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.select_related('brand','category').prefetch_related('images').all()
    serializer_class=ProductSerializer; permission_classes=[PublicReadStaffWrite]
    lookup_field='slug'
    filter_backends=[filters.SearchFilter,filters.OrderingFilter]; search_fields=['name','description','brand__name','category__name']; ordering_fields=['price','name','created_at']
    def get_queryset(self):
        qs=super().get_queryset()
        category=self.request.query_params.get('category')
        if category: qs=qs.filter(category__slug=category)
        if self.request.query_params.get('featured') == 'true': qs=qs.filter(is_featured=True)
        brand=self.request.query_params.get('brand')
        if brand: qs=qs.filter(brand__name__iexact=brand)
        return qs
class CategoryViewSet(viewsets.ReadOnlyModelViewSet): queryset=ProductCategory.objects.all(); serializer_class=CategorySerializer; permission_classes=[AllowAny]; pagination_class=None
class BrandViewSet(viewsets.ReadOnlyModelViewSet): queryset=Brand.objects.all(); serializer_class=BrandSerializer; permission_classes=[AllowAny]; pagination_class=None
class ServiceViewSet(viewsets.ModelViewSet): queryset=Service.objects.filter(is_active=True); serializer_class=ServiceSerializer; permission_classes=[PublicReadStaffWrite]
class BookingCreateView(generics.CreateAPIView): queryset=RepairBooking.objects.all(); serializer_class=BookingSerializer; permission_classes=[AllowAny]
class BookingLookupView(generics.RetrieveAPIView): queryset=RepairBooking.objects.all(); serializer_class=PublicBookingLookupSerializer; permission_classes=[AllowAny]; lookup_field='reference'
class BookingAdminViewSet(viewsets.ModelViewSet): queryset=RepairBooking.objects.all(); serializer_class=BookingSerializer; permission_classes=[IsAdminUser]; http_method_names=['get','patch','head','options']
class EnquiryCreateView(generics.CreateAPIView): queryset=CustomerEnquiry.objects.all(); serializer_class=EnquirySerializer; permission_classes=[AllowAny]
class EnquiryAdminViewSet(viewsets.ModelViewSet): queryset=CustomerEnquiry.objects.all(); serializer_class=EnquirySerializer; permission_classes=[IsAdminUser]; http_method_names=['get','patch','head','options']
class BusinessSettingsView(generics.RetrieveAPIView):
    serializer_class=BusinessSettingsSerializer; permission_classes=[AllowAny]
    def get_object(self): return BusinessSettings.objects.first() or BusinessSettings()

class AdminDashboardView(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        return Response({'total_products':Product.objects.count(),'total_bookings':RepairBooking.objects.count(),'pending_bookings':RepairBooking.objects.filter(status='pending').count(),'completed_bookings':RepairBooking.objects.filter(status='completed').count(),'total_enquiries':CustomerEnquiry.objects.count()})
