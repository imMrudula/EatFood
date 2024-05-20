from django.db import models

# Create your models here


class Categorymodel(models.Model):
    Category_id=models.AutoField(primary_key=True)
    Category=models.CharField(max_length=200)
    Image = models.ImageField(upload_to='images/category/')

    class Meta:
        db_table = 'catagory'

    def __str__(self):
        return self.Category
from django.db import models

# Create your models here.
