from django.http import JsonResponse, HttpResponse
import urllib.request, urllib.parse, json
from exp import settings
from elasticsearch import Elasticsearch

def search_items(request):
	if request.method != 'GET': return _error_response(request, "must make GET request")
	search_query = request.GET['search_query'] if 'search_query' in request.GET else ""
	# get data from elastic search
	es = Elasticsearch(['es'])
	try: query_results = es.search(index='items_index', body={'query': {'query_string': {'query': str(search_query)}}, 'size': 10})
	except: return _error_response(request, "Problem fetching search results")
	search_results = []
	for i in query_results['hits']['hits']:
		item_data = i['_source']
		item_id = item_data['id']
		url = 'http://' + settings.MODELS_API + ':8000/api/v1/items/' + str(item_id) 
		req = urllib.request.Request(url)
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		if (resp["ok"] == False): return _error_response(request, resp["error"])
		search_results.append(resp['resp'])
	return _success_response(request, {"search_results": search_results})

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp: return JsonResponse({'ok': True, 'resp': resp})
    else: return JsonResponse({'ok': True})
