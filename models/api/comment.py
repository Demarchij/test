from django.http import JsonResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django import db
from models import models
from datetime import datetime, timedelta

def add_comment(request, item_id):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'owner' not in request.POST or  \
       'text' not in request.POST:     \
       return _error_response(request, "missing required fields")
       
    # Check if the owner exists
    try: user = models.User.objects.get(username=request.POST['owner'])
    except models.User.DoesNotExist: return _error_response(request, "user not found")
    # Check if the item exists
    try: i = models.Item.objects.get(pk=item_id)
    except models.Item.DoesNotExist: return _error_response(request, "item not found")
   
    c = models.Comment(owner=user,              \
                    item=i,                     \
                    text=request.POST['text'],  \
                    )
    try: c.save()
    except db.Error: return _error_response(request, "db error")
    return _success_response(request, {'comment_id': c.pk})

def find_comment(request, comment_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")
    try: c = models.Comment.objects.get(pk=comment_id)
    except models.Comment.DoesNotExist:
        return _error_response(request, "comment not found")
    return _success_response(request, {'owner': c.owner.pk,   \
                                       'item': c.item.pk,     \
                                       'text': c.text,	      \
                                       })

def update_comment(request, comment_id):
    if request.method != 'POST': return _error_response(request, "must make POST request")
    try: c = models.Comment.objects.get(pk=comment_id)
    except models.Comment.DoesNotExist: return _error_response(request, "comment not found")

    changed = False
    if 'owner' in request.POST:
        try: user = models.User.objects.get(username=request.POST['owner'])
        except models.User.DoesNotExist: return _error_response(request, "user not found")
        c.owner = user
        changed = True
    if 'item' in request.POST:
        try: i = models.Item.objects.get(pk=request.POST['item'])
        except models.Item.DoesNotExist: return _error_response(request, "item not found")
        c.item = i        
        changed = True
    if 'text' in request.POST:
        c.text = request.POST['text']
    if not changed: return _error_response(request, "no fields updated")
    c.save()
    return _success_response(request)

def _success_response(request, resp=None):
    if resp: return JsonResponse({'ok': True, 'resp': resp})
    else: return JsonResponse({'ok': True})

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})
