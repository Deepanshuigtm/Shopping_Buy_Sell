from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, response
from shop.models import Product, Contact, Order, OrderUpdate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from shop.models import *
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import uuid
User = get_user_model()


# Create your views here.
@login_required(login_url='/seller/login/')
def index(request):
    return render(request, "index.html")


def handlelogin(request):
    if request.method == 'POST':
        loginusername = request.POST.get('LoginUsername')
        loginpassword = request.POST.get('LoginPassword')
        user = authenticate(request, username=loginusername,
                            password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully.")
            return redirect('seller_index')
        else:
            messages.error(request, 'Invalid Credentials, Please try again.')
            return redirect('seller_login')
    else:
        return render(request, 'login.html')


def handlelogout(request):
    logout(request)
    messages.info(request, "Logged Out Successfully.")
    return redirect('seller_login')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        punctuations = '''!()/[]{}:;'",<>/?\~`$^&%*-=+'''
        # check for errorneous input
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('SignUp')

        for char in username:
            if char in punctuations:
                messages.error(
                    request, "Username should only contain letters and number!! ")
                return redirect('SignUp')

        if User.objects.filter(username=username).exists():
            messages.error(
                request, "Username already exists!! Try some different name. ")
            return redirect('SignUp')

        if User.objects.filter(email=email).exists():
            messages.error(
                request, "An account is already registered with the same email id!!")
            return redirect('SignUp')

        if len(pass1) < 8:
            messages.error(
                request, "Password length should be atleast 8 characters!!")
            return redirect('SignUp')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!!")
            return redirect('SignUp')

        # Create the user
        myuser = User.objects.create_user(
            username, email, pass1, is_seller=True)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        myseller = Seller(Name=fname + " "+lname, user=myuser)
        myseller.save()
        messages.success(
            request, " Your Account has been successfully created.")
        return redirect('seller_login')
    else:
        return render(request, 'signup.html')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
@login_required(login_url='/seller/login')
def seller_arts(request):
    myuser = request.user
    allarts = []
    myseller = Seller.objects.get(user=myuser)
    allarts = list(Product.objects.filter(
        seller=myseller).order_by('-pub_date'))
    return render(request, 'arts.html', {"allProds": allarts})


@csrf_exempt
def update_data_arts(request):
    if request.method == "POST":
        name = request.POST.get("name", '')
        price = request.POST.get("price", '')
        desc = request.POST.get("desc", '')
        category = request.POST.get("category", '')
        subcat = request.POST.get("subcat", '')
        Product.objects.filter(product_id=request.POST.get("pid")).update(
            product_name=name, category=category, price=price, desc=desc, subcategory=subcat)
        return HttpResponse(status=200)


@csrf_exempt
def add_new_arts(request):
    if request.method == "POST":
        rq = request.POST
        pname = rq["pname"]
        pcat = rq["pcat"]
        psubcat = rq["psubcat"]
        pprice = rq["pprice"]
        pdesc = rq["pdesc"]
        images = request.FILES.getlist('pimage')
        myuser = request.user
        myseller = Seller.objects.get(user=myuser)
        prod = Product(product_name=pname, category=pcat, subcategory=psubcat,
                       price=pprice, desc=pdesc, seller=myseller)
        prod.save()
        for img in images:
            filename = img.name
            ext = filename.split('.')[-1]
            img.name = "%s.%s" % (uuid.uuid4(), ext)
            i = Product_image(image=img)
            i.save()
            prod.img.add(i)
    return render(request, "add_new.html")


def settings(request):
    myuser = request.user
    allarts = []
    myseller = Seller.objects.get(user=myuser)
    seller_name = myseller.Name
    seller_discription = myseller.Description
    seller_sid = myseller.sid
    seller_product = myseller.products_json
    seller_accountNo = myseller.Account_number
    seller_ifccode = myseller.ifsc_code
    seller_account_holder_name = myseller.account_holder_name
    seller_profile_photo = myseller.profile_photo
    seller_address = myseller.address
    seller_pincode = myseller.pincode
    seller_city = myseller.city

    allarts = list(Product.objects.filter(
        seller=myseller).order_by('-pub_date'))
    return render(request, "settings.html", {"allProds": allarts, "seller_name": seller_name, "seller_discription": seller_discription, "seller_sid": seller_sid,
                                             "seller_product": seller_product, "seller_accountNo": seller_accountNo, "seller_ifccode": seller_ifccode, "seller_account_holder_name": seller_account_holder_name,
                                             "seller_profile_photo": seller_profile_photo, "seller_address": seller_address, "seller_pincode": seller_pincode, "seller_city": seller_city})
