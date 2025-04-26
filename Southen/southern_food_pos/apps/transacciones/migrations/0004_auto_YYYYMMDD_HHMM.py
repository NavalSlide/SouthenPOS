from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('transacciones', '0003_transaccion_numero_factura_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='numero_factura_usuario',
            field=models.PositiveIntegerField(editable=False, default=1000),
            preserve_default=False,
        ),
        migrations.RunPython(
            code=lambda apps, schema_editor: None,  # No-op forward
            reverse_code=lambda apps, schema_editor: None,  # No-op reverse
        ),
    ]