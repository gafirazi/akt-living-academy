from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.http import HttpResponse, QueryDict
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages

# import traceback, xlwt, datetime, json
# from datetime import date

from .middleware import is_superuser
from .models import Murid, ReferralCode
from .utils import get_new_nim

from .data import program_studis


from django.contrib.auth.decorators import login_required
# Create your views here.
import pytz

def login(request):
    if request.method == 'POST':
        data = request.POST

        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            print('berhasil bray')
            auth_login(request, user)
            return redirect('/backoffice')
        else:
            print('gagal bray')
            return render(request, 'login.html')

    else:
        if request.user.is_authenticated:
            return redirect('/backoffice')
        return render(request, 'login.html')

@csrf_exempt
def add_murid(request):
    if request.method == "POST":
        print('masuk POST')
        try:
            data = request.POST
            # data = json.loads(list(data.keys())[0])
            # print('1')
            # print('test', type(json.loads(list(data.keys())[0])))
            programStudi = data["programStudi"]
            # print('2')
            hargaProgram = data["hargaProgram"]
            namaLengkap = data["namaLengkap"]
            alamatLengkap = data["alamatLengkap"]
            tanggal = data["tanggal"]
            bulan = data["bulan"]
            tahun = data["tahun"]
            jenisKelamin = data["jenisKelamin"]
            noTelp = data["noTelp"]
            email = data['email']
            referral_code = data["referralCode"]
            hariBelajar = data['hariBelajar']
            jamBelajar = data['jamBelajar']

            print('selesai post data')

            print('tahun' + ' ' + str(tahun))
            print('bulan' + ' ' + str(int(bulan)))
            print('tanggal' + ' ' + str(tanggal))

            # insert to DB
            # new_date = date(int(tahun), int(bulan), int(tanggal))
            new_date = 'test'

            nim = get_new_nim(programStudi)

            murid = Murid(program_studi=programStudi, harga_program=hargaProgram, nama=namaLengkap, nim=nim, alamat=alamatLengkap, tanggal_lahir=new_date, email=email, jenis_kelamin=jenisKelamin, no_telp=noTelp, sudah_bayar=False, accepted=False, referral_code=referral_code, hari_belajar=hariBelajar, jam_belajar=jamBelajar)
            murid.save()

            print('berhasil save')

        except Exception as e:
            print(e)

        # except Exception as e:
        #     print('gagal', e)
        #     # with open('log.txt', 'w') as file:
        #     #     file.write(e)
        #     #     file.write("---------------")
        #     #     file.write(e.args)
        #     filez = open('loggagal.txt', 'w')
        #     filez.write(traceback.format_exc())
        #     filez.close()

    return HttpResponse(status=200)

@login_required
@is_superuser
@csrf_exempt
def index(request):
    messages = get_messages(request)
    show_toast = True if len(messages) > 0 else False
    if len(messages) > 0:
        for message in messages:
            toast_message = message
            break
    else:
        toast_message = ''
    murids = Murid.objects.all()
    print(pytz.all_timezones_set)
    return render(request, 'index.html', {
        'murids': murids,
        'show_toast': show_toast,
        'message': toast_message,
        'is_superuser': request.user.is_superuser
    })

@login_required
@is_superuser
def update_murid(request):
    if request.method == 'POST':
        data = request.POST
        # print(data)
        # print('id', data['id'])
        # print(data['radioSudahBayar'])
        # print(data['radioDiterima'])

        selected_murid = Murid.objects.get(id = data['id'])
        
        if data['radioSudahBayar'] == "True":
            selected_murid.sudah_bayar = True
        elif data['radioSudahBayar'] == "False":
            selected_murid.sudah_bayar = False

        selected_murid.last_updated_by = request.user.username
        
        selected_murid.save()
        messages.success(request, 'Data berhasil diubah!')
        # storage = get_messages(request)
        # print('storage')
        # print(storage)
        # for message in storage:
        #     print(message.message)
    
    return redirect('/backoffice')
    # murids = Murid.objects.all()
    # return render(request, 'index.html', {
    #     'murids': murids
    # })

@login_required
@is_superuser
def data_absensi(request):
    if len(request.GET) == 0:
        program_studi = "Personal Branding"
    else:
        program_studi = request.GET['programStudi']
    murids = Murid.objects.filter(sudah_bayar = True, program_studi=program_studi)
    messages = get_messages(request)
    show_toast = True if len(messages) > 0 else False
    if len(messages) > 0:
        for message in messages:
            toast_message = message
            break
    else:
        toast_message = ''
    return render(request, 'data_absensi.html', {
        'murids': murids,
        'program_studis': program_studis,
        'selected_program_studi': program_studi,
        'show_toast': show_toast,
        'message': toast_message,
        'is_superuser': request.user.is_superuser
    })

@login_required
@is_superuser
def referral_codes(request):
    referral_codes = ReferralCode.objects.all()
    users = User.objects.filter(is_superuser = False)
    messages = get_messages(request)
    show_toast = True if len(messages) > 0 else False
    if len(messages) > 0:
        print('masukz')
        for message in messages:
            toast_message = message
            break
    else:
        print('ga masukz')
        toast_message = ''
    return render(request, 'referral_codes.html', {
        'referral_codes': referral_codes,
        'users': users,
        'show_toast': show_toast,
        'message': toast_message,
        'is_superuser': request.user.is_superuser
    })

@login_required
def list_murid_referral(request):
    # print('get query params', request.GET)
    print(get_new_nim('Personal Branding'))
    if request.user.is_superuser:
        referral_codes = ReferralCode.objects.all()
        if len(request.GET) == 0 and len(referral_codes) > 0:
            referral_code = referral_codes[0].code
        elif len(referral_codes) == 0:
            referral_code = ''
        else:
            referral_code = request.GET['referralCode']
    else:
        referral_codes = ReferralCode.objects.filter(owner = request.user.username)

        if len(referral_codes) == 0:
            referral_code = ''
        elif len(request.GET) == 0:
            referral_code = referral_codes[0].code
        else:
            referral_code = request.GET['referralCode']

    murids = Murid.objects.filter(sudah_bayar = True, referral_code = referral_code)

    return render(request, 'list_murid_referral.html', {
        'murids': murids,
        'referral_codes': referral_codes,
        'selected_referral_code': referral_code,
        'is_superuser': request.user.is_superuser
    })

@login_required
def create_referral_code(request):
    if request.method == "POST":
        data = request.POST

        print(data.keys())

        referral_code = ReferralCode(code = data['referralCode'], owner = data['owner'],created_by = request.user.username)
        referral_code.save()
        messages.success(request, 'Referral code berhasil ditambahkan!')

        return redirect('/backoffice/referral-codes')
        
def download_excel_data(request):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')
    
    # today = datetime.datetime.now()
    
    # #accessing the year attribute
    # year = today.year

    if len(request.GET) == 0:
        program_studi = "Personal Branding"
    else:
        program_studi = request.GET['programStudi']
    
    # #decide file name
    # response['Content-Disposition'] = 'attachment; filename="data_absensi_{}_{}.xls"'.format(program_studi, year)
    
    # #creating workbook
    # wb = xlwt.Workbook(encoding='utf-8')
    
    # #adding sheet
    # ws = wb.add_sheet("Sheet1")
    
    # # Sheet header, first row
    # row_num = 0
    
    # font_style = xlwt.XFStyle()
    # # headers are bold
    # font_style.font.bold = True
    
    # #column header names, you can use your own headers here
    # columns = ['No', 'Nama', 'NIM', 'Tanda Tangan', ]
    
    # #write column headers in sheet
    # for col_num in range(len(columns)):
    #     ws.write(row_num, col_num, columns[col_num], font_style)
        
    # # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()
    
    # #get your data, from database or from a text file...
    # data = Murid.objects.filter(sudah_bayar = True, program_studi = program_studi)
    
    # for my_row in data:
    #     row_num = row_num + 1
    #     ws.write(row_num, 0, row_num, font_style)
    #     ws.write(row_num, 1, my_row.nama, font_style)
    #     ws.write(row_num, 2, my_row.nim, font_style)
    #     ws.write(row_num, 3, "", font_style)
        
    # wb.save(response)
    # return response
    return True

def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('/backoffice/login')