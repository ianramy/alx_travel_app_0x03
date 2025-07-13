"""
URL configuration for alx_travel_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

The router creates endpoints like:
    a. /api/listings/ (GET, POST)
    b. /api/listings/<id>/ (GET, PUT, DELETE)
    c. /api/bookings/ (GET, POST)
    d. /api/bookings/<id>/ (GET, PUT, DELETE)

The swagger/ endpoint provides Swagger UI for API documentation.
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from listings.views import InitiatePaymentView, VerifyPaymentView


# Setting up Swagger with project metadata
schema_view = get_schema_view(
    openapi.Info(
        title="ALX Travel App API",
        default_version='v1',
        description="API for ALX Travel App",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@alxtravelapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),        # Routes to Django admin
    path('api/', include('listings.urls')), # Routes to listings/urls.py
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),        # Routes to Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),                 # Routes to ReDoc UI
    path('api/payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('api/payments/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]
