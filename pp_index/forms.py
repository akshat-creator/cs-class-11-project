from django import forms

COUNTRY_CHOICES = [
    ('india','India'),
]

STATE_CHOICES = [
    ('ncr', 'N.C.R'),
]


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St' 
    }))
    appartment_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite' 
    }))
    country = forms.CharField(label='Country', widget=forms.Select(choices=COUNTRY_CHOICES))
    state = forms.CharField(label='State', widget=forms.Select(choices=STATE_CHOICES))
    zip_code = forms.CharField()
    name_on_card = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'JOHN WICK'
         
    }))
    pp_card = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'XXX-XXX-XXX-XXX' 
    }))
    expiry_date = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'MM/YY' 
    }))
    cvv = forms.CharField(widget=forms.TextInput(attrs={
        'label': 'CVV' 
    }))

