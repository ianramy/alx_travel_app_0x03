from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, test_chapa_key

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

app_name = 'listings'
urlpatterns = [
    path('api/', include(router.urls)),
    # future API endpoints

    path('test-key/', test_chapa_key, name='test-key')        # temporay
]
