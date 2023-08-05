from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
import importlib
from django.apps import apps
from rest_framework import serializers

from df_permission.permissions import DFMethods
from df_permission.variables import prefix


class Command(BaseCommand):
    def handle(self, *args, **options):
        permission_objects = []

        codenames = list(Permission.objects.filter(name__startswith=prefix).values_list("codename", flat=True))

        content_type = ContentType.objects.get(app_label="auth", model="permission")

        # get all apps
        app_configs = apps.get_app_configs()

        for app in app_configs:
            # Assuming your serializer classes are defined in myapp/serializers.py
            module_name = f"{app.name}.serializers"

            try:
                # import module
                module = importlib.import_module(module_name)

                # Get a list of all serializer classes defined in the module
                serializer_classes = [cls for name, cls in module.__dict__.items() if
                                      isinstance(cls, type) and issubclass(cls, serializers.Serializer)]

                for serializer_class in serializer_classes:
                    # get serializer fields
                    serializer_fields = list(serializer_class().get_fields().keys())

                    fields = serializer_fields

                    # remove model fields
                    if issubclass(serializer_class, serializers.ModelSerializer):
                        model_fields = [field.name for field in serializer_class.Meta.model._meta.fields]
                        fields = [serializer_field for serializer_field in serializer_fields if
                                  serializer_field not in model_fields]

                    # Generate required permissions
                    for action in [DFMethods.CREATE, DFMethods.RETRIEVE, DFMethods.UPDATE, DFMethods.LIST]:
                        for field in fields:
                            codename = f'{action}--{serializer_class.__name__.lower()}--{field}'
                            name = f'{prefix} {action.capitalize()} {serializer_class.__name__} {field}'

                            if codename not in codenames:
                                permission_objects.append(
                                    Permission(codename=codename, name=name, content_type=content_type))
            except Exception:
                pass

        if len(permission_objects) > 0:
            Permission.objects.bulk_create(permission_objects)
