from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser,BaseUserManager
from django.db.models.base import Model
from datetime import date

import uuid


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_admin(self, username, nama, jabatan, password=None):
        if not username:
            raise ValueError("Username tidak boleh kosong")
        if not password:
            raise ValueError("Password tidak boleh kosong")
        if not nama:
            raise ValueError("Nama tidak boleh kosong")
        if not jabatan:
            raise ValueError("Jabatan tidak boleh kosong")

        user = self.model()
        user.id=uuid.uuid4()
        user.username = username
        user.nama = nama
        user.jabatan = jabatan
        user.set_password(password)  # change password to hash
        user.isadmin = True
        user.is_active = 1
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nama, jabatan, password=None):
        if not username:
            raise ValueError("Username tidak boleh kosong")
        if not password:
            raise ValueError("Password tidak boleh kosong")
        if not nama:
            raise ValueError("Nama tidak boleh kosong")
        if not jabatan:
            raise ValueError("Jabatan tidak boleh kosong")

        user = self.model()
        user.id=uuid.uuid4()
        user.username = username
        user.nama = nama
        user.jabatan = jabatan
        user.set_password(password)  # change password to hash
        user.isadmin = True
        user.is_active = 1
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Username tidak boleh kosong")
        if not password:
            raise ValueError("Password tidak boleh kosong")
        # if not nama:
        #     raise ValueError("Nama tidak boleh kosong")
        # if not jabatan:
        #     raise ValueError("Jabatan tidak boleh kosong")

        user = self.model()
        user.id=uuid.uuid4()
        user.username = username
        # user.nama = nama
        # user.jabatan = jabatan
        user.set_password(password)  # change password to hash
        user.isadmin = False
        user.is_active = 1
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, nama, jabatan, password=None):
        if not username:
            raise ValueError("Username tidak boleh kosong")
        if not password:
            raise ValueError("Password tidak boleh kosong")
        if not nama:
            raise ValueError("Nama tidak boleh kosong")
        if not jabatan:
            raise ValueError("Jabatan tidak boleh kosong")

        user = self.model()
        user.id=uuid.uuid4()
        user.username = username
        user.nama = nama
        user.jabatan = jabatan
        user.set_password(password)  # change password to hash
        user.isadmin = False
        user.is_active = 1
        user.save(using=self._db)
        return user

    # def create_form(self, name, description, created_by, questions):
    #     if not name:
    #         raise ValueError("Judul form tidak boleh kosong")
    #     if not questions:
    #         raise ValueError("Form harus memiliki setidaknya satu pertanyaan")

    #     form = self.model()
    #     form.name = name
    #     form.description = description
    #     form.created_by = created_by
    #     form.date_created = date.today()
    #     form.is_active = True
    #     form.questions = questions

    #     return form

    # def create_question(self, question_no, question_text, input):
    #     if not question_text:
    #         raise ValueError("Pertanyaan harus diisi")
    #     if not input:
    #         raise ValueError("Harus memilih tipe pertanyaan")

class UserModel(AbstractBaseUser):
    id=models.CharField(max_length=50,primary_key=True,)
    nama = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255,unique=True, null=True)
    password = models.CharField(max_length=255, null=True)
    jabatan = models.CharField(max_length=255, null=True)
    isadmin = models.BooleanField(db_column='isAdmin', null=True)  # Field name made lowercase.
    is_active = models.IntegerField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nama', 'password']

    class Meta:
        managed = True
        db_table = 'user'

# class FormModel():
#     name = models.CharField(max_length=255)
#     description = models.CharField(max_length=255)
#     created_by = models.CharField(max_length=255)
#     date_created = models.DateField()
#     is_active = models.BooleanField()
#     # question = models.ExpressionList() # GAK TAU pake apa

# class QuestionModel():
#     question_no = models.IntegerField(max_length=255)
#     question_text = models.CharField(max_length=255)
#     # input = models.ExpressionList() #gak tahu pake apa

# class InputModel():
#     SHORT_TEXT = 'SHORT'
#     PARAGRAPH = 'PARAGRAPH'
#     RADIO_BUTTON = 'RADIO'
#     CHECKBOX = 'CHECKBOX'
#     DROPDOWN = 'DROPDOWN'
#     DATE = 'DATE'

#     INPUT_TYPE_CHOICES = [
#         (SHORT_TEXT, 'Short'),
#         (PARAGRAPH, 'Paragraph'),
#         (RADIO_BUTTON, 'Radio'),
#         (CHECKBOX, 'Checkbox'),
#         (DROPDOWN, 'Dropdown'),
#         (DATE, 'Date'),
#     ]
    
#     input_text = models.CharField(max_length=255)
#     input_type = models.CharField(
#         max_length=10,
#         choices=INPUT_TYPE_CHOICES,
#         default=SHORT_TEXT,
#     )
