from django.db import models

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,   # delete category → products keep NULL
        null=True,
        blank=True,
        related_name="products"
    )
    desc = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True,blank=True,default='/placeholder.png')
    createdTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.desc}  {self.price}"

