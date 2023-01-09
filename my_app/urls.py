from django.urls import path

from . import views

urlpatterns = [

    path('admin_page/', views.admin_page, name='admin_page'),
    path('', views.gateway, name='gateway'),  # one only ... blank ('')

    path('create_contract/', views.create_contract, name='create_contract'),

    path('billing/', views.billing, name='billing'),

    path('payment_individual/', views.payment_individual, name='payment_individual'),
    path('pay_rent/str<bref>/', views.pay_rent, name='pay_rent'),

    path('report_type/', views.report_type, name='report_type'),
    path('report_parameters/', views.report_parameters, name='report_parameters'),
    path('current_tenant/', views.current_tenant, name='current_tenant'),
    path('extra_service/', views.extra_service, name='extra_service'),
    path('elec_cpu_change/', views.elec_cpu_change, name='elec_cpu_change'),
    path('water_cpu_change/', views.water_cpu_change, name='water_cpu_change'),
    path('room_type_rate/', views.room_type_rate, name='room_type_rate'),
    path('current_tenant/', views.current_tenant, name='current_tenant'),
    path('vacant_rooms/', views.vacant_rooms, name='vacant_rooms'),
    path('monthly_report_mini/', views.monthly_report_mini, name='monthly_report_mini'),

    path('misc_contents/', views.misc_contents, name='misc_contents'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('user_list_to_delete/', views.user_list_to_delete, name='user_list_to_delete'),
    path('delete_user/<str:rmn>/', views.delete_user, name='delete_user'),
    path('confirm_delete_user/<str:k>/', views.confirm_delete_user, name='confirm_delete_user'),
    path('register/', views.Register.as_view(), name='register'),
    path('register/done/', views.register_done, name='register_done'),
    path('change_password/', views.change_password, name='change_password'),

    path('maintenance_charge/', views.maintenance_charge, name='maintenance_charge'),

    path('new_tenant/', views.new_tenant, name='new_tenant'),
    path('tenant_profile/', views.tenant_profile, name='tenant_profile'),
    path('tenant_bill/', views.tenant_bill, name='tenant_bill'),
    path('tenant_feedback/', views.tenant_feedback, name='tenant_feedback'),

    # path('payment/', views.payment, name='payment'),
    # path('register new users/', views.Register_new_users, name='register_new_users'),
    # path('confirm_delete/', views.confirm_delete, name='confirm_delete'),
    # path('reset_password/', views.reset_password, name='reset_password'),
    # path('tenant_page/', views.tenant_page, name='tenant_page'),
    # path('monthly_report/', views.monthly_report, name='monthly_report'),
    # path('tenant_comment/', views.tenant_comment, name='tenant_comment'),
    # path('send_sms_to_individual_room/', views.send_sms_to_individual_room, name='send_sms_to_individual_room'),
    # path('send_general_sms/', views.send_general_sms, name='send_general_sms'),
    # path('send_bill_sms_to_all_tenants/', views.send_bill_sms_to_all_tenants, name='send_bill_sms_to_all_tenants'),
    # path('tenant_bill/', views.tenant_bill, name='tenant_bill'),

    # path('confirmation/', views.send_sms_confirmation, name='confirmation'),
    # path('send_sms_execution/', views.send_sms_execution, name='send_sms_execution'),

]
