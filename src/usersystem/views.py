from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from operator import attrgetter
from django.views.decorators.csrf import csrf_exempt
from usersystem.models import Bill, Particulate
import json
import datetime
from datetime import datetime
from account.models import Account
from django.http import JsonResponse
from django.db import connection


def system_detail_view(request):
  if request.user.is_authenticated:
    context = {}
    return render(request, 'usersystem/detail.html', context)
  else:
    return redirect("home")
@csrf_exempt
def billing_view(request):
  if request.user.is_authenticated:
    context = {}
    if request.POST:
      # fromJs = json.loads(request.body)
      # print(fromJs[0]["particulars"])
      # fromJs = json.loads(request.body)
      # print(fromJs["menu"][0]["rate"])
      bills_instance = Bill()
      data = json.loads(request.body)
      if data["name"] is None:
        print("NO customer name")
      else:
        bills_instance.name = data["name"]
      if data["billno"] is None:
        print("No billno")
      else:
        if Bill.objects.filter(billno=data["billno"]).exists():
          return HttpResponse("Exists")
        bills_instance.billno = data["billno"]
      if data["date"] is None:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
      if data["total"] is None:
        print("total is not there")
      else:
        bills_instance.total= data["total"]
      if data["vehicleno"] is None:
        print("no vehicle no")
      else:
        bills_instance.vehicleno = data["vehicleno"]
      if data["vehiclename"] is None:
        print("no veicle name")
      else:
        bills_instance.vehiclename = data["vehiclename"]
      if data["km"] is None:
        print("NO km")
      else: 
        bills_instance.km = data["km"]
      if data["email"] is None:
        print("NO mail")
      else:
        bills_instance.email = data["email"]
      if data["mobileno"] is None:
        print("No mobile")
      else:
        bills_instance.mobileno = data["mobileno"]
      bills_instance.accountid=Account.objects.filter(email=request.user.email).first()
      bills_instance.save()

      for m in data['menu']:
        particulate_instance = Particulate()
        if m["particulars"] is None:
          print("no particulars")
        else:
          particulate_instance.particulrs=m["particulars"]
          particulate_instance.rate=m["rate"]
          particulate_instance.quantity=m["quantity"]
          particulate_instance.gst=m["gst"]
          particulate_instance.sum=m["amount"]
          particulate_instance.fid=bills_instance
          particulate_instance.save()
          # print(m["particulars"])
          # print(m["rate"])
          # print(m["quantity"])
          # print(m["total"])

      return HttpResponse("OK")    
      context["saving_data"]="fucked"
    query = Account.objects.filter(email=request.user.email).first()
    context["here"]="printhere"
    if request.GET:
      return redirect("home")
    # bill_post = sorted(fetchbill(query),key=attrgetter('created_at'), reverse=True)
    bill_post = fetchbill(query)
    context['bill_post'] = bill_post
    return render(request, 'usersystem/billing.html', context)
  else:
    return redirect("home")
