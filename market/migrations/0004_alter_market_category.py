from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_marketzzim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='category',
            field=models.CharField(choices=[('의약품', '#의약품'), ('티켓', '#티켓'), ('음식', '#음식'), ('생활용품', '#생활용품'), ('기념품', '#기념품'), ('기타', '#기타')], max_length=10),
        ),
    ]
