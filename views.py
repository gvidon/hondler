import json

from django.shortcuts import render, get_object_or_404 as or404
from django.db.models import F
from django.http      import HttpResponse, Http404
from cart             import Cart, ItemAlreadyExists
from cart.models      import Item

from models           import *


def handle500(request, template_name='500.html'):
	import sys
	ltype, lvalue, ltraceback = sys.exc_info()
	sys.exc_clear()
	return render(request, template_name, {'type': ltype, 'value': lvalue, 'traceback': ltraceback})

def JSON(response):
	return HttpResponse(json.dumps(response), content_type='application/json')

def add(request, pk):
	product = or404(Product, pk=pk)
	cart = Cart(request)

	try:
		cart.add(product, product.unit_price, 1)
	except ItemAlreadyExists:
		# Update cart item quantity if product already exists in the cart
		cart_item(cart.cart, product.pk).update(quantity=F('quantity') + 1)

	return items(request)

def cart_item(cart, id, **kwargs):
	return Item.objects.filter(cart=cart, object_id=id)

def checkout(request):
	from django.contrib.auth.models import User
	from django.core.validators import email_re

	if not Cart(request).cart.item_set.all().count():
		raise Http404

	return render(request, 'hondler/checkout.html')

def index(request):
	cart = Cart(request)

	return render(request, 'index.html', {
		'featured': Product.objects.order_by('-featured').all(),
		'cart': cart,
	})

def items(request):
	cart = Cart(request)

	return JSON(map(lambda I: {
		'id'      : I.product.pk,
		'quantity': I.quantity,
		'title'   : I.product.title,
		'price'   : I.product.unit_price,
		'total'   : str(I.total_price),
	}, cart))

def order(request):
	from django.contrib.auth.models import User
	from django.core.exceptions     import ValidationError
	from django.conf                import settings

	P = lambda N: request.POST.get(N, '')

	shipping = OrderShipping(
		address = P('address'),
		city    = P('city'),
		cost    = settings.HONDLER_SHIPPING_COSTS[P('method')],
		email   = P('email'),
		method  = P('method'),
		name    = P('name'),
		phone   = P('phone'),
		zip     = P('zip'),
	)

	try:
		shipping.full_clean()
	except ValidationError as e:
		return JSON({'success': False, 'errors': e.message_dict})

	shipping.save()

	cart = Cart(request)
	order = Order.objects.create(shipping=shipping)

	OrderItem.objects.bulk_create(map(lambda I: OrderItem(
		order      = order,
		product    = I.product,
		title      = I.product.title,
		quantity   = I.quantity,
		unit_price = I.product.unit_price,
	), cart))
	
	# Cart.clear() is not yet fixed in pypi
	cart.cart.item_set.all().delete()
	
	return JSON({'success': True, 'order': order.id})

def remove(request, pk):
	Cart(request).remove(or404(Product, pk=pk))
	return items(request)

def update(request):
	cart = Cart(request)

	def updateItem(I):
		if not I.get('quantity', 0):
			cart.remove(or404(Product, pk=I['id']))
		else:
			cart_item(cart.cart, I['id']).update(quantity=I.get('quantity'))
	
	map(updateItem, json.loads(request.POST['items']))
	
	return items(request)