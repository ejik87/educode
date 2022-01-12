from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views import View
from json import load, loads, dump, dumps


def json_load():
    with open(settings.NEWS_JSON_PATH, 'r') as json_file:
        return load(json_file)


def hello(request):
    return redirect('news/')


class NewsShow(View):

    def get(self, request, *args, **kwargs):
        news_list = json_load()
        search_list = list()
        if request.GET.get('q'):
            for art in news_list:
                if request.GET.get('q') in art['title']:
                    search_list.append(art)
        else:
            search_list = news_list
        return render(request, 'news/list_news.html', {'news': search_list})


def news_view(request, link):
    news_list = json_load()
    current_news = {}
    for jsn in news_list:
        if jsn['link'] == link:
            current_news = jsn
    return render(request, 'news/article.html', {'current_news': current_news})


class NewsPost(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        news_list = json_load()
        post_dict = {'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     'text': request.POST.get('text'),
                     'title': request.POST.get('title'),
                     'link': len(news_list) + 1}
        news_list.append(post_dict)
        json_str = dumps(news_list)
        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            dump(loads(json_str), json_file)
        return redirect('/news/')


'''
    def get(self, request, *args, **kwargs):
        with open(NEWS_JSON_PATH, 'r') as json_file:
            news_dict = json.load(json_file)
        return render(request, 'news/article.html', context={'title': title})
'''
