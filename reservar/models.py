from django.db import models
from django.contrib.auth.models import User
from pagos.models import Pago
import datetime

class Sala(models.Model):
    user = models.ForeignKey(User)
    description = models.CharField(('Description'), max_length=255)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
