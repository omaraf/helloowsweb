from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from reservar.models import Sala
from pagos.models import Pago
from accounts.models import MyProfile
from rest_framework import status
from serializers import SalaSerializer
import datetime
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from reservar.forms import Salaform

class reservar_sala(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post( self, request,format=None):
        data = request.DATA
        data['user'] = request.user.id
        if not data.get('fecha') or not data.get('hora_inicio') or not data.get('hora_fin'):
            return Response("{'Error':'Missing Data'}",status=status.HTTP_409_CONFLICT)

        data['fecha_inicio'] = data['fecha']+' '+data['hora_inicio']
        data['fecha_fin'] = data['fecha']+' '+data['hora_fin']

        #Overlap Check
        fecha_inicio_res = datetime.datetime.strptime( data['fecha_inicio'],'%Y-%m-%d %H:%M:%S')
        fecha_fin_res = datetime.datetime.strptime( data['fecha_fin'],'%Y-%m-%d %H:%M:%S' )

        if fecha_inicio_res >= fecha_fin_res:
            return Response("{'error':'check times'}",status=status.HTTP_409_CONFLICT) 
     
        overlap_check = Sala.objects.filter( Q(user_id=data['user']) , Q(fecha_inicio__range=[fecha_inicio_res,fecha_fin_res]) | Q(fecha_inicio__lte=fecha_inicio_res,fecha_fin__gte=fecha_inicio_res) )

        if overlap_check:
            #for over_check in overlap_check:
            #    print over_check.fecha_inicio
            #    print over_check.fecha_fin
            return Response("{'overlap':'true'}",status=status.HTTP_409_CONFLICT)
       
        if not request.user.is_superuser:
            try:
                hours = MyProfile.objects.get(user_id=data['user'])
            except MyProfile.DoesNotExist:
                return Response("{'Error':'No Profile'}",status=status.HTTP_409_CONFLICT)

            total_hours = datetime.timedelta(hours = hours.horas_sala)

            fecha_sala = datetime.date( year=fecha_inicio_res.year, month=fecha_inicio_res.month, day=fecha_inicio_res.day)

            try:
                pago = Pago.objects.get( fecha_pago__lte=fecha_sala , fecha_expiracion__gte=fecha_sala)
            except Pago.DoesNotExist:
                return Response("{'Error':'No Pago'}",status=status.HTTP_409_CONFLICT)

            fecha_inicio_pago = pago.fecha_pago
            fecha_fin_pago = pago.fecha_expiracion

            if pago.numero_de_meses > 1:
                fecha_fin_pago = fecha_inicio_pago + relativedelta( months=+1) - relativedelta( days=+1)
                while not( fecha_inicio_pago <= fecha_sala and fecha_fin_pago >= fecha_sala ):
                    fecha_inicio_pago = fecha_fin_pago + relativedelta( days=+1)
                    fecha_fin_pago = fecha_inicio_pago + relativedelta( months=+1)
                    if fecha_fin_pago <> pago.fecha_expiracion:
                       fecha_fin_pago = fecha_fin_pago - relativedelta( days=+1)

            fecha_fin_pago = fecha_fin_pago + datetime.timedelta( hours=23,minutes=59,seconds=59)
            total_horas_sala = fecha_fin_res - fecha_inicio_res
            horas_sala = Sala.objects.filter( fecha_inicio__range=[fecha_inicio_pago,fecha_fin_pago])
            for sala in horas_sala:
                total_horas_sala += sala.fecha_fin - sala.fecha_inicio

            if total_horas_sala > total_hours:
                return Response("{'Error':'No Hours'}",status=status.HTTP_409_CONFLICT)

        serializer = SalaSerializer(data={'user':data['user'],'description':data['description'],'fecha_inicio':data['fecha_inicio'],'fecha_fin':data['fecha_fin']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)

def reserv_sala(request):
    if request.method == 'POST':
        form = Salaform(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = Salaform()

    return render( request,'res_sala.html',{ 'form':Salaform})
