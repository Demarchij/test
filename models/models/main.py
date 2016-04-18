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
    if request.method != 'GET':
        return _error_response(request, "must make GET request")
    try: u = models.User.objects.get(pk=user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")
    return _success_response(request, {'username': u.username,    \
                                       'email': u.email,          \
                                       'phone': u.phone,          \
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

def create_item(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'owner' not in request.POST or   \
       'title' not in request.POST or   \
       'description' not in request.POST or   \
       'filename' not in request.POST or   \
       'size' not in request.POST or   \
       'tags' not in request.POST or   \
       'category' not in request.POST:   \
       return _error_response(request, "missing required fields")
       
    # Check if the owner exists
    try:
        user = models.User.objects.get(username=request.POST['owner'])
    except models.User.DoesNotExist:
        return _error_response(request, "user not found")
    # Check if the categories exist
    categories = request.POST.copy().pop('category')
    categories_to_add = []
    for cat in categories:
        try:
            c = models.ItemCategory.objects.get(category=cat)
            categories_to_add.append(c)
        except models.ItemCategory.DoesNotExist:
            pass
    categories_to_add = list(set(categories_to_add))

    # Check if tags exist, if not, create them
    tags = request.POST.copy().pop('tags')
    tags_to_add = []
    for t in tags:
        try: 
            tag = models.Tag.objects.get(token=t)
            tags_to_add.append(tag)
        except models.Tag.DoesNotExist: 
            tag = models.Tag.objects.create(token=t)
            tags_to_add.append(tag) 
    tags_to_add = list(set(tags_to_add))   
    i = models.Item(owner=user,                                 \
                    title=request.POST['title'],              \
                    description=request.POST['description'],    \
                    filename=request.POST['filename'],          \
                    size=request.POST['size'],                  \
                    )
    try: 
        i.save()
        i.tags.add(*tags_to_add)
        i.category.add(*categories_to_add)
    except db.Error: return _error_response(request, "db error")
    return _success_response(request, {'item_id': i.pk})

def find_item(request, item_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")
    try: i = models.Item.objects.get(pk=item_id)
    except models.Item.DoesNotExist:
        return _error_response(request, "item not found")
    return _success_response(request, {'owner': i.owner.pk,           \
                                       'title': i.title,              \
                                       'description': i.description,  \
                                       'filename': i.filename,	      \
                                       'size': i.size,	              \
                                       'date_created' : i.date_created, \
                                       'tags': [t.json() for t in i.tags.all()],	              \
                                       'category': [c.json() for c in i.category.all()],	      \
                                       })

def update_item(request, item_id):
    if request.method != 'POST': return _error_response(request, "must make POST request")
    try: i = models.Item.objects.get(pk=item_id)
    except models.Item.DoesNotExist: return _error_response(request, "item not found")

    tags_to_add = []
    categories_to_add = []
    changed = False
    if 'owner' in request.POST:
        try: user = models.User.objects.get(username=request.POST['owner'])
        except models.User.DoesNotExist: return _error_response(request, "user not found")
        i.owner = user
        changed = True
    if 'title' in request.POST:
        i.title = request.POST['title']
        changed = True
    if 'description' in request.POST:
        i.description = request.POST['description']
        changed = True
    if 'filename' in request.POST:
        i.filename = request.POST['filename']
        changed = True
    if 'size' in request.POST:
        i.size = request.POST['size']
        changed = True
    if 'category' in request.POST:
        categories = request.POST.copy().pop('category')
        for cat in categories:
            try:
                c = models.ItemCategory.objects.get(category=cat)
                categories_to_add.append(c)
            except models.ItemCategory.DoesNotExist:
                pass
        categories_to_add = list(set(categories_to_add))     
        changed = True
    if 'tags' in request.POST:
        tags = request.POST.copy().pop('tags')
        for t in tags:
            try: 
                tag = models.Tag.objects.get(token=t)
                tags_to_add.append(tag)
            except models.Tag.DoesNotExist: 
                tag = models.Tag.objects.create(token=t)
                tags_to_add.append(tag) 
        tags_to_add = list(set(tags_to_add))   
        changed = True
    if not changed: return _error_response(request, "no fields updated")
    i.save()
    i.tags.clear()
    i.tags.add(*tags_to_add)
    i.category.clear()
    i.category.add(*categories_to_add)
    return _success_response(request)

def get_all_items(request):
    if request.method != 'GET': return _error_response(request, "must make GET request")
    all_items = models.Item.objects.all()
    return _success_response(request, {'items': [i.json() for i in all_items],       \
                                       })
def get_recent(request, quantity):
    quantity = int(quantity)
    if request.method != 'GET': return _error_response(request, "must make GET request")
    if quantity < 0: return _error_response(request, "Must be positive integer")
    items = models.Item.objects.order_by('-date_created')[:quantity]
    return _success_response(request, {'items': [i.json() for i in items],       \
                                       })
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
