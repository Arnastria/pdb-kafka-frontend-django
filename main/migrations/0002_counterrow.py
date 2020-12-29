# Generated by Django 3.1.4 on 2020-12-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CounterRow',
            fields=[
                ('cnt_id', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='cntr_id')),
                ('cnt', models.IntegerField(verbose_name='counter')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
