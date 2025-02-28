# Generated by Django 5.1.6 on 2025-02-13 09:35

import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('is_globally_unsubscribed', models.BooleanField(default=False)),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'workspaces',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O', max_length=1)),
                ('country', django_countries.fields.CountryField(default='US', max_length=2, verbose_name='Country')),
                ('city', models.CharField(default='Los Angeles', max_length=180, verbose_name='City')),
                ('address', models.CharField(max_length=255, null=True)),
                ('zipcode', models.CharField(max_length=255, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='+250784123456', max_length=30, region=None, verbose_name='Phone Number')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profiles',
            },
        ),
    ]
