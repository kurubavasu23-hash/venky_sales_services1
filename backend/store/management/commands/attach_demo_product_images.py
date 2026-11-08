from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from store.models import Product, ProductImage


class Command(BaseCommand):
    help = 'Attach locally stored, attributed reference photos to demo product records.'

    image_map = {
        'demo-iphone': ('apple-iphone.jpg', 'Apple iPhone reference photo; model and inventory not verified.'),
        'demo-galaxy': ('samsung-galaxy.jpg', 'Samsung Galaxy reference photo; model and inventory not verified.'),
        'demo-oneplus': ('oneplus.jpg', 'OnePlus reference photo; model and inventory not verified.'),
        'demo-redmi': ('redmi.jpg', 'Redmi reference photo; model and inventory not verified.'),
        'demo-realme': ('realme.jpg', 'realme reference photo; model and inventory not verified.'),
        'demo-vivo': ('vivo.jpg', 'Vivo reference photo; model and inventory not verified.'),
        'demo-oppo': ('oppo.jpg', 'OPPO reference photo; model and inventory not verified.'),
        'demo-motorola': ('motorola.jpg', 'Motorola reference photo; model and inventory not verified.'),
        'demo-wireless-earbuds': ('wireless-earbuds.jpg', 'Wireless earbuds reference photo; demo listing only.'),
        'demo-wired-earphones': ('wired-earphones.jpg', 'Wired earphones reference photo; demo listing only.'),
        'demo-usb-cable': ('usb-cable.jpg', 'USB cable reference photo; demo listing only.'),
        'demo-mobile-cover': ('mobile-cover.jpg', 'Mobile phone cover reference photo; demo listing only.'),
        'demo-power-bank': ('power-bank.jpg', 'Power bank reference photo; demo listing only.'),
    }

    def handle(self, *args, **options):
        attached = 0
        missing = []
        for slug, (filename, alt_text) in self.image_map.items():
            product = Product.objects.filter(slug=slug).first()
            if not product:
                missing.append(f'{slug} (run seed_demo_products first)')
                continue
            if ProductImage.objects.filter(product=product).exists():
                continue  # Preserve admin-uploaded images and their gallery ordering.
            path = Path(settings.MEDIA_ROOT) / 'products' / 'demo' / filename
            if not path.exists():
                missing.append(str(path))
                continue
            with path.open('rb') as image_file:
                image = ProductImage(product=product, alt_text=alt_text, sort_order=0)
                image.image.save(filename, File(image_file), save=True)
            attached += 1

        if missing:
            self.stdout.write(self.style.WARNING('Skipped unavailable photos: ' + ', '.join(missing)))
        self.stdout.write(self.style.SUCCESS(f'Attached {attached} demo reference photos; existing product galleries were preserved.'))
