from django.db import models

# Create your models here.
class Murid(models.Model):
    id = models.AutoField(primary_key=True)
    program_studi = models.CharField(max_length=100)
    harga_program = models.CharField(max_length=100)
    nama = models.CharField(max_length=60)
    alamat = models.CharField(max_length=500)
    tanggal_lahir = models.DateField()
    email = models.CharField(max_length=60)
    jenis_kelamin = models.CharField(max_length=20)
    no_telp = models.CharField(max_length=20)
    sudah_bayar = models.BooleanField()
    accepted = models.BooleanField()


