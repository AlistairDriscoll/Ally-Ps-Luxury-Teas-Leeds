from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form for updating UserProfile details.
    """

    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "email",
            "phone_number",
            "address_line1",
            "address_line2",
            "town_or_city",
            "state_or_region",
            "postal_code",
            "country",
            "subscribed_to_members_club",
        ]

    def __init__(self, *args, **kwargs):
        """
        Customize form placeholders and attributes.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "address_line1": "Address Line 1",
            "address_line2": "Address Line 2",
            "town_or_city": "Town or City",
            "state_or_region": "State or Region",
            "postal_code": "Postal Code",
            "country": "Country",
        }

        self.fields["full_name"].widget.attrs["autofocus"] = True

        for field in self.fields:
            # Add placeholders where appropriate
            if field in placeholders:
                self.fields[field].widget.attrs[
                    "placeholder"] = placeholders[field]

            # Style all fields except the checkbox
            if field != "subscribed_to_members_club":
                self.fields[field].widget.attrs["class"] = "form-control"
                self.fields[field].label = False
