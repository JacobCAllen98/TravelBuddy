from django.db import models
import re
import bcrypt
from datetime import datetime

# Create your models here.
class AccValid(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        alpha = re.compile(r'^[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors["name"] = "First Name must be atleast three characters"
        elif not alpha.match(postData['name']):
            errors["nameAlpha"] = "Name can only contain letters"
        if len(User.objects.filter(username=postData['username'])) >0:
            errors['usernameTaken'] = "That username is already in use"
        if len(postData['username']) < 3:
            errors["usernameLength"] = "Username must be atleast three characters"
        if len(postData['pw']) < 8:
            errors["pw"] = "Password must be atleast eight characters"
        if postData['pw'] != postData['cpw']:
            errors["cpw"] = "Passwords do not match"
        return errors
    def login_validator(self, postData):
        errors = {}
        passw = postData['pw']
        if len(postData['username']) < 3:
            errors["usernameLength"] = "Username is required to login"
            return errors
        elif len(User.objects.filter(username=postData['username'])) == 0:
            errors['emailUnused'] = "That Username is not registered"
            return errors
        person = User.objects.get(username=postData['username'])
        if not bcrypt.checkpw(passw.encode(), person.passw.encode()):
            errors['password'] = "Username or password is incorrect"
        return errors

    def trip_validator(self, postData):
        errors = {}
        if len(postData['dest']) < 1:
            errors["destName"] = "Please select a destination"
        if len(postData['desc']) < 1:
            errors["desc"] = "Please describe the trip"
        if len(postData['startDate']) < 1:
            errors["noStart"] = "Please select a start date"
        if len(postData['endDate']) < 1:
            errors["noEnd"] = "Please select an ending date"
        if len(errors) > 0:
            return errors
        start = str(postData['startDate'])
        end = str(postData['endDate'])
        year,month,day = start.split('-')
        eyear,emonth,eday = end.split('-')
        if int(eyear) < int(year):
            errors["year"] = "Year ends before it begins"
            return errors
        elif int(eyear) == int(year):
            if int(emonth) < int(month):
                errors["month"] = "Month ends before it begins"
                return errors
            elif int(emonth) == int(month):
                if int(eday) < int(day):
                    errors["day"] = "Day ends before it begins"
                    return errors
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    passw = models.CharField(max_length=255)
    objects = AccValid()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField()
    attend = models.ManyToManyField(User, related_name="trips")
    objects = AccValid()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)