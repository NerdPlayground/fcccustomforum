from typing import Any
from .models import Topic
from django.views import View
from django.urls import reverse
from replies.models import Reply
from replies.forms import ReplyForm 
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView,ListView,FormView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

class CreateTopicView(CreateView):
    model=Topic
    fields=["title","category","content"]
    template_name="topics/create-topic.html"

    def form_valid(self,form):
        topic=form.save(commit=False)
        topic.author=self.request.user
        topic.save()
        return super().form_valid(form)

class DetailReplyView(DetailView):
    model=Topic
    template_name="topics/topic.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['form']=ReplyForm()
        return context

class CreateReplyView(FormView,SingleObjectMixin):
    model=Topic
    form_class=ReplyForm
    template_name="topics/topic.html"

    def post(self,request,*args,**kwargs):
        self.object=self.get_object()
        return super().post(request,*args,**kwargs)

    def form_valid(self,form):
        reply=form.save(commit=False)
        reply.topic=self.object
        reply.member=self.request.user
        reply.save()
        return super().form_valid(form)

    def get_success_url(self):
        topic=self.get_object()
        return reverse("topic",kwargs={"pk":topic.pk})

class DetailTopicView(View):
    def get(self,request,*args,**kwargs):
        view=DetailReplyView.as_view()
        return view(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        view=CreateReplyView.as_view()
        return view(request,*args,**kwargs)

class ListTopicView(ListView):
    model=Topic
    context_object_name="topics"
    template_name="topics/topics.html"

class UpdateTopicView(UpdateView):
    model=Topic
    fields=["title","category","content"]
    template_name="topics/update-topic.html"

class DeleteTopicView(DeleteView):
    model=Topic
    template_name="topics/delete-topic.html"

    def get_success_url(self):
        return reverse("category",kwargs={"pk":self.object.category.pk})