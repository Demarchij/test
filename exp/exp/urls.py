from django.conf.urls import patterns, include, url
from exp import data_retrieval_api, auth_api, search_api

urlpatterns = patterns('',
	url(r'^api/data/all$', data_retrieval_api.get_all_items),
	url(r'^api/data/recent/(\d+)$', data_retrieval_api.get_recent_items),
	url(r'^api/data/createItem$', data_retrieval_api.create_item),
	url(r'^api/data/getItemsUserid$', data_retrieval_api.get_items_of_user),

	url(r'^api/auth/verify$', auth_api.verify_auth),
	url(r'^api/auth/login$', auth_api.login),
	url(r'^api/auth/logout$', auth_api.logout),
	url(r'^api/auth/register$', auth_api.register),

	url(r'^api/search/searchItems$', search_api.search_items),
)
