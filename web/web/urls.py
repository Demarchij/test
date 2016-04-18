from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'web.views.home', name='home'),  
    url(r'^list$', 'web.views.item_list', name='item_list'),
    url(r'^submit$', 'web.views.submit_item', name='submit'),
    url(r'^gallery$', 'web.views.gallery', name='gallery'),

    url(r'^login/', 'web.views.login', name='login'),
    url(r'^logout/', 'web.views.logout', name='logout'),
    url(r'^register/', 'web.views.register', name='register'),

    url(r'^search/', 'web.views.search', name='search'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
