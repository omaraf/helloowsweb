from reservar.models import Sala
from rest_framework import serializers

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ('user', 'description', 'fecha_inicio', 'fecha_fin')
