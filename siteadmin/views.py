from django.shortcuts import render
from siteadmin.models import *
from voters.models import  *
from candidates.models import  *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import string


# Create your views here.
def index(request):
    return render(request,"index.html")

def loginView(request):
    return render(request,"login.html")

def loginaction(request):
    ob=login.objects.filter(username=request.POST['uname'],password=request.POST['pname'])
    if(ob.count()>0):
        request.session['id']=ob[0].id
        return render(request,"admin/adminhome.html")
    else:
        ob =voterregister.objects.filter(username=request.POST['uname'], password=request.POST['pname'],status='approved')
        if (ob.count() > 0):
            request.session['id'] = ob[0].id
            return render(request, "voter/voterhome.html")
        else:
            ob=candidateregister.objects.filter(username=request.POST['uname'], password=request.POST['pname'],status='approved')
            if(ob.count()>0):
                request.session['id'] = ob[0].id
                symbol_id=ob[0].symbol

                return render(request, "candidate/candidatehome.html",{'symbol':symbol_id.symbol,'candidateregister':ob})
            else:
                return render(request, "login.html", {'msg': 'Invalid.....'})


def addstate(request):
        return render(request, "admin/state.html")


def stateaddaction(request):
    ob=state.objects.filter(state=request.POST['state'])
    if(ob.count()>0):
        return render(request,"admin/state.html",{'msg':"State already exist"})
    else:
        ob=state(state=request.POST['state'])
        ob.save()
        return render(request,"admin/state.html",{'msg': "Added Successfully"})


def adddistrict(request):
    ob=state.objects.all()
    return render(request, "admin/district.html",{'data':ob})



def districtaddaction(request):
    obstate=state.objects.get(id=request.POST['state'])
    ob=district.objects.filter(stateid=obstate,district=request.POST['district'])
    if (ob.count() > 0):
        return render(request,"admin/district.html",{'msg':"District already exist"})
    else:
        obstate=state.objects.get(id=request.POST['state'])
        ob=district(stateid=obstate,district=request.POST['district'])
        ob.save()
    ob = state.objects.all()
    return render(request,"admin/district.html",{'data':ob,'msg': "Added Successfully"})

def addlandmark(request):
        ob=district.objects.all()
        return render(request, "admin/addlandmark.html",{'data':ob})

def landmarkaddaction(request):
    obdistrict=district.objects.get(id=request.POST['district'])
    ob=landmark.objects.filter(districtid=obdistrict,place=request.POST['landmark'])
    if(ob.count()>0):
        return render(request,"admin/addlandmark.html",{'msg':"LandMark already exist"})
    else:
        obdistrict=district.objects.get(id=request.POST['district'])
        ob =landmark(districtid=obdistrict,place=request.POST['landmark'])
        ob.save()
    ob = district.objects.all()
    return render(request,"admin/addlandmark.html",{'data':ob,'msg': "Added Successfully"})

def addparty(request):
    return render(request, "admin/addparty.html")

def partyaddaction(request):
    ob = party.objects.filter(partyname=request.POST['addparty'])
    if(ob.count() > 0):
            return render(request, "admin/addparty.html", {'msg': "party already exist"})
    else:
            ob = party(partyname=request.POST['addparty'])
            ob.save()
            return render(request, "admin/addparty.html",{'msg': "Added Successfully"})

def addassembly(request):
        ob = landmark.objects.all()
        return render(request, "admin/addassembly.html", {'data': ob})

def assemblyaddaction(request):
    oblandmark= landmark.objects.get(id=request.POST['landmark'])
    ob = assembly.objects.filter(landmarkid=oblandmark, assemblyname=request.POST['assembly'])
    if (ob.count() > 0):
        return render(request, "admin/addassembly.html", {'msg': "Assembly already exist"})
    else:
        oblandmark = landmark.objects.get(id=request.POST['landmark'])
        ob = assembly(landmarkid=oblandmark, assemblyname=request.POST['assembly'])
        ob.save()
    ob = landmark.objects.all()
    return render(request, "admin/addassembly.html", {'data': ob,'msg': "Added Successfully"})

def addsymbol(request):
        ob = party.objects.all()
        return render(request, "admin/addsymbol.html", {'data': ob})

def symboladdaction(request):
    if len(request.FILES) != 0:
        obparty= party.objects.get(id=request.POST['party'])
    ob = symbol.objects.filter(partyid=obparty,symbol=request.FILES['symbol'],symbolname=request.POST['symbolname'])

    if (ob.count() > 0):
        return render(request, "admin/addsymbol.html", {'msg': "Symbol already exist"})
    else:
        obparty = party.objects.get(id=request.POST['party'])
        ob = symbol(partyid=obparty, symbol=request.FILES['symbol'],symbolname=request.POST['symbolname'])
        ob.save()
    ob = party.objects.all()
    return render(request, "admin/addsymbol.html", {'data': ob,'msg': "Added Successfully"})

########################################################################################################################################################

def view_regvoters(request):
    ob=voterregister.objects.filter(status='pending')
    ef = state.objects.all()
    gh = district.objects.all()
    ij = landmark.objects.all()
    kl = assembly.objects.all()
    return render(request,"admin/viewvoters.html", {'data':ob,'state':ef,'district':gh,'landmark':ij,'assembly':kl})

def details(request,uid):
    ob = voterregister.objects.get(id=uid)

    ef=voter_adhar.objects.filter(voterregisterid=ob)
    #ob = voterregister.objects.filter(id=uid)

    gh=voter_idcopy.objects.filter(voterregisterid=ob)
    #ob = voterregister.objects.filter(id=uid)

    ij=voter_photo.objects.filter(voterregisterid=ob)
    #ob = voterregister.objects.filter(id=uid)
    return render(request, "admin/details.html",{'adhar':ef ,'voterid':gh ,'photo':ij,'voterregid':ob.id})

def manageUseraction(request):
##    if 'approve' in request.POST:
##        voterregister.objects.filter(id=request.POST['hdnid']).update(status='approved')
##    else:
##        voterregister.objects.filter(id=request.POST['hdnid']).update(status='rejected')
##
##
##    ob = voterregister.objects.filter(status='pending')
##    return render(request, "admin/viewvoters.html", {'data': ob})
    if 'approve' in request.POST:
        #voterregister.objects.filter(id=request.POST['hdnid']).update(status='approved')
        #create random password for cryptography        

        font = ImageFont.truetype("D:\shaharbana\BRITANIC.ttf",25)
        img=Image.new("RGBA", (200,200),(0,0,0))
        draw = ImageDraw.Draw(img)
        #password=''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        password=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        print(password)
        draw.text((0, 0),password,(255,255,255),font=font)
        draw = ImageDraw.Draw(img)
        #draw = ImageDraw.Draw(img)
        file="crypto_password/generate_"+request.POST['hdnid']+".png"
        img.save(file)
        
        obVoterID= voterregister.objects.filter(id=request.POST['hdnid']).update(secret_password=password)
        
        #Creating Share
        #-------------CMY_Decomposition----------------------#
        #image = Image.open("color_image.jpg")
        
        image = Image.open("./crypto_password/generate_"+request.POST['hdnid']+".png")
        #image = Image.open("generate_3.png")
        color_image = image.convert('CMYK')
        bw_image = image.convert('1')
        outfile1 = Image.new("CMYK", [dimension for dimension in image.size])

        outfile2 = Image.new("CMYK", [dimension for dimension in image.size])

        outfilenew = Image.new("CMYK", [dimension for dimension in image.size])



        for x in range(0, image.size[0], 1):
            
            for y in range(0, image.size[1], 1):
                sourcepixel = image.getpixel((x, y))
                outfile1.putpixel((x, y),(sourcepixel[0],0,0,0))
                outfile2.putpixel((x, y),(0,sourcepixel[1],0,0))
                outfilenew.putpixel((x, y),(0,0,sourcepixel[2],0))

        file_1="crypto_password/out1_"+request.POST['hdnid']+".jpg"
        #file_1="out1.jpg"
        outfile1.save(file_1)
        file_2="crypto_password/out2_"+request.POST['hdnid']+".jpg"
        #file_2="out2.jpg"
        outfile2.save(file_2)
        #-------completed two shares---------------#
        
        file_new="crypto_password/outnew_"+request.POST['hdnid']+".jpg"
        #file_new="out3.jpg"
        outfilenew.save(file_new)
        #-------------------------End of CMY_Decomposition--------------------#
        
        #------------------------halftone-------------------------------------#
        image1 = Image.open(file_1)
        image2 = Image.open(file_2)

        
        imagenew = Image.open(file_new)

        image1 = image1.convert('1')
        image2 = image2.convert('1')
        
        imagenew = imagenew.convert('1')

        hf1 = Image.new("CMYK", [dimension for dimension in image1.size])
        hf2 = Image.new("CMYK", [dimension for dimension in image1.size])
        hfnew = Image.new("CMYK", [dimension for dimension in image1.size])

        for x in range(0, image1.size[0]):            
            for y in range(0, image1.size[1]):
                pixel_color1 = image1.getpixel((x, y))
                pixel_color2 = image2.getpixel((x, y))
                pixel_color3 = imagenew.getpixel((x, y))
                if pixel_color1 == 255:
                    hf1.putpixel((x, y),(255,0,0,0))
                else:
                    hf1.putpixel((x, y),(0,0,0,0))

                if pixel_color2 == 255:
                    hf2.putpixel((x, y),(0,255,0,0))
                else:
                    hf2.putpixel((x, y),(0,0,0,0))

                if pixel_color3 == 255:
                    hfnew.putpixel((x, y),(0,0,255,0))
                else:
                    hfnew.putpixel((x, y),(0,0,0,0))


        hf_file_1="crypto_password/hf1_"+request.POST['hdnid']+".jpg"
        #hf_file_1="hf1.jpg"
        hf1.save(hf_file_1)
        hf_file_2="crypto_password/hf2_"+request.POST['hdnid']+".jpg"
        #hf_file_2="hf2.jpg"
        hf2.save(hf_file_2)

        hf_file_new="crypto_password/hfnew_"+request.POST['hdnid']+".jpg"
        #hf_file_new="hf3.jpg"
        hfnew.save(hf_file_new)
        #--------------------------------end of halftone-------------------#

        #------------------------main processing---------------------------#
        
        image1 = Image.open(hf_file_1)
        image1 = image1.convert('CMYK')

        image2 = Image.open(hf_file_2)
        image2 = image2.convert('CMYK')

        imagenew = Image.open(hf_file_new)
        imagenew = imagenew.convert('CMYK')


        share1 = Image.new("CMYK", [dimension * 2 for dimension in image1.size])

        share2 = Image.new("CMYK", [dimension * 2 for dimension in image2.size])

        sharenew = Image.new("CMYK", [dimension * 2 for dimension in imagenew.size])

        for x in range(0, image1.size[0]):
            for y in range(0, image1.size[1]):
                pixelcolor = image1.getpixel((x, y))
                

                if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
                    share1.putpixel((x * 2, y * 2), (255,0,0,0))
                    share1.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
                    share1.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
                    share1.putpixel((x * 2 + 1, y * 2 + 1), (255,0,0,0))

                else:
                    print("work-------------------------")
                    share1.putpixel((x * 2, y * 2), (0,0,0,0))
                    share1.putpixel((x * 2 + 1, y * 2), (255,0,0,0))
                    share1.putpixel((x * 2, y * 2 + 1), (255,0,0,0))
                    share1.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

                pixelcolor = image2.getpixel((x, y))

                if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
                    share2.putpixel((x * 2, y * 2), (0,255,0,0))
                    share2.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
                    share2.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
                    share2.putpixel((x * 2 + 1, y * 2 + 1), (0,255,0,0))

                else:
                    share2.putpixel((x * 2, y * 2), (0,0,0,0))
                    share2.putpixel((x * 2 + 1, y * 2), (0,255,0,0))
                    share2.putpixel((x * 2, y * 2 + 1), (0,255,0,0))
                    share2.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))

                pixelcolor = imagenew.getpixel((x, y))

                if pixelcolor[0]+pixelcolor[1]+pixelcolor[2] == 0:
                    sharenew.putpixel((x * 2, y * 2), (0,0,255,0))
                    sharenew.putpixel((x * 2 + 1, y * 2), (0,0,0,0))
                    sharenew.putpixel((x * 2, y * 2 + 1), (0,0,0,0))
                    sharenew.putpixel((x * 2 + 1, y * 2 + 1), (0,0,255,0))

                else:
                    sharenew.putpixel((x * 2, y * 2), (0,0,0,0))
                    sharenew.putpixel((x * 2 + 1, y * 2), (0,0,255,0))
                    sharenew.putpixel((x * 2, y * 2 + 1), (0,0,255,0))
                    sharenew.putpixel((x * 2 + 1, y * 2 + 1), (0,0,0,0))


        share_path1="crypto_password/vshare1_"+request.POST['hdnid']+".jpg"
        share1.save(share_path1)
        share_path2="crypto_password/vshare2_"+request.POST['hdnid']+".jpg"
        share2.save(share_path2)
        #----------completed share generation---------------------------#
        
        pathnew="crypto_password/vsharenew_"+request.POST['hdnid']+".jpg"
        sharenew.save(pathnew)


        

        voterregister.objects.filter(id=request.POST['hdnid']).update(status='approved')
    else:
        voterregister.objects.filter(id=request.POST['hdnid']).update(status='rejected')


    ob = voterregister.objects.filter(status='pending')
    return render(request, "admin/viewvoters.html", {'data': ob})


def view_approvedvoters(request):
    ob=voterregister.objects.filter(status='approved')
    ef = state.objects.all()
    gh = district.objects.all()
    ij = landmark.objects.all()
    kl = assembly.objects.all()
    return render(request,"admin/viewapprovedvoters.html", {'data':ob,'state':ef,'district':gh,'landmark':ij,'assembly':kl})

def view_rejectedvoters(request):
    ob=voterregister.objects.filter(status='rejected')
    ef = state.objects.all()
    gh = district.objects.all()
    ij = landmark.objects.all()
    kl = assembly.objects.all()
    return render(request,"admin/viewrejectedvoters.html", {'data':ob,'state':ef,'district':gh,'landmark':ij,'assembly':kl})

def view_regcandidates(request):
    ob=candidateregister.objects.filter(status='pending')
    ef = state.objects.all()
    gh = district.objects.all()
    ij = landmark.objects.all()
    kl = assembly.objects.all()

    return render(request,"admin/viewcandidates.html", {'data':ob,'state':ef,'district':gh,'landmark':ij,'assembly':kl})

def candidate_details(request,uid):
    ob = candidateregister.objects.get(id=uid)

    ef=adhar.objects.filter(candidateregisterid=ob)
    #ob = voterregister.objects.filter(id=uid)

    gh=voteridcopy.objects.filter(candidateregisterid=ob)
    #ob = voterregister.objects.filter(id=uid)

    ij=photo.objects.filter(candidateregisterid=ob)
    #kl=symbol.objects.filter(candidateregisterid=ob)
    obcandidate = candidateregister.objects.filter(id=uid)

    username=obcandidate[0].username
    obproposer=proposertb.objects.filter(username=username)
    obwork=addprofile.objects.filter(username=username)
    return render(request, "admin/candidate_details.html",{'adhar':ef ,'voterid':gh ,'photo':ij,'symbol':ob.symbol,'candidateregid':ob.id,'proposertb':obproposer,'addprofile':obwork})


def managecandidateaction(request):
    if 'approve' in request.POST:
        candidateregister.objects.filter(id=request.POST['hdnid']).update(status='approved')
    else:
       candidateregister.objects.filter(id=request.POST['hdnid']).update(status='rejected')


    ob = candidateregister.objects.filter(status='pending')
    return render(request, "admin/viewcandidates.html", {'data':ob})


def view_approvedcandidates(request):
    ob = candidateregister.objects.filter(status='approved')
    ef = state.objects.all()
    gh = district.objects.all()
    ij = landmark.objects.all()
    kl = assembly.objects.all()

    return render(request,"admin/viewapprovedcandidates.html", {'data':ob,'state':ef,'district':gh,'landmark':ij,'assembly':kl})

def view_rejectedcandidates(request):
    ob=candidateregister.objects.filter(status='rejected')
    ef = state.objects.all()
    gh = district.objects.all()
    ij = landmark.objects.all()
    kl = assembly.objects.all()

    return render(request,"admin/viewrejectedcandidates.html", {'data':ob,'state':ef,'district':gh,'landmark':ij,'assembly':kl})

def announce_election(request):
    ef = state.objects.all()
    gh = district.objects.all()
    ij = landmark.objects.all()
    ab = assembly.objects.all()
    return render(request, "admin/election_announcement.html",{'state':ef,'district':gh,'landmark':ij,'assembly':ab})

def election_announcement_action(request):
    obstate = state.objects.get(id=request.POST['state'])
    obdistrict = district.objects.get(id=request.POST['district'])
    oblandmark = landmark.objects.get(id=request.POST['location'])
    obassembly = assembly.objects.get(id=request.POST['assembly'])
    obcheckAssembly=election_announcement.objects.filter(assembly=obassembly)
    if(obcheckAssembly.count()>0):
        obcheckAssembly=election_announcement.objects.filter(assembly=obassembly).delete()
        ob = election_announcement(election_name=request.POST['election_name'],declarationdate=request.POST['declaration_date'],nominationsubmissiondate=request.POST['nomination_submission_date'],nominationwithdrawdate=request.POST['nomination_withdraw_date'],campinestartingdate=request.POST['campine_starting_date'],campineendingdate=request.POST['campine_ending_date'],electiondate=request.POST['election_date'],resultdate=request.POST['result_date'],assembly=obassembly,district=obdistrict,landmark=oblandmark,stateid=obstate)
        ob.save()
        
    else:
        ob = election_announcement(election_name=request.POST['election_name'],declarationdate=request.POST['declaration_date'],nominationsubmissiondate=request.POST['nomination_submission_date'],nominationwithdrawdate=request.POST['nomination_withdraw_date'],campinestartingdate=request.POST['campine_starting_date'],campineendingdate=request.POST['campine_ending_date'],electiondate=request.POST['election_date'],resultdate=request.POST['result_date'],assembly=obassembly,district=obdistrict,landmark=oblandmark,stateid=obstate)
        ob.save()
    return render(request, "admin/election_announcement.html",{'msg': "Added Successfully"})

def view_all_announcedelection(request):
    ob = election_announcement.objects.all()

    return render(request, "admin/announced_election.html", {'data': ob})

def approved_candidate_details(request,uid):
    ob = candidateregister.objects.get(id=uid)
    ef = adhar.objects.filter(candidateregisterid=ob)
    obsymbol = candidateregister.objects.filter(id=uid)

    gh = voteridcopy.objects.filter(candidateregisterid=ob)
    ij = photo.objects.filter(candidateregisterid=ob)
    return render(request, "admin/approved_candidate_details.html", {'adhar': ef, 'symbol':obsymbol,'voterid': gh, 'photo': ij})


def rejected_candidate_details(request,uid):
    ob = candidateregister.objects.get(id=uid)
    ef = adhar.objects.filter(candidateregisterid=ob)
    obsymbol = candidateregister.objects.filter(id=uid)

    gh = voteridcopy.objects.filter(candidateregisterid=ob)
    ij = photo.objects.filter(candidateregisterid=ob)
    return render(request, "admin/rejected_candidate_details.html", {'adhar': ef, 'symbol':obsymbol,'voterid': gh, 'photo': ij})


def approved_voter_details(request,uid):
    ob = voterregister.objects.get(id=uid)
    ef = voter_adhar.objects.filter(voterregisterid=ob)
    gh = voter_idcopy.objects.filter(voterregisterid=ob)
    ij = voter_photo.objects.filter(voterregisterid=ob)
    return render(request, "admin/approved_voter_details.html", {'adhar': ef, 'voterid': gh, 'photo': ij})

def rejected_voter_details(request,uid):
    ob = voterregister.objects.get(id=uid)
    ef = voter_adhar.objects.filter(voterregisterid=ob)
    gh = voter_idcopy.objects.filter(voterregisterid=ob)
    ij = voter_photo.objects.filter(voterregisterid=ob)
    return render(request, "admin/rejected_voter_details.html", {'adhar': ef, 'voterid': gh, 'photo': ij})

def getdata(request):
    obAssembly=assembly.objects.get(id=request.GET.get('assembly_id'))
    ob = candidateregister.objects.filter(assemblyname=obAssembly,status='pending')
    return render(request, "admin/view_assembly_candidates.html", {'data': ob})


def getapproveddata(request):
    obAssembly=assembly.objects.get(id=request.GET.get('assembly_id'))
    ob = candidateregister.objects.filter(assemblyname=obAssembly,status='approved')
    return render(request, "admin/view_assembly_approved_candidates.html", {'data': ob})

def getrejecteddata(request):
    obAssembly=assembly.objects.get(id=request.GET.get('assembly_id'))
    ob = candidateregister.objects.filter(assemblyname=obAssembly,status='rejected')
    return render(request, "admin/view_assembly_rejected_candidates.html", {'data': ob})

def get_voterdata(request):
    obAssembly=assembly.objects.get(id=request.GET.get('assembly_id'))
    ob = voterregister.objects.filter(assembly=obAssembly,status='pending')
    return render(request, "admin/view_assembly_voters.html", {'data': ob})

def get_voter_approveddata(request):
    obAssembly = assembly.objects.get(id=request.GET.get('assembly_id'))
    ob = voterregister.objects.filter(assembly=obAssembly, status='approved')
    return render(request, "admin/view_assembly_approved_voters.html", {'data': ob})

def get_voter_rejecteddata(request):
    obAssembly = assembly.objects.get(id=request.GET.get('assembly_id'))
    ob = voterregister.objects.filter(assembly=obAssembly, status='rejected')
    return render(request, "admin/view_assembly_rejected_voters.html", {'data': ob})

def change_password(request):
    return render(request, "admin/change_password.html")

def change_password_action(request):
    ob=login.objects.filter(id=request.session['id'],password=request.POST['currentpswd'])
    if(ob.count()>0):
        if(request.POST['newpswd']==request.POST['confirmpswd']):
            ob=login.objects.filter(id=request.session['id']).update(password=request.POST['newpswd'])
            return render(request, "admin/change_password.html",{'msg':'Password changed successfully'})

        else:
            return render(request, "admin/change_password.html",{'msg':'Passwod Mismatch'})
    else:
        return render(request, "admin/change_password.html", {'msg': 'Invalid User'})
##not used
def image_share(request):
    return render(request, "admin/image_share.html")


def admin_mail_action(request):

    fromaddr = "amanyaAmmu123@gmail.com"
    toaddr = "amanyaAmmu123@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = "amanyaAmmu123@gmail.com"

    # storing the receivers email address
    msg['To'] = "amanyaAmmu123@gmail.com"

    # storing the subject
    msg['Subject'] = "image share"

    # string to store the body of the mail
    body = "use for vote"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "1527074238048.jpg"
    attachment = open("F:\\.thumbnails\\1527074238048.jpg", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("amanyaAmmu123@gmail.com","amanya@123")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail("amanyaAmmu123@gmail.com", "amanyaAmmu123@gmail.com", text)

    # terminating the session
    s.quit()

    return render(request, "admin/image_share.html")

def view_withdraw_candidates(request):
    ef = state.objects.all()
    gh = district.objects.all()
    ij = landmark.objects.all()
    kl = assembly.objects.all()

    return render(request, "admin/view_withdraw_candidates.html",{ 'state': ef, 'district': gh, 'landmark': ij, 'assembly': kl})

def getwithdrawcandidate(request):
    obAssembly = assembly.objects.get(id=request.GET.get('assembly_id'))
    #ob = candidateregister.objects.filter(assemblyname=obAssembly)
   # ob=withdraw_candidate.objects.all()
    ob=withdraw_candidate.objects.filter(c_id__in=candidateregister.objects.filter(assemblyname=obAssembly,status='withdraw'))
    return render(request, "admin/view_assembly_withdraw_candidates.html", {'data': ob})


def publish_result(request):
##    vote_count=1
##    obCandidate=vote_count.objects.all()
##    if(obCandidate.count()>0):

    state_details = state.objects.all()    
    return render(request, "admin/result_publishing/view_state_dis_assembly_for_result.html",{'state':state_details})
        

def publish_result_candidate(request):
    obAssembly=assembly.objects.get(id=request.GET.get('assembly_id'))
    
    obCandidate=vote_count.objects.filter(candidateregisterid__in= candidateregister.objects.filter(assemblyname=obAssembly,status='approved'))
   # ob = candidateregister.objects.filter(assemblyname=obAssembly,status='approved')
    return render(request, "admin/result_publishing/view_assembly_candidates_for_result.html", {'data': obCandidate,'assembly':request.GET.get('assembly_id')})


def publish_result_action(request):
    import datetime
    print('publish_result_action')
    print('assembly', request.POST['hdn_assembly'])
    obassembly = assembly.objects.get(id=request.POST['hdn_assembly'])
    obcheckAssembly = election_announcement.objects.filter(assembly=obassembly)
    if (obcheckAssembly.count() > 0):
        election_date = obcheckAssembly[0].electiondate
        election_date_format = datetime.datetime.strptime(election_date, '%Y-%m-%d').date()
        print('1. election_date_format', election_date_format)

        result_date = obcheckAssembly[0].resultdate
        result_date_format = datetime.datetime.strptime(result_date, '%Y-%m-%d').date()
        print('result_date_format', result_date_format)

        current_date = datetime.date.today()
        print('current_date', current_date)
        if (result_date_format == current_date):
            print("YES")

            max_count = 0
            maxcandidate_id = 0
            vote_count_id = request.POST.getlist('chk[]')
            print('vote_count_id', vote_count_id)
            for vid in vote_count_id:
                print('id:', vid)
                obVoteCount = vote_count.objects.filter(id=vid)
                votecount = int(obVoteCount[0].count)
                if (votecount > max_count):
                    max_count = votecount
                    maxcandidate_id = obVoteCount[0].candidateregisterid_id

            print("winner:", maxcandidate_id)

            obCandidate = candidateregister.objects.get(id=maxcandidate_id)
            assemblyID = obCandidate.assemblyname_id
            obAssembly = assembly.objects.get(id=assemblyID)

            obVoteCount = vote_count.objects.filter(candidateregisterid=obCandidate)
            # VoteCount Same
            TieUpList = []
            obVoteCountTieUp = vote_count.objects.filter(count=obVoteCount[0].count,
                                                         candidateregisterid__in=candidateregister.objects.filter(
                                                             assemblyname=obAssembly, status='approved'))
            # .exclude(candidateregisterid=obCandidate)
            # print('TCount',obVoteCountTieUp.count())
            if obVoteCountTieUp.count() > 1:

                for candid in obVoteCountTieUp:
                    TieUpList.append(candid.candidateregisterid)
            print("len", len(TieUpList))

            if len(TieUpList) > 0:
                for candid in TieUpList:
                    print("candid", candid.id)
                    obCandidate = candidateregister.objects.get(id=candid.id)

                    obResult = result_tb(candidateregisterid=obCandidate, assembly=obAssembly,
                                         vote_count=obVoteCount[0].count)
                    obResult.save()
                    obCandidateUpdate = candidateregister.objects.filter(id=candid.id).update(
                        count_vote=obVoteCount[0].count)
                obCandidatePhoto = photo.objects.filter(candidateregisterid__in=TieUpList)
                return render(request, "admin/result_publishing/view_result_candidates.html",
                              {'data': obCandidatePhoto, 'msg': 'tie_up'})






            else:
                obCheckExists = result_tb.objects.filter(assembly=obAssembly)
                if (obCheckExists.count() > 0):
                    ##                              state_details = state.objects.all()
                    ##                              return render(request, "admin/result_publishing/view_state_dis_assembly_for_result.html",{'state':state_details,'msg':'published'})
                    obCandidatePhoto = photo.objects.filter(candidateregisterid=obCandidate)
                    return render(request, "admin/result_publishing/view_result_candidates.html",
                                  {'data': obCandidatePhoto, 'msg': 'published'})


                else:
                    obResult = result_tb(candidateregisterid=obCandidate, assembly=obAssembly,
                                         vote_count=obVoteCount[0].count)
                    obResult.save()
                    obCandidateUpdate = candidateregister.objects.filter(id=maxcandidate_id).update(
                        count_vote=obVoteCount[0].count)

            # obCandidate= candidateregister.objects.filter(id=maxcandidate_id)
            obCandidatePhoto = photo.objects.filter(candidateregisterid=obCandidate)
            return render(request, "admin/result_publishing/view_result_candidates.html", {'data': obCandidatePhoto})
        else:
            print("invalid Date")
            state_details = state.objects.all()
            return render(request, "admin/result_publishing/view_state_dis_assembly_for_result.html",
                          {'state': state_details, 'msg': 'invalid'})


def view_resultant_candidates(request):
    state_details = state.objects.all()    
    return render(request, "admin/result_publishing/view_state_dis_assembly_for_resultDisplay.html",{'state':state_details})


def view_resultant_candidatesAction(request):
    # obAssembly=assembly.objects.get(id=3)
    # obCandidate=photo.objects.filter(candidateregisterid__in=result_tb.objects.filter(assembly=obAssembly))#
    msg = ""
    ResultList = []
    obCandidateResult = result_tb.objects.filter(assembly=request.POST['ddlassembly'])
    for res in obCandidateResult:
        print('Resultlist', res.candidateregisterid_id)
        ResultList.append(res.candidateregisterid_id)

    if len(ResultList) > 1:
        msg = "tie_up"
    obRemaining = candidateregister.objects.filter(assemblyname=request.POST['ddlassembly']).exclude(id__in=ResultList)
    # result_tb.objects.all()
    return render(request, "admin/result_publishing/view_result_candidates_forDisplay.html",
                  {'data': obCandidateResult, 'rem': obRemaining, 'msg': msg})


    
            

































