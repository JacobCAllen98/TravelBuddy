from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addUser', views.addUser),
    path('success', views.success),
    path('login', views.login),
    path('dash', views.dash),
    path('logout', views.logout),
    path('makePlan', views.makePlan),
    path('createPlan', views.createPlan),
    path('joinTrip/<tripID>', views.joinTrip),
    path('viewTrip/<tripID>', views.viewTrip),
]