from django import forms
from .models import TenantProfile, MaintenanceCharge

from django.contrib.auth import get_user_model

CUser = get_user_model()


class TenantCreateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = CUser
        fields = ('username', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     if CUser.objects.filter(email=data).exists():
    #         # if settings.AUTH_USER_MODEL.objects.filter(email=data).exists():
    #         raise forms.ValidationError('Email already in use.')
    #     return data


class TenantProfileCreateForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        # fields = {'room_no','elec_unit','water_unit','misc_cost'}
        exclude = ['tenant', 'deduct', 'cum_ovd', 'elec_unit', 'water_unit', 'misc_cost', 'late_fee', 'maint_cost']


class PaymentForm(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceCharge
        fields = {'room_no', 'job_cost'}
        widgets = {

            'job_cost': forms.NumberInput(attrs={'class': 'job_cost', 'placeholder': 'Baht', 'min': 0})
        }

class Elec_cpu_change(forms.Form):
    elec_cpu = forms.DecimalField(max_digits=7, decimal_places=2,
                                  widget=forms.NumberInput(
                                      attrs={'class': 'elec_cpu', 'placeholder': 'elec_cpu', 'min': 0}))

class Water_cpu_change(forms.Form):
    water_cpu = forms.DecimalField(max_digits=7, decimal_places=2,
                                   widget=forms.NumberInput(
                                       attrs={'class': 'water_cpu', 'placeholder': 'water_cpu', 'min': 0}))

class PhoneNoMessage(forms.Form):
    phone_no = forms.CharField(max_length=10)
    sms_msg = forms.CharField(widget=forms.Textarea)
    # msg = forms.CharField(widget=forms.TextInput( attrs={'class': 'msg'}))


class PFormRM101A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM102A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM103A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM104A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM105A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM106A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM201A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM202A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM203A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM204A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM205A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM206A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM301A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM302A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM303A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM304A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM305A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM306A(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM201B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM202B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM203B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM204B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM205B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM301B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM302B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM303B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM304B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM305B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM401B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM402B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM403B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM404B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class PFormRM405B(forms.Form):
    payment_amount = forms.DecimalField(max_digits=7, decimal_places=2,
                                        widget=forms.NumberInput(
                                            attrs={'class': 'paid_amount', 'placeholder': 'paid_amount', 'min': 0}))
    payment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'pay_date', 'placeholder': 'pay_date'}))


class RM101A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM102A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM103A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM104A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM105A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM106A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM201A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM202A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM203A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM204A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM205A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM206A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM301A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM302A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM303A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM304A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM305A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM306A_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM201B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM202B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM203B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM204B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM205B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM301B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM302B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM303B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})

        }


class RM304B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM305B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM401B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM402B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM403B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})

        }


class RM404B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }


class RM405B_BillForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = {'elec_unit', 'water_unit'}
        widgets = {
            'elec_unit': forms.NumberInput({'class': 'eu', 'placeholder': 'elect-unit', 'min': 0}),
            'water_unit': forms.NumberInput(attrs={'class': 'wu', 'placeholder': 'water-unit', 'min': 0})
        }

class confirm_send_all_message(forms.ModelForm):
    pass


