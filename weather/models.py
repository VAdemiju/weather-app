from django.db import models
from django.utils.text import slugify

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=25)
    name_slug = models.SlugField(max_length=35)

    class Meta:
        verbose_name_plural = 'cities'

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    