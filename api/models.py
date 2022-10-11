from unittest.util import _MAX_LENGTH
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from computer_shop.util import unique_slug_generator
# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class Product(models.Model):
  categories = models.ManyToManyField(Category, related_name="product_list", blank=True)
  name = models.CharField(max_length=200)
  price = models.FloatField()
  description_from_crawler = models.CharField(max_length=1500)
  # category
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  # new
  slug = models.SlugField(unique=True, max_length=300, blank=True, null=True)

  def __str__(self):
    return self.name

@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
  if not instance.slug:
      instance.slug = unique_slug_generator(instance)

class ImageURL(models.Model):
  url = models.CharField(max_length=300)
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image_urls", blank=True, null=True)

  def __str__(self):
    return self.url
  
 