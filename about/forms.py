from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    """Forms for customer to be able to send an enquiry"""
    class Meta:
        model = Enquiry
        fields = (
            'email',
            'subject',
            'content',
        )
