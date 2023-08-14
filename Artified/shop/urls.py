from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("signup/", views.signup, name="SignUp"),
    path("login/", views.handlelogin, name="Login"),
    path('apply_filter/', views.apply_filter, name='apply_filter'),
    path("updatepass/<path:username>/<path:email>/",
         views.updatepass, name="updatepass"),
    path("forgot_password/", views.forgotpass, name="Forgotpass"),
    path("logout/", views.handlelogout, name="Logout"),
    path("", views.index, name="ShopHome"),
    path("shopnow/", views.shopnow, name="shopnow"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("orders/tracker/<track_id>", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("orders/", views.orders, name="Orders"),
    path('accounts/', include('allauth.urls')),

]
