from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


# views設定利用のための設定
from boards import views

urlpatterns = [
    path('admin/', admin.site.urls),

#twitter取り込みかける(後adminへ)
    path('gettweet', views.gettweet, name='gettweet'),

#ホームの設定
	path('', views.home, name='home'),

	path('detail/<int:key>/', views.detail, name='detail'),

#markdownx
    path('markdownx/', include('markdownx.urls')),

    path('search', views.search),

]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)