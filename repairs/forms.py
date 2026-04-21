from django import forms
from django.forms import modelformset_factory
from .models import Ticket, Job, Instrument, Owner


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ['owner', 'instrument_type', 'make', 'model', 'serial_number']
        widgets = {
            'owner': forms.Select(attrs={'class': 'form-select'}),
            'instrument_type': forms.TextInput(attrs={'class': 'form-control'}),
            'make': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['instrument', 'status', 'notes']
        widgets = {
            'instrument': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_type', 'price', 'notes']
        widgets = {
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }


JobFormSet = modelformset_factory(Job, form=JobForm, extra=1, can_delete=True)
