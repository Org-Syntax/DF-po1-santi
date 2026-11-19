from django.db import models
from django.contrib.auth.models import User


# =====================================================================
# TABLA 1: Perfil del Conductor
# =====================================================================
class PerfilConductor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    licencia = models.CharField(max_length=50, verbose_name="Número de Licencia")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")

    class Meta:
        db_table = 'perfil_conductor'
        verbose_name = "Perfil de Conductor"
        verbose_name_plural = "Perfiles de Conductores"

    def __str__(self):
        return f"Perfil de {self.usuario.username} (Licencia: {self.licencia})"


# =====================================================================
# TABLA 2: Categorías de Incidentes
# =====================================================================
class CategoriaIncidente(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        db_table = 'categoria_incidente'
        verbose_name = "Categoría de Incidente"
        verbose_name_plural = "Categorías de Incidentes"

    def __str__(self):
        return self.nombre


# =====================================================================
# TABLA 3: Reportes Viales (Tabla Principal)
# =====================================================================
class ReporteVial(models.Model):
    TIPO_CHOICES = [
        ('👮 Retén / Agentes', '👮 Retén / Agentes de Tránsito'),
        ('🚨 Accidente', '🚨 Accidente de Tránsito'),
        ('🚗 Trancón', '🚗 Trancón / Congestión Alta'),
        ('🚧 Obras', '🚧 Obras en la Vía'),
        ('⚠️ Peligro', '⚠️ Peligro / Estado de la Vía'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reportes_viales')
    tipo_incidente = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    categorias = models.ManyToManyField(CategoriaIncidente, related_name='reportes_viales', blank=True)

    class Meta:
        db_table = 'reportes_reportevial'
        verbose_name = "Reporte Vial"
        verbose_name_plural = "Reportes Viales"

    def __str__(self):
        return f"{self.tipo_incidente} - {self.fecha_creacion.strftime('%H:%M %d/%m/%Y')}"