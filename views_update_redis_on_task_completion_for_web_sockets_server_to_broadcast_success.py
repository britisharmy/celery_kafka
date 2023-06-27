from celery import Celery
from kafka import KafkaConsumer
import json
import redis

# Create a Celery instance
celery = Celery('worker', broker='kafka://localhost:9092')

# Create a Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Define the task
@celery.task
def process_task(arg1, arg2):
    result = arg1 + arg2
    return result

# Define the worker
@celery.task
def worker():
    # Create a Kafka consumer
    consumer = KafkaConsumer('celery', bootstrap_servers='localhost:9092')

    # Continuously listen for tasks from Kafka
    for message in consumer:
        # Retrieve the task data from the Kafka message
        task_data = json.loads(message.value.decode('utf-8'))

        # Extract the arguments
        arg1 = task_data['arg1']
        arg2 = task_data['arg2']

        # Perform the task
        result = process_task.delay(arg1, arg2)

        # Print the result (you can modify this part to handle the result as desired)
        print(f"Task processed: arg1={arg1}, arg2={arg2}, result={result.get()}")

        # Insert message into Redis after the task is successfully completed
        redis_client.set('task_status', 'Task done successfully')

if __name__ == '__main__':
    # Start the worker
    worker()
