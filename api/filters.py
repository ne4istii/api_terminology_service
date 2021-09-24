from django_filters import DateFilter, FilterSet

from directories.models import Directory


class DirectoryFilter(FilterSet):
    search = DateFilter(
        field_name='versions__pub_date',
        lookup_expr='gte'
    )

    class Meta:
        model = Directory
        fields = ('search',)
