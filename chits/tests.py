from django.test import TestCase,client
from accounts.models import * 
from django.contrib.auth import authenticate,login
from chits.models import *
import random
import json
from django.urls import reverse

# Create your tests here.


def create_chit(status,chit_from,chit_to,reply_to_chit,chit) :
    return Chit.objects.create(chit_from = chit_from , chit = chit ,chit_to=chit_to ,reply_to_chit=reply_to_chit,status = status)

def create_deligates_teams_countries() :
        for i in range(75) :
            Country.objects.create(name="Country_{}".format(i+1),country_id="country_{}@iitgmun".format(i+1))
    
        for i in range(15) :
            team = Team.objects.create(name="Team_{}".format(i+1),info="Dummy data")
            for j in range(5) :
                user =  User.objects.create(username="Country{}_deligate".format(i*5+j+1),role="DT",email="Country{}_deligate@gmail.com".format(i*5+j+1))
                profile = DeligateProfile.objects.create(user=user,country=Country.objects.get(name="Country_{}".format(i*5+j+1)),team=team,first_name="Who tf care!",last_name="Oh lol")
                user.save()
                profile.save()
                if j==0 :
                   team.leader = user
            team.save()


def create_judge_moderator() :
        User.objects.create(username="moderator1",role="MD",email="moderator1@gmail.com")
        User.objects.create(username="moderator2",role="MD",email="moderator2@gmail.com")
        User.objects.create(username="judge",role="JD",email="judge@gmail.com")
        

class ChitsViewTestClass(TestCase) :
    @classmethod
    def setUpTestData(cls) :
        create_deligates_teams_countries()
        create_judge_moderator()
        cls.user = User.objects.get(username="Country{}_deligate".format(random.randint(1,75)))
        cls.user.set_password("TestUser")
        cls.user.save()
        cls.moderator1 = User.objects.get(username="moderator1",role="MD")
        cls.moderator2 = User.objects.get(username="moderator2",role="MD")
        cls.judge = User.objects.get(username="judge",role="JD")
        cls.moderator1.set_password("TestUser")
        cls.moderator1.save()
        cls.moderator2.set_password("TestUser")
        cls.moderator2.save()
        cls.judge.set_password("TestUser")
        cls.judge.save()

    def setUp(self) :
        team1 = Team.objects.get(pk=random.randint(1,3))
        team2 = Team.objects.get(pk=random.randint(4,6))
        team3 = Team.objects.get(pk=random.randint(7,9))
        team4 = Team.objects.get(pk=random.randint(10,12))
        team5 = Team.objects.get(pk=random.randint(13,15))

    
    def logout_user(self) :
        self.client.logout()

    def tearDown(self) :
        self.logout_user()


    def login_user(self,user) :
        self.client.login(username=user.username,password ="TestUser")
    
    
        
   
    def check_redirect(self,url) :
       self.assertEqual(self.client.get(url).status_code,302)





    '''
         Checking the countries returned and login  redirect
    '''

    def test_index_view_countries(self) :

       

        #login
        response = self.client.get(reverse('chits:deligate_index'))
        self.check_redirect(reverse('chits:deligate_index'))
        self.assertEqual(self.user.role,"DT")
        
        response = self.client.post(reverse('accounts:login'),{
            'username':self.user.username,
            'password' :"TestUser"
        })
        self.assertEqual(response.status_code ,302)
        self.assertEqual(response.url,reverse('chits:deligate_index'))

        #after login
        self.login_user(self.user)

        response = self.client.get(reverse('chits:deligate_index'))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(list(response.context["countries"]),[f'<Country: Country object ({c.id})>' for c in Country.objects.all()])
        self.logout_user()
        

     





    '''
       deligate_post_view
    '''   
    def test_deligate_post(self) :


        
        #before login








        #after login
        self.login_user(self.user)
        send_to = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        response = self.client.post(reverse('chits:deligate_index'),{
            'chit_to':send_to.country_id,
            'content' :"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised."
        },content_type='application/json')
        
        response_data = json.loads(response.content)

        chit_created= Chit.objects.get(pk=response_data['id'])

        self.assertEqual(response.status_code,200) 
        self.assertEqual(response_data['message'],"Chit sent to Moderator for checking")
        self.assertEqual(chit_created.chit,"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")
        self.assertEqual(chit_created.chit_from,self.user.deligate_profile.country)
        self.assertEqual(chit_created.chit_to,send_to)
        self.assertEqual(chit_created.reply_to_chit,None)

        self.logout_user()





           







    '''
       deligate_reply_view
    '''
    def test_deligate_reply(self) :
        self.test_deligate_post()
        









        #after login
        self.login_user(self.user)
        chit_from = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        create_chit(status=3,chit_from =chit_from,chit_to=self.user.deligate_profile.country,reply_to_chit=None,
        chit="By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")

        send_to = Chit.objects.all().last()

        



        
        # send_to = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        response = self.client.post(reverse('chits:deligate_reply'),{
            'chit_to':send_to.chit_from.country_id,
            'reply_to' : send_to.id ,

            'content' :"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised."
        },content_type='application/json')
        
        response_data = json.loads(response.content)


        chit_created= Chit.objects.get(pk=response_data['id'])
        self.assertEqual(response.status_code,200)


        
        self.assertEqual(response_data['message'],"Reply to chit {} sent to moderator".format(send_to.id))
        self.assertEqual(chit_created.chit,"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")
        self.assertEqual(chit_created.chit_from,self.user.deligate_profile.country)
        self.assertEqual(chit_created.chit_to,send_to.chit_from)
        self.assertEqual(chit_created.reply_to_chit,send_to)

        self.logout_user() 
        
    




    def test_moderator_approve(self) :







        #after login
        self.login_user(self.user)
        chit_from = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        create_chit(status=1,chit_from =chit_from,chit_to=self.user.deligate_profile.country,reply_to_chit=None,
           chit="By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")

        send_to = Chit.objects.all().last()

        



        
        # send_to = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        response = self.client.post(reverse('chits:deligate_reply'),{
            'chit_to':send_to.chit_from.country_id,
            'reply_to' : send_to.id ,

            'content' :"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised."
        },content_type='application/json')
        
        response_data = json.loads(response.content)


        chit_created= Chit.objects.get(pk=response_data['id'])
        self.assertEqual(response.status_code,200)


        
        self.assertEqual(response_data['message'],"Reply to chit {} sent to moderator".format(send_to.id))
        self.assertEqual(chit_created.chit,"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")
        self.assertEqual(chit_created.chit_from,self.user.deligate_profile.country)
        self.assertEqual(chit_created.chit_to,send_to.chit_from)
        self.assertEqual(chit_created.reply_to_chit,send_to)

        self.logout_user() 
    



    def test_moderator_reject(self) :




        #after login
        self.login_user(self.user)
        chit_from = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        create_chit(status=3,chit_from =chit_from,chit_to=self.user.deligate_profile.country,reply_to_chit=None,
        chit="By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")

        send_to = Chit.objects.all().last()

        



        
        # send_to = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        response = self.client.post(reverse('chits:deligate_reply'),{
            'chit_to':send_to.chit_from.country_id,
            'reply_to' : send_to.id ,

            'content' :"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised."
        },content_type='application/json')
        
        response_data = json.loads(response.content)


        chit_created= Chit.objects.get(pk=response_data['id'])
        self.assertEqual(response.status_code,200)


        
        self.assertEqual(response_data['message'],"Reply to chit {} sent to moderator".format(send_to.id))
        self.assertEqual(chit_created.chit,"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")
        self.assertEqual(chit_created.chit_from,self.user.deligate_profile.country)
        self.assertEqual(chit_created.chit_to,send_to.chit_from)
        self.assertEqual(chit_created.reply_to_chit,send_to)

        self.logout_user() 
    




    def test_judge_ratify(self) :
        #after login
        self.login_user(self.user)
        chit_from = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        create_chit(status=3,chit_from =chit_from,chit_to=self.user.deligate_profile.country,reply_to_chit=None,
        chit="By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")

        send_to = Chit.objects.all().last()

        



        
        # send_to = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        response = self.client.post(reverse('chits:deligate_reply'),{
            'chit_to':send_to.chit_from.country_id,
            'reply_to' : send_to.id ,

            'content' :"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised."
        },content_type='application/json')
        
        response_data = json.loads(response.content)


        chit_created= Chit.objects.get(pk=response_data['id'])
        self.assertEqual(response.status_code,200)


        
        self.assertEqual(response_data['message'],"Reply to chit {} sent to moderator".format(send_to.id))
        self.assertEqual(chit_created.chit,"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")
        self.assertEqual(chit_created.chit_from,self.user.deligate_profile.country)
        self.assertEqual(chit_created.chit_to,send_to.chit_from)
        self.assertEqual(chit_created.reply_to_chit,send_to)

        self.logout_user() 
    



    def test_judge_reject(self) :







        #after login
        self.login_user(self.user)
        chit_from = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        create_chit(status=3,chit_from =chit_from,chit_to=self.user.deligate_profile.country,reply_to_chit=None,
        chit="By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")

        send_to = Chit.objects.all().last()

        



        
        # send_to = Country.objects.all().exclude(deligate__user__username=self.user.username)[random.randint(1,74)]
        response = self.client.post(reverse('chits:deligate_reply'),{
            'chit_to':send_to.chit_from.country_id,
            'reply_to' : send_to.id ,

            'content' :"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised."
        },content_type='application/json')
        
        response_data = json.loads(response.content)


        chit_created= Chit.objects.get(pk=response_data['id'])
        self.assertEqual(response.status_code,200)


        
        self.assertEqual(response_data['message'],"Reply to chit {} sent to moderator".format(send_to.id))
        self.assertEqual(chit_created.chit,"By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering, you can set the ordered parameter to False, which turns the comparison into a collections.Counter comparison. If the order is undefined (if the given qs isn’t ordered and the comparison is against more than one ordered values), a ValueError is raised.")
        self.assertEqual(chit_created.chit_from,self.user.deligate_profile.country)
        self.assertEqual(chit_created.chit_to,send_to.chit_from)
        self.assertEqual(chit_created.reply_to_chit,send_to)

        self.logout_user() 
    

    


    def test_chit_received_by_modertor(self) :
        pass





    def test_chit_received_by_judge(self) :
        pass
    




    def test_chit_received_by_deligate(self) :
        pass
