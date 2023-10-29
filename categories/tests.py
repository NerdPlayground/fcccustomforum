from .models import Category
from django.urls import reverse
from django.conf import settings
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model

class CategoryTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_create_category(self):
        self.url_template(
            "create-category",
            "categories/create_category.html",
            "Category"
        )
        self.member_login(self.admin,self.password)

        title="Python"
        description="Ask questions and share tips for Python."
        response=self.client.post(reverse("create-category"),{
            "title":title,
            "description":description,
        })
        self.assertEqual(response.status_code,302)

        category=Category.objects.last()
        self.assertRedirects(response,reverse(
            "category",
            kwargs={"pk":category.pk})
        )
        self.assertEqual(category.author,self.admin)
        self.assertEqual(category.title,title)
        self.assertEqual(category.description,description)
    
    def test_retrieve_categories(self):
        self.url_template(
            "category",
            "categories/category.html",
            "<title>%s</title>" %(self.category.title),
            kwargs={"pk":self.category.pk}
        )
        
        self.url_template(
            "categories",
            "categories/categories.html",
            "<title>Categories</title>",
        )
    
    def test_update_category(self):
        self.url_template(
            "update-category",
            "categories/update_category.html",
            "<title>%s</title>" %(self.category.title),
            kwargs={"pk":self.category.pk}
        )

        title="Javascript (Updated)"
        description="Ask questions and share tips for JavaScript and its ecosystem."
        response=self.client.post(reverse("update-category",kwargs={"pk":self.category.pk}),{
            "title":title,
            "description":description,
        })
        self.assertEqual(response.status_code,302)

        category=Category.objects.get(pk=self.category.pk)
        self.assertRedirects(response,reverse(
            "category",
            kwargs={"pk":category.pk})
        )
        self.assertEqual(category.author,self.admin)
        self.assertEqual(category.title,title)
        self.assertEqual(category.description,description)
    
    def test_delete_category(self):
        self.url_template(
            "update-category",
            "categories/update_category.html",
            "<title>%s</title>" %(self.category.title),
            kwargs={"pk":self.category.pk}
        )

        categories_count=Category.objects.count()
        response=self.client.delete(reverse(
            "delete-category",
            kwargs={"pk":self.category.pk}
        ))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("categories"))
        self.assertEqual(categories_count-1,Category.objects.count())