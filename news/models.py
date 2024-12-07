from django.db import models

class News(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Содержание")
    image = models.ImageField("Изображение", upload_to='news_images/')
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def short_content(self):
        return f"{self.content[:100]}..." if len(self.content) > 100 else self.content