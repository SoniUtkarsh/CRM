import random
from typing import Any
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views import generic
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self) -> str:
        return reverse("agents:agent-list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()

        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )

        send_mail(
            from_email="sender@domain.com",
            recipient_list=["receiver1@domain.com",],
            subject="You are invited to be an agent",
            message="You were added as an agent in CRM"
        )

        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"

    def get_queryset(self) -> QuerySet[Any]:
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_queryset(self) -> QuerySet[Any]:
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self) -> str:
        return reverse("agents:agent-list")


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"

    def get_queryset(self) -> QuerySet[Any]:
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self) -> str:
        return reverse("agents:agent-list")
