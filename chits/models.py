from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from accounts.models import Country,Team

# Create your models here.




class Chit(models.Model) :
    class Status(models.IntegerChoices):
            DISAPPROVED=0
            CHECKING= 1
            APPROVED= 2
            RATIFIED= 3

    
    
    chit = models.TextField(_("chit"),blank=False) #message 
    chit_from = models.ForeignKey(Country,on_delete=models.CASCADE,related_name='sent_chits')
    chit_to = models.ForeignKey(Country,on_delete=models.CASCADE,related_name='received_chits',blank=True,null=True)
    status = models.IntegerField(choices=Status.choices)
    timestamp = models.DateTimeField(auto_now=True,auto_now_add=False)  
    reply_to_chit = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name="reply")


    class Meta :
        ordering = ["timestamp"]#oldest at top
        get_latest_by = "-timestamp"
        verbose_name_plural = "chits"
        verbose_name="chit"



class Round(models.Model) :
      name = models.CharField(max_length=255)
      teams = models.ManyToManyField(Team,related_name='round')
      chits= models.ManyToManyField(Chit,related_name = 'round_in')
      start_time = models.DateTimeField(auto_now=False,auto_now_add=False)
      end_time = models.DateTimeField(auto_now=False,auto_now_add=False)

