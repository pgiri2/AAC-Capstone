from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, DetailView
from django.views.generic import RedirectView
from django.urls import reverse_lazy, reverse
from makeReports.models import *
from makeReports.forms import *
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin

class AdminHome(TemplateView, FormMixin):
    template_name = "makeReports/AACAdmin/adminHome.html"
    form_class = JustHitButton
    success_url = reverse_lazy('makeReports:admin-home')
    def form_valid(self, form):
        #generate this years reports
        return super(AdminHome, self).form_valid(form)
class CreateCollege(CreateView):
    model = College
    template_name = "makeReports/AACAdmin/addCollege.html"
    fields = ['name']
    success_url = reverse_lazy('makeReports:admin-home')
class UpdateCollege(UpdateView):
    model = College
    template_name = "makeReports/AACAdmin/updateCollege.html"
    fields = ['name']
    success_url = reverse_lazy('makeReports:admin-home')
class CollegeList(ListView):
    model = College
    template_name = "makeReports/AACAdmin/collegeList.html"
class CreateDepartment(CreateView):
    model = Department
    fields = ['name', 'college']
    template_name = "makeReports/AACAdmin/addDepartment.html"
    success_url = reverse_lazy('makeReports:admin-home')
class DepartmentList(ListView):
    model = Department
    template_name = "makeReports/AACAdmin/deptList.html"
    def get_queryset(self):
        objs = Department.objects.order_by('college__name')
        return objs
class UpdateDepartment(UpdateView):
    model = Department
    fields = ['name', 'college']
    template_name = "makeReports/AACAdmin/updateDepartment.html"
    success_url = reverse_lazy('makeReports:admin-home')
class CreateDegreeProgram(CreateView):
    model = DegreeProgram
    form_class = CreateDPByDept
    template_name = "makeReports/AACAdmin/addDP.html"
    success_url = reverse_lazy('makeReports:admin-home')
class UpdateDegreeProgram(UpdateView):
    model = DegreeProgram
    form_class = CreateDPByDept
    template_name = "makeReports/AACAdmin/updateDP.html"
    success_url = reverse_lazy('makeReports:admin-home')
class DegreeProgramList(ListView):
    model = DegreeProgram
    def get_queryset(self):
        objs = DegreeProgram.objects.get(department=Department.objects.get(pk=self.request.GET['dept']))
        return objs
class CreateReport(CreateView):
    model = Report
    form_class = CreateReportByDept
    template_name = "makeReports/AACAdmin/manualReportCreate.html"
    success_url = reverse_lazy('makeReports:admin-home')
    def get_form_kwargs(self):
        kwargs = super(CreateReport, self).get_form_kwargs()
        kwargs.update({'dept': self.request.GET['dept']})
        return kwargs
class DeleteReport(DeleteView):
    model = Report
    template_name = "makeReports/AACAdmin/deleteReport.html"
    success_url = reverse_lazy('makeReports:admin-home')
class ReportList(ListView):
    model = Report
    template_name = "makeReports/AACAdmin/reportList.html"



