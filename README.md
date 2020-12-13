## PDB Big Data Project
#### Python Django + React (?) as Frontend
----
This is a simple django app and frontend for displaying data from Kafka topics.

Prerequisite :
- Python with **Django 3**
- Redis. [Install it from here](https://redis.io/download) or any other installation source like ```apt-get``` and ```brew```. Make sure redis is started at port **6379**

## How to Run
### Install requirements.txt :
- It is better to use python virtual environment 
```
pip install -r requirements.txt
```
### Migrate any migration :
* make sure you are at directory with ```manage.py```
```
python manage.py migrate
```
### Runserver :
* make sure you are at directory with ```manage.py```
```
python manage.py runserver
```
