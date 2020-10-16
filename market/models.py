from django.contrib.auth.models import User
from django.db import models


class Dyqan(models.Model):
    emri = models.CharField(verbose_name='Emri', max_length=25)
    adresa = models.CharField(verbose_name='Adresa', max_length=25)
    tel = models.CharField(verbose_name='Tel', max_length=25)
    logo = models.ImageField(verbose_name='Logo', upload_to='static/media/')

    class Meta:
        verbose_name = 'Dyqan'
        verbose_name_plural = 'Dyqanet'

    def __str__(self):
        return f'{self.emri}'


class Kategori(models.Model):
    emri = models.CharField(verbose_name='Emri', max_length=25)
    logo = models.ImageField(verbose_name='Logo', upload_to='static/media/')

    class Meta:
        verbose_name = 'Keategori'
        verbose_name_plural = 'Keategoritë'

    def __str__(self):
        return f'{self.emri}'


NJESITE = [
    ('kg', 'kilogram'),
    ('g', 'gram'),
    ('cope', 'cope'),
    ('l', 'liter'),
]


class Product(models.Model):
    name = models.CharField(verbose_name='Emri', max_length=25)
    image = models.ImageField(verbose_name='Logo', upload_to='static/media/')
    cmimi_blerje = models.DecimalField(verbose_name='Cmimi i blerjes', max_digits=50, decimal_places=2)
    price = models.DecimalField(verbose_name='Cmimi ', max_digits=50, decimal_places=2)
    sasia = models.IntegerField(verbose_name='Sasia')
    njesia_matese = models.CharField(choices=NJESITE, default=NJESITE[0][0], max_length=10)
    kategoria = models.ForeignKey(to=Kategori, on_delete=models.CASCADE, related_name='produktet')
    dyqani = models.ForeignKey(to=Dyqan, on_delete=models.CASCADE, related_name='produktet')

    class Meta:
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkte'

    def __str__(self):
        return f'{self.name}'


class Receipt(models.Model):
    klient = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='receipt')
    totali = models.DecimalField(verbose_name='Cmimi total', max_digits=50, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturat'

    def __str__(self):
        return f'F-{self.id}-{self.klient.get_full_name()}'


class ReceiptProducts(models.Model):
    produkti = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='receipt_products')
    receipt = models.ForeignKey(to=Receipt, on_delete=models.CASCADE, related_name='receipt_products')
    sasia = models.IntegerField(verbose_name='Sasia')
    cmimi_total = models.DecimalField(verbose_name='Cmimi total', max_digits=50, decimal_places=2)

    def __str__(self):
        return f'PF-{self.id}-{self.produkti.id}-{self.produkti.name}'
