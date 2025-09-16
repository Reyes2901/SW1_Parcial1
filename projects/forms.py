from django import forms
from .models import Project
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    collaborators = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'collaborators']
        # Exclude the owner field as it will be set in the view
        exclude = ['owner']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }