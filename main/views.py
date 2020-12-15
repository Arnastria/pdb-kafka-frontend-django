from django.shortcuts import render
from threading import Thread
import websocket
from websocket import create_connection
import time, json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from kafka import KafkaConsumer
from json import loads
from pdbfrontend import settings
import queue
import time

# Create your views here.

ratingThread = None
queueThread = None
bus_code = "MYS"
obj_queue = queue.Queue()

def put_queue_thread(obj):
    obj_queue.put(obj)
    
def save_queue_thread():
    while True:
        if (obj_queue.qsize() != 0):
            obj = obj_queue.get()
            obj.save()
            print("[STORE] " + str(obj))

def rating_thread():
    print("asik")
    consumer = KafkaConsumer(
        'dbserver1.rating.product_rating',
        bootstrap_servers=[settings.KAFKA_PRODUCER_IP+':9092'],
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    consumer.poll()
    #go to end of the stream
    consumer.seek_to_end()
    for message in consumer:
        try:
            msg = message.value['payload']['after']
            channel_layer = get_channel_layer()
            print("<><><><><>")
            print(msg)
            print("<><><><><>")
            async_to_sync(channel_layer.group_send)("events", {"type": "rating.message","message": message.value})
        except Exception as e:
            print(str(e))

def index(request):

    global obj_queue

    global bus_code
    # bus_code = request.GET['bus_code']

    global ratingThread
    if ratingThread is None:
        thread = Thread(target=rating_thread)
        thread.daemon = True
        thread.start()
        ratingThread = True

    global queueThread
    if queueThread is None:
        thread = Thread(target=save_queue_thread)
        thread.daemon = True
        thread.start()

    print(settings.KAFKA_PRODUCER_IP)

    response = {"bus_code":bus_code}
    return render(request, 'index.html', response)