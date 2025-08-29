from django.shortcuts import render,redirect
from travels.models import TravelOption
from django.utils import timezone
from .models import *

# Create your views here.
def index(request):
    bookings = Booking.objects.filter(user=request.user,status = 'Confirmed',travel_option__date_time__gt = timezone.now())
    cancelled = Booking.objects.filter(user=request.user,status = 'Cancelled')
    previous = Booking.objects.filter(user=request.user,travel_option__date_time__lte = timezone.now())
    return render(request,'bookings/index.html',{'bookings': bookings,'cancelled': cancelled,'previous': previous})

def book(request):
    if (request.user.is_authenticated):
        id = request.GET.get('id')
        topt = TravelOption.objects.get(id=id) 
        return render(request,'bookings/booking_form.html',{'travel_option': topt})
    else:
        return redirect('/user/auth/')
    
def postBook(request):
    user = request.user
    travel_option = int(request.POST.get('travel_option'))
    travel_option = TravelOption.objects.get(id=travel_option) 
    no_of_seats = int(request.POST.get('number_of_seats'))
    total_price = request.POST.get('total_price')
    status = 'Confirmed'
    if no_of_seats <= travel_option.available_seats:
        travel_option.available_seats -= no_of_seats
        travel_option.save()
        Booking.objects.create(user=user,travel_option=travel_option,number_of_seats=no_of_seats,total_price=total_price,status=status)
        return redirect('/bookings/')
    else:
        previous_url = request.META.get('HTTP_REFERER')
        return redirect(previous_url,{'message': f'only {travel_option.available_seats} are available'})
    
def cancel(request):
    id = int(request.GET.get('id'))
    booking = Booking.objects.get(id=id)
    travel = booking.travel_option
    travel.available_seats += booking.number_of_seats
    travel.save()
    booking.status = 'Cancelled'
    booking.save()
    return redirect('/bookings/')