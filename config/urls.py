"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
"""
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt import views as jwt_views
from Auth.views import CustomConfirmEmailView
from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("Devices.urls")),
    path("auth/", include("Auth.urls")),
    
    # django jwt 
     # dj rest framework
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('rest-auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('rest-auth/registration/account-confirm-email/(?P<key>.+)/', CustomConfirmEmailView.as_view(), name='account_confirm_email')
    re_path(
        r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', CustomConfirmEmailView.as_view(),
        name='account_confirm_email',
    ),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

