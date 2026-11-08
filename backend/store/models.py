import secrets
from django.core.validators import MinValueValidator
from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    def __str__(self): return self.name

class Brand(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    AVAILABILITY_CHOICES = [('unknown', 'Contact to check availability'), ('available', 'Available'), ('unavailable', 'Unavailable')]
    name = models.CharField(max_length=160)
    model_name = models.CharField(max_length=120, blank=True, help_text='Verified product model, if known.')
    slug = models.SlugField(max_length=180, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
    description = models.TextField(blank=True)
    ram = models.CharField(max_length=40, blank=True, help_text='Verified RAM specification only.')
    storage = models.CharField(max_length=40, blank=True, help_text='Verified storage specification only.')
    colour = models.CharField(max_length=120, blank=True, help_text='Verified colour or colour options only.')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True, help_text='Verified original price only; leave blank unless confirmed.')
    availability_status = models.CharField(max_length=16, choices=AVAILABILITY_CHOICES, default='unknown')
    is_demo = models.BooleanField(default=False, help_text='Demo listing only; not verified shop inventory.')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering=['name']; indexes=[models.Index(fields=['availability_status','category'])]
    def __str__(self): return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/')
    alt_text = models.CharField(max_length=180, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering=['sort_order']

class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    def __str__(self): return self.title

class RepairBooking(models.Model):
    STATUS_CHOICES=[('pending','Pending'),('confirmed','Confirmed'),('in_progress','In progress'),('completed','Completed'),('cancelled','Cancelled')]
    reference = models.CharField(max_length=14, unique=True, editable=False, db_index=True)
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=100, blank=True)
    service = models.CharField(max_length=120)
    problem_description = models.TextField(blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.reference:
            self.reference='VM'+secrets.token_hex(5).upper()
        super().save(*args,**kwargs)
    class Meta: ordering=['-created_at']; indexes=[models.Index(fields=['status','created_at'])]
    def __str__(self): return f'{self.reference} — {self.customer_name}'

class CustomerEnquiry(models.Model):
    name=models.CharField(max_length=120); phone=models.CharField(max_length=20); email=models.EmailField(blank=True)
    subject=models.CharField(max_length=160); message=models.TextField(); resolved=models.BooleanField(default=False); is_spam=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.subject} — {self.name}'

class BusinessSettings(models.Model):
    name=models.CharField(max_length=120,default='Venky Mobiles Sales & Services'); phone=models.CharField(max_length=20,default='+91 8555077760')
    whatsapp_number=models.CharField(max_length=20,default='918555077760'); address=models.CharField(max_length=240,default='Near Clock Tower, Uravakonda, Andhra Pradesh, India')
    opening_hours=models.CharField(max_length=120,default='Every day, 9:00 AM to 9:00 PM'); description=models.TextField(blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.name
