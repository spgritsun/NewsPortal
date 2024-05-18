from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
from django.urls import reverse

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from pytz import timezone
from django.utils import timezone
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating_sum = self.post_set.aggregate(Sum('post_rating'))['post_rating__sum'] or 0
        comment_rating_sum = self.user.comment_set.aggregate(Sum('comment_rating'))['comment_rating__sum'] or 0
        post_comment_rating_sum = Comment.objects.filter(post__author=self).aggregate(Sum('comment_rating'))[
                                      'comment_rating__sum'] or 0
        self.author_rating = post_rating_sum * 3 + comment_rating_sum + post_comment_rating_sum
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_news = models.BooleanField(default=True)
    post_time = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, through='PostCategory')
    post_headline = models.CharField(max_length=100)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    @classmethod
    def get_latest_news_pk(cls):
        latest_news_pk = cls.objects.filter(is_news=True).last().pk
        return latest_news_pk

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...' if len(self.post_text) > 124 else self.post_text

    def __str__(self):
        return f'{self.post_headline}, {self.post_time}, {self.post_text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
