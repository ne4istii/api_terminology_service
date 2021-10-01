from django_filters import DateFilter, FilterSet

from directories.models import Directory


class DirectoryFilter(FilterSet):
    '''Filter for Dictionaries by pub_date of all versions.'''
    search = DateFilter(
        field_name='versions__pub_date',
        method='filter_pub_date',
    )

    def filter_pub_date(self, queryset, name, value):
        '''Construct the full lookup expression.'''
        if value:
            return queryset.filter(versions__pub_date__lte=value).distinct()
        return queryset

    class Meta:
        model = Directory
        fields = ('search',)
