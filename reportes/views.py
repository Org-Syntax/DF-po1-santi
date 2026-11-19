from django.shortcuts import render, redirect
from .models import ReporteVial
from pymongo import MongoClient
from django.conf import settings


def index(request):
    # 1. Capturar la base de datos seleccionada (por defecto 'mysql_db')
    db_elegida = request.GET.get('db_target', 'mysql_db')
    error = None
    reportes = []

    # 2. Si envían el formulario por POST, guardamos el reporte
    if request.method == 'POST':
        tipo = request.POST.get('tipo_incidente')
        desc = request.POST.get('descripcion')
        lat = request.POST.get('latitud')
        lon = request.POST.get('longitud')

        foto = request.FILES.get('foto')
        video = request.FILES.get('video')
        audio = request.FILES.get('audio')
        pdf = request.FILES.get('pdf')

        try:
            if db_elegida == 'mongodb':
                # Guardado en MongoDB Atlas (NoSQL)
                client = MongoClient(settings.MONGO_URI)
                db = client.get_database("despliegue_atlas")
                db.reportes_reportevial.insert_one({
                    "tipo_incidente": tipo,
                    "descripcion": desc,
                    "latitud": float(lat) if lat else None,
                    "longitud": float(lon) if lon else None,
                    "foto": foto.name if foto else None,
                    "video": video.name if video else None,
                    "audio": audio.name if audio else None,
                    "pdf": pdf.name if pdf else None,
                })
            else:
                # Guardado en bases relacionales (postgres_sena, mysql_db, sqlite_alternativa, default)
                # Guarda el archivo en MEDIA_ROOT/<upload_to>/ y registra la ruta en PostgreSQL/SQL
                ReporteVial.objects.using(db_elegida).create(
                    tipo_incidente=tipo,
                    descripcion=desc,
                    latitud=float(lat) if lat else None,
                    longitud=float(lon) if lon else None,
                    foto=foto,
                    video=video,
                    audio=audio,
                    pdf=pdf
                )

            return redirect(f'/?db_target={db_elegida}')
        except Exception as e:
            error = f"Error al guardar en la BD '{db_elegida}': {e}"

    # 3. Consultar los reportes usando la base de datos seleccionada
    try:
        if db_elegida == 'mongodb':
            # Consulta en MongoDB Atlas (NoSQL)
            client = MongoClient(settings.MONGO_URI)
            db = client.get_database("despliegue_atlas")
            docs = list(db.reportes_reportevial.find().sort('_id', -1))
            reportes = []
            for d in docs:
                reportes.append({
                    'tipo_incidente': d.get('tipo_incidente'),
                    'descripcion': d.get('descripcion'),
                    'latitud': d.get('latitud'),
                    'longitud': d.get('longitud'),
                    'foto': d.get('foto'),
                    'video': d.get('video'),
                    'audio': d.get('audio'),
                    'pdf': d.get('pdf'),
                    'fecha_creacion': 'Reciente en Atlas'
                })
        else:
            # Consulta relacional con Django ORM (incluyendo postgres_sena)
            reportes = ReporteVial.objects.using(db_elegida).all().order_by('-fecha_creacion')
    except Exception as e:
        error = f"Error al conectar con la base de datos '{db_elegida}': {e}"

    context = {
        'reportes': reportes,
        'db_elegida': db_elegida,
        'error': error
    }
    return render(request, 'index.html', context)