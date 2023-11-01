from .models import Category
from django.urls import reverse_lazy
from django.views.generic import DetailView,ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class CreateCategoryView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Category
    fields=("title","description",)
    template_name="categories/create_category.html"

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_staff

class CategoryView(DetailView):
    model=Category
    template_name="categories/category.html"

class CategoriesView(ListView):
    model=Category
    context_object_name="categories"
    template_name="categories/categories.html"

class UpdateCategoryView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Category
    fields=("title","description",)
    template_name="categories/update_category.html"

    def test_func(self):
        return self.get_object().author==self.request.user

class DeleteCategoryView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Category
    success_url=reverse_lazy("categories")
    template_name="categories/delete_category.html"

    def test_func(self):
        return self.get_object().author==self.request.user