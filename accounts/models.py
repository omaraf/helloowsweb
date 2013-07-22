from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from userena.models import UserenaSignup
from userena import signals as userena_signals
# Create your models here.

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,unique=True,verbose_name=_('User'),related_name='my_profile')
    miembro_desde = models.DateField(verbose_name=_('Miembro Desde'),null=False,blank=False)
    tel = models.CharField(verbose_name=_('Tel'),max_length=20,null=True,blank=True)
    horas_sala = models.PositiveSmallIntegerField(verbose_name=_('Horas Sala x MES'),null=False,blank=False)
    
    def __unicode__(self):
        return '%s'%self.user


#@receiver(post_save, sender=MyProfile, dispatch_uid='user.created')
#def user_created(sender, instance, created, raw, using, **kwargs):
#  """ Adds 'change_profile' permission to created user objects """

#  if created:
#     user_inst = User.objects.get(username=instance)
#     userenasignup_inst = UserenaSignup.objects.get(user_id=user_inst.id)
#     from guardian.shortcuts import assign_perm
#     assign_perm('change_profile', user_inst, user_inst.get_profile())
     #userena_signals.confirmation_complete.send(sender=None,user=user_inst.username,old_email=userenasignup_inst.email_unconfirmed)
