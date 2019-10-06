from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin

class SLOSummary(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = SLOInReport
    template_name ="makeReports/SLO/sloSummary.html"
    context_object_name = "slo_list"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(SLOSummary,self).dispatch(request,*args,**kwargs)
    def get_queryset(self):
        report = self.report
        objs = SLOInReport.objects.filter(report=report)
        return objs
    def get_context_data(self, **kwargs):
        context = super(SLOSummary, self).get_context_data()
        context['rpt'] = self.report
        return context
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class AddNewSLO(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/addSLO.html"
    form_class = CreateNewSLO
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(AddNewSLO,self).dispatch(request,*args,**kwargs)
    def get_form_kwargs(self):
        kwargs = super(AddNewSLO,self).get_form_kwargs()
        if self.report.degreeProgram.level == "GR":
            kwargs['grad'] = True
        else:
            kwargs['grad'] = False
        return kwargs
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self, form):
        try:
            gGoals = form.cleaned_data["gradGoals"]
        except:
            gGoals = []
        rpt = self.report
        sloObj = SLO.objects.create(blooms=form.cleaned_data['blooms'])
        sloObj.gradGoals.set(gGoals)
        sloRpt = SLOInReport.objects.create(date=datetime.now(), goalText =form.cleaned_data['text'], slo=sloObj, firstInstance= True, changedFromPrior=False, report=rpt)
        sloObj.save()
        sloRpt.save()
        return super(AddNewSLO, self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class ImportSLO(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/importSLO.html"
    form_class = ImportSLOForm
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(ImportSLO,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportSLO,self).get_form_kwargs()
         yearIn = self.request.GET['year']
         dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
         kwargs['sloChoices'] = SLOInReport.objects.filter(report__year=yearIn, report__degreeProgram=dPobj)
         return kwargs
    def form_valid(self,form):
        rpt = self.report
        for sloInRpt in form.cleaned_data['slo']:
            SLOInReport.objects.create(date=datetime.now(),goalText=sloInRpt.goalText,slo=sloInRpt.slo, firstInstance=False, report=rpt, changedFromPrior=False)
        return super(ImportSLO,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportSLO, self).get_context_data(**kwargs)
        r = self.report
        context['currentDPpk'] = Report.objects.get(pk=self.kwargs['report']).degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=r.degreeProgram.department)
        context['rpt']=self.kwargs['report']
        return context
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class EditImportedSLO(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/editImportedSLO.html"
    form_class = EditImportedSLOForm
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.sloInRpt = SLOInReport.objects.get(pk=self.kwargs['sloIR'])
        return super(EditImportedSLO,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        initial = super(EditImportedSLO, self).get_initial()
        initial['text'] = self.sloInRpt.goalText
        return initial
    def get_success_url(self):
        r = Report.objects.get(pk=self.kwargs['report'])
        return reverse_lazy('makeReports:slo-summary', args=[r.pk])
    def form_valid(self,form):
        r = self.report
        self.sloInRpt.date=datetime.now()
        self.sloInRpt.goalText=form.cleaned_data['text']
        self.sloInRpt.changedFromPrior = True
        self.sloInRpt.save()
        #newSLOInRpt = SLOInReport.objects.create(report=r,date=datetime.now(), goalText=form.cleaned_data['text'], slo = sloInRpt.slo, changedFromPrior=False, firstInstance=False)
        #newSLOInRpt.save()
        return super(EditImportedSLO, self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class EditNewSLO(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/editNewSLO.html"
    form_class = EditNewSLOForm
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.sloInRpt = SLOInReport.objects.get(pk=self.kwargs['sloIR'])
        return super(EditNewSLO,self).dispatch(request,*args,**kwargs)
    def get_initial(self):
        initial = super(EditNewSLO, self).get_initial()
        initial['text'] = self.sloInRpt.goalText
        initial['blooms'] = self.sloInRpt.slo.blooms
        initial['gradGoals'] = self.sloInRpt.slo.gradGoals.all
        return initial
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.sloInRpt.goalText = form.cleaned_data['text']
        self.sloInRpt.date = datetime.now()
        self.sloInRpt.slo.blooms = form.cleaned_data['blooms']
        self.sloInRpt.slo.gradGoals.set(form.cleaned_data['gradGoals'])
        self.sloInRpt.save()
        self.sloInRpt.slo.save()
        return super(EditNewSLO,self).form_valid(form)
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class StakeholderEntry(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/stakeholdersSLO.html"
    form_class = Single2000Textbox
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        self.sts = SLOsToStakeholder.objects.filter(report=self.report).first()
        return super(StakeholderEntry,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-comment', args=[self.report.pk])
    def get_initial(self):
        initial = super(StakeholderEntry,self).get_initial()
        try:
            #if sts:
            initial['text']=self.sts.text
        except:
            pass
        return initial
    def form_valid(self,form):
        try:
            self.sts.text = form.cleaned_data['text']
            sts.save()
        except:
            sTs = SLOsToStakeholder.objects.create(text=form.cleaned_data['text'], report=self.report)
        return super(StakeholderEntry,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(StakeholderEntry, self).get_context_data(**kwargs)
        context['rpt']=self.report
        return context
    def test_func(self):
        return (self.report.degreeProgram.department==self.request.user.profile.department)
class ImportStakeholderEntry(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/importStakeholderComm.html"
    form_class = ImportStakeholderForm
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(ImportStakeholderEntry,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        return reverse_lazy('makeReports:slo-stakeholders', args=[self.report.pk])
    def get_form_kwargs(self):
         kwargs = super(ImportStakeholderEntry,self).get_form_kwargs()
         yearIn = self.request.GET['year']
         dPobj = DegreeProgram.objects.get(pk=self.request.GET['dp'])
         kwargs['stkChoices'] = SLOsToStakeholder.objects.filter(report__year=yearIn, report__degreeProgram=dPobj)
         return kwargs
    def form_valid(self,form):
        oldSTS = form.cleaned_data["stk"]
        try:
            sts = SLOsToStakeholder.objects.filter(report=self.report).first()
            if oldSTS.report == self.report:
                pass
            elif sts:
                sts.text = form.cleaned_data['stk'].text
                sts.save()
            else:
                sTsNew = SLOsToStakeholder.objects.create(text=form.cleaned_data['stk'].text, report=self.report)
        except:
            sTs = SLOsToStakeholder.objects.create(text=form.cleaned_data['stk'].text, report=self.report)
        return super(ImportStakeholderEntry,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ImportStakeholderEntry, self).get_context_data(**kwargs)
        context['currentDPpk'] = self.report.degreeProgram.pk
        context['degPro_list'] = DegreeProgram.objects.filter(department=self.report.degreeProgram.department)
        context['rpt']=self.kwargs['report']
        return context
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class Section1Comment(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "makeReports/SLO/sloComment.html"
    form_class = Single2000Textbox
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(Section1Comment,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        #to be changed to assessment page!
        return reverse_lazy('makeReports:assessment-summary', args=[self.report.pk])
    def form_valid(self, form):
        self.report.section1Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section1Comment,self).form_valid(form)
    def get_initial(self):
        initial = super(Section1Comment,self).get_initial()
        initial['text']="No comment."
        return initial
    def test_func(self):
        return (self.report.degreeProgram.department == self.request.user.profile.department)
class DeleteImportedSLO(DeleteView):
    model = SLOInReport
    template_name = "makeReports/SLO/deleteSLO.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeleteImportedSLO,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        #to be changed to assessment page!
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
class DeleteNewSLO(DeleteView):
    model = SLOInReport
    template_name = "makeReports/SLO/deleteSLO.html"
    def dispatch(self,request,*args,**kwargs):
        self.report = Report.objects.get(pk=self.kwargs['report'])
        return super(DeleteNewSLO,self).dispatch(request,*args,**kwargs)
    def get_success_url(self):
        #to be changed to assessment page!
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
    def form_valid(self,form):
        SLOIR = SLOInReport.objects.get(pk=self.kwargs['pk'])
        slo = SLOIR.slo
        slo.delete()
        slo.save()
        return super(DeleteNewSLO,self).form_valid(form)