from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=255)
    website_url = models.URLField()  # For storing brand's Amazon page URL

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    asin = models.CharField(max_length=50, unique=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name