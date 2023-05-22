"""voting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from siteadmin import views as admin_view
from voters import views as voter_view
from candidates import views as candidates_view
from django.conf.urls.static import static
from django.conf import settings


urlpatterns =[
     path('admin/', admin.site.urls),

    url(r'^$',admin_view.index,name='index'),
    url(r'^login/', admin_view.loginView, name='login'),

    url(r'^LoginAction/',admin_view.loginaction,name='LoginAction'),

    url(r'^register/',voter_view.vregister,name='register'),

    url(r'^voterregisteraction/',voter_view.voterregisteraction,name='voterregisteraction'),

    url(r'^addstate/', admin_view.addstate, name='addstate'),

    url(r'^stateaddaction/', admin_view.stateaddaction, name='stateaddaction'),

    url(r'^adddistrict/', admin_view.adddistrict, name='adddistrict'),

    url(r'^districtaddaction/', admin_view.districtaddaction, name='districtaddaction'),

    url(r'^addlandmark/', admin_view.addlandmark, name='addlandmark'),

    url(r'^landmarkaddaction/', admin_view.landmarkaddaction, name='landmarkaddaction'),

    url(r'^addparty/', admin_view.addparty, name='addparty'),

    url(r'^partyaddaction/', admin_view.partyaddaction, name='partyaddaction'),


    url(r'^checkUsername/', voter_view.checkUsernameAction, name='checkUsername'),

    url(r'^addassembly/', admin_view.addassembly, name='addassembly'),

    url(r'^assemblyaddaction/', admin_view.assemblyaddaction, name='assemblyaddaction'),

    url(r'^addsymbol/', admin_view.addsymbol, name='addsymbol'),

    url(r'^symboladdaction/', admin_view.symboladdaction, name='symboladdaction'),

    url(r'^view_regvoters/', admin_view.view_regvoters, name='view_regvoters'),


    url(r'^details/(?P<uid>\d+)/$', admin_view.details, name='details'),


    url(r'^manageUser/',admin_view.manageUseraction,name='manageUser'),

    url(r'^view_approvedvoters/', admin_view.view_approvedvoters, name='view_approvedvoters'),

    url(r'^view_rejectedvoters/', admin_view.view_rejectedvoters, name='view_rejectedvoters'),

    url(r'^cregister/',candidates_view.cregister,name='cregister'),

    url(r'^candidateregisteraction/',candidates_view.candidateregisteraction,name='candidateregisteraction'),

    url(r'^view_regcandidates/', admin_view.view_regcandidates, name='view_regcandidates'),

    url(r'^proposeraddaction/', candidates_view.proposeraddaction, name='proposeraddaction'),

    url(r'^edit_profile/', candidates_view.edit_profile, name='edit_profile'),

    url(r'^candidate_updateaction/', candidates_view.candidate_updateaction, name='candidate_updateaction'),

    url(r'^voter_edit_profile/', voter_view.voter_edit_profile, name='voter_edit_profile'),

    url(r'^voter_updateaction/', voter_view.voter_updateaction, name='voter_updateaction'),


    url(r'^candidate_details/(?P<uid>\d+)/$', admin_view.candidate_details, name='candidate_details'),

    url(r'^managecandidate/',admin_view.managecandidateaction,name='managecandidate'),

    url(r'^view_approvedcandidates/', admin_view.view_approvedcandidates, name='view_approvedcandidates'),


    url(r'^view_rejectedcandidates/', admin_view.view_rejectedcandidates, name='view_rejectedcandidates'),

    url(r'^getDistrict/', candidates_view.getDistrict, name='getDistrict'),

    url(r'^getplace/', candidates_view.getplace, name='getplace'),

    url(r'^getassembly/', candidates_view.getassembly, name='getassembly'),


    #url(r'^vote/', voter_view.vote, name='vote'),
    url(r'^view_regassembly_candidates_forVote/', voter_view.view_regassembly_candidates_forVote, name='view_regassembly_candidates_forVote'),

    

      url(r'^view_regassembly_candidate_forWork/', voter_view.view_regassembly_candidate_forWork, name='view_regassembly_candidate_forWork'),
     
   # url(r'^view_vote/', voter_view.vote, name='view_vote'),

    url(r'^announce_election/', admin_view.announce_election, name='announce_election'),

    url(r'^election_announcement_action/', admin_view.election_announcement_action,name='election_announcement_action'),

    url(r'^view_electiondetails/', candidates_view.view_electiondetails,name='view_electiondetails'),

    url(r'^view_all_announcedelection/', admin_view.view_all_announcedelection,name='view_all_announcedelection'),

    url(r'^approved_candidate_details/(?P<uid>\d+)/$', admin_view.approved_candidate_details,name='approved_candidate_details'),

    url(r'^rejected_candidate_details/(?P<uid>\d+)/$', admin_view.rejected_candidate_details,name='rejected_candidate_details'),

    url(r'^approved_voter_details/(?P<uid>\d+)/$', admin_view.approved_voter_details,name='approved_voter_details'),

    url(r'^rejected_voter_details/(?P<uid>\d+)/$', admin_view.rejected_voter_details,name='rejected_voter_details'),

    url(r'^getdata/', admin_view.getdata, name='getdata'),

    url(r'^getapproveddata/', admin_view.getapproveddata, name='getapproveddata'),

    url(r'^getrejecteddata/', admin_view.getrejecteddata, name='getrejecteddata'),

    url(r'^get_voterdata/', admin_view.get_voterdata, name='get_voterdata'),

    url(r'^get_voter_approveddata/', admin_view.get_voter_approveddata, name='get_voter_approveddata'),

    url(r'^get_voter_rejecteddata/', admin_view.get_voter_rejecteddata, name='get_voter_rejecteddata'),

    url(r'^change_password/', admin_view.change_password, name='change_password'),

    url(r'^change_password_action/', admin_view.change_password_action, name='change_password_action'),

    url(r'^candidate_change_password/', candidates_view.candidate_change_password, name='candidate_change_password'),

    url(r'^candidate_change_password_action/', candidates_view.candidate_change_password_action, name='candidate_change_password_action'),

    url(r'^voter_change_password/', voter_view.voter_change_password, name='voter_change_password'),

    url(r'^voter_change_password_action/', voter_view.voter_change_password_action, name='voter_change_password_action'),

    url(r'^candidate_forgot_password/', candidates_view.candidate_forgot_password, name='candidate_forgot_password'),

    url(r'^candidate_forgot_password_action/', candidates_view.candidate_forgot_password_action, name='candidate_forgot_password_action'),

    url(r'^candidate_update_password_action/', candidates_view.candidate_update_password_action, name='candidate_update_password_action'),

    url(r'^image_share/', admin_view.image_share, name='image_share'),

    url(r'^admin_mail_action/', admin_view.admin_mail_action, name='admin_mail_action'),

    url(r'^add_profile/', candidates_view.add_profile, name='add_profile'),

    url(r'^add_profile_action/', candidates_view.add_profile_action, name='add_profile_action'),

   # url(r'^view_regassembly_candidate/', voter_view.view_regassembly_candidate, name='view_regassembly_candidate'),

    url(r'^assembly_candidate_details/(?P<uid>\d+)/$', voter_view.assembly_candidate_details, name='assembly_candidate_details'),

    url(r'^view_work/', candidates_view.view_work, name='view_work'),

    url(r'^work_delete/(?P<uid>\d+)/$', candidates_view.work_delete, name='work_delete'),

    url(r'^getsymbol/', candidates_view.getsymbol, name='getsymbol'),

    url(r'^view_velectiondetails/', voter_view.view_velectiondetails, name='view_velectiondetails'),

    url(r'^withdraw/', candidates_view.withdraw, name='withdraw'),

    url(r'^withdrawaction/', candidates_view.withdrawaction, name='withdrawaction'),

    url(r'^view_withdraw_candidates/', admin_view.view_withdraw_candidates, name='view_withdraw_candidates'),


    url(r'^getwithdrawcandidate/', admin_view.getwithdrawcandidate, name='getwithdrawcandidate'),

    url(r'^view_opposing_candidates/', candidates_view.view_opposing_candidates, name='view_opposing_candidates'),


     url(r'^view_resultant_ForCandidate/', candidates_view.view_resultant_ForCandidate, name='view_resultant_ForCandidate'),    
    url(r'^ view_resultant_ForCandidateAction/', candidates_view.view_resultant_ForCandidateAction, name='view_resultant_ForCandidateAction'),



     

    url(r'^processingVisualCrypto/(?P<candidate_id>\d+)/$',voter_view.processingVisualCrypto,name='processingVisualCrypto') ,
    url(r'^processingVisualCryptoAction/',voter_view.processingVisualCryptoAction,name='processingVisualCryptoAction') ,
    url(r'^decryptionAction/',voter_view.decryptionAction,name='decryptionAction'),
     
##    url(r'^voteAction/',voter_view.voteAction,name='voteAction'),

  url(r'^publish_result/$',admin_view.publish_result,name='publish_result'),


    url(r'^publish_result_candidate/$', admin_view.publish_result_candidate, name='publish_result_candidate'),
     
    url(r'^publish_result/publish_result_action', admin_view.publish_result_action, name='publish_result/publish_result_action'),

    url(r'^view_resultant_candidates/', admin_view.view_resultant_candidates, name='view_resultant_candidates'),


     url(r'^view_resultant_candidatesAction/', admin_view.view_resultant_candidatesAction, name='view_resultant_candidatesAction'),
      #url(r'^view_result/', voter_view.view_result, name='view_result'),
     
     url(r'^view_resultant_ForVoter/', voter_view.view_resultant_ForVoter, name='view_resultant_ForVoter'),

    
      url(r'^ view_resultant_ForVoterAction/', voter_view.view_resultant_ForVoterAction, name='view_resultant_ForVoterAction'),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
