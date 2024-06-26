# Generated by Django 4.2.7 on 2023-11-28 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0004_remove_classmodel_age_remove_classmodel_email_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("age", models.IntegerField()),
                (
                    "class_attending",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crm.classmodel"
                    ),
                ),
            ],
        ),
    ]
