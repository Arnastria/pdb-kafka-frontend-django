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
import datetime

from main.models import AverageAge, AverageRating, ProductRating, CounterRow

# Create your views here.

ratingThread = None
queueThread = None
salesThread = None
obj_queue = queue.Queue()

def put_queue_thread(obj):
    print("[Putting object in save queue..] " + str(obj))
    obj_queue.put(obj)
    
def save_queue_thread():
    while True:
        if (obj_queue.qsize() != 0):
            obj = obj_queue.get()
            obj.save()
            print("[Storing Object..] " + str(obj))

def rating_thread():
    print("starting rating_thread")
    consumer = KafkaConsumer(
        'dbserver1.rating.product_rating',
        bootstrap_servers=[settings.KAFKA_PRODUCER_IP+':9092'],
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    consumer.poll()
    
    #go to end of the stream
    # consumer.seek_to_end()

    for message in consumer:
        try:
            timestamp = datetime.datetime.now()
            try:
                counter = CounterRow.objects.get(cnt_id=1)
            except CounterRow.DoesNotExist:
                counter = CounterRow.create(1,1,timestamp)

            msg = message.value['payload']
            channel_layer = get_channel_layer()
            print("[Getting data from kafka..]")
            print(msg)
            print()
            async_to_sync(channel_layer.group_send)("events", {"type": "rating.message","message": msg})

            thread_avg_rating = Thread(target=average_rating_thread, args=(msg,counter.cnt,))
            thread_avg_age = Thread(target=average_age_thread, args=(msg,counter.cnt,))
            thread_avg_rating.start()
            thread_avg_age.start()

            counter.cnt = counter.cnt +1
            thread_cnt = Thread(target=put_queue_thread,args=(counter,))
            thread_cnt.start()
        except Exception as e:
            print(str(e))

def average_rating_thread(msg,cnt):
    print("starting average_rating_thread")
    try:
        msg = msg['after']
        average_rating = msg['rating']
        timestamp = datetime.datetime.now()

        try:
            current_avg_rating = AverageRating.objects.get(avg_id=1)
            current_avg_rating.average_rating = (current_avg_rating.average_rating*cnt + average_rating)/(cnt+1)
            current_avg_rating.timestamp = timestamp
        except AverageRating.DoesNotExist:
            current_avg_rating = AverageRating.create(1,average_rating,timestamp)

        data_dict = current_avg_rating.to_dict()
        data_dict['timestamp'] = str(data_dict['timestamp'])
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("events", {"type": "average_rating.message","message": data_dict})


        thread = Thread(target=put_queue_thread,args=(current_avg_rating,))
        thread.start()
    except Exception as e :
        print(str(e))

def average_age_thread(msg,cnt):
    print("starting average_age_thread")
    try:
        msg = msg['after']
        average_age = msg['age']
        timestamp = datetime.datetime.now()

        try:
            current_avg_age = AverageAge.objects.get(avg_id=1)
            current_avg_age.average_age = (current_avg_age.average_age*cnt + average_age)/(cnt+1)
            current_avg_age.timestamp = timestamp
        except AverageAge.DoesNotExist:
            current_avg_age = AverageAge.create(1,average_age,timestamp)

        data_dict = current_avg_age.to_dict()
        data_dict['timestamp'] = str(data_dict['timestamp'])
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("events", {"type": "average_age.message","message": data_dict})

        thread = Thread(target=put_queue_thread,args=(current_avg_age,))
        thread.start()
    except Exception as e :
        print(str(e))

def sales_thread():
    print("starting sales_thread")
    consumer = KafkaConsumer(
        'sales.most-sales-product',
        bootstrap_servers=[settings.KAFKA_PRODUCER_IP+':9093'],
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    consumer.poll()
    

    for message in consumer:
        try:
            msg = message.value
            channel_layer = get_channel_layer()
            print("[Getting data from kafka..]")
            print(msg)
            print()
            async_to_sync(channel_layer.group_send)("events", {"type": "sales.message","message": msg})

        except Exception as e:
            print(str(e))

def index(request):

    global obj_queue

    global ratingThread
    if ratingThread is None:
        thread = Thread(target=rating_thread)
        thread.daemon = True
        thread.start()

    global queueThread
    if queueThread is None:
        thread = Thread(target=save_queue_thread)
        thread.daemon = True
        thread.start()
    
    global salesThread
    if salesThread is None:
        thread = Thread(target=sales_thread)
        thread.daemon = True
        thread.start()

    print(settings.KAFKA_PRODUCER_IP)

    response = {"rating":"bruh"}
    return render(request, 'index.html', response)