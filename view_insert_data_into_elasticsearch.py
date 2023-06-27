from django.http import JsonResponse
from elasticsearch import Elasticsearch

def insert_document(request):
    # Establish a connection to Elasticsearch
    es = Elasticsearch(hosts=['localhost'])

    # Your complex JSON object
    json_object = {
        'field1': 'value1',
        'field2': 'value2',
        'nested_field': {
            'nested_field1': 'nested_value1',
            'nested_field2': 'nested_value2',
        },
        'array_field': ['item1', 'item2', 'item3'],
        # Add more fields and nesting as needed
    }

    # Index the JSON object in Elasticsearch
    index_name = 'your_index_name'  # Replace with your desired index name
    document_id = 'your_document_id'  # Replace with your desired document ID
    es.index(index=index_name, id=document_id, body=json_object)

    return JsonResponse({'message': 'Document inserted successfully'})
