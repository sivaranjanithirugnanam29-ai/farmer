from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
from django.db.models import Sum
import random 
from django.conf import settings
from django.utils import timezone
from django.db import connection
from django.db.models import Q

def category(request):
	if request.method == 'POST':
		a=request.POST.get('name')
		b = request.POST.get('con')
		post=Category.objects.create(name=a,description=b)
		messages.success(request,'Category Added Successfully')
	return render(request,'category.html',{})
def farmer_login(request):
	if request.method == 'POST':
		name=request.POST.get('username')
		pwd=request.POST.get('password')
		user_exist=Register_Detail.objects.filter(name=name,password=pwd,user_type='farmer')
		if user_exist:
			request.session['name']= request.POST.get('username')
			a = request.session['name']
			sess = Register_Detail.objects.only('id').get(name=a).id
			request.session['user_id']= sess
			return redirect('form')
		else:
			messages.success(request,'Invalid username or Password')
	return render(request,'admin_login.html',{})
def form(request):
	a=Category.objects.all()
	return render(request,'catform.html',{'b':a})
def product_list(request):
	a=Product.objects.all()
	return render(request,'product_list.html',{'b':a})
def catedit(request,pk):
	a=Category.objects.filter(id=pk)
	if request.method == 'POST':
		c=request.POST.get('name')
		b = request.POST.get('con')
		update=Category.objects.filter(id=pk).update(name=c,description=b)
		if update:
			messages.success(request,'Category Updated Successfully')
	return render(request,'cat_edit.html',{'value':a})
def catdelete(request,pk):
	a=Category.objects.filter(id=pk).delete()
	return redirect('form')
def login_details(request):
	if request.method == 'POST':
		name=request.POST.get('username')
		pwd=request.POST.get('password')
		user_exist=Register_Detail.objects.filter(name=name,password=pwd,user_type='public')
		if user_exist:
			request.session['name']= request.POST.get('username')
			a = request.session['name']
			sess = Register_Detail.objects.only('id').get(name=a).id
			request.session['user_id']= sess
			return redirect('view_farmer')
		else:
			messages.success(request,'Invalid username or Password')
	return render(request,'temlogin.html',{})
def profile(request):
	return render(request,'dashboard.html',{})
	
def tem(request):
	return render(request,'home.html',{})
def reg(request):
	if request.method == 'POST':
		Name = request.POST.get('uname')
		Adddress = request.POST.get('address')
		Mobile= request.POST.get('mobile')
		Email = request.POST.get('email')
		Password = request.POST.get('pwd')
		utype = request.POST.get('user_type')
		crt = Register_Detail.objects.create(name=Name,
		address=Adddress,mobile=Mobile,password=Password,email=Email,user_type=utype)
		if crt:
			messages.success(request,'Registered Successfully')
	return render(request,'register.html',{})
def con(request):
	if request.method == 'POST':
		a = request.POST.get('name')
		b =request.POST.get('mail')
		c = request.POST.get('subject')
		d = request.POST.get('msg')
		crt = Contact_Detail.objects.create(name=a,email=b,subject=c,msg=d)
		if crt:
			messages.success(request,'Thanks for Contact Us.')
	return render(request,'contact.html',{})

def dash(request):
	return render(request,'dashboard.html',{})
def userdash(request):
	return render(request,'user_dashboard.html',{})
def product(request):
	a=Category.objects.all()
	user_id = request.session['user_id']
	uid = Register_Detail.objects.get(id=int(user_id))
	if request.method == 'POST':
		a=request.POST.get('name')
		b=request.POST.get('price')
		c=request.POST.get('category')
		d=request.POST.get('con')
		f =request.FILES['pic']
		c_id=Category.objects.get(id=int(c))
		prt = Product.objects.create(p_name=a,p_price=b,category=c_id,note=d,cmp_price='',image=f,user_id=uid)
		if prt:
			messages.success(request,'Product Added Successfully')
			return redirect('product')
	return render(request,'product.html',{'a':a})
def logout(request):
    try:
        del request.session['user_id']
    except:
     pass
    return render(request, 'temlogin.html', {})
def order(request):
	order = Booking_Detail.objects.all()
	return render(request,'order.html',{'order':order})
def view_product(request):
	user_id = request.session['user_id']
	a=Product.objects.filter(user_id=int(user_id))
	return render(request,'view_product.html',{'b':a})
def view_farmer(request):
	a=Register_Detail.objects.filter(user_type='farmer')
	return render(request,'farmer_info.html',{'b':a})
def product_edit(request,pk):
	a=Product.objects.filter(id=pk)
	b = Category.objects.all()
	if request.method == 'POST':
		a=request.POST.get('name')
		b=request.POST.get('price')
		c=request.POST.get('category')
		d=request.POST.get('con')
		e = request.POST.get('others')
		c_id=Category.objects.get(id=int(c))
		prt = Product.objects.filter(id=pk).update(p_name=a,p_price=b,category=c_id,note=d,cmp_price=e)
		if prt:
			return redirect('view_product')
			messages.success(request,'Product Updated Successfully')
	return render(request,'product_edit.html',{'value':a,'b':b})
def product_delete(request,pk):
	a=Product.objects.filter(id=pk).delete()
	return redirect('view_product')
def veg_product(request):
	user_id = request.GET.get('fid')
	product = Product.objects.filter(user_id=int(user_id))
	uid = request.session['user_id']
	return render(request,'veg_product.html',{'product':product})
def add_to_cart(request,pk):
	if request.session.has_key('user_id'):
		uid = request.session['user_id']
		farmer_id = request.GET.get('fid')
		user_id = Register_Detail.objects.get(id=int(uid))
		product_id = Product.objects.get(id=int(pk))
		product_detail = Product.objects.filter(id=int(pk))
		if request.method == 'POST':
			price = request.GET.get('price')
			tot = request.POST.get('tot')
			tot_price = float(price)*int(tot)
			crt = Cart_Details.objects.create(user_id=user_id,product_id=product_id,status='pending',
			tot=tot,tot_price=tot_price,farmer_id=int(farmer_id))
			if crt:
				return redirect('view_items_cart_product')
		return render(request,'add_to_cart.html',{'product_detail':product_detail})
	else:
		return render(request,'temlogin.html',{})

def remove_item(request,pk):
	Cart_Details.objects.filter(id=int(pk)).delete()
	return redirect('view_items_cart_product')
def cart(request):
	uid = request.session['user_id']
	product_details = Cart_Details.objects.filter(user_id=int(uid),status='pending')
	return render(request,'cart.html',{'product_details':product_details})
def view_items_cart(request,pk):
	product_details = Cart_Details.objects.filter(book_id=int(pk))
	tot = Cart_Details.objects.filter(book_id=int(pk)).aggregate(Sum('tot'))
	return render(request,'view_items_cart.html',{'product_details':product_details,'pk':pk,'tot':tot})
def payment_received(request,pk):
	Cart_Details.objects.filter(book_id=int(pk)).update(status='paid')
	return redirect('order')
def purchased(request):
	uid = request.session['user_id']
	product_details = Cart_Details.objects.filter(user_id=int(uid),status='paid')
	return render(request,'purchased.html',{'product_details':product_details})
def order_purchased(request):
	product_details = Cart_Details.objects.filter(user_id=int(uid),status='paid')
	return render(request,'purchased.html',{'product_details':product_details})
def ordered_item(request):
	uid = request.session['user_id']
	order = Booking_Detail.objects.filter(user_id=int(uid))
	return render(request,'ordered_item.html',{'order':order})
def view_items_cart_product(request):
	uid = request.session['user_id']
	r_num =  random.randrange(20, 50, 3)
	product_details = Cart_Details.objects.filter(status='pending',user_id=int(uid))
	tot = Cart_Details.objects.filter(status='pending',user_id=int(uid)).aggregate(Sum('tot_price'))
	return render(request,'view_items_cart_product.html',{'product_details':product_details,'tot':tot,'r_num':r_num})
def purchase(request):
	uid = request.session['user_id']
	order_id =  request.GET.get('order_id')
	addr = Register_Detail.objects.filter(id=int(uid))
	if request.method == 'POST':
		upd = Cart_Details.objects.filter(user_id=int(uid),status='pending').update(status='order',book_id=order_id,date=timezone.now())
		if upd:
			return redirect('order_item_user')
	return render(request,'purchase.html',{'addr':addr})
def purchased_item(request,pk,status):
	uid = request.session['user_id']
	product_details = Cart_Details.objects.filter(book_id=pk,user_id=int(uid))
	tot = Cart_Details.objects.filter(book_id=pk,user_id=int(uid)).aggregate(Sum('tot_price'))
	return render(request,'purchased_item.html',{'product_details':product_details,'tot':tot,'status':status})
def order_item_user(request):
	uid = request.session['user_id']
	cursor = connection.cursor()
	post = '''SELECT Sum(app_cart_details.tot_price), app_cart_details.book_id, app_cart_details.date, app_cart_details.status,
	app_cart_details.user_id_id  from app_cart_details where app_cart_details.status='order' OR app_cart_details.status='paid' AND 
	app_cart_details.user_id_id = '%d' Group By app_cart_details.book_id  '''  % (int(uid))
	query = cursor.execute(post)
	row = cursor.fetchall()
	return render(request,'order_item_user.html',{'product_details':row})
def order_item(request):
	farmer_id = request.session['user_id']
	cursor = connection.cursor()
	post = '''SELECT Sum(app_cart_details.tot_price), app_cart_details.book_id, app_cart_details.date, app_cart_details.status,
	app_cart_details.user_id_id from app_cart_details where app_cart_details.status='order' OR app_cart_details.status='paid' 
	AND app_cart_details.farmer_id='%d' Group By app_cart_details.book_id  ''' % (int(farmer_id))
	query = cursor.execute(post)
	row = cursor.fetchall()
	return render(request,'order_item.html',{'product_details':row})
def status_order(request,pk,user_id,status):
	addr = Register_Detail.objects.filter(id=int(user_id))
	product_details = Cart_Details.objects.filter(book_id=pk)
	tot = Cart_Details.objects.filter(book_id=pk).aggregate(Sum('tot_price'))
	if request.method == 'POST':
		upd = Cart_Details.objects.filter(book_id=pk).update(status='paid')
		if upd:
			return redirect('order_item')
	return render(request,'status_order.html',{'tot':tot,'product_details':product_details,'addr':addr,'pk':pk,'user_id':user_id,'status':status})
def search_market(request):
	if request.method == 'POST':
		a = request.POST.get('search')
		ids = Market_Detail.objects.filter(Q(city__istartswith=a)| Q(area__istartswith=a))
		return render(request,'search_product.html',{'ids':ids})
	else:
		return render(request,'search_product.html',{})
def veg_details(request,pk):
	ids = Veg_Detail.objects.filter(market_id=int(pk))
	return render(request,'veg_details.html',{'ids':ids})
def search(request):
	if request.method == 'POST':
		a = request.POST.get('search')
		ids = Forming_Detail.objects.filter(name__istartswith=a)
		return render(request,'search.html',{'ids':ids})
	else:
		return render(request,'search.html',{})

