from firebase_admin import storage

def subir_a_firebase_storage(archivo):
    if not archivo:
        return None
    try:
        # Ruta en la que se guardará dentro de tu Storage de Firebase
        ruta_bucket = f"reportes_multimedia/{archivo.name}"
        
        bucket = storage.bucket()
        blob = bucket.blob(ruta_bucket)
        
        # Subir el archivo
        blob.upload_from_file(archivo, content_type=archivo.content_type)
        
        # Hacerlo público para poder visualizarlo en la web
        blob.make_public()
        
        # Retornar la URL pública de descarga
        return blob.public_url
    except Exception as e:
        print(f"Error al subir archivo a Firebase Storage: {e}")
        return None