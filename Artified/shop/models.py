from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

# from django.contrib.auth import get_user_model
# User = get_user_model()
# from django.contrib.auth.models import User
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.


class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)


class Seller(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=100)
    sid = models.AutoField(primary_key=True)
    products_json = models.CharField(max_length=800)
    Account_number = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=100)
    profile_photo = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=40, default="Indore")
    user = models.ForeignKey(User, default=None, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.Name + " " + str(self.sid)


class Product_image(models.Model):
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.image.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=3000)
    pub_date = models.DateTimeField(default=timezone.now)
    # image = models.CharField(max_length = )
    # image = models.ImageField(upload_to="shop/images", default="")
    img = models.ManyToManyField(Product_image)
    seller = models.ForeignKey(
        Seller, default=None, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.product_id) + " " + self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=3000, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=80)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, default="")
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.order_id) + " " + self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=100, default="1")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
