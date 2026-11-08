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
        ('Apple', 'iPhone 16 Pro · Demo reference', 'smartphones', 'demo-iphone', 'iPhone 16 Pro catalogue reference: 6.3-inch Pro display, A18 Pro chip and Pro camera system. Reference photo and details are for product identification; shop price and stock must be confirmed.'),
        ('Samsung', 'Galaxy S25 Ultra · Demo reference', 'smartphones', 'demo-galaxy', 'Galaxy S25 Ultra catalogue reference: 6.9-inch Dynamic AMOLED 2X display, Snapdragon 8 Elite for Galaxy and 200MP wide camera. Reference photo and shop availability must be confirmed.'),
        ('OnePlus', 'OnePlus 13 · Demo reference', 'smartphones', 'demo-oneplus', 'OnePlus 13 catalogue reference: 6.82-inch 120Hz ProXDR display, Snapdragon 8 Elite platform and 6,000mAh dual-cell battery. Confirm regional configuration and shop stock.'),
        ('Redmi', 'Redmi Note 14 Pro+ 5G · Demo reference', 'smartphones', 'demo-redmi', 'Redmi Note 14 Pro+ 5G catalogue reference: 6.67-inch 120Hz AMOLED display, 200MP OIS camera and 120W HyperCharge. Confirm regional configuration, price and stock.'),
        ('realme', 'realme GT 7 Pro · Demo reference', 'smartphones', 'demo-realme', 'realme GT 7 Pro catalogue reference: flagship GT performance phone with AMOLED display, high-capacity battery and fast charging. Exact configuration, price and stock must be confirmed.'),
        ('Vivo', 'vivo X200 Pro · Demo reference', 'smartphones', 'demo-vivo', 'vivo X200 Pro catalogue reference: premium X-series camera phone with ZEISS imaging system and flagship performance. Regional configuration, price and shop stock must be confirmed.'),
        ('OPPO', 'OPPO Find X8 Pro · Demo reference', 'smartphones', 'demo-oppo', 'OPPO Find X8 Pro catalogue reference: premium Find-series phone with Hasselblad camera features and flagship performance. Confirm regional configuration, price and stock.'),
        ('Motorola', 'motorola Edge 50 Ultra · Demo reference', 'smartphones', 'demo-motorola', 'motorola Edge 50 Ultra catalogue reference: premium Edge-series phone with high-resolution camera, curved display and fast charging. Confirm regional configuration, price and stock.'),
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
                product.model_name = name.replace(' · Demo reference', '')
                product.save(update_fields=['name', 'description', 'model_name', 'updated_at'])
            elif was_created:
                product.model_name = name.replace(' · Demo reference', '')
                product.save(update_fields=['model_name', 'updated_at'])
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f'Demo catalogue ready. {created} product records created; existing records were left unchanged.'))
