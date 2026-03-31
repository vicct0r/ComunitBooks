from django.db import migrations


def update_old_values(apps, schema_editor):
    Book = apps.get_model('books', 'Book')

    status_map = {'av': 'available', 'un': 'unavailable', 'rs': 'reserved'}
    condition_map = {'nw': 'new', 'gd': 'good', 'fr': 'fair', 'dm': 'damaged'}

    for old, new in status_map.items():
        Book.objects.filter(status=old).update(status=new)

    for old, new in condition_map.items():
        Book.objects.filter(condition=old).update(condition=new)


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_condition_alter_book_status'),
    ]

    operations = [
        migrations.RunPython(update_old_values, migrations.RunPython.noop),
    ]
