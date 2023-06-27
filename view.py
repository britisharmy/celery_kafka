from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
import json

@csrf_exempt
def insert_to_kafka(request):
    if request.method == 'GET':
        # Extract the arguments from the request
        arg1 = request.GET.get('arg1')
        arg2 = request.GET.get('arg2')

        # Create a Kafka producer
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        # Prepare the task data as a dictionary
        task_data = {
            'arg1': arg1,
            'arg2': arg2
        }

        # Convert the task data to JSON and send it to Kafka
        producer.send('celery', value=task_data)

        # Close the Kafka producer
        producer.close()

        # Return a response indicating successful insertion
        return HttpResponse("Data inserted into Kafka.")

    # Return an error response for unsupported request methods
    return HttpResponse(status=405)
