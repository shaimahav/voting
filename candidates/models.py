from django.db import models
from siteadmin.models import *

# Create your models here.

class candidateregister(models.Model):
    firstname= models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    dateofbirth= models.CharField(max_length=20)
    adharno= models.CharField(max_length=20)
    voterid = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    partyid = models.ForeignKey(party, on_delete=models.CASCADE)
    symbol= models.ForeignKey(symbol, on_delete=models.CASCADE)
    stateid = models.ForeignKey(state, on_delete=models.CASCADE)
    district = models.ForeignKey(district, on_delete=models.CASCADE)
    assemblyname= models.ForeignKey(assembly, on_delete=models.CASCADE)

    place = models.ForeignKey(landmark, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    status = models.CharField(max_length=20,default='pending')
    count_vote = models.CharField(max_length=20,default='0')

class adhar(models.Model):
        candidateregisterid = models.ForeignKey(candidateregister, on_delete=models.CASCADE)
        adhar = models.FileField()

class voteridcopy(models.Model):
        candidateregisterid = models.ForeignKey(candidateregister, on_delete=models.CASCADE)
        voteridcopy = models.FileField()

class photo(models.Model):
        candidateregisterid = models.ForeignKey(candidateregister, on_delete=models.CASCADE)
        photo = models.FileField()


class proposertb(models.Model):
    pname1=models.CharField(max_length=20)
    voterid1 = models.CharField(max_length=20)
    pname2 = models.CharField(max_length=20)
    voterid2 = models.CharField(max_length=20)
    username=models.CharField(max_length=20,default='abc')

class addprofile(models.Model):
    username = models.CharField(max_length=20, default='abc')
    qualification = models.CharField(max_length=20)
    work1 = models.CharField(max_length=20)
    work1photo= models.FileField()
    work2 = models.CharField(max_length=20)
    work2photo = models.FileField()
    work3 = models.CharField(max_length=20)
    work3photo = models.FileField()
    achievements= models.CharField(max_length=20)

class withdraw_candidate(models.Model):
    c_id = models.ForeignKey(candidateregister, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20)

class result_tb(models.Model):
    candidateregisterid = models.ForeignKey(candidateregister, on_delete=models.CASCADE)
    assembly= models.ForeignKey(assembly, on_delete=models.CASCADE)
    vote_count=models.CharField(max_length=20)

    
    
