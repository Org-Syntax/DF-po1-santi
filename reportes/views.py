from django.shortcuts import render, redirect
from .models import ReporteVial
from pymongo import MongoClient
from django.conf import settings
from firebase_admin import firestore

def index(request):
    # 1. Capturar la base de datos seleccionada (por defecto 'default')
    db_elegida = request.GET.get('db_target', 'default')
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
                db = client.get_database("db_reportes_sena")
                db.reportes_viales.insert_one({
                    "tipo_incidente": tipo,
                    "descripcion": desc,
                    "latitud": float(lat) if lat else None,
                    "longitud": float(lon) if lon else None,
                })
            elif db_elegida == 'firebase':
                # Guardado en Firebase Firestore (Cloud NoSQL)
                db_firestore = firestore.client()
                db_firestore.collection('reportes_viales').add({
                    "tipo_incidente": tipo,
                    "descripcion": desc,
                    "latitud": float(lat) if lat else None,
                    "longitud": float(lon) if lon else None,
                    "fecha_creacion": firestore.SERVER_TIMESTAMP
                })
            else:
                # Guardar usando la base de datos relacional seleccionada dinámicamente
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
        except Exception as e:
            error = f"Error al guardar en la BD '{db_elegida}': {e}"

        return redirect(f'/?db_target={db_elegida}')

    # 3. Consultar los reportes usando la base de datos seleccionada
    try:
        if db_elegida == 'mongodb':
            # Consulta en MongoDB Atlas (NoSQL)
            client = MongoClient(settings.MONGO_URI)
            db = client.get_database("db_reportes_sena")
            reportes = list(db.reportes_viales.find().sort('_id', -1))
        elif db_elegida == 'firebase':
            # Consulta en Firebase Firestore
            db_firestore = firestore.client()
            docs = db_firestore.collection('reportes_viales').stream()
            reportes = []
            for doc in docs:
                data = doc.to_dict()
                reportes.append({
                    'tipo_incidente': data.get('tipo_incidente'),
                    'descripcion': data.get('descripcion'),
                    'latitud': data.get('latitud'),
                    'longitud': data.get('longitud'),
                    'fecha_creacion': data.get('fecha_creacion', 'Reciente en Cloud')
                })
        else:
            # Consulta relacional con Django ORM
            reportes = ReporteVial.objects.using(db_elegida).all().order_by('-fecha_creacion')
    except Exception as e:
        error = f"Error al conectar con la base de datos '{db_elegida}': {e}"

    context = {
        'reportes': reportes,
        'db_elegida': db_elegida,
        'error': error
    }
    return render(request, 'index.html', context)