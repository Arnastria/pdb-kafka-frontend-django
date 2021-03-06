from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class VisualizationCustomer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)('events', self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("events", self.channel_name)
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def rating_message(self, text_data):
        text_data_json = text_data
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'type':'rating',
            'message': message
        }))
    
    def average_rating_message(self, text_data):
        text_data_json = text_data
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'type':'average_rating',
            'message': message
        }))
    
    def average_age_message(self, text_data):
        text_data_json = text_data
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'type':'average_age',
            'message': message
        }))
    
    def sales_message(self, text_data):
        text_data_json = text_data
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'type':'sales',
            'message': message
        }))