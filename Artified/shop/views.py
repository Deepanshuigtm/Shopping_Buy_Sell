from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, response
from .forms import ChangePasswordForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from math import ceil
import json
import xlwings as xw
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


def apply_filter(request):
    price_filter = request.GET.get('price')
    category_filter = request.GET.get('category')

    filtered_items = Product.objects.all()
    if price_filter == 'low':
        filtered_items = filtered_items.filter(price__lt=200)
    elif price_filter == 'medium':
        filtered_items = filtered_items.filter(price__range=(10, 50))
    elif price_filter == 'high':
        filtered_items = filtered_items.filter(price__gt=9800)
    if category_filter != 'all':
        filtered_items = filtered_items.filter(category=category_filter)
    allProds = []
    filtered_items = list(filtered_items)
    print(price_filter)
    print(filtered_items)
    temp = {}
    for i in filtered_items:
        cat = i.category
        if cat in temp:
            temp[cat].append(i)
        else:
            temp[cat] = [i]
    for key, prod in temp.items():
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, "shop/shopnow.html", params)

def signup(request):
    if request.method == "POST":
      # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        seller = request.POST.get("is_buyer", "") == ""
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
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_seller = seller
        if seller:
            myseller = Seller(Name=fname + " "+lname, user=myuser)
            myseller.save()
        myuser.save()
        messages.success(
            request, " Your Account has been successfully created.")
        return redirect('ShopHome')
    else:
        return render(request, 'shop/signup.html')


def forgotpass(request):
    if request.method == 'POST':
        loginusername = request.POST.get('LoginUsername')

        try:
            user = User.objects.get(username=loginusername)
            password = user.password
            email = user.email
            username = user.username
            # Display the password or use it as needed

            # Return to the same page with the password
            print(password)
            print(email)
            return redirect('updatepass', username=username, email=email)
            # return render(request, 'shop/', {'password': password})
        except User.DoesNotExist:
            messages.error(request, "Username does not exist!!")
            return redirect('Login')

    return render(request, 'shop/login.html')


def updatepass(request, username, email):
    if request.method == "POST":
        newpassword = request.POST['newpassword']
        confirmpass = request.POST['confirmpassword']

        if newpassword != confirmpass:
            messages.error(
                request, "new password and confirm password are not same!")
            return redirect('updatepass', username=username, email=email)
        if len(newpassword) < 8:
            messages.error(
                request, "Password length should be atleast 8 characters!!")
            return redirect('updatepass', username=username, email=email)
        user = User.objects.get(username=username, email=email)
        user.set_password(newpassword)
        user.save()
        messages.success(request, "Password updated successfully!")
        return redirect('Login')

    return render(request, 'shop/updatepass.html', {'username': username, 'email': email})


def handlelogin(request):
    if request.method == 'POST':
        loginusername = request.POST.get('LoginUsername')
        loginpassword = request.POST.get('LoginPassword')
        user = authenticate(request, username=loginusername,
                            password=loginpassword)
        if user is not None:
            login(request, user)
            if user.is_seller:
                return redirect("seller_index")
            messages.success(request, "Logged In Successfully  .")
            return redirect('ShopHome')
        else:
            messages.error(request, 'Invalid Credentials, Please try again.')
            return redirect('Login')
    else:
        if request.user.is_authenticated:
            if request.user.is_seller:
                return redirect("seller_index")
            return redirect('shopnow')
        return render(request, 'shop/login.html')


@ login_required(login_url='/login/')
def handlelogout(request):
    logout(request)
    messages.info(request, "Logged Out Successfully.")
    return redirect('Login')


def add_data():
    ws = xw.Book("shop/book1.xlsx").sheets['list_of_products']
    sl = Seller.objects.get(sid=1)
    v1 = ws.range("A2:E11").value
    for row in v1:
        prod = Product(product_name=row[0], price=row[1],
                       category=row[2], subcategory=row[3], desc=row[4], seller=sl)
        # prod.save()


@ login_required(login_url='/login/')
def index(request):
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)


@ login_required(login_url='/login/')
def shopnow(request):
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "shop/shopnow.html", params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    # add_data()
    if request.method == "POST":
        Name = request.POST.get('name', '')
        Email = request.POST.get('email', '')
        Phone = request.POST.get('phone', '')
        Desc = request.POST.get('desc', '')
        contact = Contact(name=Name, email=Email, phone=Phone, desc=Desc)
        contact.save()
    return render(request, 'shop/contact.html')


def tracker(request, track_id):
    temp = []
    data = Order.objects.filter(user_id=request.user)
    st = set()  # set for storing the order_id of all the orders to use it later,
    for i in data:
        json_data = json.loads(i.items_json)
        tt = ""
        for key, val in json_data.items():
            txt = Product.objects.filter(product_id=key[2:])
            if txt:
                txt = txt[0]
                tt += txt.product_name
                tt += "\n"
                tt += str(txt.price)
                tt += "\n"
        i.items_json = tt[:]
        st.add(i.order_id)
        temp.append(i)
    track_data = []
    if track_id != None and int(track_id) in st:
        track_data = list(OrderUpdate.objects.filter(
            order_id=str(track_id)).order_by("timestamp"))
        curr_order = Order.objects.get(order_id=str(track_id))
        curr_items_data = json.loads(curr_order.items_json)
        curr_order.items_json = nav_view_item(curr_items_data)
    return render(request, 'shop/tracker.html', {"data": curr_order, "track_data": track_data})


def searchMatch(query, item):
    print("Item is1", item)
    if query.lower() in (item.desc.lower()) or query.lower() in (item.product_name.lower()) or query.lower() in (item.category.lower()) or query.lower() in (item.subcategory.lower()):
        print("Item is", item)
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if n != 0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)


def productView(request, myid):
    product = Product.objects.filter(product_id=myid)
    return render(request, 'shop/prodView.html', {'Vproduct': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        checkout = Order(items_json=items_json, name=name, email=email,
                         address=address, city=city, state=state, zip_code=zip_code, phone=phone, user_id=request.user)
        checkout.save()
        update = OrderUpdate(order_id=checkout.order_id,
                             update_desc="The order has been placed")
        update.save()
        thank = True
        id = checkout.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')


def orders(request):
    order = list(Order.objects.filter(user_id=request.user))
    # add_data()
    for i in range(len(order)):
        curr_order = order[i]
        curr_items_data = json.loads(curr_order.items_json)
        curr_order.items_json = nav_view_item(curr_items_data)

    return render(request, 'shop/orders.html', {"data": order})


def nav_view_item(data):
    arr = []
    for key, val in data.items():
        temp = int(key[2:])  # removing prefix from the product id
        prod = Product.objects.get(product_id=temp)
        game = [temp, prod.product_name, val[0], val[2],
                val[0]*val[2], prod.img.all()[0].image.url]
        print(game)
        arr.append(game[:])
    return arr
