from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

#twitter表示用
class Post(models.Model):
    # id = AutoField(primary_key=True)  # 自動的に追加されるので定義不要
    tweet_id = models.CharField(max_length=25,primary_key=True) #primary_key=True,null blank
    tweet_words = models.TextField(max_length=140)
    tweet_date = models.DateTimeField(default=timezone.now)
    tweet_origin = models.URLField(max_length=200,null=True)
    blog_published_date = models.DateTimeField(blank=True,null=True)
    blog_update_date = models.DateTimeField(blank=True,null=True)
    blog_content = MarkdownxField('content', help_text='markdown format',max_length=1000,null=True) #マイクロブログ本文
    blog_category = models.CharField(max_length=25,null=True,blank=True) #ブログカテゴリ
    blog_tag = models.CharField(max_length=25,null=True,blank=True) #ブログタグ

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.tweet_words

    def blog_content_to_markdown(self):
        return markdownify(self.blog_content)