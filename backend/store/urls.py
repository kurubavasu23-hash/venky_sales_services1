from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (AdminDashboardView, BookingAdminViewSet, BookingCreateView, BookingLookupView, BrandViewSet, BusinessSettingsView, CategoryViewSet, EnquiryAdminViewSet, EnquiryCreateView, ProductViewSet, ServiceViewSet)

router=DefaultRouter()
router.register('products',ProductViewSet)
router.register('categories',CategoryViewSet)
router.register('brands',BrandViewSet)
router.register('services',ServiceViewSet)
router.register('admin/bookings',BookingAdminViewSet,basename='admin-bookings')
router.register('admin/enquiries',EnquiryAdminViewSet,basename='admin-enquiries')
urlpatterns=[path('',include(router.urls)),path('admin/dashboard/',AdminDashboardView.as_view(),name='admin-dashboard'),path('bookings/',BookingCreateView.as_view(),name='booking-create'),path('bookings/<str:reference>/',BookingLookupView.as_view(),name='booking-lookup'),path('enquiries/',EnquiryCreateView.as_view(),name='enquiry-create'),path('business-settings/',BusinessSettingsView.as_view(),name='business-settings')]
