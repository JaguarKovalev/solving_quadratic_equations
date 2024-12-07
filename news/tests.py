from django.test import TestCase
from django.urls import reverse
from .models import News, Category, Tag
from accounts.models import CustomUser

class NewsTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='TestCategory', slug='test-category')
        self.tag = Tag.objects.create(name='TestTag', slug='test-tag')
        self.news = News.objects.create(
            title='Test News',
            content='This is a test news content.',
            status='published',
            author=self.user,
            category=self.category
        )
        self.news.tags.add(self.tag)

    def test_news_list_view(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News')

    def test_news_detail_view(self):
        response = self.client.get(reverse('news_detail', args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test news content.')

    def test_news_by_category(self):
        response = self.client.get(reverse('news_by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News')

    def test_news_by_tag(self):
        response = self.client.get(reverse('news_by_tag', args=[self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News')

    def test_create_post_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('create_post'), {
            'title': 'New Post',
            'content': 'Content for new post',
            'category': self.category.id,
            'tags': [self.tag.id],
            'status': 'pending'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(News.objects.count(), 2)
