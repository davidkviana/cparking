from django.utils.timezone import utc
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from parkapp.models import VehIn,VehHist
from parkapp.serializers import VehInSerializer, VehHistSerializer
from re import compile
import datetime, time


class VehicleHist(APIView):
    '''
    VehicleHist is used to show the historical of plates.
    The method get equivals or response the GET request.
    '''
    #convert_time return the elapsed time in format hh:mm:ss
    def convert_time(self, start,end):
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
    
    #get_object return the vehicle from plate
    def get_object(self, plat):
        try:
            ret = VehIn.objects.all().filter(plate=plat)
            return ret
        except VehIn.DoesNotExist:
            return Http404
    
    def get(self,request, plate, format=None):
        '''
        get is called by GET request and return cars by plates does not show the plate
        [
            { id: 42, time: '00:25:34', paid: true, left: true }
            { id: 2042, time: '00:44:35', paid: true, left: true }
        ]
        '''
        vehicles = self.get_object(plate)
        veh_hist = []
        for vehicle in vehicles:
            veh = VehHist()
            veh.id = vehicle.id
            veh.plate = vehicle.plate
            veh.left = vehicle.left
            veh.paid = vehicle.paid
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            now = time.mktime(now.timetuple()) + now.microsecond / 1E6
            bef = time.mktime(vehicle.time.timetuple()) + vehicle.time.microsecond / 1E6
            veh.time = self.convert_time(bef, now)
            veh_hist.append(veh)
        serializer = VehInSerializer(vehicles, many=True)
        serializer2 = VehHistSerializer(veh_hist, many=True)
        return Response(serializer2.data, status=status.HTTP_200_OK)

class VehiclePay(APIView):
    '''
    VehiclePay update the pyament of vehicles
    return True (ok 200) to confirm the payment else return False(bad request 404)
    and if already paid return True (already reported 208)
    '''
    #get_object get the vehicle by id in db.
    def get_object(self, pk):
        try:
            return VehIn.objects.get(pk=pk)
        except VehIn.DoesNotExist:
            return Http404
    
    #put - does a update in database if id exits and conditions are ok.
    def put(self, request, pk, format=None):
        vehicle = self.get_object(pk)
        serializer = VehInSerializer(vehicle)
        if vehicle.paid == False:
            vehicle.paid = True
            serializer = VehInSerializer(vehicle, data=serializer.data)
            if serializer.is_valid():
                serializer.save()
                return Response(True, status=status.HTTP_200_OK)
            else:
                return Response(False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(True, status=status.HTTP_208_ALREADY_REPORTED)


class VehicleOut(APIView):
    '''
    VehicleOut update the left of vehicles
    return True (ok 200) when confirm if the payment is checked, if not True, return False(payment required 402)
    and also return False if car not exist (bad request 400)
    '''
    #get_object get the vehicle by id in db.
    def get_object(self, pk):
        try:
            return VehIn.objects.get(pk=pk)
        except VehIn.DoesNotExist:
            return Http404
    
    #put - does a update in database if id exits and conditions are ok.
    def put(self, request, pk, format=None):
        vehicle = self.get_object(pk)
        serializer = VehInSerializer(vehicle)
        if vehicle.paid == True:
            vehicle.out = True
            serializer = VehInSerializer(vehicle, data=serializer.data)
            if serializer.is_valid():
                serializer.save()
                return Response(True, tatus=status.HTTP_200_OK)
            else:
                return Response(False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(False, status=status.HTTP_402_PAYMENT_REQUIRED)
    
class VehicleIn(APIView):
    '''
    VehicleIn insert the vehicles
    return True (created 201) when plate format if ok, else return False(not acceptable 406)
    and also return False if a invalid json or address is passed (bad request 400)
    '''
    #get_object - get the vehicle by id in db.
    def get_object(self, pk):
        try:
            return VehIn.objects.get(pk=pk)
        except VehIn.DoesNotExist:
            return Http404
    
    #validate_plate - verify the plate
    def validate_plate(self, plate):
        plate_format = compile('[A-Z]{3}-[0-9]{4}$')
        if plate_format.match(plate) is not None:
            return True
        else:
            return False
    
    #post - if plate is valid then it is created in db.
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = VehInSerializer(data=data)
        if serializer.is_valid():
            if self.validate_plate(data['plate']):
                serializer.save()
                ret = {'reserva':serializer.data['id']}
                return Response(ret, status=status.HTTP_201_CREATED)
            else:
                err = {'error':'invalid plate'}
                return Response(err, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
