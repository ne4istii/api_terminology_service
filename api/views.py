from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView

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
    Get a list of elements of the directory of the current version.
    '''
    queryset = Item.objects.all()
    serializer_class = ItemGetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        dictionary_uid = self.kwargs.get('dictionary_uid')
        actual_dictionary_version = Version.objects.filter(
            directory__uid=dictionary_uid
        ).order_by('-pub_date').first()
        if not actual_dictionary_version:
            raise ValidationError(
                'The directory does not exist!'
            )
        version_name = actual_dictionary_version.name
        return queryset.filter(versions__name=version_name)


class VersionItemListView(ListAPIView):
    '''
    Get a list of directory items for the specified version.
    '''
    queryset = Item.objects.all()
    serializer_class = ItemGetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        dictionary_uid, dictionary_version = self.kwargs.values()
        filtered_queryset = queryset.filter(
            itemsversion__version__name=dictionary_version,
            itemsversion__version__directory__uid=dictionary_uid
        )
        if not filtered_queryset:
            raise ValidationError(
                'This version of the directory does not exist '
                'or elements of the directory are missing!'
            )
        return filtered_queryset


class ItemPostView(CreateAPIView):
    '''
    Validate a directory element of the current version.
    '''
    queryset = Item.objects.all()
    serializer_class = ItemValidateSerializer

    def perform_create(self, serializer):
        dictionary_uid, item_code = self.kwargs.values()
        actual_dictionary_version = Version.objects.filter(
            directory__uid=dictionary_uid
        ).order_by('-pub_date').first()
        if not actual_dictionary_version:
            raise ValidationError(
                'The directory does not exist!'
            )
        version_name = actual_dictionary_version.name
        directory_version = Item.objects.filter(
            versions__name=version_name,
        )
        if not directory_version:
            raise ValidationError(
                'The directory is missing versions and elements!'
            )
        directory_item = directory_version.filter(
            code=item_code
        )
        if directory_item.exists():
            serializer.validated_data['result'] = True
        else:
            serializer.validated_data['result'] = False


class VersionItemPostView(CreateAPIView):
    '''
    Validate the element of the directory of the current version.
    '''
    queryset = Item.objects.all()
    serializer_class = ItemValidateSerializer

    def perform_create(self, serializer):
        dictionary_uid, dictionary_version, item_code = self.kwargs.values()
        directory = Item.objects.filter(
            itemsversion__version__directory__uid=dictionary_uid,
        )
        if not directory:
            raise ValidationError(
                'The directory does not exist!'
            )
        directory_version = directory.filter(
            itemsversion__version__name=dictionary_version,
        )
        if not directory_version:
            raise ValidationError(
                'This version of the directory does not exist!'
            )
        directory_item = directory_version.filter(
            code=item_code
        )
        if directory_item.exists():
            serializer.validated_data['result'] = True
        else:
            serializer.validated_data['result'] = False
