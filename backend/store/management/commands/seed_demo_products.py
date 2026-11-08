from django.core.management.base import BaseCommand
from django.utils.text import slugify

from store.models import Brand, Product, ProductCategory


class Command(BaseCommand):
    help = 'Create clearly labeled sample products for preview; does not set prices or claim stock.'

    categories = [
        ('Smartphones', 'smartphones'),
        ('Mobile Accessories', 'mobile-accessories'),
        ('Earphones & Headphones', 'earphones-headphones'),
        ('Chargers & Cables', 'chargers-cables'),
    ]

    products = [
        ('Apple', 'iPhone Pro Series · Demo reference', 'smartphones', 'demo-iphone', 'Catalogue reference for the latest iPhone Pro range. Exact model, specifications, pricing and shop availability must be verified.'),
        ('Samsung', 'Galaxy S Series · Demo reference', 'smartphones', 'demo-galaxy', 'Catalogue reference for the latest Galaxy S range. Exact model, specifications, pricing and shop availability must be verified.'),
        ('OnePlus', 'OnePlus Flagship Series · Demo reference', 'smartphones', 'demo-oneplus', 'Catalogue reference for the latest OnePlus flagship range. Exact model, specifications, pricing and shop availability must be verified.'),
        ('Redmi', 'Redmi Note Series · Demo reference', 'smartphones', 'demo-redmi', 'Catalogue reference for the latest Redmi Note range. Exact model, specifications, pricing and shop availability must be verified.'),
        ('realme', 'realme GT Series · Demo reference', 'smartphones', 'demo-realme', 'Catalogue reference for the latest realme GT range. Exact model, specifications, pricing and shop availability must be verified.'),
        ('Vivo', 'vivo V Series · Demo reference', 'smartphones', 'demo-vivo', 'Catalogue reference for the latest vivo V range. Exact model, specifications, pricing and shop availability must be verified.'),
        ('OPPO', 'OPPO Reno Series · Demo reference', 'smartphones', 'demo-oppo', 'Catalogue reference for the latest OPPO Reno range. Exact model, specifications, pricing and shop availability must be verified.'),
        ('Motorola', 'motorola edge Series · Demo reference', 'smartphones', 'demo-motorola', 'Catalogue reference for the latest motorola edge range. Exact model, specifications, pricing and shop availability must be verified.'),
        ('Accessories', 'True Wireless Earbuds · Demo reference', 'earphones-headphones', 'demo-wireless-earbuds', 'Premium audio catalogue reference. Brand, model, features, pricing and shop availability must be verified.'),
        ('Accessories', 'Premium Wired Earphones · Demo reference', 'earphones-headphones', 'demo-wired-earphones', 'Premium audio catalogue reference. Brand, model, features, pricing and shop availability must be verified.'),
        ('Accessories', 'Fast Charger · Demo reference', 'chargers-cables', 'demo-fast-charger', 'Modern charging catalogue reference. Connector, wattage, compatibility, pricing and shop availability must be verified.'),
        ('Accessories', 'USB Cable · Demo reference', 'chargers-cables', 'demo-usb-cable', 'Modern charging catalogue reference. Connector, length, compatibility, pricing and shop availability must be verified.'),
        ('Accessories', 'Premium Protective Cover · Demo reference', 'mobile-accessories', 'demo-mobile-cover', 'Premium protection catalogue reference. Compatible model, material, pricing and shop availability must be verified.'),
        ('Accessories', 'Screen Protector · Demo reference', 'mobile-accessories', 'demo-screen-protector', 'Premium protection catalogue reference. Compatible model, type, pricing and shop availability must be verified.'),
        ('Accessories', 'Power Bank · Demo reference', 'mobile-accessories', 'demo-power-bank', 'Modern power catalogue reference. Capacity, compatibility, pricing and shop availability must be verified.'),
        ('Accessories', 'Wireless Headphones · Demo reference', 'earphones-headphones', 'demo-headphones', 'Premium audio catalogue reference. Brand, model, features, pricing and shop availability must be verified.'),
    ]

    def handle(self, *args, **options):
        category_by_slug = {}
        for name, slug in self.categories:
            category_by_slug[slug], _ = ProductCategory.objects.get_or_create(slug=slug, defaults={'name': name})

        brand_by_name = {}
        for brand_name, *_ in self.products:
            brand_by_name[brand_name], _ = Brand.objects.get_or_create(name=brand_name)

        created = 0
        for brand_name, name, category_slug, product_slug, description in self.products:
            product, was_created = Product.objects.get_or_create(
                slug=product_slug,
                defaults={
                    'name': name,
                    'brand': brand_by_name[brand_name],
                    'category': category_by_slug[category_slug],
                    'description': description,
                    'price': None,
                    'availability_status': 'unknown',
                    'is_demo': True,
                    'is_featured': category_slug == 'smartphones',
                },
            )
            if not was_created and product.is_demo and (product.name != name or product.description != description):
                product.name = name
                product.description = description
                product.save(update_fields=['name', 'description', 'updated_at'])
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f'Demo catalogue ready. {created} product records created; existing records were left unchanged.'))
