from django.db import models

# Create your models here.


class Category(models.Model):
    men = models.BooleanField()
    women = models.BooleanField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta():
        verbose_name_plural = 'Categories'

    def __str__(self):
        return ("Men's " + self.name) if self.men else ("Women's " + self.name)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta():
        verbose_name = 'Sub-Category'
        verbose_name_plural = 'Sub-Categories'

    def __str__(self):
        return ("Men's " + self.name) if self.category.men else ("Women's " + self.name)


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField(default='0')
    discount = models.IntegerField(null=True, blank=True)
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    image_1 = models.ImageField(upload_to='items/')
    image_2 = models.ImageField(upload_to='items/', blank=True)
    image_3 = models.ImageField(upload_to='items/', blank=True)
    image_4 = models.ImageField(upload_to='items/', blank=True)
    image_5 = models.ImageField(upload_to='items/', blank=True)

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return self.name

    def discounted_price(self):
        return int(self.price * (100 - self.discount) * 0.01)
