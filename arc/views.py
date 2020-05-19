from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import DonationUser,paymentCP
import razorpay
import json
from django.views import View
client = razorpay.Client(auth=("rzp_test_Z7MdZA5qRchXLL", "LzzAeIOlzaiz1lJ69rk5NJ10"))
client.set_app_details({"title" : "arc", "version" : "1.0.1"})

class homepage(View):
	def get(self, request):
		return render(request, "arc/homepage.html")

class checkout(View):
	def get(self, request):
		return redirect("homepage")
	def post(self, request):
		fullname=request.POST['fname']
		email=request.POST['email']
		adr=request.POST['adr']
		city=request.POST['city']
		amount=int(request.POST['amount'])*100
		mobile = int(request.POST['mobile'])
		DATA ={
			"amount" : amount,
			"currency" : "INR",
			"receipt" : "Donation",
			"payment_capture"  : 1,
		}
		response =client.order.create(data=DATA)
		order_id = response['id']
		Dn = DonationUser()
		Dn.fullname = fullname
		Dn.email = email
		Dn.adr = adr
		Dn.city = city
		Dn.amount = amount / 100
		Dn.mobile = mobile
		Dn.order_id = order_id
		Dn.save()
		return render(request,"arc/checkout.html",context={
			"order_id" : order_id,
			"amount" : amount,
			"name" : fullname,
			"mobile" : mobile,
			"email" : email
			})

class success(View):
	def get(self, request):
		return redirect("homepage")
	def post(self, request):
		razorpay_order_id=request.POST['razorpay_order_id']
		razorpay_payment_id=request.POST['razorpay_payment_id']
		razorpay_signature=request.POST['razorpay_signature']
		pay = paymentCP()
		pay.User = DonationUser.objects.get(order_id = razorpay_order_id)
		pay.order_id = razorpay_order_id
		pay.payment_id = razorpay_payment_id
		pay.signature_hash = razorpay_signature
		pay.status = 0
		pay.save()
		params_dict = {
			'razorpay_order_id': razorpay_order_id,
			'razorpay_payment_id': razorpay_payment_id,
			'razorpay_signature': razorpay_signature
			}
		try:
			client.utility.verify_payment_signature(params_dict)
			paymentCP.objects.filter(order_id=razorpay_order_id).update(status=1)
			return HttpResponse("""<center><h1>Thanks!</h1>
									<p>Talk is cheap. Show me the code. ;-) </p></center>"""
								)
		except:
			return HttpResponse('Unauthorized', status=401)