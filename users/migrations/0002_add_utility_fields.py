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
            name='custom_user_css',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='utility.customusercss', related_name="selected_user_css", verbose_name="Selected Color Profile"),
        ),
        migrations.AddField(
            model_name='CustomUser',
            name='affiliated_projects',
            field=models.ManyToManyField(related_name='affiliated_projects', to='utility.Project', verbose_name='Affiliated Project(s)'),
        ),
    ]
