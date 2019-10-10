# from django.shortcuts import render

# Create your views here.

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
import simplejson
from .models import User
from django.conf import settings
import jwt
import datetime
from bcrypt import hashpw, checkpw, gensalt

AUTH_EXPIRE = 8 * 60 * 60


def gen_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE
    }, settings.SECRET_KEY, 'HS256').decode()


def authenticate(view):
    def wrapper(request: HttpRequest):
        payload = request.META.get('HTTP_JWT')
        if not payload:
            return HttpResponse(status=401)
        try:
            payload = jwt.decode(payload, settings.SECRET_KEY, algorithms=['HS256'])
            # 验证失败会抛出错误

            user_id = payload.get('user_id', -1)
            user = User.objects.filter(pk=user_id).get()
            request.user = user
        except Exception as e:
            print(e)
            return HttpResponse(status=401)
        return view(request)

    return wrapper


def reg(request: HttpRequest):
    print(request.body)
    payload = simplejson.loads(request.body)
    try:
        email = payload['email']
        query = User.objects.filter(email=email)
        if query:
            return HttpResponseBadRequest()
        name = payload['name']
        # password = payload['password']
        password = hashpw(payload['password'].encode(), gensalt())
        print(email, name, password)

        user = User()
        user.email = email
        user.name = name
        user.password = password

        try:
            user.save()
            return JsonResponse({'token': gen_token(user.id)})
        except:
            raise
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def login(request: HttpRequest):
    payload = simplejson.loads(request.body)
    try:
        email = payload['email']
        user = User.objects.filter(email=email).get()

        if checkpw(payload['password'].encode(), user.password.encode()):
            token = gen_token(user.id)
            res = JsonResponse({
                'user': {
                    'user_id': user.id,
                    'name': user.name,
                    'email': user.email,
                }, 'token': token
            })

            res.set_cookie('Jwt', token)
            return res
        else:
            return HttpResponseBadRequest()

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
