from django.contrib import admin

#models機能利用
from .models import Post

admin.site.index_title = ''

class PostAdmin(admin.ModelAdmin):
	list_display = ('tweet_id', 'tweet_words', 'tweet_date')
	search_fields = ['tweet_words']
	list_filter = ('tweet_date', 'blog_category', 'blog_tag')
	list_per_page = 30
	ordering = ['-tweet_date']

admin.site.register(Post,PostAdmin)