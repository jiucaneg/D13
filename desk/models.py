from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='posts', null=True)
    title = models.CharField(verbose_name='Заголовок объявления', max_length=255)
    text = models.TextField(verbose_name='Текст объявления')
    CATEGORIES = (
        ('T', 'Танки'),
        ('HM', 'Хилы'),
        ('DD', 'ДД'),
        ('TrM', 'Торговцы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('FM', 'Кузнецы'),
        ('LM', 'Кожевники'),
        ('PM', 'Зельевары'),
        ('WM', 'Мастера заклинаний')
    )
    category = models.CharField(verbose_name='Категория', max_length=3, choices=CATEGORIES)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    @property
    def new_responses(self):
        responses = self.responses.all().order_by('-pub_date')
        return responses


class Response(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='responses', null=True
    )
    text = models.TextField('Текст отклика')
    BOOL_CHOICES = (
        (True, 'Принято'),
        (False, 'Отклонено')
    )
    status = models.BooleanField(choices=BOOL_CHOICES, blank=True, verbose_name='Статус', null=True)
    post = models.ForeignKey(Post, related_name='responses', verbose_name='Пост', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.author.username} - {self.text[:20]}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Shot(models.Model):
    post = models.ForeignKey(Post, related_name='shots', verbose_name='Пост', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
