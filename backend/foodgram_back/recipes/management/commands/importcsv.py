'''TO START!: python manage.py importcsv'''
from django.core.management.base import BaseCommand

from csv import DictReader

from recipes.models import Ingredient


class Command(BaseCommand):
    """Importing csv file in local db."""
    help = (
        'Import list of files from data/:'
        + 'ingredients.csv,'
        # + ' title.csv and user.csv'
    )

    def handle(self, *args, **option):
        print("Loading DB data")
        # print("pwd=" + os.getcwd())
        for row in DictReader(open('../../data/ingredients.csv')):
            ingredient = Ingredient.objects.get_or_create(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            print(ingredient)
        print('Ingredients done..')
        print('DB filled')
