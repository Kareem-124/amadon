from django.shortcuts import render, redirect
from .models import Order, Product


def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    id = request.POST['id']
    product = Product.objects.get(id=id)
    quantity_from_form = int(request.POST["quantity"])
    price_from_form = float(product.price)
    total_charge = quantity_from_form * price_from_form

    all_orders = Order.objects.all()
    total_orders = 0
    cumulative_price =0
    for order in all_orders:
        total_orders += order.quantity_ordered
        cumulative_price += order.total_price
    
    request.session['total_price'] = str(total_charge)
    request.session['total_items'] = str(quantity_from_form)
    request.session['total_orders'] = str(total_orders)
    request.session['cumulative_price'] = str(cumulative_price)


    print("Charging credit card...")
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    return redirect('/checkout_page')

def checkout_page(request):
    context = {
        'total_price' :str(request.session['total_price']),
        'total_items' : str(request.session['total_items']),
        'total_orders' :str(request.session['total_orders']),
        'cumulative_price' : str(request.session['cumulative_price']),
    }
            
    return render(request, "store/checkout.html", context)