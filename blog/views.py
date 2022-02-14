from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, ArticleCategory
from django.core.paginator import Paginator
from account.models import User
from account.mixins import AuthorAccessMixin
from django.db.models import Q

# Create your views here.

class ArticleList (ListView):
	queryset = Article.objects.published()
	paginate_by = 12


class ArticleDetail(DetailView):
	def get_object(self):
		slug = self.kwargs.get('slug')
		article = get_object_or_404(Article, slug=slug)

		ip_address = self.request.user.ip_address
		if ip_address not in article.hits.all():
			article.hits.add(ip_address)

		return article


class ArticlePreview(AuthorAccessMixin, DetailView):
	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Article, pk=pk)


class CategoryList(ListView):
	paginate_by = 12
	template_name = "blog/article_category.html"

	def get_queryset(self):
		global category
		slug = self.kwargs.get('slug')
		category = get_object_or_404(ArticleCategory.objects.active(), slug=slug)
		return category.article.published()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category'] = category
		return context


class AuthorList(ListView):
	paginate_by = 12
	template_name = "blog/article_author.html"

	def get_queryset(self):
		global author
		username = self.kwargs.get('username')
		author = get_object_or_404(User, username=username)
		return author.articles.published()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['author'] = author
		return context


class SearchList(ListView):
	paginate_by = 12
	template_name = "blog/search.html"

	def get_queryset(self):
		search = self.request.GET.get('q')
		return Article.objects.filter(Q(descripiton__icontains=search) | Q(title__icontains=search))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search'] = self.request.GET.get('q')
		return context