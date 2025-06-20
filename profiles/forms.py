from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
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
            "subscribed_to_members_club",  # updated field
        ]

    def __init__(self, *args, **kwargs):
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
            if field in placeholders:
                self.fields[field].widget.attrs[
                    "placeholder"] = placeholders[field]

            if field != "subscribed_to_members_club":
                self.fields[field].widget.attrs["class"] = "form-control"
                self.fields[field].label = False

        # 💡 Custom label for the checkbox
        self.fields["subscribed_to_members_club"].label = (
            "Join the Special Members Club for early access to new teas!"
        )
