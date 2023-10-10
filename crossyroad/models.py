from django.contrib.gis.db import models

# Create your models here.
class CrosswalkModel(models.Model):
    geom = models.GeometryField()
    
    class Meta:
        db_table = 'crosswalk'


class TrafficModel(models.Model):
    geom = models.GeometryField()
    
    class Meta:
        db_table = 'traffic'


class CCTVModel(models.Model):
    geom = models.GeometryField()
    
    class Meta:
        db_table = 'cctv'
