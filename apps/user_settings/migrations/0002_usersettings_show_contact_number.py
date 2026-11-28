from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='show_contact_number',
            field=models.BooleanField(default=False),
        ),
    ]
