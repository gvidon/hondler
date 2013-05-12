# coding: utf-8
from easy_thumbnails.signal_handlers import generate_aliases_global
from easy_thumbnails.signals         import saved_file
from easy_thumbnails.fields          import ThumbnailerImageField
from django.contrib.auth.models      import User
from django.core.exceptions          import ValidationError
from django.conf                     import settings
from django.db                       import models


saved_file.connect(generate_aliases_global)

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

# Models itself
class Category(models.Model):
	title = models.CharField(max_length=32)
	slug  = models.CharField(max_length=32)

	def __unicode__(self):
		return self.title
	
	class Meta:
		abstract = True

class Product(models.Model):
	category    = models.ForeignKey(settings.HONDLER_CATEGORY_MODEL, blank=True, null=True)
	brand       = models.CharField(max_length=32, blank=True, null=True)
	slug        = models.SlugField(max_length=32)
	title       = models.CharField(max_length=32)
	description = models.TextField(max_length=32, blank=True, null=True)
	unit_price  = models.FloatField()

	def get_title(self):
		try:
			return (' ').join((self.brand.title, self.title))
		except AttributeError:
			return self.title

	def __unicode__(self):
		return '%s %.2f' % (self.title, self.unit_price)

	class Meta:
		abstract = True

class ProductImage(models.Model):
	product = models.ForeignKey(settings.HONDLER_PRODUCT_MODEL, related_name='images')
	image   = ThumbnailerImageField(upload_to='product')

	class Meta:
		db_table = 'product_image'

class OrderShipping(models.Model):
	name    = models.CharField(max_length=64, validators=[atleast(2)])
	city    = models.CharField(max_length=32, validators=[atleast(2)])
	address = models.CharField(max_length=255, validators=[atleast(3)])
	zip     = models.CharField(max_length=6, validators=[atleast(5), integer])
	phone   = models.CharField(max_length=24, validators=[atleast(5)], blank=True, null=True)
	email   = models.EmailField(blank=True, null=True)
	method  = models.CharField(choices=(('pek', u'ПЭК'), ('ems', u'EMS'), ('spsr', u'СПСР')), max_length=16)

	class Meta:
		db_table = 'order_shipping'

class Order(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	user       = models.ForeignKey(User, blank=True, null=True)
	shipping   = models.ForeignKey(OrderShipping)
	
	class Meta:
		db_table = 'order'

class OrderItem(models.Model):
	order      = models.ForeignKey(Order, related_name='items')
	product    = models.ForeignKey(settings.HONDLER_PRODUCT_MODEL)
	title      = models.CharField(max_length=32)
	quantity   = models.IntegerField()
	unit_price = models.FloatField()

	class Meta:
		db_table = 'order_item'