from django.db import models

# Create your models here.


class Category(models.Model):
    men = models.BooleanField()
    women = models.BooleanField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return ("Men's " + self.name) if self.men else ("Women's " + self.name)

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return ("Men's " + self.name) if self.category.men else ("Women's " + self.name)

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    price = models.FloatField(default='0')
    discount = models.IntegerField(default='0')
    uploaded_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return self.name
