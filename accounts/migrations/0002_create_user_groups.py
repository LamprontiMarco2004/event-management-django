from django.db import migrations


def create_groups(apps, schema_editor):
    """Crea i due ruoli del progetto come Gruppi di Django."""
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name="Organizer")
    Group.objects.get_or_create(name="Attendee")


def remove_groups(apps, schema_editor):
    """Operazione inversa: rimuove i gruppi se la migration viene annullata."""
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Organizer", "Attendee"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]
