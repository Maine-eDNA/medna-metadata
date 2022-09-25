from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('utility', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='CustomUser',
            name='affiliated_projects',
            field=models.ManyToManyField(blank=True, related_name='affiliated_projects', to='utility.Project', verbose_name='Affiliated Project(s)'),
        ),
    ]
