from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0003_rename_registration_data_client_registration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='', upload_to='product_photos/'),
            preserve_default=False,
        ),
    ]