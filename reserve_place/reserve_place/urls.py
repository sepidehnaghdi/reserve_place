"""reserve_place URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import database_files
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from rest_framework_extensions.routers import ExtendedSimpleRouter
from django.conf.urls import *
from user_app.views import UserViewSet, GroupViewSet, RegisterViewSet, ConfirmationViewSet
from locator.views import LocatorProfileViewSet
from database_files import views
from renter.views import RenterProfileViewSet
from place_app.views import PlaceViewSet, RentViewSet, RenterCommentViewSet, PlaceImageViewSet

router = ExtendedSimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet, base_name="user")
router.register(r'groups', GroupViewSet,  base_name="group")
router.register(r'register', RegisterViewSet,  base_name="register")
router.register(r'confirm', ConfirmationViewSet,  base_name="confirm")
router.register(r'locators', LocatorProfileViewSet, base_name="locator")
router.register(r'renters', RenterProfileViewSet, base_name="renter")
router.register(r'rents', RentViewSet, base_name='rent')

place_router = router.register(r'places', PlaceViewSet, base_name='place')
place_router.register(r'images', PlaceImageViewSet, base_name='place-image', parents_query_lookups=['place'])
place_router.register(r'comments', RenterCommentViewSet, base_name='comment', parents_query_lookups=['place'])

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/admin/', admin.site.urls),
    url(r'^api/v1/login', obtain_jwt_token),
    url(r'^api/v1/api-token-verify', verify_jwt_token),
    url(r'^api/v1/api-token-refresh', refresh_jwt_token),
    url(r'^api/v1/files/(?P<name>.+)', database_files.views.serve, name='database_file'),
    url(r'^api/v1/docs', include('rest_framework_docs.urls')),

]

# urlpatterns += router.urls
