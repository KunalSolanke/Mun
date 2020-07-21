from django.urls import path,re_path
from chits.views import *


app_name = 'chits'



urlpatterns = [
    re_path(r'^api/messages/$',view=chitlist,name="chitlist") ,
    re_path(r'^api/messages/team$',view=team_chit_list,name="teamchitlist") ,
    path('deligate/', view = deligate_index ,name = "delegate_index"),
    path('deligate/reply', view = deligate_reply ,name = "deligate_reply"),
    path('moderator/', view = moderator_index,name = "moderator_index"),
    path('moderator/disapprove', view = moderator_index_disapprove ,name = "moderator_index_disapprove"),#only post request
    path('judge/', view = judge_index ,name = "judge_index"),
    path('judge/reject', view = judge_index_reject ,name = "judge_index_reject"), #only post request  ,
]