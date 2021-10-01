from django.urls import path

from .views import DirectoryListView, ItemListView, ItemValidateView

urlpatterns = [
    path(
        'directories/',
        DirectoryListView.as_view()
    ),
    path(
        '<str:directory_uid>/',
        ItemListView.as_view()
    ),
    path(
        '<str:directory_uid>/<str:code>/',
        ItemValidateView.as_view()
    ),
    path(
        '<str:directory_uid>/version/<str:directory_version>/',
        ItemListView.as_view()
    ),
    path(
        '<str:directory_uid>/version/<str:directory_version>/<str:code>/',
        ItemValidateView.as_view()
    ),
]
