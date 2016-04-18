from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json, time

es = Elasticsearch(['es'])

# Receive queued items

created = False
while(not created):
	try: 
		time.sleep(20)
		item_consumer = KafkaConsumer('items', group_id='items_indexer', bootstrap_servers=['kafka:9092'])
		created = True
	except:
		created = False

while True:
	changed = False
	for item in item_consumer:
		changed = True
		new_listing = json.loads((item.value).decode('utf-8'))
		# insert items into elastic search
		es.index(index='items_index', doc_type='listing', id=new_listing['id'], body=new_listing)
	if changed: es.indices.refresh(index='items_index')
