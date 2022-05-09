from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, \
    MaxValueValidator

# TODO ==> Add loging state field(success, info, failure ...)
# TODO ==> Add validation for each field or make it automatic from django useing "meta"
# TODO ==> add field to delete log after specific timeout, to handel the increased number of logs

class AuditLog(models.Model):
    userName = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    ip = models.GenericIPAddressField()
    eventName = models.CharField(max_length=100)
    description =  models.CharField(max_length=500)
    actionType = models.CharField(max_length=100)
    eventSpecificFields =  models.JSONField(null=True)
    def __str__(self):
        return f'{self.userName} => {self.eventName}'
    
    def fieldsList():
        fields_list  = []
        for field in AuditLog._meta.fields:
            fields_list.append(field.name)
        return fields_list

      
class Products(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    price = models.IntegerField(validators=[MinValueValidator(20), MaxValueValidator(1000)])
    count = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("productDetials", args=[self.id])
    
    def get_edit_url(self):
        return reverse("editProduct", args=[self.id])
    
    def get_delete_url(self):
        return reverse("deleteProduct", args=[self.id])




