from django.contrib.auth.models import User
from django.db import models
import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save

class Pago(models.Model):
    user = models.ForeignKey(User,related_name='agregar_pago')
    monto = models.DecimalField(null=False,blank=False,decimal_places=2,max_digits=8)
    fecha_pago = models.DateField(null=False,blank=False)
    numero_de_meses = models.PositiveSmallIntegerField(null=False,blank=False)
    fecha_expiracion = models.DateField(editable=False)

    def save(self):
        self.fecha_expiracion = self.fecha_pago + relativedelta( months =+ self.numero_de_meses )
        super(Pago, self).save(self)

    def __unicode__(self):
        return "Monto:$%s---Fecha de Exp.:%s---User:%s" %(self.monto,self.fecha_expiracion,self.user)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
