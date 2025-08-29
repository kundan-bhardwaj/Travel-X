from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.utils import timezone

# Create your views here.
def index(request):
    search = request.GET.get("search", "")
    type = request.GET.get("type", "")
    source = request.GET.get("source","")
    destination = request.GET.get("destination","")
    date = request.GET.get("date","")

    travels = TravelOption.objects.filter(date_time__gt=timezone.now())
    sources = TravelOption.objects.values_list("source", flat=True).distinct()
    destinations = TravelOption.objects.values_list("destination", flat=True).distinct()
    date_time = TravelOption.objects.values_list("date_time", flat=True).distinct()

    if search:
        travels = travels.filter(
            Q(destination__icontains=search) |
            Q(source__icontains=search)
        )
    if type:
        travels = travels.filter(type=type)
    if source:
        travels = travels.filter(source=source)
    if destination:
        travels = travels.filter(destination=destination)
    if date:
        travels = travels.filter(date_time=date)
    if request.htmx:
        return render(request, "partials/travel-option.html", {"travels": travels})
    return render(request,'travels/index.html',{'travels':travels, 'sources': sources,'destinations': destinations,'dates': date_time})