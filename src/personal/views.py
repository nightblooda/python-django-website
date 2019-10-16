from django.shortcuts import render

def home_screen_view(request):
  return render(request, "personal/home.html")

def support_view(request):
  return render(request, "personal/support.html")

def pricing_view(request):
  return render(request, "personal/pricing.html")
