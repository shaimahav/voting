from django.shortcuts import render
from candidates.models import *
from django.http import JsonResponse

import datetime

from voters.models import *
# Create your views here.
def cregister(request):
    ob = party.objects.all()
    ab = assembly.objects.all()
    cd = symbol.objects.all()
    ef = state.objects.all()
    gh = district.objects.all()
    ij=landmark.objects.all()
    return render(request, "candidateregister.html",{'party':ob,'assembly':ab,'symbol':cd,'state':ef,'district':gh,'landmark':ij})

def candidateregisteraction(request):
    obparty = party.objects.get(id=request.POST['party'])
    obsymbol = symbol.objects.get(id=request.POST['symbol'])
    obstate=state.objects.get(id=request.POST['state'])
    obdistrict = district.objects.get(id=request.POST['district'])
    obassembly = assembly.objects.get(id=request.POST['assembly'])
    oblandmark=landmark.objects.get(id=request.POST['location'])
    obc = candidateregister.objects.filter(partyid=request.POST['party'], assemblyname_id=request.POST['assembly'])
    if (obc.count() > 0):
        return render(request, "candidateregister.html", {'msg1': "Already a candidate Registered "})
    else:
        obe=candidateregister.objects.filter(email=request.POST['email'])
        if(obe.count() > 0):
            return render(request, "candidateregister.html", {'msg2': "email already registered "})
        else:

            obcheckAssembly=election_announcement.objects.filter(assembly=obassembly)
            if(obcheckAssembly.count()>0):
                nomination_date=obcheckAssembly[0].nominationsubmissiondate
                nomination_date_format = datetime.datetime.strptime(nomination_date, '%Y-%m-%d').date()
                current_date=datetime.date.today()
                print('nomination_date_format',nomination_date_format)
                print('current_date',current_date)
                if(nomination_date_format>=current_date):
                    #check Age
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
                    
                            ob = candidateregister(firstname=request.POST['fname'], lastname=request.POST['lname'], address=request.POST['address'],
                                gender=request.POST['gender'],
                               dateofbirth=request.POST['dob'], adharno=request.POST['adharno'],
                               voterid=request.POST['voterid'], email=request.POST['email'],
                               mobile=request.POST['mobile'],partyid=obparty,symbol=obsymbol,stateid=obstate,district=obdistrict,place=oblandmark,assemblyname=obassembly,username=request.POST['uname'],password=request.POST['pswd'])
                            ob.save()
                            if len(request.FILES) != 0:
                                obcandidate = candidateregister.objects.get(username=request.POST['uname'])
                                ab = adhar(candidateregisterid=obcandidate, adhar=request.FILES['adharcopy'])
                                ab.save()
                                cd = voteridcopy(candidateregisterid=obcandidate, voteridcopy=request.FILES['voteridcopy'])
                                cd.save()
                                ef = photo(candidateregisterid=obcandidate, photo=request.FILES['photo'])
                                ef.save()
                                return render(request, "candidate/proposerform.html",{'username':request.POST['uname']})
                    else:

                            ob = party.objects.all()
                            ab = assembly.objects.all()
                            cd = symbol.objects.all()
                            ef = state.objects.all()
                            gh = district.objects.all()
                            ij=landmark.objects.all()
                            return render(request, "candidateregister.html",{'party':ob,'assembly':ab,'symbol':cd,'state':ef,'district':gh,'landmark':ij,'msg':'InvalidAge'})
                        
                else:
                    print('nomination date exceeded')
                    ob = party.objects.all()
                    ab = assembly.objects.all()
                    cd = symbol.objects.all()
                    ef = state.objects.all()
                    gh = district.objects.all()
                    ij=landmark.objects.all()
                    return render(request, "candidateregister.html",{'party':ob,'assembly':ab,'symbol':cd,'state':ef,'district':gh,'landmark':ij,'msg':'exceeded'})

    

            else:
                print('No announce')
                ob = party.objects.all()
                ab = assembly.objects.all()
                cd = symbol.objects.all()
                ef = state.objects.all()
                gh = district.objects.all()
                ij=landmark.objects.all()
                return render(request, "candidateregister.html",{'party':ob,'assembly':ab,'symbol':cd,'state':ef,'district':gh,'landmark':ij,'msg':'No_Announcement'})

                
def proposeraddaction(request):
    proposerformob=proposertb(pname1=request.POST['p1name'], voterid1=request.POST['vrid1'],pname2=request.POST['p2name'],voterid2=request.POST['vrid2'],username=request.POST['hdn'])

    proposerformob.save()

    return render(request,"candidate/add_profile.html",{'username':request.POST['hdn']})

def edit_profile(request):
    ob = candidateregister.objects.filter(id=request.session['id'])
    if (ob.count() > 0):
        request.session['id'] = ob[0].id
        symbol_id = ob[0].symbol

    return render(request, "candidate/edit_profile.html", {'symbol': symbol_id.symbol, 'candidateregister': ob})

   # return render(request, "candidate/edit_profile.html")


def candidate_updateaction(request):
    ob = candidateregister.objects.filter(id=request.session['id']).update(firstname=request.POST['fname'], lastname=request.POST['lname'], address=request.POST['address'], gender=request.POST['gender'],dateofbirth=request.POST['dob'],email=request.POST['email'],mobile=request.POST['mobile'])
    ob =candidateregister.objects.filter(id=request.session['id'])
    if (ob.count() > 0):
        request.session['id'] = ob[0].id
        symbol_id = ob[0].symbol

    return render(request, "candidate/edit_profile.html", {'symbol':symbol_id.symbol, 'candidateregister': ob,'msg': "Updated Successfully"})


def getDistrict(request):
    obDistrict=district.objects.filter(stateid=request.GET.get('state_id'))

    return render(request, "candidate/getDistrict.html", {'district': obDistrict})


def getplace(request):
    obplace=landmark.objects.filter(districtid=request.GET.get('district_id'))

    return render(request, "candidate/getplace.html", {'landmark': obplace})

def getassembly(request):
    obassembly=assembly.objects.filter(landmarkid=request.GET.get('place_id'))

    return render(request, "candidate/getassembly.html", {'assembly': obassembly})

def checkUsernameAction(request):
    data={}
    obadmin=login.objects.filter(username=request.GET.get('username')).exists()

    ob=candidateregister.objects.filter(username=request.GET.get('username')).exists()

    obvoter = voterregister.objects.filter(username=request.GET.get('username')).exists()

    if(ob or obadmin or obvoter ):
        data['k1']="exists"
    else:
        data['k1'] = "valid"
    return  JsonResponse(data)

def view_electiondetails(request):
    ob = candidateregister.objects.filter(id=request.session['id'])
    if (ob.count() > 0):
        assembly=ob[0].assemblyname_id
        ob=election_announcement.objects.filter(assembly=assembly)
    return render(request, "candidate/election_details.html", {'data': ob})

def candidate_change_password(request):
    return render(request, "candidate/candidate_change_password.html")

def candidate_change_password_action(request):
    ob = candidateregister.objects.filter(id=request.session['id'], password=request.POST['currentpswd'])
    if (ob.count() > 0):
        if (request.POST['newpswd'] == request.POST['confirmpswd']):
            ob = candidateregister.objects.filter(id=request.session['id']).update(password=request.POST['newpswd'])
            return render(request, "candidate/candidate_change_password.html", {'msg': 'password changed successfully'})

        else:
            return render(request, "candidate/candidate_change_password.html", {'msg': 'Passwod Mismatch'})
    else:
        return render(request, "candidate/candidate_change_password.html", {'msg': 'Invalid User'})

def candidate_forgot_password(request):
    return render(request, "candidate/candidate_forgot_password.html")

def candidate_forgot_password_action(request):
    ob=candidateregister.objects.filter(firstname=request.POST['fname'],dateofbirth=request.POST['dob'],mobile=request.POST['mobile'],email=request.POST['email'],username=request.POST['uname'],status='approved')
    if(ob.count()>0):
        return render(request,"candidate/candidate_update_password.html",{'uname':request.POST['uname'],'type':'candidate'})
    else:
        ob=voterregister.objects.filter(firstname=request.POST['fname'],dateofbirth=request.POST['dob'],mobile=request.POST['mobile'],email=request.POST['email'],username=request.POST['uname'],status='approved')
        if (ob.count() > 0):
            return render(request, "candidate/candidate_update_password.html",{'uname': request.POST['uname'], 'type': 'voter'})
        else:
                return render(request, "candidate/candidate_forgot_password.html", {'msg':'invalid user'})

def candidate_update_password_action(request):
    if(request.POST['newpswd']==request.POST['confirmpswd']):
        if (request.POST['hdn1'] == 'candidate'):
            ob=candidateregister.objects.filter(username=request.POST['hdn']).update(password=request.POST['newpswd'])
            return render(request, "candidate/candidate_forgot_password.html",{'msg': 'password Updated successfully'})
        else:
            if (request.POST['hdn1'] == 'voter'):
                ob=voterregister.objects.filter(username=request.POST['hdn']).update(password=request.POST['newpswd'])
                return render(request, "candidate/candidate_forgot_password.html",{'msg': 'Password updated successfully'})
            else:
             return render(request, "candidate/candidate_update_password.html")
    else:
        return render(request, "candidate/candidate_update_password.html", {'msg': 'Password Mismatch'})

def add_profile(request):
    return render(request, "candidate/add_profile.html")

def add_profile_action(request):
    if len(request.FILES) != 0:
        #obid = candidateregister.objects.get(id=request.POST['hdn'])
        ob = addprofile(qualification=request.POST['qualification'],work1=request.POST['work1'],work1photo=request.FILES['work1photo'],work2=request.POST['work2'],work2photo=request.FILES['work2photo'],work3=request.POST['work3'],work3photo=request.FILES['work3photo'],achievements=request.POST['achievements'],username=request.POST['hdn'])

        ob.save()

        return render(request, "candidate/add_profile.html",{'username':request.POST['hdn'],'msg': "Registration completed  Successfully"})

def view_work(request):
    obw=candidateregister.objects.filter(id=request.session['id'])
    ob=addprofile.objects.filter(username=obw[0].username)
    return render(request, "candidate/view_work.html", {'data': ob})


def work_delete(request,uid):
    ob = addprofile.objects.filter(id=uid).delete()
    obw = candidateregister.objects.filter(id=request.session['id'])
    ob = addprofile.objects.filter(username=obw[0].username)

    return render(request, "candidate/view_work.html", {'data': ob})


def getsymbol(request):
    obsymbol = symbol.objects.filter(partyid=request.GET.get('party_id'))

    return render(request, "candidate/getsymbol.html", {'symbol': obsymbol})

def withdraw(request):
    return render(request, "candidate/withdraw.html")

def withdrawaction(request):
    
    ob_cid = candidateregister.objects.get(id=request.session['id'])
    assemblyID=ob_cid.assemblyname_id
    print('assemblyID',assemblyID)
    obassembly = assembly.objects.get(id=assemblyID)
    obcheckAssembly=election_announcement.objects.filter(assembly=obassembly)
    if(obcheckAssembly.count()>0):
                nomination_wdate=obcheckAssembly[0].nominationwithdrawdate
                nomination_wdate_format = datetime.datetime.strptime(nomination_wdate, '%Y-%m-%d').date()
                current_date=datetime.date.today()
                print('nominationwithdrawdate',nomination_wdate_format)
                print('current_date',current_date)
                if(nomination_wdate_format>=current_date):
    
                    ob = withdraw_candidate(reason=request.POST['reason'],c_id=ob_cid)
                    ob.save()
                    obcandidate = candidateregister.objects.filter(id=request.session['id']).update(status='withdraw')
    

                    return render(request, "candidate/withdraw.html",{'msg1': "Withdraw  Successfully"})
                else:
                    return render(request, "candidate/withdraw.html",{'msg2': "Cannot Withdraw  Date Exceeded"})
    else:
                    return render(request, "candidate/withdraw.html",{'msg3': "Election not Announced"})
                                


def view_opposing_candidates(request):
    ob = candidateregister.objects.filter(id=request.session['id'])
    if (ob.count() > 0):
        assembly = ob[0].assemblyname_id
        ob = candidateregister.objects.filter(assemblyname=assembly,status='approved').exclude(id=request.session['id'])
    return render(request, "candidate/view_opposing_candidate.html", {'data': ob})



def view_resultant_ForCandidate(request):
    state_details = state.objects.all()    
    return render(request, "candidate/view_state_dis_assembly_for_resultDisplay.html",{'state':state_details})
    
    
def view_resultant_ForCandidateAction(request):
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
        return render(request, "candidate/view_result_candidates_forDisplay.html",{'data':obCandidateResult,'rem':obRemaining,'msg':msg})
    else:
        return render(request, "candidate/view_result_candidates_forDisplay.html")























