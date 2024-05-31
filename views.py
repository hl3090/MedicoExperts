from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import mySendmail
from random import *
# Create your views here.
def home(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            context = {
                "uid" : uid,
                "did" : did,
            }
            return render(request,"myapp/doctor_index.html",context)
        else:
            pid = Patient.objects.get(uid = uid)
            context = {
                "uid" : uid,
                "pid" : pid,
            }
            return render(request,"myapp/patient_index.html",context)
            
    else:    
        return render(request,"myapp/login.html")

def login(request):
    if "email" in request.session:
        return HttpResponseRedirect (reverse('home'))
    else:    
        if request.POST:
            # print("login button clicked")
            email = request.POST['email']
            password = request.POST['password']
            
            try:
                uid = User.objects.get(email = email,password = password)
                print(uid)
                request.session["email"] = uid.email   #session
                if uid.role == "Doctor":
                    return HttpResponseRedirect (reverse('home')) 
                else:
                    return HttpResponseRedirect (reverse('home')) 
            except:

                e_msg = "Invalid email or password"
                return render(request,"myapp/login.html",{'e_msg':e_msg})       
        else:
            print("only page loaded")    
        return render(request,"myapp/login.html")


def signup(request):  
    if request.POST:
        print("Submit button clicked")
        role = request.POST['role']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        contact = request.POST['contact']
        print("------------>> role",role)
        print("------------>> username",username)
        print("------------>> email",email)
        try:
            uid = User.objects.create(email = email,password = password,role=role)
            if role == "Doctor":
                
                did = Doctor.objects.create(uid = uid,username = username,contactno = contact)
                if did:
                    s_msg = "Successfully Records Added"
                    return render(request,"myapp/signup.html",{'s_msg':s_msg})
                else:
                    e_msg = "Something went wrong - Please enter valid details"
                    return render(request,"myapp/signup.html",{'e_msg':e_msg})
            else:
                pid = Patient.objects.create(uid = uid,username = username,contactno = contact)
                if pid:
                    s_msg = "Successfully Records Added"
                    return render(request,"myapp/signup.html",{'s_msg':s_msg})
                else:
                    e_msg = "Something went wrong - Please enter valid details"
                    return render(request,"myapp/signup.html",{'e_msg':e_msg})    
        except:
            e_msg = "Email already exists"
            return render(request,"myapp/signup.html",{'e_msg':e_msg})
    else:
        print("SIGNUP page loaded")
        return render(request,"myapp/signup.html")
    
# def doctor_home(request):
#     return render (request,"myapp/doctor_index.html")

def logout(request):
    if "email" in request.session:
        del request.session['email']
        return HttpResponseRedirect(reverse('login'))
    return render(request,"myapp/login.html")


def doctor_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            context = {
                "uid" : uid,
                "did" : did,
            }
            return render(request,"myapp/doctor_profile.html",context)
        
        
def change_password(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)

            currentpassword = request.POST['currentpassword']
            newpassword = request.POST['newpassword']

            if uid.password == currentpassword:
                uid.password = newpassword
                uid.save()  # update new password
                del request.session['email']
                s_msg = "Successfully password reset !!"
                return render(request,"myapp/login.html",{'s_msg':s_msg})
            else:
                del request.session['email']
                e_msg = "You have entered wrong password "
                return render(request,"myapp/login.html",{'e_msg':e_msg})
                
def doctor_profile_update(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)

            did.username = request.POST['username']
            did.contactno = request.POST['contactno']
            did.specification = request.POST['specification'] 
            did.experience = request.POST['experience']
            did.address = request.POST['address']
            did.visiting_hours = request.POST['visiting_hours']

            did.save()

            if "pic" in request.FILES:
                did.pic = request.FILES['pic']
                did.save()

            
            context = {
                "uid" : uid,
                "did" : did,
            }
            return HttpResponseRedirect(reverse('doctor-profile'))
        
def all_doctor(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            dall = Doctor.objects.exclude(uid = uid)
            print("------------------>>>> dall ",dall)
            context = {
                "uid" : uid,
                "did" : did,
                "dall" : dall
            }
            return render(request,"myapp/doctors.html",context)
    
def specific_doctor(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            s_did = Doctor.objects.get(id = pk)
            print("------------>>>>>SDID",s_did)
            context = {
                "uid" : uid,
                "did" : did,
                "s_id" : s_did,
            }
            return render(request,"myapp/doctor_specific_profile.html",context)
        

def patient_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Patient":
            pid = Patient.objects.get(uid = uid)

            context = {
                "uid" : uid,
                "pid" : pid,
            }

            return render(request,"myapp/patient_profile.html",context)
        
def patient_allDoctors(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Patient":
            pid = Patient.objects.get(uid = uid)
            dall = Doctor.objects.all()
            context = {
                "uid" : uid,
                "pid" : pid,
                "dall" : dall,
            }
            return render(request,"myapp/doctors_patient_side.html",context)
        
def specific_doctor_appointment(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Patient":
            pid = Patient.objects.get(uid = uid)
            s_did = Doctor.objects.get(id = pk)
            print("------------>>>>>SDID",s_did)

            context = {
                "uid" : uid,
                "pid" : pid,
                "s_id" : s_did,
                "pk" : pk
            }
            return render(request,"myapp/book-appointment.html",context)    
    
def book_appointment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Patient":
            pid = Patient.objects.get(uid = uid)

            doctor_id = request.POST['pk']
            doctor_id = Doctor.objects.get(id = doctor_id)
            print("------------<<<",doctor_id.username)
            # print("---->>>> ",doctor_id)
            # doc_id = Doctor.objects.get(id = doctor_id)
            # print("---->>> doc_id",doc_id)
            a_date = request.POST['a_date']
            a_time = request.POST['a_time']
            a_reason = request.POST['a_reason']
            
            a_id = Appointment.objects.create(pid=pid,did=doctor_id,date= a_date,time = a_time,remarks = a_reason)

            if a_id:
                s_msg = "Successfully appointment request send"
                context = {
                    "uid" : uid,
                    "pid" : pid,
                    "s_msg" : s_msg,
                }
                return render(request,"myapp/book-appointment.html",context)    
            return render(request,"myapp/book-appointment.html",context)    
            

def doctor_appointment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            # to fetch multiple records condition wise 
            a_all = Appointment.objects.filter(did = did,status = "PENDING")
            print("=====>>>")
            print(a_all)
            context = {
                "uid" : uid,
                "did" : did,
                "a_all" : a_all,
            }
            return render(request,"myapp/all_appointments_doctor_side.html",context)
        
def approve_appointment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            # to fetch multiple records condition wise 
            a_all = Appointment.objects.filter(did = did,status = "APPROVE")
            print("=====>>>")
            print(a_all)
            context = {
                "uid" : uid,
                "did" : did,
                "a_all" : a_all,
            }
            return render(request,"myapp/approve_appointment.html",context)
        
def approve_by_doctor(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            
            a_all = Appointment.objects.get(id = pk)
            print("=====>>> approve ")
            print(a_all)

            a_all.status = "APPROVE"
            a_all.save() # update 

            return HttpResponseRedirect(reverse('approve-appointment'))
        
def reject_by_doctor(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            
            a_all = Appointment.objects.get(id = pk)

            a_all.status = "REJECT"
            a_all.save() # update 

            return HttpResponseRedirect(reverse('reject-appointment'))
        
def reject_appointment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Doctor":
            did = Doctor.objects.get(uid = uid)
            # to fetch multiple records condition wise 
            a_all = Appointment.objects.filter(did = did,status = "REJECT")
            print("=====>>>")
            print(a_all)
            context = {
                "uid" : uid,
                "did" : did,
                "a_all" : a_all,
            }
            return render(request,"myapp/reject_appointment.html",context)
        
def patient_appointment(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "Patient":
            pid = Patient.objects.get(uid = uid)
            # to fetch multiple records condition wise 
            a_all = Appointment.objects.filter(pid = pid)
            print("=====>>>")
            print(a_all)
            context = {
                "uid" : uid,
                "pid" : pid,
                "a_all" : a_all,
            }
            return render(request,"myapp/patient_appointment.html",context)        
        
def forgot_password(request):
    return render(request,"myapp/forgotpassword.html")       
        
def reset_password(request):
    if request.POST:
        email = request.POST['email']
        try:
            uid = User.objects.get(email = email)
            if uid:
                otp = randint(1111,9999)
                uid.otp = otp
                uid.save()
                print(otp)

                mySendmail("Forgot Password","otptemplate",email,{"otp" : otp})
            else:
                return render(request,"myapp/reset_password.html",{"email" : email})       
        except:
            return render(request,"myapp/forgotpassword.html",{"e_msg" : "invalid email address"})
        

def reset_update_password(request):
    if request.POST:
        email = request.POST['email']
        otp = request.POST['otp']
        newpassword = request.POST['newpassword']
        repassword = request.POST['repassword']

        uid = User.objects.get(email = email)
        if str(uid.otp) == otp and newpassword == repassword:
            uid.password = newpassword
            uid.save()

        return render(request,"myapp/login.html",{"s_msg": "Successfully password reset"})            
        