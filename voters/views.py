from django.shortcuts import render
from voters.models import *
from siteadmin.models import *
from candidates.models import *


from django.http import JsonResponse
import PIL
from PIL import Image
import datetime


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Create your views here.
def vregister(request):
    ef = state.objects.all()
    gh = district.objects.all()
    ob=landmark.objects.all()
    ab= assembly.objects.all()

    return render(request,"voterregister.html",{'landmark':ob,'assembly':ab,'state':ef,'district':gh})



def voterregisteraction(request):
    obstate = state.objects.get(id=request.POST['state'])
    obdistrict = district.objects.get(id=request.POST['district'])
    oblandmark=landmark.objects.get(id=request.POST['location'])
    obassembly=assembly.objects.get(id=request.POST['assembly'])
    obe = voterregister.objects.filter(email=request.POST['email'])
    if (obe.count() > 0):
        ef = state.objects.all()
        gh = district.objects.all()
        ob=landmark.objects.all()
        ab= assembly.objects.all()

        return render(request,"voterregister.html",{'landmark':ob,'assembly':ab,'state':ef,'district':gh,'msg3': "email already registered "})
        
    else:
        age=0
        dob=request.POST['dob']
        print(dob)
        #datetime_object = datetime.datetime.strptime(dob, '%d/%m/%Y')
        #print(datetime_object)
        #user_dob=str(datetime_object)
        if '-' in dob:
            print('-')
            dob_ar=dob.split('-')
            yr=int(dob_ar[0])
        if '/' in dob:
            print('/')
            dob_ar = dob.split('/')
            yr =int(dob_ar[2])
        current_yr=datetime.date.today().strftime("%Y")
        c_yr=int(current_yr)
        age=c_yr-yr
        print("age is",age)
        if age>=18:
            ob=voterregister(firstname=request.POST['fname'],lastname=request.POST['lname'],address=request.POST['address'],gender=request.POST['gender'],
                     dateofbirth=request.POST['dob'],adharno=request.POST['adharno'],voterid=request.POST['voterid'],email=request.POST['email'],
                     mobile=request.POST['mobile'],state=obstate,district=obdistrict,location=oblandmark,assembly=obassembly,username=request.POST['uname'],
                     password=request.POST['pswd'])

            ob.save()

            if len(request.FILES)!=0:
                obvoter=voterregister.objects.get(username=request.POST['uname'])
                ab=voter_adhar(voterregisterid=obvoter,adhar=request.FILES['adharcopy'])
                ab.save()
                cd = voter_idcopy(voterregisterid=obvoter,voteridcopy=request.FILES['voteridcopy'])
                cd.save()
                ef = voter_photo(voterregisterid=obvoter,photo=request.FILES['photo'])
                ef.save()
                ef = state.objects.all()
                gh = district.objects.all()
                ob=landmark.objects.all()
                ab= assembly.objects.all()

                return render(request,"voterregister.html",{'landmark':ob,'assembly':ab,'state':ef,'district':gh,'msg1': "Registration completed successfully "})
        

                
        else:
            ef = state.objects.all()
            gh = district.objects.all()
            ob=landmark.objects.all()
            ab= assembly.objects.all()

            return render(request,"voterregister.html",{'landmark':ob,'assembly':ab,'state':ef,'district':gh,'msg2': "Age is Invalid "})
        
            
            


def checkUsernameAction(request):

    data={}
    obadmin=login.objects.filter(username=request.GET.get('username')).exists()
    obCandidate = candidateregister.objects.filter(username=request.GET.get('username')).exists()

    ob=voterregister.objects.filter(username=request.GET.get('username')).exists()
    if(ob or obadmin or obCandidate ):
        data['k1']="exists"
    else:
        data['k1'] = "valid"
    return  JsonResponse(data)


##def vote(request):
##    ob = voterregister.objects.filter(id=request.session['id'])
##    if (ob.count() > 0):
##        assembly=ob[0].assembly_id
##        ob=candidateregister.objects.filter(assemblyname=assembly)
##        return render(request, "voter/vote.html",{'data':ob})

def view_regassembly_candidates_forVote(request):
    ob = voterregister.objects.filter(id=request.session['id'])
    assemblyID=ob[0].assembly_id
    obassembly = assembly.objects.get(id=assemblyID)
    obcheckAssembly=election_announcement.objects.filter(assembly=obassembly)
    if(obcheckAssembly.count()>0):
                election_date=obcheckAssembly[0].electiondate
                election_date_format =datetime.datetime.strptime(election_date, '%Y-%m-%d').date()
                print('1. election_date_format',election_date_format)
                #election_date_format =str(datetime.datetime.strptime(election_date, '%Y-%m-%d'))
                #print('election_date_format',election_date_format)
                #election_date_ar=election_date_format.split(' ')
                #election_day=election_date_ar[0]
                #election_day_format = datetime.datetime.strptime(election_day, '%Y-%m-%d')
                current_date=datetime.date.today()
                #print('election_day_format',election_day_format)
                print('current_date',current_date)
                if(election_date_format==current_date):
                        print("YES")
                        #ob = voterregister.objects.filter(id=request.session['id'])
                        #if (ob.count() > 0):
                        #assembly=ob[0].assembly_id
                        print("assemblyID",assemblyID)
                        ob=photo.objects.filter(candidateregisterid__in=candidateregister.objects.filter(assemblyname=assemblyID,status='approved'))
                        return render(request, "voter/view_assembly_candidates.html",{'data':ob})
                else:
                    print("else")
                    return render(request, "voter/view_assembly_candidates.html")
    else:
        print("No aannounc")
        return render(request, "voter/view_assembly_candidates.html")
                    



def processingVisualCrypto(request,candidate_id):
    
    
    from datetime import datetime, time
    begin_time=time(7,00)
    print('begin_time',begin_time)

    end_time=time(23,00)
    print('end_time',end_time)

    current_time= datetime.now().time()
    print("check_time",current_time)
    if begin_time < end_time:
        

        if current_time >= begin_time and current_time <= end_time:
            print('checking whether already done...')
            obVoterID= voterregister.objects.get(id=request.session['id'])
            obvoter_check=voter_check.objects.filter(voterregisterid=obVoterID)
            if(obvoter_check.count()>0):
                ob = voterregister.objects.filter(id=request.session['id'])
                if (ob.count() > 0):
                    assembly=ob[0].assembly_id
                    ob=photo.objects.filter(candidateregisterid__in=candidateregister.objects.filter(assemblyname=assembly))
                    return render(request, "voter/view_assembly_candidates.html",{'data':ob,'msg':'done'})
        
            else:
                
        
        
        
                #Send Mail Here..
                path="D:\\shaharbana\\Complete_Works\\voting\\crypto_password\\vshare1_"+str(request.session['id'])+".jpg"

                fromaddr = "shaharbana997@gmail.com"
               # toaddr = "shaharbanaaze@gmail.com"
                toaddr = obVoterID.email
                print('toMailid',obVoterID.email,"path",path)
                try:


             # code here
                 #instance of MIMEMultipart
                    msg = MIMEMultipart()
                    print("asd")
##                # storing the senders email address
                    msg['From'] = "shaharbana997@gmail.com"
##
##                # storing the receivers email address
                    msg['To'] = toaddr
##
##                # storing the subject
                    msg['Subject'] = "image share"
##
##                # string to store the body of the mail
                    body = "use for vote"
##
##                # attach the body with the msg instance
                    msg.attach(MIMEText(body, 'plain'))
##
##                # open the file to be sent
                    filename = "vshare1_"+str(request.session['id'])+".jpg"
                    attachment = open(path, "rb")
##
##                # instance of MIMEBase and named as p
                    p = MIMEBase('application', 'octet-stream')
##
##                # To change the payload into encoded form
                    p.set_payload((attachment).read())
##
##                # encode into base64
                    encoders.encode_base64(p)
##
                    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
##
##                # attach the instance 'p' to instance 'msg'
                    msg.attach(p)
##
##                # creates SMTP session
                    s = smtplib.SMTP('smtp.gmail.com', 587)
##
##                # start TLS for security
                    s.starttls()
                    
##                # Authentication
    
                    s.login("shaharbana997@gmail.com","mariyam123")
##
##                # Converts the Multipart msg into a string
                    text = msg.as_string()
##
##                # sending the mail
                    s.sendmail("shaharbana997@gmail.com",  toaddr, text)
##
##                # terminating the session
                    s.quit()
                except Exception as e:
                    print(e)
                    ob=voterregister.objects.filter(id=request.session['id'])
                    if(ob.count()>0):
                        assembly=ob[0].assembly_id

                        ob=photo.objects.filter(candidateregisterid__in=candidateregister.objects.filter(assemblyname=assembly))
                        return render(request, "voter/view_assembly_candidates.html",{'data':ob,'msg':'Network_Error'})
                ob=photo.objects.filter(id=candidate_id)
                return render(request, "voter/processingvisualcrypto.html",{'data':ob})
    
        else:
                ob = voterregister.objects.filter(id=request.session['id'])
                if (ob.count() > 0):
                    assembly=ob[0].assembly_id
                    ob=photo.objects.filter(candidateregisterid__in=candidateregister.objects.filter(assemblyname=assembly))
                    return render(request, "voter/view_assembly_candidates.html",{'data':ob,'msg':'exceeded'})
                
                
        #ob=photo.objects.filter(candidateregisterid=candidate_id)
        


def processingVisualCryptoAction(request):
    #generating password using share
    import os
    try:
        msg=''
        if(len(request.FILES['upload_share'])>0):
        
            obVoterID= voterregister.objects.get(id=request.session['id'])
            obQuerySet=voter_share.objects.filter(voterregisterid=obVoterID)
            if(obQuerySet.count()>0):
                obQuerySet=voter_share.objects.filter(voterregisterid=obVoterID).delete()

                #if os.path.exists("media/"+request.FILES['upload_share']):
                    #os.remove("media/"+request.FILES['upload_share'])
                #obQuerySet=voter_share(voterregisterid=obVoterID,upload_share=request.FILES['upload_share'])
                #obQuerySet.save()
                
            
            else:
                obQuerySet=voter_share(voterregisterid=obVoterID,upload_share=request.FILES['upload_share'])
                obQuerySet.save()
                    
            myshare=str(request.FILES['upload_share'])
            print("share",myshare)
            share1=myshare
            print("share1",share1)
            print("sess",str(request.session['id']))
            if myshare=="vshare1_"+str(request.session['id'])+".jpg":
                
                #if os.path.exists("crypto_password/"+myshare):
                if os.path.exists("crypto_password/vshare1_"+str(request.session['id'])+".jpg"):
                    print("yes file exists")
            
                    #share_path1="media/"+myshare
                    share_path1="media/vshare1_"+str(request.session['id'])+".jpg" 
                    print(share_path1)
                    share_path2="crypto_password/vshare2_"+str(request.session['id'])+".jpg"       
                    infile1 = Image.open(share_path1)
                    infile2 = Image.open(share_path2)
        

                    pathnew="crypto_password/vsharenew_"+str(request.session['id'])+".jpg"
                    infilenew = Image.open(pathnew)
                    print(infile1)
                    print(infile2)
                    print(infilenew)
                    outfile = Image.new('CMYK', infile1.size)

                    for x in range(0,infile1.size[0],2):
                        for y in range(0,infile1.size[1],2):
                            C = infile1.getpixel((x+1, y))[0]
                            M = infile2.getpixel((x+1, y))[1]
                            Y = infilenew.getpixel((x+1, y))[2]


                            outfile.putpixel((x, y), (C,M,Y,0))
                            outfile.putpixel((x+1, y), (C,M,Y,0))
                            outfile.putpixel((x, y+1), (C,M,Y,0))
                            outfile.putpixel((x+1, y+1), (C,M,Y,0))

                    final_path="media/final_"+str(request.session['id'])+".jpg"      
                    outfile.save("./media/final.jpg")
                    finalpath="final.jpg"
                    candidatephoto_id=request.POST['hdn_candidatephoto_id']
                    obCandidate=photo.objects.filter(id=candidatephoto_id)
        
        
                    #obj=VoterShareImage.objects.filter(userid=request.session['id']).update(share='final.jpg')
                    #obj=VoterShareImage.objects.filter(userid=request.session['id'])
                    return render(request,'voter/decryption.html',{'path':finalpath,'candidate':obCandidate})
                else:
                
                    print("no file dsnt exists")
            else:
                print("Invalid File Name")
                #ob = voterregister.objects.filter(id=request.session['id'])
                #if (ob.count() > 0):
                    #assembly=ob[0].assembly_id
                    #ob=photo.objects.filter(candidateregisterid__in=candidateregister.objects.filter(assemblyname=assembly))
                    #return render(request, "voter/view_assembly_candidates.html",{'data':ob,'msg':'invalid'})
                candidatephoto_id=request.POST['hdn_candidatephoto_id']
                ob=photo.objects.filter(id=candidatephoto_id)
                return render(request,"voter/processingvisualcrypto.html",{'data':ob,'msg':'invalid_file'})
                

        else:
            msg='upload'
        
        
    
    

        ob = voterregister.objects.filter(id=request.session['id'])
        if (ob.count() > 0):
            assembly=ob[0].assembly_id
            ob=candidateregister.objects.filter(assemblyname=assembly)
            return render(request, "voter/view_assembly_candidates.html",{'data':ob})
    except:
        ob = voterregister.objects.filter(id=request.session['id'])
        if (ob.count() > 0):
            assembly=ob[0].assembly_id
            ob=photo.objects.filter(candidateregisterid__in=candidateregister.objects.filter(assemblyname=assembly))
            return render(request, "voter/view_assembly_candidates.html",{'data':ob,'msg':'invalid'})
        
    
def decryptionAction(request):
    voting_count=1
    candidate_id=request.POST['hdn_candidate_id']
    obCandidateID=candidateregister.objects.get(id=candidate_id)
    obVoterID= voterregister.objects.filter(id=request.session['id'])
    if(obVoterID.count()>0):
        secret_password=obVoterID[0].secret_password
        if(secret_password==request.POST['txtpswd']):
            
            
            obVoterID= voterregister.objects.get(id=request.session['id'])
            
            
            
            
           
                
            
            
            obvoter_check=voter_check(voterregisterid=obVoterID)
            obvoter_check.save()
            obvote=vote_count.objects.filter(candidateregisterid=obCandidateID)
            if(obvote.count()>0):
                voting_count=int(obvote[0].count)
                voting_count+=1
                obvote=vote_count.objects.filter(candidateregisterid=obCandidateID).update(count=voting_count)
                obCandidatevote=candidateregister.objects.filter(id=obCandidateID.id).update(count_vote=voting_count)
                
            else:
                obvote=vote_count(candidateregisterid=obCandidateID,voting_time=datetime.datetime.now(),count=voting_count)
                obvote.save()
                obCandidatevote=candidateregister.objects.filter(id=obCandidateID.id).update(count_vote=voting_count)
                
                
            ## Test case when range crosses midnight
            #(time(22,0), time(4,00))#10:00 PM and 4:00 AM
            
            #return render(request, "voter/success.html")
            ob = voterregister.objects.filter(id=request.session['id'])
            if (ob.count() > 0):
                assembly=ob[0].assembly_id
                ob=photo.objects.filter(candidateregisterid__in=candidateregister.objects.filter(assemblyname=assembly))
                return render(request, "voter/view_assembly_candidates.html",{'data':ob,'msg':'success'})
            
            
            
        else:
           
            ob=photo.objects.filter(candidateregisterid=obCandidateID)    
            return render(request, "voter/processingVisualCrypto.html",{'data':ob,'msg':'invalid'})
            
            
            
            
    













   
def voter_change_password(request):
    return render(request, "voter/voter_change_password.html")

def voter_change_password_action(request):
    ob = voterregister.objects.filter(id=request.session['id'], password=request.POST['currentpswd'])
    if (ob.count() > 0):
        if (request.POST['newpswd'] == request.POST['confirmpswd']):
            ob = voterregister.objects.filter(id=request.session['id']).update(password=request.POST['newpswd'])
            return render(request, "voter/voter_change_password.html", {'msg': 'passwrod changed'})

        else:
            return render(request, "voter/voter_change_password.html", {'msg': 'Passwod Mismatch'})
    else:
        return render(request, "voter/voter_change_password.html", {'msg': 'Invalid User'})


def voter_edit_profile(request):
    ob = voterregister.objects.filter(id=request.session['id'])
    if (ob.count() > 0):
        request.session['id'] = ob[0].id
        #symbol_id = ob[0].symbol

    return render(request, "voter/edit_profile.html",{'voterregister':ob})

def voter_updateaction(request):
    ob = voterregister.objects.filter(id=request.session['id']).update(firstname=request.POST['fname'],lastname=request.POST['lname'],address=request.POST['address'], gender=request.POST['gender'], dateofbirth=request.POST['dob'],email=request.POST['email'],mobile=request.POST['mobile'])
    ob = voterregister.objects.filter(id=request.session['id'])
    if (ob.count() > 0):
        request.session['id'] = ob[0].id
        #symbol_id = ob[0].symbol

    return render(request, "voter/edit_profile.html", {'voterregister':ob,'msg': "Updated Successfully"})

def view_regassembly_candidate_forWork(request):
    ob = voterregister.objects.filter(id=request.session['id'])
    if (ob.count() > 0):
        assembly = ob[0].assembly_id
        ob = candidateregister.objects.filter(assemblyname=assembly,status='approved')
        return render(request, "voter/view_regassembly_candidate.html", {'data': ob})

def assembly_candidate_details(request,uid):
    ob=candidateregister.objects.filter(id=uid)
    ef=addprofile.objects.filter(username=ob[0].username)
    return render(request, "voter/candidate_work.html", {'data': ef})


def view_velectiondetails(request):
    ob = voterregister.objects.filter(id=request.session['id'])
    if (ob.count() > 0):
        assembly = ob[0].assembly_id
        ob = election_announcement.objects.filter(assembly=assembly)
        return render(request, "voter/election_details.html", {'data': ob})






##def view_result(request):
##   
##    obCandidate=result_tb.objects.all()
## 
##    return render(request, "voter/view_result_candidates.html",{'data':obCandidate})
def view_resultant_ForVoter(request):
    state_details = state.objects.all()    
    return render(request, "voter/view_state_dis_assembly_for_resultDisplay.html",{'state':state_details})
    
    
def view_resultant_ForVoterAction(request):
    #obAssembly=assembly.objects.get(id=3)
    #obCandidate=photo.objects.filter(candidateregisterid__in=result_tb.objects.filter(assembly=obAssembly))#
    msg = ""
    ResultList=[]
    obCandidateResult=result_tb.objects.filter(assembly=request.POST['ddlassembly'])
    for res in obCandidateResult:
        print('Resultlist',res.candidateregisterid_id)
        ResultList.append(res.candidateregisterid_id)
        
        
    obRemaining=candidateregister.objects.filter(assemblyname=request.POST['ddlassembly']).exclude(id__in=ResultList)

    if len(ResultList) > 1:
        msg = "tie_up"
    obCandidateResult=result_tb.objects.filter(assembly=request.POST['ddlassembly'])
    if(obCandidateResult.count()>0):
        return render(request, "voter/view_result_candidates_forDisplay.html",{'data':obCandidateResult,'rem':obRemaining,'msg': msg})
    else:
        return render(request, "voter/view_result_candidates_forDisplay.html")
        










