from .models import Topic
from django.urls import reverse
from django.views.generic import DetailView,ListView
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

class DetailTopicView(DetailView):
    model=Topic
    template_name="topics/topic.html"

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