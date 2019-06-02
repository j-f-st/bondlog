from django.shortcuts import render, redirect, get_object_or_404
#twitter
from requests_oauthlib import OAuth1Session
import time, calendar
import datetime
import json
import re
import os
import requests
import sys, codecs


## デバッグフラグ ##
DEBUG = False
## ---------- ##
try:
	from . import config
except ImportError:
	pass
## -----------##


sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
from django.http.response import HttpResponse


from .models import Post

#twitter更新(直近200件までしか取得できない(19/5現在)(やろうと思えば出来る))->redirect admin画面
def gettweet(request):

	# C_KEY = os.environ["CONSUMER_KEY"]
	C_KEY = config.CONSUMER_KEY

	# C_SECRET = os.environ["CONSUMER_SECRET"]
	C_SECRET = config.CONSUMER_SECRET

	# A_KEY = os.environ["ACCESS_TOKEN"]
	A_KEY = config.ACCESS_TOKEN

	# A_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
	A_SECRET = config.ACCESS_TOKEN_SECRET


	# T_UN = os.environ["TWITTER_USERNAME"]
	T_UN = config.TWITTER_USERNAME

	###===================================================###
	# C_KEY C_SECRET A_KEY A_SECRET T_UN 上:heroku 下:ローカル #
	###===================================================###

	twitter = OAuth1Session(C_KEY,C_SECRET,A_KEY,A_SECRET) #認証

	url = "https://api.twitter.com/1.1/statuses/user_timeline.json" #タイムライン取得エンドポイント
	params = {'count': 300}
	req = twitter.get(url, params = params)

	if req.status_code == 200:
		timelines = json.loads(req.text) #配列で入ってるタイムライン
		limit = req.headers['x-rate-limit-remaining']

		#更新部
		postchecks = Post.objects.values('tweet_id')
		#リスト形式

		for tweet in timelines:

			#既存DBに無いtweet(id)分のみをDBに登録
			if 	tweet['id_str'] not in postchecks:

				data = Post()

				data.tweet_words = tweet['text']
				data.tweet_date = YmdHMS(tweet['created_at'])
				data.tweet_id = tweet['id_str']
				#tweetリンクURL設定
				data.tweet_origin = 'https://twitter.com/' + T_UN + '/status/' + tweet['id_str']

				data.save()

		return redirect('admin/')

	#error時
	else:
		return redirect('admin/')

#twitterの日時形式をDB用に変更用関数
def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_local)

#homeにアクセス時
def home(request):

	posts = Post.objects.all()

	#検索窓
	searchForm = SearchForm()

	return render(request, 'home.html', {'posts': posts ,'searchform': searchForm }) #第2 template , 第3 タプルで渡す、keyが表示変数


# 個別記事
def detail(request ,key):
	# adminで作成した記事を全て出す
	detail = get_object_or_404(Post, tweet_id=key)

	#検索窓
	searchForm = SearchForm()

	return render(request, 'detail.html',{'detail': detail,'searchform': searchForm})


# 検索時
from .forms import SearchForm

def search(request):
	searchForm = SearchForm(request.POST)

	message = ''

	if searchForm.is_valid():
		keyword = searchForm.cleaned_data['keyword']
		posts = Post.objects.filter(blog_content__icontains=keyword)
		if len(posts) == 0:
			message = '検索結果はありません(記事一覧へ戻る)'
	else:
		searchForm = SearchForm()
		posts = Post.objects.all()
		message = '入力文字をご確認下さい(記事一覧へ戻る)'

	reaction = {
		'message': message,
		'posts': posts, #記事データ
		'searchform': searchForm, #検索文字
	}

	return render(request, 'home.html', reaction)