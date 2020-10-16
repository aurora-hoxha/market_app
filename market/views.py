from pyexpat.errors import messages

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

from .models import Dyqan, Kategori, Receipt, ReceiptProducts


def dyqanet(request):
    dyqane = Dyqan.objects.all()
    data = {
        'dyqanet': dyqane,
    }
    return render(request=request, template_name='dyqanet.html', context=data)


def kategorite(request, dyqan_id):
    kategori = Kategori.objects.all()
    produkte = Product.objects.filter(dyqani=dyqan_id).order_by('-id')

    data = {
        'kategorite': kategori,
        'produkte': produkte,
        'dyqan_id': dyqan_id
    }
    return render(request, 'kategorite.html', data)


def produktet(request, dyqan_id, kategori_id):
    produkte = Product.objects.filter(dyqani=dyqan_id, kategoria=kategori_id)
    kategori = Kategori.objects.values('emri').get(id=kategori_id)
    return render(request, 'produkte.html', {'produkte': produkte, 'kategori': kategori})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Llogaria e re eshte krijuar:{username}")
            login(request, user)
            messages.info(request, f"Ju jeni te loguar si {username} ")
            return redirect("register")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = UserCreationForm
    return render(request, "identifikim/register.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="identifikim/login.html",
                  context={"form": form})


from market.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    dyqani_id = Product.objects.values('dyqani_id').get(id=id)['dyqani_id']
    return redirect("/kategori/{}".format(dyqani_id))


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'shporta/cart_detail.html')


@login_required(login_url="/login")
def porosit(request):
    shporta = request.session.get('cart')
    receipt = Receipt.objects.create(klient=request.user)
    cmimi_total = 0
    for produkt in shporta.values():
        produkti_kerkuar = Product.objects.get(id=produkt['product_id'])
        sasia_kerkuar = produkt['quantity']

        if produkti_kerkuar.sasia >= sasia_kerkuar:
            receipt_product = ReceiptProducts.objects.create(receipt=receipt, sasia=sasia_kerkuar,
                                                             cmimi_total=float(produkt['price']) * sasia_kerkuar,
                                                             produkti_id=produkt['product_id'])
            produkti_kerkuar.sasia = produkti_kerkuar.sasia - sasia_kerkuar
            produkti_kerkuar.save()
            cmimi_total = cmimi_total + receipt_product.cmimi_total
        else:
            messages.error(request, f'Produkti {produkti_kerkuar.name}, ka ne gjendje vetem {produkti_kerkuar.sasia}')
            receipt.delete()
            return redirect("cart_detail")

    if not receipt.receipt_products.all():
        receipt.delete()

    receipt.totali = cmimi_total
    receipt.save()
    messages.success(request, 'Blerja u krye me sukses!')
    cart_clear(request)
    return redirect("cart_detail")


produkt_ne_sesion_shembull = [{'userid': 1, 'product_id': 1, 'name': 'domate', 'quantity': 4, 'price': '200.00',
                               'image': '/static/media/avatar_cover_1.webp'}]
