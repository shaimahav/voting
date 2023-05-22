from django.db import models
from siteadmin.models import *
from candidates.models import *


# Create your models here.
class voterregister(models.Model):
    firstname= models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    dateofbirth= models.CharField(max_length=20)
    state = models.ForeignKey(state, on_delete=models.CASCADE)
    district = models.ForeignKey(district, on_delete=models.CASCADE)

    location = models.ForeignKey(landmark, on_delete=models.CASCADE)
    assembly = models.ForeignKey(assembly, on_delete=models.CASCADE)

    adharno= models.CharField(max_length=20)
    voterid = models.CharField(max_length=20)
    email = models.CharField(max_length=20,default="abc22")
    mobile = models.CharField(max_length=20)
    username= models.CharField(max_length=20)
    password= models.CharField(max_length=20)
    #confirmpassword=models.CharField(max_length=20, default="confirm")
    status = models.CharField(max_length=20, default="pending")
    secret_password=models.CharField(max_length=20, default="pending")




class voter_adhar(models.Model):
    voterregisterid=models.ForeignKey(voterregister,on_delete=models.CASCADE)
    adhar=models.FileField()


class voter_idcopy(models.Model):
    voterregisterid=models.ForeignKey(voterregister, on_delete=models.CASCADE)
    voteridcopy=models.FileField()


class voter_photo(models.Model):
    voterregisterid = models.ForeignKey(voterregister, on_delete=models.CASCADE)
    photo = models.FileField()

class voter_share(models.Model):
    voterregisterid = models.ForeignKey(voterregister, on_delete=models.CASCADE)
    upload_share=models.FileField(default="pending")

class voter_check(models.Model) :
    voterregisterid = models.ForeignKey(voterregister, on_delete=models.CASCADE)
    
    

class vote_count(models.Model) :
    #voterregisterid = models.ForeignKey(voterregister, on_delete=models.CASCADE)
    candidateregisterid = models.ForeignKey(candidateregister, on_delete=models.CASCADE)
    count= models.CharField(max_length=20,default=0)
    voting_time = models.TimeField()





