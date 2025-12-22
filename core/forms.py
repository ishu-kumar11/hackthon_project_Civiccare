from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'full_name',
            'phone',
            'category',
            'urgency',
            'title',
            'description',
            'state',
            'district',
            'location',
            'pincode',
            'photo'
        ]


        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '10-digit mobile number',
                'maxlength': '10'
            }),
        }
