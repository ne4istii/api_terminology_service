from django.urls import path

from .views import (DirectoryListView, ItemListView, ItemPostView,
                    VersionItemListView, VersionItemPostView)

urlpatterns = [
    path(
        'directories/',
        DirectoryListView.as_view()
    ),
    path(
        '<str:dictionary_uid>/',
        ItemListView.as_view()
    ),
    path(
        '<str:dictionary_uid>/<str:code>/',
        ItemPostView.as_view()
    ),
    path(
        '<str:dictionary_uid>/version/<str:dictionary_version>/',
        VersionItemListView.as_view()
    ),
    path(
        '<str:dictionary_uid>/version/<str:dictionary_version>/<str:code>/',
        VersionItemPostView.as_view()
    ),
]
