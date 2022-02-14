from django import template
from ..models import ArticleCategory 
from django.db.models import Count, Q
from datetime import datetime, timedelta
from ..models import Article

register = template.Library()

@register.simple_tag
def title ():
	return "وبلاگ جنگویی من "


@register.inclusion_tag("blog/parsial/category_navbar.html")
def category_navbar(request):
	last_month = datetime.today() - timedelta(days=30)
	return {
		"category" : ArticleCategory.objects.active(),
		'request' : request,
		'popular_article' : Article.objects.published().annotate(count=Count('hits', filter = Q(articlehit__date__gt=last_month))).order_by('-count', '-publish')[:5],
		'hot_article' : Article.objects.published().annotate(count=Count('comments', filter = Q(comments__posted__gt=last_month)and Q(comments__content_type_id=7))).order_by('count')
	}

@register.inclusion_tag('registration/parsial/link.html')
def link (request, link_name, content, classes):
	return {
		'request' : request,
		'link_name' : link_name,
		'link' : 'account:{}'.format(link_name),
		'content' : content,
		'classes' : classes, 
	}






















