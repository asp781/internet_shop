import json
from .models import *


def cookieCart(request):
    # print('request:', request, type(request))
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart: # перебираем корзину по типам товара
        try:
            cartItems += cart[i]['quantity'] # суммируем кол товаров всех типов

            product = Product.objects.get(id=i) # подтягиваеи из БД объект товара
            total = (product.price * cart[i]['quantity']) # стоимость товаров одного типа

            order['get_cart_total'] += total # стоимость всех товаров в заказе
            order['get_cart_items'] += cart[i]['quantity'] # кол товаров в заказе

            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item) # пока юзер - ананимус собираем сюда его заказ, так как не можем записать его в базу без имени пользователя

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items }


def cartData(request):
    # print('request:', request, type(request))
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items }


def guestOrder(request, data):

    print('User is not authenticated')

    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id = item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order
