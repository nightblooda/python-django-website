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


      return HttpResponse("OK")    
      context["saving_data"]="fucked"
    query = Account.objects.filter(email=request.user.email).first()
    context["here"]="printhere"
    if request.GET:
      return redirect("home")
    bill_post = fetchbill(query)
    context['bill_post'] = bill_post
    return render(request, 'usersystem/billing.html', context)
  else:
    return redirect("home")

def fullbill_view(request):
  if request.POST:
    return HttpResponse("OK")
  else:
    data = request.GET["bill"]
    rooms = list(Particulate.objects.filter(fid=data).values())
    d =  dict()
    d['rooms'] = rooms
    return JsonResponse(d)

def deletebill_view(request):
  if request.POST:
    return HttpResponse("OK")
  else:
    data = request.GET["bill"]
    Bill.objects.filter(billno=data).delete()
    return HttpResponse("OK")


def fetchbill(query=None):
  queryset = []
  allset = []
  bill = Bill.objects.filter(accountid=query).order_by('-created_at')
  return bill

def screen_view(request):

  context = {}

  query = ""
  if request.GET:
    query = request.GET['q']
    context['query'] = str(query)

  bill_post = sorted(fetchbill(query),key=attrgetter('created_at'), reverse=True)
  context['bill_post'] = bill_post

  #Pagination
  

  return render(request, "usersystem/billing.html", context)

@csrf_exempt
def report_view(request):
  if request.POST:
    return HttpResponse("OK")
  else:
    data = request.GET["bill"]
    m = data.split('-')
    userl = Account.objects.filter(email=request.user.email).first()

    customer = Bill.objects.filter(created_at__date=data, accountid=userl)
    customer_amount_d = customer.aggregate(total_sum=Round(Sum('total')))['total_sum']
    customer_count_d = customer.count()
    alignment = Bill.objects.filter(particulate__particulrs='Wheel Alignment', accountid=userl, created_at__date=data)
    alignment_count_d = alignment.count()
    alignment_amount_d = alignment.aggregate(particulate_sum=Round(Sum('particulate__sum')))['particulate_sum']
    washing = Bill.objects.filter(particulate__particulrs='Washing', accountid=userl, created_at__date=data)
    washing_count_d = washing.count()
    washing_amount_d = washing.aggregate(particulate_sum=Round(Sum('particulate__sum')))['particulate_sum']
    labour_amount_d = Bill.objects.filter(particulate__particulrs='Labour', accountid=userl, created_at__date=data).aggregate(particulate_sum=Round(Sum('particulate__sum')))['particulate_sum']



    customer_m = Bill.objects.filter(created_at__month=m[1], accountid=userl)
    customer_amount_m = customer_m.aggregate(total_sum=Round(Sum('total')))['total_sum']
    customer_count_m = customer_m.count()
    alignment_m = Bill.objects.filter(particulate__particulrs='Wheel Alignment', accountid=userl, created_at__month=m[1])
    alignment_count_m = alignment_m.count()
    alignment_amount_m = alignment_m.aggregate(particulate_sum=Round(Sum('particulate__sum')))['particulate_sum']
    washing_m = Bill.objects.filter(particulate__particulrs='Washing', accountid=userl, created_at__month=m[1])
    washing_count_m = washing_m.count()
    washing_amount_m = washing_m.aggregate(particulate_sum=Round(Sum('particulate__sum')))['particulate_sum']
    labour_amount_m = Bill.objects.filter(particulate__particulrs='Labour', accountid=userl, created_at__month=m[1]).aggregate(particulate_sum=Round(Sum('particulate__sum')))['particulate_sum']
    d =  dict()
    d['customer_count_d'] = customer_count_d
    d['customer_amount_d'] = customer_amount_d
    d['alignment_count_d'] = alignment_count_d
    d['alignment_amount_d'] = alignment_amount_d
    d['washing_count_d'] = washing_count_d
    d['washing_amount_d'] = washing_amount_d
    d['labour_amount_d'] = labour_amount_d
    
    d['customer_count_m'] = customer_count_m
    d['customer_amount_m'] = customer_amount_m
    d['alignment_count_m'] = alignment_count_m
    d['alignment_amount_m'] = alignment_amount_m
    d['washing_count_m'] = washing_count_m
    d['washing_amount_m'] = washing_amount_m
    d['labour_amount_m'] = labour_amount_m
    return JsonResponse(d)


@csrf_exempt
def search_view(request):
  if request.POST:
    return HttpResponse("OK")
  else:
    context = {}
    data = request.GET["bill"]
    userl = Account.objects.filter(email=request.user.email).first()
    searchbill = list(Bill.objects.filter(accountid=userl,vehicleno=data).order_by('-created_at').values())
    d = dict()
    d['searchbill']=searchbill
    return JsonResponse(d)