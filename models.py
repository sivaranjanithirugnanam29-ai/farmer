from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=1000,null=True)
	def __str__(self):
		return self.name
class Register_Detail(models.Model):
	name = models.CharField(max_length=50,unique=True)
	address = models.CharField(max_length=50)
	mobile = models.CharField(max_length=20)
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	user_type = models.CharField(max_length=30,null=True)
	def __str__(self):
		return self.name
class Product(models.Model):
	p_name = models.CharField(max_length=50)
	p_price = models.CharField(max_length=50)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	note = models.TextField(max_length=2000)
	cmp_price = models.CharField(max_length=50,null=True)
	image = models.FileField('Upload Image',upload_to='documents/',null=True)
	user_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.p_name
class Service(models.Model):
	service = models.CharField(max_length=50)
	date = models.CharField(max_length=50)
	time = models.CharField(max_length=20)
	member = models.CharField(max_length=50)
	note = models.EmailField(max_length=50)
class Cart_Details(models.Model):
	user_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE,null=True)
	book_id = models.CharField(null=True,max_length=30)
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
	farmer_id = models.IntegerField(null=True)
	status = models.CharField(max_length=50)
	tot = models.IntegerField(null=True)
	tot_price = models.FloatField(null=True)
	date = models.DateField(null=True)
class Market_Detail(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=1000)
	city = models.CharField(max_length=100)
	area = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	image = models.FileField('Upload Image',upload_to='documents/',null=True)
	def __str__(self):
		return self.name
class Veg_Detail(models.Model):
	market_id = models.ForeignKey(Market_Detail, on_delete=models.CASCADE)
	veg_name = models.CharField(max_length=1000)
	quantity = models.CharField(max_length=100)
	price = models.CharField(max_length=100)
	date = models.DateField(null=True)
	image = models.FileField('Upload Image',upload_to='documents/',null=True)
	def __str__(self):
		return self.veg_name
class Forming_Detail(models.Model):
	name = models.CharField('Vegetable Name',max_length=100)
	water_contain = models.TextField('Water Level',max_length=3000)
	fertilizer = models.TextField('Fertilizer',max_length=3000)
	soil = models.TextField('Nature of Soli',max_length=3000)
	others = models.TextField(max_length=3000)
	image = models.FileField('Upload Image',upload_to='farmer/')
	def __str__(self):
		return self.name
