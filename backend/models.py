from django.db import models

# Create your models here.
class Murid(models.Model):
    id = models.AutoField(primary_key=True)
    program_studi = models.CharField(max_length=100)
    harga_program = models.CharField(max_length=100)
    nama = models.CharField(max_length=60)
    nim = models.CharField(max_length=30, default="")
    hari_belajar = models.CharField(max_length=100, default="")
    jam_belajar = models.CharField(max_length=400, default="")
    alamat = models.CharField(max_length=500)
    tanggal_lahir = models.DateField()
    email = models.CharField(max_length=60)
    jenis_kelamin = models.CharField(max_length=20)
    no_telp = models.CharField(max_length=20)
    sudah_bayar = models.BooleanField()
    accepted = models.BooleanField()
    last_updated_by = models.CharField(max_length = 100, default="")
    last_updated_date = models.DateTimeField(auto_now=True)
    referral_code = models.CharField(max_length = 100, default="")

class ReferralCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length = 100)
    owner = models.CharField(max_length = 100, default="")
    created_by = models.CharField(max_length = 100)


