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
* **Warning please start the [kafka-backend](https://github.com/Arnastria/Kafka-big-data-project) first before this !!!**
* make sure you are at directory with ```manage.py```
```
python manage.py runserver
```

### Tugas :
* Benerin initable.sql di repo kafka. Supaya bentuk tabelnya sesuai sama dataset
* Bikin coded python queryinserter yang:
```
- bisa baca CSV / apapun dataset yang kita pake kemaren
- setengah dimasukin, setengah dibiarin
- baca nya berkala, 5 baris-baris setiap 5 detik, terus tembak terus kayak yang dicontoh.
```
* Django :
```
- Bikin django models untuk nyimpen data ()
- Bikin endpoint (websocket) lagi kalau disuruh > 1 topik
```

* React :
```
- Bikin react project
- somehow konek ke websocket
- Bikin halaman dashboard yang isinya 1 tabel 2 grafik 
```
