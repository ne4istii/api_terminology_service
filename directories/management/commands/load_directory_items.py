import csv

from django.core.management.base import BaseCommand

from directories.models import Item


class Command(BaseCommand):
    help = 'Add the elements of the directory to the database.'

    def handle(self, *args, **options):
        with open('directories/data/directory_items.csv') as file:
            order = ['uid', 'code', 'value']
            reader = csv.DictReader(file, fieldnames=order, delimiter=';')
            for r in reader:
                Item.objects.get_or_create(
                    uid=r.get('uid'),
                    code=r.get('code'),
                    value=r.get('value')
                )
