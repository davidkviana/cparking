from rest_framework import serializers
from parkapp.models import VehIn, VehHist

class VehInSerializer(serializers.ModelSerializer):
    """
    VehInSerializer serializes VehIn
    """
    class Meta:
        model = VehIn
        fields = ['id', 'time', 'plate', 'left', 'paid']


class VehHistSerializer(serializers.ModelSerializer):
    """
    VehHistSerializer serializes VehHist but does not show plate
    beacuse in '/parking/{plate}' must return only as example:
    { id: 42, time: '25 minutes', paid: true, left: false }
    """
    class Meta:
        model = VehHist
        fields = ['id', 'time', 'left', 'paid']
