import csv

from django.core.management.base import BaseCommand

from directories.models import Directory


class Command(BaseCommand):
    help = 'Add directories to the database.'

    def handle(self, *args, **options):
        with open('directories/data/directories.csv') as file:
            order = ['uid', 'name']
            reader = csv.DictReader(file, fieldnames=order, delimiter=';')
            for r in reader:
                Directory.objects.get_or_create(
                    uid=r.get('uid'),
                    name=r.get('name'),
                    title=r.get('name'),
                    description=r.get('name')
                )
