# Generated by Django 3.2.25 on 2024-05-28 12:29

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import nautobot.core.celery
import nautobot.extras.models.mixins
import nautobot.extras.models.statuses
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0058_jobresult_add_time_status_idxs"),
    ]

    operations = [
        migrations.CreateModel(
            name="Design",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                (
                    "job",
                    models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to="extras.job"),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            bases=(
                models.Model,
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
            ),
        ),
        migrations.CreateModel(
            name="Deployment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("name", models.CharField(max_length=255)),
                ("first_implemented", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_implemented", models.DateTimeField(blank=True, null=True)),
                ("version", models.CharField(blank=True, default="", max_length=20)),
                (
                    "design",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="deployments",
                        to="nautobot_design_builder.design",
                    ),
                ),
                (
                    "status",
                    nautobot.extras.models.statuses.StatusField(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="deployment_statuses",
                        to="extras.status",
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "verbose_name": "Design Deployment",
                "verbose_name_plural": "Design Deployments",
            },
            bases=(
                models.Model,
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
            ),
        ),
        migrations.CreateModel(
            name="ChangeSet",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("active", models.BooleanField(default=True, editable=False)),
                (
                    "deployment",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="change_sets",
                        to="nautobot_design_builder.deployment",
                    ),
                ),
                (
                    "job_result",
                    models.OneToOneField(
                        editable=False, on_delete=django.db.models.deletion.PROTECT, to="extras.jobresult"
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "ordering": ["-last_updated"],
            },
            bases=(
                models.Model,
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
            ),
        ),
        migrations.CreateModel(
            name="ChangeRecord",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("index", models.IntegerField()),
                ("_design_object_id", models.UUIDField()),
                (
                    "changes",
                    models.JSONField(
                        blank=True, editable=False, encoder=nautobot.core.celery.NautobotKombuJSONEncoder, null=True
                    ),
                ),
                ("full_control", models.BooleanField(editable=False)),
                ("active", models.BooleanField(default=True, editable=False)),
                (
                    "_design_object_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="+", to="contenttypes.contenttype"
                    ),
                ),
                (
                    "change_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="nautobot_design_builder.changeset",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="design",
            constraint=models.UniqueConstraint(fields=("job",), name="unique_designs"),
        ),
        migrations.AddConstraint(
            model_name="deployment",
            constraint=models.UniqueConstraint(fields=("design", "name"), name="unique_deployments"),
        ),
        migrations.AlterUniqueTogether(
            name="deployment",
            unique_together={("design", "name")},
        ),
        migrations.AlterUniqueTogether(
            name="changerecord",
            unique_together={("change_set", "index"), ("change_set", "_design_object_type", "_design_object_id")},
        ),
    ]
