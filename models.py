from django.db import models

# Create your models here.
class User(models.Model):
    email=models.EmailField(max_length=35,unique=True)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=10)
    otp = models.IntegerField(default=456)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_validate = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
    
class Doctor(models.Model):
    uid = models.ForeignKey(User,on_delete = models.CASCADE)
    username = models.CharField(max_length=20)
    contactno = models.CharField(max_length=20,null=True,blank=True)
    specification = models.CharField(max_length=50,null=True,blank=True)
    experience = models.CharField(max_length=20,null=True,blank=True) 
    address = models.TextField(null=True,blank=True)
    visiting_hours = models.CharField(max_length=20,null=True,blank=True)   
    pic = models.FileField(upload_to='media/images/',default='media/doctor.jpeg')
    
    def __str__(self):
        return self.username
    
class Patient(models.Model):
    uid = models.ForeignKey(User,on_delete = models.CASCADE)
    username = models.CharField(max_length=20)
    contactno = models.CharField(max_length=20,null=True,blank=True)
    bloodgroup = models.CharField(max_length=20,null=True,blank=True)
    age = models.CharField(max_length=20,null=True,blank=True)
    gender = models.CharField(max_length=20,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    pic = models.FileField(upload_to='media/images/',default='media/patient.jpeg')
    
    def __str__(self):
        return self.username
    
class Appointment(models.Model):
    pid = models.ForeignKey(Patient,on_delete =models.CASCADE) # patient foreign key
    did = models.ForeignKey(Doctor,on_delete =models.CASCADE) # doctor foreign key 
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    status = models.CharField(max_length = 20,default="PENDING") # Approve , Reject , Pending 
    remarks = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.pid.username
    