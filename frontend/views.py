from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import ast
import logging
import traceback
import requests

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.http import HttpResponse

from datetime import date

from .models import Murid

#------------------------
import smtplib
import string, sys
import cgitb
cgitb.enable()
sys.stderr = sys.stdout

month_converter = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}




def test(request):
  return HttpResponse("test")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
@csrf_exempt
def index(request):
    print('masuk')
    if request.method == "POST":
        print('masuk POST')
        try:
            filez = open('logberhasil.txt', 'w')
            filez.write('masuk')
            filez.close()

            print('selesai buka file', request.POST)
                
            # old_data = list(request.POST.keys())[0].strip()

            # print('selesai old list', old_data)
            # new_data = old_data.replace("'", '"')
            # data = json.loads(new_data)
            # data = ast.literal_eval(old_data)
            # data = request.POST
            data = json.loads(list(request.POST.keys())[0].strip())

            print('selesai ast', data["tahun"])

            programStudi = data["programStudi"]
            hargaProgram = data["hargaProgram"]
            namaLengkap = data["namaLengkap"]
            alamatLengkap = data["alamatLengkap"]
            tanggal = data["tanggal"]
            bulan = data["bulan"]
            tahun = data["tahun"]
            jenisKelamin = data["jenisKelamin"]
            noTelp = data["noTelp"]
            email = data['email']
            # referral_code = data["referralCode"]

            print('selesai post data')

            print('tahun' + ' ' + str(tahun))
            print('bulan' + ' ' + str(int(bulan)))
            print('tanggal' + ' ' + str(tanggal))

            # send to another service

            r = requests.post("https://aktlivingacademy.com/backoffice/add-murid", data=request.POST)

            print('berhasil post')

            # insert to DB
            
            # new_date = date(int(tahun), int(bulan), int(tanggal))

            # murid = Murid(program_studi=programStudi, harga_program=hargaProgram, nama=namaLengkap, alamat=alamatLengkap, tanggal_lahir=new_date, email=email, jenis_kelamin=jenisKelamin, no_telp=noTelp, sudah_bayar=False, accepted=False)
            # murid.save()

            print('berhasil save')

            # programStudi = request.POST["programStudi"]
            # hargaProgram = request.POST["hargaProgram"]
            # namaLengkap = request.POST["namaLengkap"]
            # alamatLengkap = request.POST["alamatLengkap"]
            # tanggal = request.POST["tanggal"]
            # bulan = request.POST["bulan"]
            # tahun = request.POST["tahun"]
            # jenisKelamin = request.POST["jenisKelamin"]
            # noTelp = request.POST["noTelp"]
            # email = request.POST['email']
            
            # if referral_code == "AKS1" or referral_code == "TBL1":
            #     harga_list = hargaProgram.split(".")
            #     harga = int("".join(harga_list))
            #     hargaProgram = harga - 500000
            
            mail_subject = 'Pendaftaran Berhasil'
            message = render_to_string('email/application_success.html', {
                'programStudi': programStudi,
                'hargaProgram': hargaProgram,
                'namaLengkap': namaLengkap,
                'alamatLengkap': alamatLengkap,
                'tanggal': tanggal,
                'bulan': bulan,
                'tahun': tahun,
                'jenisKelamin': jenisKelamin,
                'noTelp': noTelp,
                # 'referralCode': referral_code,
            })
            message_strip = strip_tags(message)
            to_email = email
            email_send = EmailMultiAlternatives(
                mail_subject, message_strip, settings.EMAIL_HOST_USER, [to_email]
            )
            email_send.attach_alternative(message, "text/html")
            email_send.fail_silently = False
            email_send.send()
        except Exception as e:
            print('gagal', e)
            # with open('log.txt', 'w') as file:
            #     file.write(e)
            #     file.write("---------------")
            #     file.write(e.args)
            filez = open('loggagal.txt', 'w')
            filez.write(traceback.format_exc())
            # filez.write(data)
            filez.close()
    f = open('logmain.txt', 'w')
    f.write(str(get_client_ip(request)))
    f.close()
    return render(request, 'frontend/index.html')

# def daftar(request):
#     if request.method == "POST":
#         programStudi = request.POST["programStudi"]
#         hargaProgram = request.POST["hargaProgram"]
#         namaLengkap = request.POST["namaLengkap"]
#         alamatLengkap = request.POST["alamatLengkap"]
#         tanggal = request.POST["tanggal"]
#         bulan = request.POST["bulan"]
#         tahun = request.POST["tahun"]
#         jenisKelamin = request.POST["jenisKelamin"]
#         noTelp = request.POST["noTelp"]
#         email = request.POST['email']
        
#         mail_subject = 'Pendaftaran Berhasil'
#         message = render_to_string('email/application_success.html', {
#             'programStudi': programStudi,
#             'hargaProgram': hargaProgram,
#             'namaLengkap': namaLengkap,
#             'alamatLengkap': alamatLengkap,
#             'tanggal': tanggal,
#             'bulan': bulan,
#             'tahun': tahun,
#             'jenisKelamin': jenisKelamin,
#             'noTelp': noTelp
            
#         })
#         message_strip = strip_tags(message)
#         to_email = email
#         email_send = EmailMultiAlternatives(
#             mail_subject, message_strip, settings.EMAIL_HOST_USER, [to_email]
#         )
#         email_send.attach_alternative(message, "text/html")
#         email_send.fail_silently = False
#         email_send.send()
#     return render(request, 'email/application_success.html', {})