from django.db import models
from django.utils.timezone import now
from account.models import Account
from django.conf import settings

class Bill(models.Model):
    billno=models.CharField(max_length=50, null=False, blank=False, primary_key=True)
    created_at=models.DateTimeField(default=now, editable=False)
    vehiclename=models.CharField(max_length=50, null=False, blank=False)
    vehicleno=models.CharField(max_length=50, null=False, blank=False)
    km=models.CharField(max_length=50, null=False, blank=False)
    name=models.CharField(max_length=50, null=False, blank=False)
    total=models.CharField(max_length=50, null=False, blank=False)
    mobileno=models.CharField(max_length=13, null=False, blank=False)
    email=models.EmailField(max_length=60)
    accountid=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  

    def __str__(self):
      return self.billno
class Particulate(models.Model):
  particulrs=models.CharField(max_length=200, null=False, blank=False)
  rate=models.DecimalField(max_digits=13, decimal_places=2)
  gst=models.DecimalField(max_digits=5, decimal_places=2)
  quantity=models.DecimalField(max_digits=13, decimal_places=2)
  sum=models.DecimalField(max_digits=13, decimal_places=2)
  fid=models.ForeignKey(Bill, on_delete=models.CASCADE)