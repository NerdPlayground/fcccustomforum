from .models import Category
from django.urls import reverse
from pocket.tests import PocketTestCase

class CategoryTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
    
    def test_member_create_category(self):
        self.member_login(
            self.member,
            self.password
        )
        
        self.url_template(
            "create-category",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403
        )

    def test_create_category(self):
        url_name="create-category"

        self.member_login(
            self.admin,
            self.password
        )
        
        self.url_template(
            url_name,
            "categories/%s.html" %(url_name),
            "<title>Category</title>"
        )

        title="Python"
        description="Ask questions and share tips for Python."
        response=self.client.post(reverse(url_name),{
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
    
    def test_intruder_update_category(self):
        self.member_login(
            self.other_admin,
            self.password
        )

        self.url_template(
            "update-category",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403,
            kwargs={"pk":self.category.pk},
        )

    def test_update_category(self):
        url_name="update-category"
        kwargs={"pk":self.category.pk}

        self.member_login(
            self.admin,
            self.password
        )

        self.url_template(
            url_name,
            "categories/%s.html" %(url_name),
            "<title>%s</title>" %(self.category.title),
            kwargs=kwargs
        )

        title="Javascript (Updated)"
        description="Ask questions and share tips for JavaScript and its ecosystem."
        response=self.client.post(reverse(url_name,kwargs=kwargs),{
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
    
    def test_intruder_delete_category(self):
        self.member_login(
            self.other_admin,
            self.password
        )

        self.url_template(
            "delete-category",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403,
            kwargs={"pk":self.category.pk},
        )
    
    def test_delete_category(self):
        url_name="delete-category"
        kwargs={"pk":self.category.pk}

        self.member_login(
            self.admin,
            self.password
        )

        self.url_template(
            url_name,
            "categories/%s.html" %(url_name),
            "<title>%s</title>" %(self.category.title),
            kwargs=kwargs
        )

        categories_count=Category.objects.count()
        response=self.client.delete(reverse(url_name,kwargs=kwargs))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("categories"))
        self.assertEqual(categories_count-1,Category.objects.count())