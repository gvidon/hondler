# coding: utf-8
from easy_thumbnails.fields          import ThumbnailerImageField
from django.contrib.auth.models      import User
from django.core.exceptions          import ValidationError
from django.conf                     import settings
from django.db                       import models


# Models validators
def atleast(count):
	def validator(value):
		if len(value) < count:
			raise ValidationError(u'This field requires at least %d characters' % count)

	return validator

def integer(value):
	try:
		int(value)
	except ValueError:
		raise ValidationError(u'This field should contain just numbers')

class Supplier(models.Model):
	title       = models.CharField(max_length=64)
	description = models.CharField(max_length=64, blank=True, null=True)
	slug        = models.SlugField(max_length=32)

# Models itself
class Category(models.Model):
	title = models.CharField(max_length=32)
	slug  = models.CharField(max_length=32)

	def __unicode__(self):
		return self.title

class Product(models.Model):
	brand        = models.CharField(max_length=32, blank=True, null=True)
	slug         = models.SlugField(max_length=32)
	title        = models.CharField(max_length=32)
	description  = models.TextField(max_length=32, blank=True, null=True)
	unit_price   = models.FloatField()
	supplier     = models.ForeignKey(Supplier, blank=True, null=True)
	available_in = models.IntegerField(blank=True, null=True)

	def get_title(self):
		try:
			return (' ').join((self.brand, self.title))
		except AttributeError:
			return self.title

	def __unicode__(self):
		return '%s %.2f' % (self.title, self.unit_price)

class ProductImage(models.Model):
	product = models.ForeignKey(Product, related_name='images')
	image   = ThumbnailerImageField(upload_to=settings.HONDLER_IMAGES_UPLOAD)

class OrderShipping(models.Model):
	name    = models.CharField(max_length=64, validators=[atleast(2)])
	city    = models.CharField(max_length=32, validators=[atleast(2)])
	address = models.CharField(max_length=255, validators=[atleast(3)])
	zip     = models.CharField(max_length=6, validators=[atleast(5), integer])
	phone   = models.CharField(max_length=24, validators=[atleast(5)], blank=True, null=True)
	email   = models.EmailField(blank=True, null=True)
	method  = models.CharField(choices=(settings.HONDLER_SHIPPING_OPTIONS), max_length=16)

class Order(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	user       = models.ForeignKey(User, blank=True, null=True)
	shipping   = models.ForeignKey(OrderShipping)

class OrderItem(models.Model):
	order      = models.ForeignKey(Order, related_name='items')
	product    = models.ForeignKey(Product, related_name='order_items')
	title      = models.CharField(max_length=32)
	quantity   = models.IntegerField()
	unit_price = models.FloatField()