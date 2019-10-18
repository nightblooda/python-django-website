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
