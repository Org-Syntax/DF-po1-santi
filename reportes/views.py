from django.shortcuts import render, redirect
from .models import ReporteVial

def index(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo_incidente')
        desc = request.POST.get('descripcion')
        lat = request.POST.get('latitud')
        lon = request.POST.get('longitud')
        
        foto = request.FILES.get('foto')
        video = request.FILES.get('video')
        audio = request.FILES.get('audio')
        pdf = request.FILES.get('pdf') # 📄 Capturar el archivo PDF enviado desde el formulario

        ReporteVial.objects.create(
            tipo_incidente=tipo,
            descripcion=desc,
            latitud=float(lat) if lat else None,
            longitud=float(lon) if lon else None,
            foto=foto,
            video=video,
            audio=audio,
            pdf=pdf # 📄 Guardar el PDF en la base de datos
        )
        return redirect('index')

    reportes = ReporteVial.objects.all().order_by('-fecha_creacion')
    return render(request, 'index.html', {'reportes': reportes})