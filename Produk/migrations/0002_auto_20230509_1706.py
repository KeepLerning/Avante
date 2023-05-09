# Generated by Django 3.2.16 on 2023-05-09 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produk', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produk',
            name='kategori',
        ),
        migrations.RemoveField(
            model_name='produk',
            name='stok_produk',
        ),
        migrations.AddField(
            model_name='produk',
            name='gambar_produk',
            field=models.ImageField(default='default.png', upload_to='produk/'),
        ),
        migrations.AlterField(
            model_name='produk',
            name='harga_produk',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produk',
            name='nama_produk',
            field=models.CharField(max_length=255),
        ),
    ]
