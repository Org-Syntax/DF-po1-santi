from django.shortcuts import render, redirect
from .models import ReporteVial
from pymongo import MongoClient
from django.conf import settings
from firebase_admin import firestore
from .utils import subir_a_firebase_storage  # <--- Importamos nuestra función de subida

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
                # --- SUBIR ARCHIVOS A FIREBASE STORAGE ANTES DE GUARDAR EN SQL ---
                url_foto = subir_a_firebase_storage(foto)
                url_video = subir_a_firebase_storage(video)
                url_audio = subir_a_firebase_storage(audio)
                url_pdf = subir_a_firebase_storage(pdf)

                # Guardar usando la base de datos relacional seleccionada dinámicamente
                ReporteVial.objects.using(db_elegida).create(
                    tipo_incidente=tipo,
                    descripcion=desc,
                    latitud=float(lat) if lat else None,
                    longitud=float(lon) if lon else None,
                    foto=url_foto,
                    video=url_video,
                    audio=url_audio,
                    pdf=url_pdf
                )
        except Exception as e:
            error = f"Error al guardar en la BD '{db_elegida}': {e}"

        return redirect(f'/?db_target={db_elegida}')

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
                    'fecha_creacion': 'Reciente en Atlas'
                })
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