from django.http import JsonResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django import db
from models import models
from datetime import datetime, timedelta

# APIs for accessing Users

def create_user(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'username' not in request.POST or     \
       'email' not in request.POST or        \
       'password' not in request.POST or     \
       'phone' not in request.POST:
        return _error_response(request, "missing required fields")
    u = models.User(username=request.POST['username'],                         \
                    email=request.POST['email'],                               \
                    phone=request.POST['phone'],                               \
                    password=hashers.make_password(request.POST['password']),  \
                    )

    try: u.save()
    except db.Error as e: return _error_response(request, "db error")
    return _success_response(request, {'user_id': u.pk})

def find_user(request, user_id):
    if request.method != 'GET': return _error_response(request, "must make GET request")
    try: u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist: return _error_response(request, "user not found")
    return _success_response(request, {'username': u.username,    \
                                       'email': u.email,          \
                                       'phone': u.phone,          \
                                       'user_id': u.id
                                       })

def update_user(request, user_id):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    try: u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")

    changed = False
    if 'username' in request.POST:
        u.username = request.POST['username']
        changed = True
    if 'email' in request.POST:
        u.email = request.POST['email']
        changed = True
    if 'password' in request.POST:
        u.password = hashers.make_password(request.POST['password'])
        changed = True
    if 'phone' in request.POST:
        u.phone = request.POST['phone']
        changed = True
    if not changed: return _error_response(request, "no fields updated")
    u.save()
    return _success_response(request)

def _success_response(request, resp=None):
    if resp: return JsonResponse({'ok': True, 'resp': resp})
    else: return JsonResponse({'ok': True})

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})
