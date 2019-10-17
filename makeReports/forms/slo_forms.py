from django import forms
from makeReports.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from makeReports.choices import *
from django_summernote.widgets import SummernoteWidget

class CreateNewSLO(forms.Form):
    text = forms.CharField(widget= SummernoteWidget(), max_length=600, label="SLO: ") 
    blooms = forms.ChoiceField(choices=BLOOMS_CHOICES, label="Highest Bloom's Taxonomy Level: ")
    gradGoals = forms.ModelMultipleChoiceField(queryset=GradGoal.active_objects.all(), required=False,widget=forms.CheckboxSelectMultiple, label="Graduate-level Goals: ")
    def __init__(self,*args,**kwargs):
        grad = kwargs.pop('grad',None)
        super(CreateNewSLO,self).__init__(*args,**kwargs)
        if not grad:
            del self.fields['gradGoals']
class ImportSLOForm(forms.Form):
    slo = forms.ModelMultipleChoiceField(queryset=None, label="SLOs to Import: ")
    importAssessments = forms.BooleanField(required=False,label="Also import assessments?")
    #of type SLOInReport
    def __init__(self, *args, **kwargs):
        sloChoices = kwargs.pop('sloChoices',None)
        super(ImportSLOForm, self).__init__(*args, **kwargs)
        self.fields['slo'].queryset = sloChoices
class EditNewSLOForm(forms.Form):
    text = forms.CharField(widget= SummernoteWidget(), max_length=600, label="SLO: ")
    blooms = forms.ChoiceField(choices=BLOOMS_CHOICES, required=False, label="Highest Bloom's Taxonomy Level: ")
    gradGoals = forms.ModelMultipleChoiceField(queryset=GradGoal.active_objects.all(), required=False,widget=forms.CheckboxSelectMultiple, label="Graduate-level Goals: ")
    def __init__(self,*args,**kwargs):
        grad = kwargs.pop('grad',None)
        super(EditNewSLOForm,self).__init__(*args,**kwargs)
        if not grad:
            del self.fields['gradGoals']
class EditImportedSLOForm(forms.Form):
    text = forms.CharField(widget= SummernoteWidget(), max_length=600, label="SLO: ")
class Single2000Textbox(forms.Form):
    text = forms.CharField(max_length=2000, widget=SummernoteWidget(),label="")
class CreateReportByDept(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['year', 'degreeProgram'] 
        labels = {
            'degreeProgram': "Degree Program"
        }
    def __init__(self,*args,**kwargs):
        dept = Department.objects.get(pk=kwargs.pop('dept'))
        super(CreateReportByDept, self).__init__(*args, **kwargs)
        self.fields['degreeProgram'].queryset = DegreeProgram.objects.filter(department=dept)
        self.fields['rubric'] = forms.ModelChoiceField(queryset=Rubric.objects.all())
class CreateDPByDept(forms.ModelForm):   
    class Meta:
        model = DegreeProgram
        fields = ['name','level','cycle','startingYear']
        labels = {
            'cycle': "Number of years between automatically assigned reports (put 0 or leave blank if there is no regular cycle)",
            'startingYear': "The first year report is assigned for cycle (leave blank if no cycle)"
        }
class ImportStakeholderForm(forms.Form):
    stk = forms.ModelChoiceField(queryset=None, label="Stakeholder Communication Methods")
    def __init__(self, *args, **kwargs):
        stkChoices = kwargs.pop('stkChoices',None)
        super(ImportStakeholderForm, self).__init__(*args, **kwargs)
        self.fields['stk'].queryset = stkChoices