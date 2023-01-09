from .forms import PaymentForm
from .forms import Elec_cpu_change, Water_cpu_change
from .forms import MaintenanceForm
from .models import Extra, Room, Room_type
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from django.shortcuts import get_object_or_404
from .forms import RM101A_BillForm, RM102A_BillForm, RM103A_BillForm, RM104A_BillForm, RM105A_BillForm, RM106A_BillForm
from .forms import RM201A_BillForm, RM202A_BillForm, RM203A_BillForm, RM204A_BillForm, RM205A_BillForm, RM206A_BillForm
from .forms import RM301A_BillForm, RM302A_BillForm, RM303A_BillForm, RM304A_BillForm, RM305A_BillForm, RM306A_BillForm
from .forms import RM201B_BillForm, RM202B_BillForm, RM203B_BillForm, RM204B_BillForm, RM205B_BillForm
from .forms import RM301B_BillForm, RM302B_BillForm, RM303B_BillForm, RM304B_BillForm, RM305B_BillForm
from .forms import RM401B_BillForm, RM402B_BillForm, RM403B_BillForm, RM404B_BillForm, RM405B_BillForm
from my_app.models import Billing
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import TenantCreateForm, TenantProfileCreateForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from users.forms import CustomUserCreationForm
from my_app.models import TenantProfile
from django.contrib.auth import get_user_model


import random
import calendar
import datetime
import decimal
import GV

CUser = get_user_model()


class CholladaHomePage(TemplateView):
    template_name = 'my_app/Chollada_Apartment.html'  # default template if not defined in the url


@login_required
def gateway(request):
    return render(request, 'my_app/admin_page.html')


@login_required
def admin_page(request):
    return render(request, 'my_app/admin_page.html')


@login_required
def create_contract(request):
    if request.method == 'POST':
        tenant_form = TenantCreateForm(data=request.POST)
        # tenant_profile_form = TenantProfileCreateForm(data=request.POST, files=request.FILES)
        tenant_profile_form = TenantProfileCreateForm(data=request.POST, files=request.FILES)

        if tenant_form.is_valid() and tenant_profile_form.is_valid():

            # Create a new tenant object but avoid saving it yet
            new_tenant = tenant_form.save(commit=False)

            # Set the chosen password
            # new_tenant.set_password(tenant_form.cleaned_data['password'])
            new_tenant.set_password(tenant_form.clean_password2())

            # Save the new_tenant object
            new_tenant.save()

            # Create a new tenantprofile object but avoid saving it yet
            tenant_profile = tenant_profile_form.save(commit=False)  # save_m2m() added to tenant_profile_form

            # Set the chosen tenant field
            tenant_profile.tenant = new_tenant

            # ------------------------------------------
            # provide initial value to certain fields before saving to DB
            tenant_profile.elec_unit = 0
            tenant_profile.water_unit = 0
            tenant_profile.misc_cost = 0
            # -----------------------------------------

            # Save the tenantprofile object
            tenant_profile.save()

            # Save the ManyToMany
            tenant_profile_form.save_m2m()

            messages.success(request, 'Profile has been updated successfully')

            return HttpResponseRedirect(reverse_lazy('admin_page'))
        else:
            messages.error(request, 'Error updating your tenant_profile')

    else:
        tenant_form = TenantCreateForm()
        # tenant_profile_form = TenantProfileCreateForm()
        tenant_profile_form = TenantProfileCreateForm()

    return render(request, 'my_app/create_contract.html',
                  {'section': 'new_contract',
                   'tenant_form': tenant_form,
                   'tenant_profile_form': tenant_profile_form
                   }
                  )


# @login_required # ????? #ORIGINAL
def create_bill(room_no):
    pf = get_object_or_404(TenantProfile, room_no__room_no=room_no)
    tname = pf.tenant.first_name + ' ' + pf.tenant.last_name

    rno = pf.room_no.room_no
    adj = pf.adjust

    exd = {}
    exd.setdefault('Electricity CPU', 0)
    exd.setdefault('Water CPU', 0)
    exd.setdefault('Garbage', 0)
    exd.setdefault('Parking', 0)
    exd.setdefault('Wifi', 0)
    exd.setdefault('Cable TV', 0)
    exd.setdefault('Bed', 0)
    exd.setdefault('Bed accessories', 0)
    exd.setdefault('Dressing Table', 0)
    exd.setdefault('Clothing Cupboard', 0)
    exd.setdefault('TV Table', 0)
    exd.setdefault('Fridge', 0)
    exd.setdefault('Air-Conditioner', 0)

    for e in pf.extra.all():
        exd.update({e.desc: e.cpu})

    room_cost = pf.room_no.room_type.rate
    room_acc_cost = exd['Bed'] + exd['Bed accessories'] + exd['Dressing Table'] \
                    + exd['Clothing Cupboard'] + exd['TV Table'] + exd['Fridge'] \
                    + exd['Air-Conditioner']

    elec_cost = exd['Electricity CPU'] * pf.elec_unit
    water_cost = exd['Water CPU'] * pf.water_unit

    com_ser_cost = pf.elec_unit * GV.COMMOM_SERVICE_CPU

    oth_ser_cost = exd['Garbage'] + exd['Parking'] + exd['Wifi'] + exd['Cable TV']
    ovd_amt = pf.cum_ovd

    # -----------------------
    late_f = pf.late_fee
    maint_c = pf.maint_cost

    # RESET pf.late_fee & pf.maint_cost TO O TO BE READY FOR NEXT CYCLE
    pf.late_fee = 0
    pf.maint_cost = 0
    # -----------------------

    total = room_cost + room_acc_cost + elec_cost + water_cost + com_ser_cost + oth_ser_cost + ovd_amt + adj + late_f + maint_c

    # CREATE PRELIMINARY BILL OBJECT **************
    new_bill = Billing(bill_ref=get_ref_string(),
                       bill_date=datetime.datetime.now().date(),  # SUPPLY BILL DATE
                       tenant_name=tname,
                       room_no=rno,
                       room_cost=room_cost,
                       room_acc_cost=room_acc_cost,
                       electricity_cost=elec_cost,
                       water_cost=water_cost,
                       common_ser_cost=com_ser_cost,
                       other_ser_cost=oth_ser_cost,
                       overdue_amount=ovd_amt,

                       # -----------------------
                       late_fee=late_f,
                       maint_cost=maint_c,
                       # -----------------------

                       adjust=adj,
                       bill_total=total,

                       )

    # SAVE TENANTPROFILE OBJECT TO DB
    pf.save()

    # ADJUST PRELIMINARY BILL OBJECT
    adjust_bill(pf, new_bill)


def adjust_bill(pf, new_bill):
    tn_bill = new_bill

    bref = tn_bill.bill_ref
    bdate = tn_bill.bill_date
    # bupd # TO BE FILLED WHEN SAVED
    # bstat # TO BE FILLED WHEN SAVED
    tname = tn_bill.tenant_name
    rno = tn_bill.room_no
    room_cost = tn_bill.room_cost
    room_acc_cost = tn_bill.room_acc_cost
    elec_cost = tn_bill.electricity_cost
    water_cost = tn_bill.water_cost
    com_ser_cost = tn_bill.common_ser_cost
    oth_ser_cost = tn_bill.other_ser_cost
    ovd_amt = tn_bill.overdue_amount
    adj = tn_bill.adjust
    # total = tn_bill.bill_total # TO BE ADJUSTED IF REQUIRED

    # pay_date # TO BE FILLED AT PAYMENT
    # pay_amt #TO BE FILL AT PAYMENT
    # bf #TO BE FILLED AT PAYMENT

    late_f = tn_bill.late_fee
    maint_c = tn_bill.maint_cost

    sdate = pf.start_date  # FROM pf

    start_day = sdate.day
    bill_day = bdate.day

    start_m = sdate.month
    bill_m = bdate.month

    number_of_day_in_start_month = calendar.monthrange(sdate.year, sdate.month)[1]
    nodsm = number_of_day_in_start_month
    number_of_day_in_bill_month = calendar.monthrange(bdate.year, bdate.month)[1]
    nodbm = number_of_day_in_bill_month

    # Original Version-Bug !!! =====================================================================================
    #    if abs(start_m - bill_m) == 0:
    #        tbd = number_of_day_in_bill_month - start_day + 1  # SPECIAL CASE 1
    #    elif abs(start_m - bill_m) == 1 and start_day >= bill_day:
    #        tbd = number_of_day_in_bill_month + (number_of_day_in_start_month - start_day + 1)  # SPECIAL CASE 2
    #    else:
    #        tbd = number_of_day_in_bill_month  # ONGOING CASE
    # ======================================================================================

    # Revised-Corrected Version
    # EDITED CORRECTED  --------------------------------------------------------------------
    #    tbd = 0
    #    if sdate.year == bdate.year:
    #        if abs(start_m - bill_m) == 0:  # SAME MONTH
    #            tbd = number_of_day_in_bill_month - start_day + 1  # SPECIAL CASE 1
    #        elif abs(start_m - bill_m) == 1 and start_day >= bill_day:
    #            tbd = number_of_day_in_bill_month + (number_of_day_in_start_month - start_day + 1)  # SPECIAL CASE 2
    #    else:
    #        if start_m == 12 and sdate.year + 1 == bdate.year and start_day >= bill_day:  # DECEMBER/YEAR CHANGE
    #            tbd = number_of_day_in_bill_month + (number_of_day_in_start_month - start_day + 1)  # SPECIAL CASE 3
    #        else:
    #            tbd = number_of_day_in_bill_month  # ONGOING CASE
    #

    # -------------- TEST 2 final--------------------------------------------------------------
    tbd = 0
    if sdate.year == bdate.year:
        if start_m == bill_m:  # SAME MONTH
            tbd = number_of_day_in_bill_month - start_day + 1  # CASE 1
        elif start_m + 1 == bill_m and start_day >= bill_day:
            tbd = number_of_day_in_bill_month + (number_of_day_in_start_month - start_day + 1)  # CASE 2
        else:
            tbd = tbd = number_of_day_in_bill_month  # ONGOING CASE
    else:
        if (start_m == 12) and (sdate.year + 1 == bdate.year) and (bill_m == 1) and (
                start_day >= bill_day):  # DECEMBER/YEAR CHANGE
            tbd = number_of_day_in_bill_month + (number_of_day_in_start_month - start_day + 1)  # CASE 3
        else:
            tbd = number_of_day_in_bill_month  # ONGOING CASE

    # -----------------------------------------------------------------------------------

    # ADJUST CERTAIN VALUES IN PRELIM. BILL OBJECT
    const = decimal.Decimal((tbd / nodbm))

    room_cost = room_cost * const
    room_acc_cost = room_acc_cost * const
    com_ser_cost = com_ser_cost * const
    oth_ser_cost = oth_ser_cost * const
    adj = adj * const

    total = (room_cost + room_acc_cost + adj) + elec_cost + water_cost + (
            com_ser_cost + oth_ser_cost) + ovd_amt + late_f + maint_c

    # CREATE FINAL BILL OBJECT *******************
    new_bill = Billing(bill_ref=bref,
                       tenant_name=tname,
                       room_no=rno,
                       room_cost=room_cost,
                       room_acc_cost=room_acc_cost,
                       electricity_cost=elec_cost,
                       water_cost=water_cost,
                       common_ser_cost=com_ser_cost,
                       other_ser_cost=oth_ser_cost,
                       overdue_amount=ovd_amt,

                       # -----------------------
                       late_fee=late_f,
                       maint_cost=maint_c,
                       # -----------------------

                       adjust=adj,
                       bill_total=total,

                       )

    # SAVE BILL OBJECT TO DB
    new_bill.save()


@login_required
def billing(request):
    # bill_date=curdate
    cur_date = datetime.datetime.now().date()

    # ------------------------------------
    tenant_pf = TenantProfile.objects.filter(start_date__lt=cur_date).order_by("room_no")
    # ------------------------------------
    # tenant_pf = TenantProfile.objects.order_by("room_no")

    rm101a_form = None
    rm102a_form = None
    rm103a_form = None
    rm104a_form = None
    rm105a_form = None
    rm106a_form = None

    rm201a_form = None
    rm202a_form = None
    rm203a_form = None
    rm204a_form = None
    rm205a_form = None
    rm206a_form = None

    rm301a_form = None
    rm302a_form = None
    rm303a_form = None
    rm304a_form = None
    rm305a_form = None
    rm306a_form = None

    rm201b_form = None
    rm202b_form = None
    rm203b_form = None
    rm204b_form = None
    rm205b_form = None

    rm301b_form = None
    rm302b_form = None
    rm303b_form = None
    rm304b_form = None
    rm305b_form = None

    rm401b_form = None
    rm402b_form = None
    rm403b_form = None
    rm404b_form = None
    rm405b_form = None

    no_of_bill = 0
    for tpf in tenant_pf:
        rmn = tpf.room_no.room_no

        if request.method == 'POST':

            if rmn == '101A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm101a_form = RM101A_BillForm(data=request.POST, instance=pf, prefix='rm101a')
                if rm101a_form.is_valid():
                    rm101a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)

                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 101A Billing')
            if rmn == '102A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm102a_form = RM102A_BillForm(data=request.POST, instance=pf, prefix='rm102a')
                if rm102a_form.is_valid():
                    rm102a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 102A Billing')
            if rmn == '103A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm103a_form = RM103A_BillForm(data=request.POST, instance=pf, prefix='rm103a')
                if rm103a_form.is_valid():
                    rm103a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 103A Billing')

            if rmn == '104A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm104a_form = RM104A_BillForm(data=request.POST, instance=pf, prefix='rm104a')
                if rm104a_form.is_valid():
                    rm104a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 104A Billing')

            if rmn == '105A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm105a_form = RM105A_BillForm(data=request.POST, instance=pf, prefix='rm105a')
                if rm105a_form.is_valid():
                    rm105a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 105A Billing')

            if rmn == '106A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm106a_form = RM106A_BillForm(data=request.POST, instance=pf, prefix='rm106a')
                if rm106a_form.is_valid():
                    rm106a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 106A Billing')

            if rmn == '201A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm201a_form = RM201A_BillForm(data=request.POST, instance=pf, prefix='rm201a')
                if rm201a_form.is_valid():
                    rm201a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 201A Billing')

            if rmn == '202A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm202a_form = RM202A_BillForm(data=request.POST, instance=pf, prefix='rm202a')
                if rm202a_form.is_valid():
                    rm202a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 202A Billing')

            if rmn == '203A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm203a_form = RM203A_BillForm(data=request.POST, instance=pf, prefix='rm203a')
                if rm203a_form.is_valid():
                    rm203a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 203A Billing')

            if rmn == '204A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm204a_form = RM204A_BillForm(data=request.POST, instance=pf, prefix='rm204a')
                if rm204a_form.is_valid():
                    rm204a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 204A Billing')

            if rmn == '205A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm205a_form = RM205A_BillForm(data=request.POST, instance=pf, prefix='rm205a')
                if rm205a_form.is_valid():
                    rm205a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 205A Billing')

            if rmn == '206A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm206a_form = RM206A_BillForm(data=request.POST, instance=pf, prefix='rm206a')
                if rm206a_form.is_valid():
                    rm206a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 206A Billing')

            if rmn == '301A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm301a_form = RM301A_BillForm(data=request.POST, instance=pf, prefix='rm301a')
                if rm301a_form.is_valid():
                    rm301a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 301A Billing')

            if rmn == '302A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm302a_form = RM302A_BillForm(data=request.POST, instance=pf, prefix='rm302a')
                if rm302a_form.is_valid():
                    rm302a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 302A Billing')

            if rmn == '303A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm303a_form = RM303A_BillForm(data=request.POST, instance=pf, prefix='rm303a')
                if rm303a_form.is_valid():
                    rm303a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 303A Billing')

            if rmn == '304A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm304a_form = RM304A_BillForm(data=request.POST, instance=pf, prefix='rm304a')
                if rm304a_form.is_valid():
                    rm304a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 304A Billing')

            if rmn == '305A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm305a_form = RM305A_BillForm(data=request.POST, instance=pf, prefix='rm305a')
                if rm305a_form.is_valid():
                    rm305a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 305A Billing')

            if rmn == '306A':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm306a_form = RM306A_BillForm(data=request.POST, instance=pf, prefix='rm306a')
                if rm306a_form.is_valid():
                    rm306a_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 306A Billing')

            if rmn == '201B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm201b_form = RM201B_BillForm(data=request.POST, instance=pf, prefix='rm201b')
                if rm201b_form.is_valid():
                    rm201b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 201B Billing')

            if rmn == '202B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm202b_form = RM202B_BillForm(data=request.POST, instance=pf, prefix='rm202b')
                if rm202b_form.is_valid():
                    rm202b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 202B Billing')

            if rmn == '203B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm203b_form = RM203B_BillForm(data=request.POST, instance=pf, prefix='rm203b')
                if rm203b_form.is_valid():
                    rm203b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 203B Billing')

            if rmn == '204B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm204b_form = RM204B_BillForm(data=request.POST, instance=pf, prefix='rm204b')
                if rm204b_form.is_valid():
                    rm204b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 204B Billing')

            if rmn == '205B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm205b_form = RM205B_BillForm(data=request.POST, instance=pf, prefix='rm205b')
                if rm205b_form.is_valid():
                    rm205b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 205B Billing')

            if rmn == '301B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm301b_form = RM301B_BillForm(data=request.POST, instance=pf, prefix='rm301b')
                if rm301b_form.is_valid():
                    rm301b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 301B Billing')

            if rmn == '302B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm302b_form = RM302B_BillForm(data=request.POST, instance=pf, prefix='rm302b')
                if rm302b_form.is_valid():
                    rm302b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 302B Billing')

            if rmn == '303B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm303b_form = RM303B_BillForm(data=request.POST, instance=pf, prefix='rm303b')
                if rm303b_form.is_valid():
                    rm303b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 303B Billing')

            if rmn == '304B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm304b_form = RM304B_BillForm(data=request.POST, instance=pf, prefix='rm304b')
                if rm304b_form.is_valid():
                    rm304b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 304B Billing')

            if rmn == '305B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm305b_form = RM305B_BillForm(data=request.POST, instance=pf, prefix='rm305b')
                if rm305b_form.is_valid():
                    rm305b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 305B Billing')

            if rmn == '401B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm401b_form = RM401B_BillForm(data=request.POST, instance=pf, prefix='rm401b')
                if rm401b_form.is_valid():
                    rm401b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 401B Billing')

            if rmn == '402B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm402b_form = RM402B_BillForm(data=request.POST, instance=pf, prefix='rm402b')
                if rm402b_form.is_valid():
                    rm402b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 402B Billing')

            if rmn == '403B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm403b_form = RM403B_BillForm(data=request.POST, instance=pf, prefix='rm403b')
                if rm403b_form.is_valid():
                    rm403b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 403B Billing')

            if rmn == '404B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm404b_form = RM404B_BillForm(data=request.POST, instance=pf, prefix='rm404b')
                if rm404b_form.is_valid():
                    rm404b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 404B Billing')

            if rmn == '405B':
                pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)
                rm405b_form = RM405B_BillForm(data=request.POST, instance=pf, prefix='rm405b')
                if rm405b_form.is_valid():
                    rm405b_form.save(commit=True)
                    # -------------------
                    create_bill(rmn)
                    no_of_bill += 1
                    # ------------------
                else:
                    messages.error(request, 'Error updating Room 405B Billing')

        else:
            if rmn == '101A':
                rm101a_form = RM101A_BillForm(prefix='rm101a')

            if rmn == '102A':
                rm102a_form = RM102A_BillForm(prefix='rm102a')

            if rmn == '103A':
                rm103a_form = RM103A_BillForm(prefix='rm103a')

            if rmn == '104A':
                rm104a_form = RM104A_BillForm(prefix='rm104a')

            if rmn == '105A':
                rm105a_form = RM105A_BillForm(prefix='rm105a')

            if rmn == '106A':
                rm106a_form = RM106A_BillForm(prefix='rm106a')

            if rmn == '201A':
                rm201a_form = RM201A_BillForm(prefix='rm201a')

            if rmn == '202A':
                rm202a_form = RM202A_BillForm(prefix='rm202a')

            if rmn == '203A':
                rm203a_form = RM203A_BillForm(prefix='rm203a')

            if rmn == '204A':
                rm204a_form = RM204A_BillForm(prefix='rm204a')

            if rmn == '205A':
                rm205a_form = RM205A_BillForm(prefix='rm205a')

            if rmn == '206A':
                rm206a_form = RM206A_BillForm(prefix='rm206a')

            if rmn == '301A':
                rm301a_form = RM301A_BillForm(prefix='rm301a')

            if rmn == '302A':
                rm302a_form = RM302A_BillForm(prefix='rm302a')

            if rmn == '303A':
                rm303a_form = RM303A_BillForm(prefix='rm303a')

            if rmn == '304A':
                rm304a_form = RM304A_BillForm(prefix='rm304a')

            if rmn == '305A':
                rm305a_form = RM305A_BillForm(prefix='rm305a')

            if rmn == '306A':
                rm306a_form = RM306A_BillForm(prefix='rm306a')

            if rmn == '201B':
                rm201b_form = RM201B_BillForm(prefix='rm201b')

            if rmn == '202B':
                rm202b_form = RM202B_BillForm(prefix='rm202b')

            if rmn == '203B':
                rm203b_form = RM203B_BillForm(prefix='rm203b')

            if rmn == '204B':
                rm204b_form = RM204B_BillForm(prefix='rm204b')

            if rmn == '205B':
                rm205b_form = RM205B_BillForm(prefix='rm205b')

            if rmn == '301B':
                rm301b_form = RM301B_BillForm(prefix='rm301b')

            if rmn == '302B':
                rm302b_form = RM302B_BillForm(prefix='rm302b')

            if rmn == '303B':
                rm303b_form = RM303B_BillForm(prefix='rm303b')

            if rmn == '304B':
                rm304b_form = RM304B_BillForm(prefix='rm304b')

            if rmn == '305B':
                rm305b_form = RM305B_BillForm(prefix='rm305b')

            if rmn == '401B':
                rm401b_form = RM401B_BillForm(prefix='rm401b')

            if rmn == '402B':
                rm402b_form = RM402B_BillForm(prefix='rm402b')

            if rmn == '403B':
                rm403b_form = RM403B_BillForm(prefix='rm403b')

            if rmn == '404B':
                rm404b_form = RM404B_BillForm(prefix='rm404b')

            if rmn == '405B':
                rm405b_form = RM405B_BillForm(prefix='rm405b')

    if request.method == 'POST':

        # WRITE TO BILL SUMMARY AND BILL SLIP (Localhost only, at this time !!!!)
        # create_exel_sheet(request)

        # -----------------
        # FOR PYTHONANYWHERE HOST (uncomment the following line !!)
        messages.success(request, 'Total {} bills have been created.'.format(no_of_bill))
        # -----------------
        return HttpResponseRedirect(reverse_lazy('admin_page'))
    else:
        return render(request, 'my_app/billing.html', {'tenant_pf': tenant_pf, 'section': 'billing',
                                                       'rm101a_form': rm101a_form,
                                                       'rm102a_form': rm102a_form,
                                                       'rm103a_form': rm103a_form,
                                                       'rm104a_form': rm104a_form,
                                                       'rm105a_form': rm105a_form,
                                                       'rm106a_form': rm106a_form,

                                                       'rm201a_form': rm201a_form,
                                                       'rm202a_form': rm202a_form,
                                                       'rm203a_form': rm203a_form,
                                                       'rm204a_form': rm204a_form,
                                                       'rm205a_form': rm205a_form,
                                                       'rm206a_form': rm206a_form,

                                                       'rm301a_form': rm301a_form,
                                                       'rm302a_form': rm302a_form,
                                                       'rm303a_form': rm303a_form,
                                                       'rm304a_form': rm304a_form,
                                                       'rm305a_form': rm305a_form,
                                                       'rm306a_form': rm306a_form,

                                                       'rm201b_form': rm201b_form,
                                                       'rm202b_form': rm202b_form,
                                                       'rm203b_form': rm203b_form,
                                                       'rm204b_form': rm204b_form,
                                                       'rm205b_form': rm205b_form,

                                                       'rm301b_form': rm301b_form,
                                                       'rm302b_form': rm302b_form,
                                                       'rm303b_form': rm303b_form,
                                                       'rm304b_form': rm304b_form,
                                                       'rm305b_form': rm305b_form,

                                                       'rm401b_form': rm401b_form,
                                                       'rm402b_form': rm402b_form,
                                                       'rm403b_form': rm403b_form,
                                                       'rm404b_form': rm404b_form,
                                                       'rm405b_form': rm405b_form,

                                                       })


# @login_required (cannot be used here !!!)
def update_pf_and_bill(roomno, cd):
    pf = get_object_or_404(TenantProfile, room_no__room_no=roomno)
    bill = get_object_or_404(Billing, room_no=roomno, status='open')

    cf = bill.bill_total - cd['payment_amount']
    bill.cf_amount = cf
    pf.cum_ovd = cf
    bill.payment_date = cd['payment_date']
    bill.payment_amount = cd['payment_amount']
    bill.status = 'close'

    # CALCULATE LATE-FEE COST TO UPDATE PF.LATE_FEE
    bill_month = bill.bill_date.month

    pay_month = bill.payment_date.month
    pay_day = bill.payment_date.day

    late_fee = 0

    if pay_month > bill_month:
        if pay_day > GV.LATE_DAY_MAX:
            late_fee = GV.LATE_FEE_PER_DAY * (pay_day - GV.LATE_DAY_MAX)

    # Update pf for next billing
    pf.late_fee = late_fee

    # Update DB
    bill.save()
    pf.save()


@login_required
def pay_rent(request, bref):
    tenant_bill = get_object_or_404(Billing, bill_ref=bref, status='open')
    rmn = tenant_bill.room_no

    if request.method == 'POST':
        pay_form = PaymentForm(data=request.POST)

        if pay_form.is_valid():
            cd = pay_form.cleaned_data

            # -------------------
            update_pf_and_bill(rmn, cd)
            # ------------------

        else:
            messages.error(request, 'Error updating Room {} Payment'.format(tenant_bill.room_no))

    else:
        pay_form = PaymentForm()

    if request.method == 'POST':
        messages.success(request, 'Room {}: Payment has been completed !!!'.format(rmn))
        return HttpResponseRedirect(reverse_lazy('payment_individual'))
    else:
        return render(request, 'my_app/pay_rent.html', {'tenant_bill': tenant_bill, 'pay_form': pay_form})


@login_required
def payment_individual(request):
    bills = Billing.objects.filter(status='open').order_by('id')

    # -------------------new 3 jan 23--------------------------------
    bill_m_y = ""
    if bills:
        bill_m = bills[0].bill_date.month
        bill_y = str(bills[0].bill_date.year)

        bill_m = get_eng_month_name(bill_m)

        bill_m_y = bill_m + ':' + bill_y
    # ------------------------------------------------------------

    return render(request, 'my_app/payment_individual.html',
                  {'bills': bills, 'section': 'payment_individual', 'bill_month_year': bill_m_y})


@login_required
def report_type(request):
    return render(request, 'my_app/report_type.html', {'section': 'report'})


@login_required
def report_parameters(request):
    return render(request, 'my_app/report_parameters.html', {'section': 'report'})


@login_required
def monthly_report_mini(request):
    bld = request.POST['bld']
    if bld == 'AB':
        bld = 'A&B'

    mnth = int(request.POST['month'])
    mnth_name = get_eng_month_name(mnth)
    yr = int(request.POST['year'])

    no_of_day_in_cur_month = calendar.monthrange(yr, mnth)[1]

    # --------------------------------------------------------------------------
    start_date = datetime.datetime(yr, mnth, 1)
    end_date = datetime.datetime(yr, mnth, no_of_day_in_cur_month)

    start_date = start_date.date()
    end_date = end_date.date()
    # --------------------------------------------------------------------------

    opl_a = None
    opl_b = None
    if bld == 'A':
        opl_a = Billing.objects.filter(status='close', room_no__endswith='A',
                                       bill_date__range=(start_date, end_date)).order_by('room_no')

    if bld == 'B':
        opl_b = Billing.objects.filter(status='close', room_no__endswith='B',
                                       bill_date__range=(start_date, end_date)).order_by('room_no')

    if bld == 'A&B':
        opl_a = Billing.objects.filter(status='close', room_no__endswith='A',
                                       bill_date__range=(start_date, end_date)).order_by('room_no')

        opl_b = Billing.objects.filter(status='close', room_no__endswith='B',

                                       bill_date__range=(start_date, end_date)).order_by('room_no')

    trcac_a = 0

    tec_a = 0
    twc_a = 0
    tcsc_a = 0
    tosc_a = 0
    tovd_a = 0

    tlf_ma_a = 0

    tbt_a = 0
    tpa_a = 0

    trcac_b = 0

    tec_b = 0
    twc_b = 0
    tcsc_b = 0
    tosc_b = 0
    tovd_b = 0

    tlf_ma_b = 0

    tbt_b = 0
    tpa_b = 0

    trcac_ab = 0

    tec_ab = 0
    twc_ab = 0
    tcsc_ab = 0
    tosc_ab = 0
    tovd_ab = 0

    tlf_ma_ab = 0

    tbt_ab = 0
    tpa_ab = 0

    if opl_a:
        for bill in opl_a:
            trcac_a += (bill.room_cost + bill.room_acc_cost + bill.adjust)

            tec_a += bill.electricity_cost
            twc_a += bill.water_cost
            tcsc_a += bill.common_ser_cost
            tosc_a += bill.other_ser_cost
            tovd_a += bill.overdue_amount

            tlf_ma_a += (bill.late_fee + bill.maint_cost)

            tbt_a += bill.bill_total
            tpa_a += bill.payment_amount

    if opl_b:
        for bill in opl_b:
            trcac_b += (bill.room_cost + bill.room_acc_cost + bill.adjust)

            tec_b += bill.electricity_cost
            twc_b += bill.water_cost
            tcsc_b += bill.common_ser_cost
            tosc_b += bill.other_ser_cost
            tovd_b += bill.overdue_amount

            tlf_ma_b += (bill.late_fee + bill.maint_cost)

            tbt_b += bill.bill_total
            tpa_b += bill.payment_amount

    if opl_a and opl_b:
        trcac_ab = trcac_a + trcac_b

        tec_ab = tec_a + tec_b
        twc_ab = twc_a + twc_b
        tcsc_ab = tcsc_a + tcsc_b
        tosc_ab = tosc_a + tosc_b
        tovd_ab = tovd_a + tovd_b

        tlf_ma_ab = tlf_ma_a + tlf_ma_b

        tbt_ab = tbt_a + tbt_b
        tpa_ab = tpa_a + tpa_b

    return render(request, 'my_app/monthly_report_mini.html', {'opl_a': opl_a,
                                                               'opl_b': opl_b,
                                                               'bld': bld,
                                                               'mnth_name': mnth_name,
                                                               'yr': yr,

                                                               'trcac_a': trcac_a,

                                                               'tec_a': tec_a,
                                                               'twc_a': twc_a,
                                                               'tcsc_a': tcsc_a,
                                                               'tosc_a': tosc_a,
                                                               'tovd_a': tovd_a,

                                                               'tlf_ma_a': tlf_ma_a,

                                                               'tbt_a': tbt_a,
                                                               'tpa_a': tpa_a,

                                                               'trcac_b': trcac_b,

                                                               'tec_b': tec_b,
                                                               'twc_b': twc_b,
                                                               'tcsc_b': tcsc_b,
                                                               'tosc_b': tosc_b,
                                                               'tovd_b': tovd_b,

                                                               'tlf_ma_b': tlf_ma_b,

                                                               'tbt_b': tbt_b,
                                                               'tpa_b': tpa_b,

                                                               'trcac_ab': trcac_ab,

                                                               'tec_ab': tec_ab,
                                                               'twc_ab': twc_ab,
                                                               'tcsc_ab': tcsc_ab,
                                                               'tosc_ab': tosc_ab,
                                                               'tovd_ab': tovd_ab,

                                                               'tlf_ma_ab': tlf_ma_ab,

                                                               'tbt_ab': tbt_ab,
                                                               'tpa_ab': tpa_ab,

                                                               })


@login_required
def extra_service(request):
    extra = Extra.objects.all().order_by('id')

    current_dt = datetime.datetime.now()

    return render(request, 'my_app/extra_service.html', {'extra': extra, 'current_dt': current_dt})


@login_required
def elec_cpu_change(request):
    if request.method == 'POST':
        elec_cpu_form = Elec_cpu_change(request.POST)
        if elec_cpu_form.is_valid():
            cd = elec_cpu_form.cleaned_data

            ex_item = get_object_or_404(Extra, desc='Electricity CPU')
            ex_item.cpu = cd['elec_cpu']
            ex_item.save()

            messages.info(request, 'Electricity CPU has been chnaged !!')

            return HttpResponseRedirect(reverse_lazy('admin_page'))
        else:
            messages.ERROR(request, 'Error ... !!')
    else:
        elec_cpu_form = Elec_cpu_change()
    return render(request, 'my_app/elec_cpu_change.html', {'elec_cpu_form': elec_cpu_form})


@login_required
def water_cpu_change(request):
    if request.method == 'POST':
        water_cpu_form = Water_cpu_change(request.POST)
        if water_cpu_form.is_valid():
            cd = water_cpu_form.cleaned_data

            ex_item = get_object_or_404(Extra, desc='Water CPU')
            ex_item.cpu = cd['water_cpu']
            ex_item.save()

            messages.success(request, 'Water CPU has been chnaged !!')
            return HttpResponseRedirect(reverse_lazy('admin_page'))
        else:
            messages.ERROR(request, 'Error ... !!')
    else:
        water_cpu_form = Water_cpu_change()
    return render(request, 'my_app/water_cpu_change.html', {'water_cpu_form': water_cpu_form})


@login_required
def room_type_rate(request):
    rm_type_rate = Room_type.objects.all()
    current_dt = datetime.datetime.now()

    return render(request, 'my_app/room_type_rate.html', {'rm_type_rate': rm_type_rate, 'current_dt': current_dt})


@login_required
def current_tenant(request):
    cur_tenant = TenantProfile.objects.all().order_by('start_date')

    total_tn = cur_tenant.count()

    current_dt = datetime.datetime.now()

    return render(request, 'my_app/current_tenant.html',
                  {'cur_tenant': cur_tenant, 'current_dt': current_dt, 'total_tn': total_tn})


@login_required
def vacant_rooms(request):
    current_dt = datetime.datetime.now()

    all_room = Room.objects.all()
    cur_tn = TenantProfile.objects.all()
    oc_rm_set = []
    vac_rm_set = []
    for tn in cur_tn:
        oc_rm_set.append(tn.room_no.room_no)

    for rm in all_room:
        if rm.room_no not in oc_rm_set:
            vac_rm_set.append(rm.room_no)

    return render(request, 'my_app/vacant_rooms.html', {'vac_rm_set': vac_rm_set, 'current_dt': current_dt})


@login_required
def misc_contents(request):
    return render(request, 'my_app/misc_contents.html', {'section': 'misc'})


@login_required
def manage_users(request):
    return render(request, 'my_app/manage_users.html')


class Register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register_done')
    template_name = 'registration/register.html'


def register_done(request):
    return render(request, 'registration/register_done.html')


@login_required
def change_password(request):
    return render(request, 'my_app/change_password.html')


@login_required
def user_list_to_delete(request):
    query_set_tenantprofile, sorted_normal_tenantprofile_dict = list_existing_users(request)

    return render(request, 'my_app/user_list_to_delete.html',
                  {'tenantprofiles': query_set_tenantprofile, 'dict': sorted_normal_tenantprofile_dict})


@login_required
def confirm_delete_user(request, k):
    tprofile = TenantProfile.objects.get(room_no__room_no=k)

    rmn = tprofile.room_no.room_no
    name = tprofile.tenant.first_name + " " + tprofile.tenant.last_name

    return render(request, 'my_app/confirm_delete_users.html', {'rmn': rmn, 'name': name})


@login_required
def delete_user(request, rmn):
    tprofile = TenantProfile.objects.get(room_no__room_no=rmn)
    user = tprofile.tenant
    user.delete()

    query_set_tenantprofile, sorted_normal_tenantprofile_dict = list_existing_users(request)

    return render(request, 'my_app/user_list_to_delete.html',
                  {'tenantprofiles': query_set_tenantprofile, 'dict': sorted_normal_tenantprofile_dict})


def list_existing_users(request):
    query_set_tenantprofile = TenantProfile.objects.all()

    org_tenantprofile_dict = {}
    name = ""
    for i in query_set_tenantprofile:
        name = i.tenant.first_name + " " + i.tenant.last_name
        rmn = i.room_no.room_no
        phone = i.phone
        name_phone = name + " " + '(' + phone + ')'
        org_tenantprofile_dict.update({rmn: name_phone})  # {'105A': 'Ratchada R.', ....}

    org_keys_list = list(org_tenantprofile_dict.keys())  # 105A

    reversed_keys_list = []  # 105A --> A105
    for i in org_keys_list:
        reversed_keys_list.append(i[3:4] + i[0:3])

    reversed_tenantprofile_dict = {}  # {'A105': 'Ratchada R.', ....}
    org_vals_list = list(org_tenantprofile_dict.values())

    for i in range(0, len(org_keys_list)):
        reversed_tenantprofile_dict.update({reversed_keys_list[i]: org_vals_list[i]})

    reversed_keys_list = list(reversed_tenantprofile_dict.keys())
    reversed_keys_list.sort()

    sorted_reversed_dict = {}

    sorted_reversed_dict.update({i: reversed_tenantprofile_dict[i] for i in reversed_keys_list})

    sorted_reversed_keys_list = list(sorted_reversed_dict.keys())
    sorted_reversed_vals_list = list(sorted_reversed_dict.values())

    normal_keys_list = []  # A105 --> 105A

    for i in sorted_reversed_keys_list:
        normal_keys_list.append(i[1:] + i[0:1])

    sorted_normal_tenantprofile_dict = {}  # {'105A': 'Ratchada R.', ....}
    for i in range(0, len(sorted_reversed_keys_list)):
        sorted_normal_tenantprofile_dict.update({normal_keys_list[i]: sorted_reversed_vals_list[i]})

    return query_set_tenantprofile, sorted_normal_tenantprofile_dict


def maintenance_charge(request):
    if request.method == 'POST':

        maintenance_form = MaintenanceForm(data=request.POST)

        if maintenance_form.is_valid():

            cd = maintenance_form.cleaned_data

            # Create a new object but avoid saving it yet
            new_ma_charge = maintenance_form.save(commit=False)

            new_ma_charge.desc = 'Maintenance cost'

            # Save the new object(MaintenanceCharge) to DB for ref.
            new_ma_charge.save()

            rmn = cd['room_no']
            pf = get_object_or_404(TenantProfile, room_no__room_no=rmn)

            # INCREAMENT & SAVE VALUE TO PF.MAINT_COST
            pf.maint_cost += cd['job_cost']
            pf.save()

            messages.success(request, 'Maintenance cost has been charged to Room: {}.'.format(rmn))

            return HttpResponseRedirect(reverse_lazy('admin_page'))
        else:
            messages.error(request, 'Error: new record was not saved !!!')

    else:
        maintenance_form = MaintenanceForm()

    return render(request, 'my_app/maintenanace_charge.html', {'maintenance_form': maintenance_form})


@login_required
def new_tenant(request):
    tenant_name = str(request.user)

    return render(request, 'my_app/new_tenant.html', {'tenant_name': tenant_name})


@login_required
def tenant_profile(request):
    usr = str(request.user)
    fn, ln = usr.split(" ")
    # tenant_pf = get_object_or_404(TenantProfile, tenant__first_name=fn, tenant__last_name=ln)
    try:
        tenant_pf = TenantProfile.objects.get(tenant__first_name=fn, tenant__last_name=ln)
    except Exception as err:
        messages.error(request, 'ERROR: {} '.format(str(err)))
        return HttpResponseRedirect(reverse_lazy('login'))
    else:
        exd = {}
        exd.setdefault('Electricity CPU', 0)
        exd.setdefault('Water CPU', 0)
        exd.setdefault('Garbage', 0)
        exd.setdefault('Parking', 0)
        exd.setdefault('Wifi', 0)
        exd.setdefault('Cable TV', 0)
        exd.setdefault('Bed', 0)
        exd.setdefault('Bed accessories', 0)
        exd.setdefault('Dressing Table', 0)
        exd.setdefault('Clothing Cupboard', 0)
        exd.setdefault('TV Table', 0)
        exd.setdefault('Fridge', 0)
        exd.setdefault('Air-Conditioner', 0)

        for e in tenant_pf.extra.all():
            exd.update({e.desc: e.cpu})

        room_acc_cost = exd['Bed'] + exd['Bed accessories'] + exd['Dressing Table'] \
                        + exd['Clothing Cupboard'] + exd['TV Table'] + exd['Fridge'] \
                        + exd['Air-Conditioner']

        oth_ser_cost = exd['Garbage'] + exd['Parking'] + exd['Wifi'] + exd['Cable TV']

        cur_dt = datetime.datetime.now()

        return render(request, 'my_app/tenant_profile.html',
                      {'section': 'tenant_profile', 'tenant_pf': tenant_pf, 'room_acc_cost': room_acc_cost,
                       'oth_ser_cost': oth_ser_cost, 'cur_dt': cur_dt})


def tenant_bill_subroutine(tn_bill):
    bill_dt = tn_bill.bill_date
    pay_date = tn_bill.payment_date
    cur_mth = bill_dt.month
    cur_yr = bill_dt.year
    cur_th_mth = get_thai_month_name(str(bill_dt))
    cur_th_yr = get_thai_year(str(bill_dt))

    next_th_yr = cur_th_yr

    if cur_mth + 1 > 12:

        next_mth = 1
        next_yr = cur_yr + 1

        new_dt = datetime.date(next_yr, next_mth, 15)

        next_dt_mth = datetime.date(next_yr, next_mth, 15)

        next_th_yr = get_thai_year(str(new_dt))

    else:
        next_dt_mth = datetime.date(cur_yr, cur_mth + 1, 15)

    next_th_m = get_thai_month_name(str(next_dt_mth))

    room_with_acc_cost = tn_bill.room_cost + tn_bill.room_acc_cost + tn_bill.adjust

    pay_amt = tn_bill.payment_amount

    bill_misc = tn_bill.late_fee + tn_bill.maint_cost

    if tn_bill.status == 'open':
        paid_str = 'รอชำระ'
    else:
        paid_str = 'ชำระแล้ว ณ วันที่ {0} {1} {2} จำนวน {3:,.0f} บาท'.format(pay_date.day,
                                                                             get_thai_month_name(str(pay_date)),
                                                                             get_thai_year(str(pay_date)), pay_amt)

    # TEMPORARY UNTIL OVD OF RM204A HAS BEEN COVERED
    rn = tn_bill.room_no
    if rn == '204A':
        bill_total = tn_bill.bill_total
    else:
        bill_total = tn_bill.bill_total

    return room_with_acc_cost, bill_misc, bill_total, paid_str, cur_th_mth, next_th_m, cur_th_yr, next_th_yr


@login_required
def tenant_bill(request):
    tenant = str(request.user)
    bills = Billing.objects.filter(tenant_name=tenant)

    if bills:
        tnb_qs = Billing.objects.filter(tenant_name=tenant, status='open')
        if tnb_qs:
            tn_bill = get_object_or_404(Billing, tenant_name=tenant, status='open')
        else:
            bill_month = str(datetime.datetime.now().month)
            tnb_qs = Billing.objects.filter(tenant_name=tenant, status='close', bill_date__month=bill_month)
            if tnb_qs:
                tn_bill = get_object_or_404(Billing, tenant_name=tenant, status='close', bill_date__month=bill_month)
            else:
                bill_month = str(datetime.datetime.now().month - 1)
                tn_bill = get_object_or_404(Billing, tenant_name=tenant, status='close', bill_date__month=bill_month)

        room_with_acc_cost, bill_misc, bill_total, paid_str, cur_th_mth, next_th_m, cur_th_yr, next_th_yr = tenant_bill_subroutine(
            tn_bill)

        return render(request, 'my_app/tenant_bill.html',
                      {'section': 'tenant_bill', 'tn_bill': tn_bill, 'room_with_acc_cost': room_with_acc_cost,
                       'bill_misc': bill_misc, 'bill_total': bill_total, 'cur_th_mth': cur_th_mth,
                       'next_th_m': next_th_m,
                       'cur_th_yr': cur_th_yr, 'next_th_yr': next_th_yr, 'paid_str': paid_str})
    else:

        # NEW TENANT
        return HttpResponseRedirect(reverse_lazy('new_tenant'))


def tenant_feedback(request):
    return render(request, 'my_app/tenant_feedback.html', {'section': 'comment'})


def get_ref_string():
    char_str = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    random.shuffle(char_str)
    fd = random.choice(char_str)

    sd = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    ref_str = fd + '-' + sd

    return ref_str


def get_eng_month_name(m: int):
    md = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
          9: 'September',
          10: 'October', 11: 'November', 12: 'December'}
    im = int(m)
    return md[im]


def get_thai_month_name(bill_date: str):
    md = {1: 'มกราคม', 2: 'กุมภาพันธ์', 3: 'มีนาคม', 4: 'เมษายน', 5: 'พฤษภาคม', 6: 'มิถุนายน', 7: 'กรกฏาคม',
          8: 'สิงหาคม', 9: 'กันยายน',
          10: 'ตุลาคม', 11: 'พฤศจิกายน', 12: 'ธันวาคม'}

    y, m, d = bill_date.split('-')

    im = int(m)
    return md[im]


def get_thai_year(bill_date: str):
    y, m, d = bill_date.split('-')

    christ_y = int(y)
    buddist_y = christ_y + 543

    return str(buddist_y)


def make_date_string(self, ds: str):
    y, m, d = str(ds).split('-')
    return d + '-' + m + '-' + y


def give_error_message(error_msg):
    print(error_msg)


def give_info_message(error_msg):
    print(error_msg)


def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret
