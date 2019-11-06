"""
This file contains all views related to inputting decisions/actions into the form
"""
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from makeReports.models import *
from makeReports.forms import *
from makeReports.views.helperFunctions.section_context import *
from makeReports.views.helperFunctions.mixins import *

class DecisionsActionsSummary(DeptReportMixin,ListView):
    """
    View to summary decisions and actions during form entry
    """
    model = DecisionsActions
    template_name = 'makeReports/DecisionsActions/decisionsActionsSummary.html'
    context_object_name = "decisions_actions_list"
    def get_context_data(self, **kwargs):
        context = super(DecisionsActionsSummary, self).get_context_data()
        return section4Context(self,context)

class AddDecisionAction(DeptReportMixin,CreateView):
    """
    View to add new decision and action
    """
    form_class = DecActForm1Box
    template_name = "makeReports/DecisionsActions/changeDecisionAction.html"
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches view and attaches :class:`~makeReports.models.report_models.SLO` to instance

        Args:
            request (HttpRequest): request to view page
            
        Returns:
            HttpResponse : response of page to request
        """
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        return super(AddDecisionAction,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        """
        Gets context data for template, including the SLO

        Returns:
            dict : context for template
        """
        context = super(AddDecisionAction,self).get_context_data(**kwargs)
        context['slo'] = SLOInReport.objects.get(slo=self.slo, report=self.report)
        return context
    def form_valid(self,form):
        """
        Sets the SLO and Report appropriately, then creates the object from the form
        """
        form.instance.SLO = self.slo
        form.instance.report = self.report
        return super(AddDecisionAction,self).form_valid(form)
    def get_success_url(self):
        """
        Gets url of success page (decision actions summary)

        Returns:
            str : URL of decisions actions summary (:class:`~makeReports.views.decisions_actions_views.DecisionsActionsSummary`)
        """
        return reverse_lazy('makeReports:decisions-actions-summary', args=[self.report.pk])
class AddDecisionActionSLO(AddDecisionAction):
    """
    Add decision/action from SLO page
    """
    def get_success_url(self):
        """
        Gets URL to go to upon success (SLO summary)

        Returns:
            str : URL of SLO summary page (:class:`~makeReports.views.slo_views.SLOSummary`)
        """
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
class EditDecisionAction(DeptReportMixin,UpdateView):
    """
    Edit decision/action

    Keyword Args:
        pk (str): primary key of :class:`~makeReports.models.report_models.DecisionsActions` to update
        slopk (str): primary key of :class:`~makeReports.models.report_models.SLO`
    """
    model = DecisionsActions
    form_class = DecActForm1Box
    template_name = "makeReports/DecisionsActions/changeDecisionAction.html"
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches the view and attaches the :class:`~makeReports.models.report_models.SLO` to the instance

        Args:
            request (HttpRequest): request to view page
        Keyword Args:
            pk (str): primary key of :class:`~makeReports.models.report_models.DecisionsActions` to update
            slopk (str): primary key of :class:`~makeReports.models.report_models.SLO`
            
        Returns:
            HttpResponse : response of page to request
        """
        self.slo = SLO.objects.get(pk=self.kwargs['slopk'])
        return super(EditDecisionAction,self).dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        """
        Gets the context for the template, including the corresponding :class:`~makeReports.models.report_models.SLOInReport` 

        Returns:
            dict : context for template
        """
        context = super(EditDecisionAction,self).get_context_data(**kwargs)
        context['slo'] = SLOInReport.objects.get(slo=self.slo, report=self.report)
        return context
    def get_success_url(self):
        """
        Gets URL of success page (decisions/actions summary)

        Returns:
            str : URL of decisions and actions summary page (:class:`~makeReports.views.decisions_actions_views.DecisionsActionsSummary`)
        """
        return reverse_lazy('makeReports:decisions-actions-summary', args=[self.report.pk])
class EditDecisionActionSLO(EditDecisionAction):
    """
    Edit the decision/action
    """
    def get_success_url(self):
        """
        Gets URL to go to upon success (SLO summary)

        Returns:
            str : URL of SLO summary page (:class:`~makeReports.views.slo_views.SLOSummary`)
        """
        return reverse_lazy('makeReports:slo-summary', args=[self.report.pk])
class AddEditRedirect(DeptReportMixin,RedirectView):
    """
    Correctly redirects to the right new or edit view for decision/actions
    based upon whether a decision action already exists

    Keyword Args:
        slopk (str): primary key of :class:`~makeReports.models.report_models.SLO`
    """
    def get_redirect_url(self, *args,**kwargs):
        """
        Gets the redirect url

        Returns:
            str : URL of either add or edit decision action
        """
        slo = SLO.objects.get(pk=self.kwargs['slopk'])
        rpt = self.report
        try:
            dA = DecisionsActions.objects.get(SLO=slo,report=rpt)
            return reverse_lazy('makeReports:edit-decisions-actions-slo', args=[rpt.pk,slo.pk,dA.pk])
        except:
            return reverse_lazy('makeReports:add-decisions-actions-slo', args=[rpt.pk,slo.pk])
class Section4Comment(DeptReportMixin,FormView):
    """
    View to add a comment for section four
    """
    template_name = "makeReports/DecisionsActions/comment.html"
    form_class = Single2000Textbox
    def get_success_url(self):
        """
        Gets URL to go to upon success (decisions/actions summary)

        Returns:
            str : URL of decisions/actions summary page (:class:`~makeReports.views.decisions_actions_views.DecisionsActionsSummary`)
        """
        return reverse_lazy('makeReports:decisions-actions-summary', args=[self.report.pk])
    def form_valid(self, form):
        """
        Sets comment based upon form

        Args:
            form (Single2000Textbox): filled out form to be processed
            
        Returns:
            HttpResponseRedirect : redirects to success URL given by get_success_url
        """
        self.report.section4Comment = form.cleaned_data['text']
        self.report.save()
        return super(Section4Comment,self).form_valid(form)
    def get_initial(self):
        """
        Gets initial form values based upon current value

        Returns:
            dict : initial form values
        """
        initial = super(Section4Comment,self).get_initial()
        initial['text']="No comment."
        if self.report.section4Comment:
            initial['text'] = self.report.section4Comment
        return initial
