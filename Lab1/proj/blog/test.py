from django.test import TestCase
from .models import Article, Comment, Category, Tag
from django.contrib.auth.models import User
from django.urls import reverse

class BlogTests(TestCase):
    def setUp(self):
        # Create test data before each test
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article content.',
            category=self.category,
            author=self.user
        )
        self.article.tags.add(self.tag)

    def test_article_model(self):
        # Test Article model
        self.assertEqual(str(self.article), 'Test Article')

    def test_comment_model(self):
        # Test Comment model
        comment = Comment.objects.create(
            article=self.article,
            user=self.user,
            content='This is a test comment.'
        )
        self.assertEqual(str(comment), 'testuser - Test Article')

    def test_article_list_view(self):
        # Test Article list view
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')
        self.assertTemplateUsed(response, 'blog/article_list.html')
