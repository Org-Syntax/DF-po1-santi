import os
import django
import pymongo

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

def migrar_a_mongodb():
    print("Conectando a MongoDB Atlas...")
    client = pymongo.MongoClient(settings.MONGO_URI)
    db = client['despliegue_atlas']
    
    # Lista de colecciones que usará tu app de reportes en MongoDB
    colecciones = [
        'reportes_categoriaincidente',
        'reportes_reportevial',
        'reportes_perfilconductor'
    ]

    for nombre_col in colecciones:
        col = db[nombre_col]
        # Insertamos un documento temporal para forzar la creación de la colección en Atlas y luego lo borramos
        res = col.insert_one({'estado': 'inicializado_sena'})
        col.delete_one({'_id': res.inserted_id})
        print(f"✓ Colección '{nombre_col}' creada y lista en MongoDB Atlas.")

    print("\n¡Todas las colecciones de MongoDB Atlas fueron configuradas con éxito!")

if __name__ == '__main__':
    migrar_a_mongodb()