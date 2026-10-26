from django.db import models
from django.contrib.auth.models import User

# ==========================================
# 1. RELACIÓN 1 A 1 (OneToOneField)
# Un Usuario tiene exactamente UN Perfil / Licencia.
# ==========================================
class PerfilConductor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    licencia = models.CharField(max_length=50, verbose_name="Número de Licencia")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")

    def __str__(self):
        return f"Perfil de {self.usuario.username} (Licencia: {self.licencia})"


# ==========================================
# 2. TABLA PARA RELACIÓN MUCHOS A MUCHOS
# Categorías o etiquetas adicionales para los incidentes.
# ==========================================
class CategoriaIncidente(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre


# ==========================================
# 3. TABLA PRINCIPAL CON TUS CAMPOS Y LAS RELACIONES
# ==========================================
class ReporteVial(models.Model):
    TIPO_CHOICES = [
        ('👮 Retén / Agentes', '👮 Retén / Agentes de Tránsito'),
        ('🚨 Accidente', '🚨 Accidente de Tránsito'),
        ('🚗 Trancón', '🚗 Trancón / Congestión Alta'),
        ('🚧 Obras', '🚧 Obras en la Vía'),
        ('⚠️ Peligro', '⚠️ Peligro / Estado de la Vía'),
    ]

    # RELACIÓN 1 A MUCHOS (ForeignKey)
    # Un usuario puede crear muchos reportes viales (null=True para no romper datos previos)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reportes_viales')

    # Campos existentes
    tipo_incidente = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    
    # Archivos multimedia existentes
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # RELACIÓN MUCHOS A MUCHOS (ManyToManyField)
    # Un reporte puede pertenecer a múltiples categorías
    categorias = models.ManyToManyField(CategoriaIncidente, related_name='reportes_viales', blank=True)

    def __str__(self):
        return f"{self.tipo_incidente} - {self.fecha_creacion.strftime('%H:%M %d/%m/%Y')}"