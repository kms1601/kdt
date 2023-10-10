from django.contrib.gis.db import models

# Create your models here.
class Crosswalk(models.Model):
    geom = models.GeometryField()
