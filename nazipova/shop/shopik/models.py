from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Index

class Category(models.Model):
    name = models.CharField('Название', max_length=200, db_index=True)
    slug = models.SlugField('URL', max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Product(models.Model):
    category = models.ForeignKey(
        Category, 
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    name = models.CharField('Название', max_length=200, db_index=True)
    slug = models.SlugField('URL', max_length=200, unique=True)
    image = models.ImageField(
        'Изображение',
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Наличие')
    is_active = models.BooleanField('Активный', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        # Используем только slug, так как он уникальный
        return reverse('shop:product_detail', args=[self.slug])