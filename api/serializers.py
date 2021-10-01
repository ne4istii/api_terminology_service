from django.utils import dateparse, timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from directories.models import Directory, Item, Version

PUB_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class ItemGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class VersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Version
        fields = ('name', 'pub_date')


class DirectorySerializer(serializers.ModelSerializer):
    current_version = serializers.SerializerMethodField()
    creation_date = serializers.SerializerMethodField()

    def get_current_version(self, obj):
        '''
        Serialize the current version of the directory:
        if the date is specified in the query params, then
        filter the version of the directory not later than this date,
        else - get the latest version.
        '''
        search_date = self.context['request'].query_params.get('search', None)
        filtered_version = Version.objects.filter(directory=obj.pk)
        if search_date:
            search_date_obj = dateparse.parse_date(search_date)
            filtered_version = filtered_version.filter(
                pub_date__lte=search_date_obj
            )
        return VersionSerializer(filtered_version.latest('pub_date')).data

    def get_creation_date(self, obj):
        '''
        Serializing the creation date of the directory
        (pub_date of the first version).
        '''
        creation_date = Version.objects.filter(directory=obj.pk)
        if not creation_date:
            raise ValidationError(
                'Error filling the directory! '
                'The directory is missing an initial version!'
            )
        value = creation_date.earliest('pub_date').pub_date
        return timezone.localtime(value).strftime(PUB_DATE_FORMAT)

    class Meta:
        model = Directory
        fields = ('uid', 'name', 'title', 'current_version', 'creation_date')


class ItemValidateSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        '''Serializing the validation results of a directory element.'''
        if obj:
            return True
        return False

    class Meta:
        model = Item
        fields = ('result',)
