from django.contrib import admin
from .models import Article, ArticleCategory, IpAddress

# Actions 
def make_publish(modeladmin, request, queryset):
	row_updated = queryset.update(status="p")
	if row_updated == 1: 
		message_bit = "شد"
	else :
		message_bit = "شدند"
	modeladmin.message_user(request, "{} مقاله منتشر  {}".format(row_updated, message_bit)) 
make_publish.short_description = "انتشار مقالات انتخاب شده"

def make_draft(modeladmin, request, queryset):
	row_updated = queryset.update(status="d")
	if row_updated == 1:
		message_bit = "شد"
	else :
		message_bit = "شدند"
	modeladmin.message_user(request, '{} مقاله پیش نویس  {}'.format(row_updated, message_bit))
make_draft.short_description = "پئش نویس شدن مقالات انتخاب شده"


# Register your models here.

class CategoryAdmin (admin.ModelAdmin):
	list_display = ['title', 'slug', 'status', 'parent', 'position']
	list_filter  = ['position', 'status']
	prepopulated_fields = {'slug' : ('title',)}
	search_fields = ('title', 'slug', 'position')
	ordering = ['-parent', 'status']
admin.site.register(ArticleCategory, CategoryAdmin)


class ArticleAdmin (admin.ModelAdmin):
	list_display = ['title', 'slug', 'jpublish', 'show_thumbnail', 'is_special', 'category_to_str', 'author', 'descripiton', 'status']
	list_filter  = ['publish', 'status']
	prepopulated_fields = {'slug' : ('title',)}
	search_fields = ('title', 'slug', 'descripiton')
	ordering = ['-publish', 'status']
	actions = [make_publish, make_draft]
admin.site.register(Article, ArticleAdmin)
admin.site.register(IpAddress)