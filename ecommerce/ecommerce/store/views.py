from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.qtyproduct
    else:
        items = []
        order = {
            'alltotal': 0,
            'qtyproduct': 0
        }
        cartItems = order['qtyproduct']
    print(items)
    context = {
        'items': items,
        'order': order,
        'qtyproducts': cartItems
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.qtyproduct
    else:
        items = []
        order = {
            'alltotal': 0,
            'qtyproduct': 0
        }
        cartItems = order['qtyproduct']

    print(items)
    context = {
        'items': items,
        'order': order,
        'qtyproducts': cartItems
    }
    
    return render(request, 'store/checkout.html', context)

def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.qtyproduct
    else:
        items = []
        order = {
            'alltotal': 0,
            'qtyproduct': 0
        }
        cartItems = order['qtyproduct']
    context = {
        'products': products,
        'qtyproducts': cartItems
    }
    return render(request, 'store/store.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action :', action)
    print('productId :', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    print("Data =", request.body)
    return JsonResponse('Payment Complete', safe=False)