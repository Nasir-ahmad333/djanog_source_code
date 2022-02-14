from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from extentions.utils import time_converter
from account.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

# my managers
class ArticleManager (models.Manager):
	def published (self):
		return self.filter(status="p")


class CategoryManager (models.Manager):
	def active (self):
		return self.filter(status=True)
	
	


# Create your models here.
class IpAddress (models.Model):
	ip_address = models.GenericIPAddressField(verbose_name="ایپی آدرس")

	class Meta:
		verbose_name = 'ای پی ادرس'
		verbose_name_plural = "ای پی ادرس ها  "

	def __str__(self):
		return self.ip_address
	

class ArticleCategory (models.Model):
	parent   = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name = "children", verbose_name="زیردسته")
	title    = models.CharField(max_length=200, verbose_name="عنوان")
	slug     = models.SlugField(max_length=100, verbose_name="آدرس")
	status   = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود ؟ ")
	position = models.IntegerField(verbose_name="پوزیشن")

	class Meta:
		verbose_name = 'دسته بندی'
		verbose_name_plural = "دسته بندی ها "
		ordering = ('-position',)

	def __str__(self):
		return self.title

	objects = CategoryManager()


class Article(models.Model):
	STATUS_CHOICES = (
		('p', 'منتشر شده'),         # publish
		('d', 'پیش نویس'),         # draft
		('i', 'در حال برسی'),        # investegation
		('b', 'برگشت داده شده'),   # back
	)
	author 		 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="articles", verbose_name="نویسنده")
	title        = models.CharField(max_length=200, verbose_name="عنوان", unique=True)
	category     = models.ManyToManyField(ArticleCategory, verbose_name="دسته بندی", related_name="article")
	slug         = models.SlugField(max_length=100, verbose_name="آدرس")
	descripiton  = models.TextField(verbose_name="توضیخات")
	thumbnail    = models.ImageField(upload_to="images", verbose_name="تصویر")
	publish      = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
	created      = models.DateTimeField(auto_now_add=True)
	updated      = models.DateTimeField(auto_now=True)
	is_special   = models.BooleanField(default=False, verbose_name="مقاله ویژه")
	status       = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="حالت")
	comments     = GenericRelation(Comment)
	hits 		 = models.ManyToManyField(IpAddress, through="ArticleHit", blank=True, related_name="hits", verbose_name="بازدید ها ")

	class Meta:
		verbose_name = 'مقاله'
		verbose_name_plural = "مقالات"
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('account:home')

	def jpublish (self):
		return time_converter(self.publish)
	jpublish.short_description = "زمان انتشار"

	def category_to_str(self):
		return ", ".join([category.title for category in self.category.active()])
	category_to_str.short_description = "دسته یندی ها "

	def show_thumbnail(self):
		return format_html('<img src="{}" style="width:150px; height:100px; border-radius: 5px; background-size:cover; background-position:center;">'.format(self.thumbnail.url))

	objects = ArticleManager()


class ArticleHit(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	ip_address = models.ForeignKey(IpAddress, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)



