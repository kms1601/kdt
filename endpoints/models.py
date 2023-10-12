from django.contrib.gis.db import models


class CrosswalkModel(models.Model):
    geom = models.GeometryField()
    traffic = models.BooleanField()
    cctv = models.IntegerField()
    distance_to_cctv = models.FloatField()
    
    class Meta:
        db_table = 'crosswalk'
        ordering = ['id']


class TrafficModel(models.Model):
    geom = models.GeometryField()
    
    class Meta:
        db_table = 'traffic'
        ordering = ['id']


class CCTVModel(models.Model):
    geom = models.GeometryField()
    
    class Meta:
        db_table = 'cctv'
        ordering = ['id']
