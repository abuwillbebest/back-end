# from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Novel, Chapter
import math


def validate(d: dict, name: str, type_func, default, validate_func):
    try:  # 页码
        result = type_func(d.get(name, default))
        result = validate_func(result, default)
    except:
        result = default
    return result


def getbytype(request: HttpRequest, typeid):  # 类型
    typemap = {1: '奇幻玄幻', 2: '武侠仙侠', 3: '历史军事', 4: '都市娱乐'}
    t = typemap.get(int(typeid), 'All')
    page = validate(request.GET, 'page', int, 1, lambda x, y: x if x > 0 else 1)
    size = validate(request.GET, 'size', int, 9, lambda x, y: x if 101 > x > 0 else y)

    try:
        start = (page - 1) * size
        if t == 'All':
            posts = Novel.objects.order_by('-id')
        else:
            posts = Novel.objects.filter(noveltype=t).order_by('-id')
        count = posts.count()
        posts = posts[start:start + size]
        return JsonResponse({
            'info': {
                'noveltype': t
            },
            'posts': [
                {
                    'post_id': post.id,
                    'title': post.title,
                    'desc': post.desc[0:30],
                    'author': post.author
                } for post in posts
            ],
            'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages': math.ceil(count / size)
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def getbynovel(request: HttpRequest, novelid):  # 章节
    page = validate(request.GET, 'page', int, 1, lambda x, y: x if x > 0 else 1)
    size = validate(request.GET, 'size', int, 16, lambda x, y: x if 101 > x > 0 else y)

    try:
        start = (page - 1) * size
        posts = Chapter.objects.filter(novel_id=novelid).order_by('id')
        count = posts.count()
        posts = posts[start:start + size]
        return JsonResponse({
            'header': {
                'novel_id': posts.first().novel_id,
                'title': posts.first().novel.title,
                'desc': posts.first().novel.desc,
                'noveltype': posts.first().novel.noveltype,
                'tags': posts.first().novel.tags
            },
            'posts': [
                {
                    'post_id': post.id,
                    'c_title': post.c_title,
                    'content_id': post.content_id
                } for post in posts
            ],
            'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages': math.ceil(count / size)
            }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def getcontent(request: HttpRequest, contentid):  # 正文
    try:
        post = Chapter.objects.filter(content_id=contentid).get()
        paragraph = post.content.content
        chapterslist = Chapter.objects.filter(novel_id=post.novel_id)
        print(chapterslist)
        return JsonResponse({
            'info': {
                'novel_id': post.novel_id,
                'title': post.novel.title,
                'author': post.novel.author,
                'c_title': post.c_title,
                'words': post.words,
                'ctime': post.ctime,
                'noveltype': post.novel.noveltype,
                'chapterslist': [i.content_id for i in chapterslist]
            },
            'posts': paragraph
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
