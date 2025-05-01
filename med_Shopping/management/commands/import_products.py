import os
import csv
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from med_Shopping.models import Product

class Command(BaseCommand):
    help = 'Import products from CSV'

    def handle(self, *args, **options):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(BASE_DIR, '../../shopping_data/final.csv')

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    price = ''.join(c for c in row['price'] if c.isdigit() or c == '.')
                    price = Decimal(price)

                    Product.objects.get_or_create(
                        original_id=row['Unnamed: 0'],
                        defaults={
                            'category': row['label'],
                            'url': row['url'],
                            'brand': row['brand'],
                            'name': row['name'],
                            'price': price,
                            'skin_type': row['skin type'],
                            'concerns': row['concern'],
                            'image_url': row['img'],
                        }
                    )

                    self.stdout.write(self.style.SUCCESS(f"✔ Imported: {row['name']}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"✘ Failed to import row {row}: {e}"))
