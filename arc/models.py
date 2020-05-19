from django.db import models
# Create your models here.

class DonationUser(models.Model):
	fullname = models.CharField(max_length=100)
	email = models.CharField(max_length=50)
	adr = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	amount = models.IntegerField()
	mobile = models.IntegerField()
	order_id = models.CharField(max_length=50)
class paymentCP(models.Model):
	User = models.ForeignKey(DonationUser,on_delete=models.CASCADE)
	payment_id = models.CharField(max_length=300)
	order_id = models.CharField(max_length=100)
	signature_hash = models.CharField(max_length=300)
	created_at = models.DateTimeField(auto_now=True)
	status = models.IntegerField()

