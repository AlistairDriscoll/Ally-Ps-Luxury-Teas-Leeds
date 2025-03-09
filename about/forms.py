from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    """Form for customers to be able to send an enquiry"""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"aria-label": "Email Address", "required": True}
        )
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={"aria-label": "Subject", "required": True}
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"aria-label": "Content", "required": True}
        )
    )

    class Meta:
        model = Enquiry
        fields = (
            "email",
            "subject",
            "content",
        )
