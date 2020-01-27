from django.shortcuts import render, redirect
import bcrypt
import re
from .models import User, Trip
from django.contrib import messages
from datetime import date

# Create your views here.
def index(request):
    if 'LoggedUser' in request.session:
        return redirect("/dash")
    return render(request,"index.html")

def addUser(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    passw = request.POST['pw']
    pw_hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
    User.objects.create(name=request.POST['name'],username=request.POST['username'],passw=pw_hash)
    return redirect("/success")

def success(request):
    return render(request, "success.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    user = User.objects.filter(username=request.POST['username'])
    request.session['LoggedUser']=user[0].id
    return redirect("/dash")

def dash(request):
    errors = {}
    if not 'LoggedUser' in request.session:
        errors['NoUser'] = "Please log in to continue"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    user = User.objects.get(id=request.session['LoggedUser'])
    attending = Trip.objects.filter(attend=user.id)
    notattending = Trip.objects.exclude(attend=user.id)
    context = {
        'user': user,
        'currTrip': attending,
        'possTrip': notattending,
    }
    return render(request, "dash.html", context)

def logout(request):
    del request.session['LoggedUser']
    return redirect("/")

def makePlan(request):
    now = date.today()
    now = str(now)
    context = {
        'date': now
    }
    return render(request, "newTrip.html", context)

def createPlan(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/makePlan")
    creator = User.objects.get(id=request.session['LoggedUser'])
    newTrip = Trip.objects.create(dest=request.POST['dest'],desc=request.POST['desc'],startDate=request.POST['startDate'],endDate=request.POST['endDate'],created_by= creator.name)
    newTrip.attend.add(creator)
    return redirect("/dash")

def joinTrip(request, tripID):
    attendee = User.objects.get(id=request.session['LoggedUser'])
    trip = Trip.objects.get(id=tripID)
    trip.attend.add(attendee)
    return redirect("/dash")

def viewTrip(request,tripID):
    trip = Trip.objects.get(id=tripID)
    people = trip.attend.exclude(name=trip.created_by)
    context = {
        'trip': trip,
        'people': people
    }
    return render(request,"viewTrip.html",context)