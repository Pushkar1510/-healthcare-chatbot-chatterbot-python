from django import forms
import pandas as pd

class MsgForm(forms.Form):
    message = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Message', 'class': 'form-control'}))

df = pd.read_csv(
    './Symptom-severity.csv')

onls = df["Symptom"].to_list()

ans = tuple(zip(onls, onls))

DEMO_CHOICES =ans

class SympForm(forms.Form):
    symptom_field = forms.MultipleChoiceField(choices = DEMO_CHOICES)