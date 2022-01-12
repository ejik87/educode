from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views


#app_name = "news"
urlpatterns = [
    path('', views.hello),
    path('news/', views.NewsShow.as_view(), name='news_page'),
    path('news/<int:link>/', views.news_view, name='article'),
    path('news/create/', views.NewsPost.as_view(), name='post_news'),
]
