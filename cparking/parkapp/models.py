from django.db import models

class VehIn(models.Model):
    '''
    VehIn keeps car parameters: id, plate, time, left, paid.
    id - int sorted into database
    plate - string vehicle plate - format AAA-9999
    time - timestemp in
    left - boolean, False is default, True when exit
    paid - boolean, False is default, True when pay 
    It is used when to insert, change and get Vehicles in database
    '''
    id = models.AutoField(primary_key=True)
    plate = models.CharField(max_length=8, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    left = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    class Meta:
        ordering = ['id']


class VehHist(models.Model):
    '''
    VehHist keeps car parameters: id, plate, time, left, paid.
    It is used to show a historical from plate, is called to calculate 
    time elapsed from entrance of car.
    '''
    id = models.AutoField(primary_key=True)
    plate = models.CharField(max_length=8, blank=False)
    time = models.CharField(max_length=32, blank=True)
    left = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    class Meta:
        ordering = ['id']
