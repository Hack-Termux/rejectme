from django import forms

class EmailForm(forms.Form):
    job_title = forms.CharField(label='Job Title')
    company = forms.CharField(label='Company')
    your_name = forms.CharField(label='Your Name')
