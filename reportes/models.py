from django.db import models

class ReporteVial(models.Model):
    TIPO_CHOICES = [
        ('👮 Retén / Agentes', '👮 Retén / Agentes de Tránsito'),
        ('🚨 Accidente', '🚨 Accidente de Tránsito'),
        ('🚗 Trancón', '🚗 Trancón / Congestión Alta'),
        ('🚧 Obras', '🚧 Obras en la Vía'),
        ('⚠️ Peligro', '⚠️ Peligro / Estado de la Vía'),
    ]

    tipo_incidente = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_incidente} - {self.fecha_creacion.strftime('%H:%M %d/%m/%Y')}"
