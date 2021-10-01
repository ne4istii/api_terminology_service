from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView

from directories.models import Directory, Item, Version

from .filters import DirectoryFilter
from .serializers import (DirectorySerializer, ItemGetSerializer,
                          ItemValidateSerializer)


class DirectoryListView(ListAPIView):
    '''
    Get a list of directories.
    Can filter by publication date.
    '''
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    filterset_class = DirectoryFilter


class ItemListView(ListAPIView):
    '''
    Get a list of directory items:
    if the version is specified in the request parameters,
    get all items from the specified version,
    otherwise - items from the current version.
    '''
    queryset = Item.objects.all()
    serializer_class = ItemGetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'directory_version' in self.kwargs:
            directory_uid, directory_version = self.kwargs.values()
        else:
            directory_uid = self.kwargs.get('directory_uid')
            actual_directory_version = Version.objects.filter(
                directory__uid=directory_uid
            ).order_by('-pub_date').first()
            if not actual_directory_version:
                raise ValidationError(
                    'The directory does not exist!'
                )
            directory_version = actual_directory_version.name
        filtered_queryset = queryset.filter(
            versions__name=directory_version,
            itemsversion__version__directory__uid=directory_uid
        )
        if not filtered_queryset:
            raise ValidationError(
                'This version of the directory does not exist!'
            )
        return filtered_queryset


class ItemValidateView(RetrieveAPIView):
    '''
    Validate a directory element:
    if the version is specified in the request parameters,
    the item in the specified version is checked,
    otherwise - the item is in the current version.
    '''
    queryset = Item.objects.all()
    serializer_class = ItemValidateSerializer

    def get_object(self):
        if 'directory_version' in self.kwargs:
            directory_uid, directory_version, item_code = self.kwargs.values()
            version_name = directory_version
        else:
            directory_uid, item_code = self.kwargs.values()
            directory_version = Version.objects.filter(
                directory__uid=directory_uid
            ).order_by('-pub_date').first()
            if not directory_version:
                raise ValidationError(
                    'The directory does not exist!'
                )
            version_name = directory_version.name
        directory_items = Item.objects.filter(
            itemsversion__version__directory__uid=directory_uid,
            versions__name=version_name,
        )
        if not directory_items:
            raise ValidationError(
                'The directory does not exist!'
            )
        return directory_items.filter(code=item_code)
