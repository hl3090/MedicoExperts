"""
URL configuration for medicoexperts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('doctor-profile/',views.doctor_profile,name="doctor-profile"),
    # path('doctor-home/', views.doctor_home, name='doctor-home/')
    path('logout/', views.logout, name='logout'),
    
    path('change-password/',views.change_password,name="change-password"),
    path("logout/",views.logout,name="logout"),
    path("doctor-profile-update/",views.doctor_profile_update,name="doctor-profile-update"),
    path('all_doctor/',views.all_doctor,name="all_doctor"),
    path('specific-doctor/<int:pk>',views.specific_doctor,name="specific-doctor"),

    path("patient-profile/",views.patient_profile,name="patient-profile"),
    path("patient-allDoctors/",views.patient_allDoctors,name="patient-allDoctors"),
    path('specific-doctor-appointment/<int:pk>',views.specific_doctor_appointment,name="specific-doctor-appointment"),
    path("book-appointment",views.book_appointment,name="book-appointment"),
    path("doctor-appointment",views.doctor_appointment,name="doctor-appointment"),

    path("approve-appointment/",views.approve_appointment,name="approve-appointment"),

    path("approve-by-doctor/<int:pk>",views.approve_by_doctor,name="approve-by-doctor"),
    path("reject-by-doctor/<int:pk>",views.reject_by_doctor,name="reject-by-doctor"),

    path("reject-appointment/",views.reject_appointment,name="reject-appointment"),
    path("patient-appointment/",views.patient_appointment,name="patient-appointment"),
    
    path("forgot-password/",views.forgot_password,name="forgot-password"),
    path("reset-password/",views.reset_password,name="reset-password"), 

    path("reset-update-password/",views.reset_update_password,name="reset-update-password"),

]
