# Generated by Django 2.0.2 on 2019-04-05 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactdata',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='contactdata',
            name='object_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]