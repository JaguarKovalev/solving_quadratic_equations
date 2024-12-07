from django.test import TestCase
from django.urls import reverse
from news.models import News, Category, Tag
from django.core.files.uploadedfile import SimpleUploadedFile


class NewsTests(TestCase):
    def setUp(self):
        # Создаём тестовую категорию
        self.category = Category.objects.create(name="Test Category", slug="test-category")

        # Создаём тестовый тег
        self.tag = Tag.objects.create(name="Test Tag", slug="test-tag")

        # Создаём тестовую новость с изображением
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"file_content",
            content_type="image/jpeg"
        )
        self.news = News.objects.create(
            title="Test News",
            content="This is a test news content",
            category=self.category,
            image=self.image,
            status="published"
        )
        self.news.tags.add(self.tag)

    def test_news_list_view(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test News")
