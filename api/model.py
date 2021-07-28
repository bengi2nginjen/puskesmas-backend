from django.db import models

# Create your models here.
class Form(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    content = models.TextField(null=True)
    user_id = models.CharField(max_length=50, null=True)
    created_date = models.DateField(null=True)
    is_active = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'form'

class FormResponse(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    responses = models.TextField(null=True)
    user_id = models.CharField(max_length=50, null=True)
    form_id = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'form_response'