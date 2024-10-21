from django import forms


class InquiryForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Nimi")
    email = forms.EmailField(required=True, label="Sinu email")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Kirjeldus")
