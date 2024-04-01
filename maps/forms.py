from django import forms
from django.forms import ModelForm
from.models import *
from crispy_forms.helper import FormHelper

modes = (
    ("driving", "driving"),
    ("walking", "walking"),
    ("bicycling", "bicycling"),
    ("transit", "transit")
)

class DistanceForm(ModelForm):
    from_location = forms.ModelChoiceField(label="Location from", required=True, queryset=Location.objects.all())
    to_location = forms.ModelChoiceField(label="Location to", required=True, queryset=Location.objects.all())
    mode = forms.ChoiceField(choices=modes, required=True) 
    
    class Meta:
        model = Distance
        exclude = ['created_at', 'edited_at', 'distance_km', 'duration_mins', 'duration_traffic_mins']