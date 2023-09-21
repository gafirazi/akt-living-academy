from django.urls import path

from .views import index, add_murid, update_murid, login, data_absensi, logout, referral_codes, list_murid_referral, create_referral_code, download_excel_data

urlpatterns = [
  path('', index, name="index"),
  path('add-murid', add_murid, name="add_murid"),
  path('data-absensi', data_absensi, name="data_absensi"),
  path('update-murid', update_murid, name="update_murid"),
  path('login', login, name="login"),
  path('logout', logout, name="logout"),
  path('referral-codes', referral_codes, name="referral_codes"),
  path('list-murid-referral', list_murid_referral, name="list_murid_referral"),
  path('create-referral-code', create_referral_code, name="create_referral_code"),
  path('download-excel-data', download_excel_data, name="download_excel_data"),
]