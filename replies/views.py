from .models import Reply
from django.urls import reverse
from django.views.generic.edit import UpdateView,DeleteView

class UpdateReplyView(UpdateView):
    model=Reply
    fields=["content"]
    template_name="replies/update-reply.html"

    def get_success_url(self):
        return reverse("topic",kwargs={"pk":self.object.topic.pk})

class DeleteReplyView(DeleteView):
    model=Reply
    template_name="replies/delete-reply.html"

    def get_success_url(self):
        return reverse("topic",kwargs={"pk":self.object.topic.pk})