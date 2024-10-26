from django.db import models


class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', null=True, blank=True, default="placeholder.jpg")
    views = models.ManyToManyField('IpModel', related_name='views', blank=True, default=0)

    def get_unique_views_count(self):
        return self.views.count()

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    text = models.TextField(default=None)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255)
    order_count = models.IntegerField(default=1)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_ordered = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, default=None)


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='', null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class IpModel(models.Model):
    ip_address = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        return self.ip_address


class Table(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.number)


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class FoodReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField()

    def save(self, *args, **kwargs):
        if self.quantity < 1:
            raise ValueError("Количество должно быть больше нуля.")

        # Проверьте доступное количество
        total_reserved = FoodReservation.objects.filter(
            product=self.product,
            date=self.date
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        if total_reserved + self.quantity > self.product.quantity_available:
            raise ValueError("Недостаточно товара на складе для этой даты.")

        super().save(*args, **kwargs)