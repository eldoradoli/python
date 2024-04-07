from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import User
# Create your views here.


from django.http import JsonResponse
import requests

proxies = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}


def welcome(request):
    data = {'message': '欢迎使用！'}
    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # code = request.POST.get('code')
        code = data.get('code')
        print('code:', code)
        if code:
            appid = 'wxccee12c95a21c005'
            secret = 'f025d2ce6de5717bb718f5e13160628f'
            url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'

            res = requests.get(url, proxies=proxies)
            res_json = res.json()
            openid = res_json.get('openid', None)
            if openid:
                user = User.objects.get(openid=openid)
                return JsonResponse({'openid': openid,'gender':user.user_gender,'avatarindex':user.user_avatar_index,'name':user.user_name})
            else:
                return JsonResponse({'error': 'Failed to get openid'}, status=400)
        else:
            return JsonResponse({'error': 'Missing code'}, status=400)


def check_user_exists(request):
    if request.method == 'GET':
        openid = request.GET.get('openid', None)
        if openid:
            exists = User.objects.filter(openid=openid).exists()
            return JsonResponse({'exists': exists})
        else:
            return JsonResponse({'error': 'Missing openid'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def check_username(request):
    data = json.loads(request.body)
    username = data.get('username', '')
    exists = User.objects.filter(user_name=username).exists()
    return JsonResponse({'exists': exists})

@csrf_exempt
@require_http_methods(["POST"])
def save_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        openid = data.get('openid', None)
        username = data.get('username', '')
        gender = data.get('gender', '')
        avatarindex =data.get('avatarIndex', '')

        if openid:
            user, created = User.objects.get_or_create(openid=openid, defaults={'user_name': username, 'user_gender': gender, 'user_avatar_index': avatarindex})
            if created:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'User already exists'}, status=400)
        else:
            return JsonResponse({'error': 'Missing openid'}, status=400)
