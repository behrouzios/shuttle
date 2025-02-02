# Generated by Django 5.1.3 on 2024-11-22 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_emaillog_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulkemailtask',
            name='progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bulkemailtask',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('canceled', 'Canceled'), ('completed', 'Completed')], max_length=50),
        ),
    ]
