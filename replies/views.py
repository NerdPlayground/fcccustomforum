from .models import Reply
from django.urls import reverse
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class UpdateReplyView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Reply
    fields=["content"]
    template_name="replies/update-reply.html"

    def get_success_url(self):
        return reverse("topic",kwargs={"pk":self.object.topic.pk})
    
    def test_func(self):
        return self.get_object().member==self.request.user

class DeleteReplyView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Reply
    template_name="replies/delete-reply.html"

    def get_success_url(self):
        return reverse("topic",kwargs={"pk":self.object.topic.pk})
    
    def test_func(self):
        return self.get_object().member==self.request.user