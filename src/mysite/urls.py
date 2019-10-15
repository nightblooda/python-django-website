"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path

from personal.views import(
    home_screen_view,
    support_view,
    pricing_view,
)

from usersystem.views import(
    system_detail_view,
    billing_view,
    fullbill_view,
    deletebill_view,
)

from account.views import(
    login_view,
    logout_view,
)

urlpatterns = [
    path('', home_screen_view, name="home"),
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('support/', support_view, name="support"),
    path('pricing/', pricing_view, name="pricing"),
    path('detail/', system_detail_view, name="detail"),
    path('billing/', billing_view, name="billing"),
    path('fullbill/', fullbill_view, name="fullbill"),
    path('deletebill/', deletebill_view, name="deletebill"),
]
