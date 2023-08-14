from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="seller_index"),
    path("login/", views.handlelogin, name="seller_login"),
    path("signup/", views.signup, name="seller_signup"),
    path("logout/", views.handlelogout, name="seller_logout"),
    path("arts/", views.seller_arts, name="seller_arts"),
    path("update_data_arts/", views.update_data_arts, name="update_data_arts"),
    path("add_new/", views.add_new_arts, name="add_new_arts"),
    path("settings/", views.settings, name="seller_settings")
]
