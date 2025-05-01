# management/commands/import_products.py
import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from .models import Product

class Command(BaseCommand):
    help = 'Import products from CSV'

    def handle(self, *args, **options):
        csv_path = 'shopping_data\final.csv'
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Clean price data
                price = ''.join(c for c in row['price'] if c.isdigit() or c == '.')
                
                Product.objects.create(
                    original_id=row['Unnamed: 0'],
                    category=row['label'],
                    url=row['url'],
                    brand=row['brand'],
                    name=row['name'],
                    price=Decimal(price),
                    skin_type=row['skin type'],
                    concerns=row['concern'],
                    image_url=row['img']
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported products'))