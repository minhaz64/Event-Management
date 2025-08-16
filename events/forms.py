from django import forms
from events.models import Event, Participant, Category



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields =['name', 'description', 'date', 'time','location', 'category']
        widgets ={
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
    }


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields =['name', 'email', 'password','date_of_birth','gender']
        widgets ={
            'password': forms.PasswordInput(),
            'date_of_birth':forms.DateInput(attrs={'type':'date'}),
        }



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
