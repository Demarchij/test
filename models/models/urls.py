from django.conf.urls import patterns, include, url
from api import user, item, comment, auth

urlpatterns = patterns('',
	url(r'^api/v1/users/create$', user.create_user),
	url(r'^api/v1/users/(\d+)$', user.find_user),		# find by userid
	url(r'^api/v1/users/(\d+)/update$', user.update_user),	# update by userid

	url(r'^api/v1/items/create$', item.create_item),	# create with userid
	url(r'^api/v1/items/getAllItems$', item.get_all_items),	
	url(r'^api/v1/items/getRecent/(\d+)$', item.get_recent),	
	url(r'^api/v1/items/getItemsUserid$', item.get_items_of_user),	
	url(r'^api/v1/items/(\d+)$', item.find_item),		# lookup by itemid
	url(r'^api/v1/items/(\d+)/update$', item.update_item),	# update by itemid
	url(r'^api/v1/items/(\d+)/comment$', comment.add_comment), # create a comment on an item 

	url(r'^api/v1/comments/(\d+)$', comment.find_comment),
	url(r'^api/v1/comments/(\d+)/update$', comment.update_comment),

	url(r'^api/v1/auth/create$', auth.create_auth),
	url(r'^api/v1/auth/delete$', auth.delete_auth),
	url(r'^api/v1/auth/verifyAuth$', auth.verify_auth),
	url(r'^api/v1/auth/verifyUser$', auth.verify_user_password),
)
