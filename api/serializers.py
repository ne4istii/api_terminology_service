from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from directories.models import Directory, Item, Version

PUB_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class VersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Version
        fields = ('name', 'pub_date')


class DirectorySerializer(serializers.ModelSerializer):
    current_version = serializers.SerializerMethodField()
    creation_date = serializers.SerializerMethodField()

    def get_current_version(self, obj):
        current_version = Version.objects.filter(directory=obj.pk)
        if not current_version:
            raise ValidationError(
                'Ошибка заполнения справочника! '
                'У справочника нету актуальной версии!'
            )
        return VersionSerializer(current_version.latest('pub_date')).data

    def get_creation_date(self, obj):
        creation_date = Version.objects.filter(directory=obj.pk)
        if not creation_date:
            raise ValidationError(
                'Ошибка заполнения справочника! '
                'У справочника отсутствует начальная версия!'
            )
        value = creation_date.earliest('pub_date').pub_date
        return timezone.localtime(value).strftime(PUB_DATE_FORMAT)

    class Meta:
        model = Directory
        fields = ('uid', 'name', 'title', 'current_version', 'creation_date')


class ItemGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class ItemValidateSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        return obj['result']

    class Meta:
        model = Item
        fields = ('result',)
