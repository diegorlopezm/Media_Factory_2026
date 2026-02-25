import os
from config import (
    INPUT_FOLDER, APPROVED_FOLDER, REJECTED_FOLDER, 
    LOG_FILE, MIN_QUALITY_SCORE, TARGET_PROPORTIONS
)
from core.vision_engine import VisionEngine
from core.stats_manager import StatsManager
from utils.file_handler import FileHandler

def main():
    # Inicializar componentes
    vision = VisionEngine()
    stats = StatsManager(TARGET_PROPORTIONS)
    fh = FileHandler()
    
    # Asegurar directorios
    fh.ensure_dirs([APPROVED_FOLDER, REJECTED_FOLDER])
    
    # Obtener imágenes
    files = fh.get_image_files(INPUT_FOLDER)
    print(f"🔍 Encontradas {len(files)} imágenes. Iniciando análisis v2.0...")
    
    for filename in files:
        img_path = os.path.join(INPUT_FOLDER, filename)
        print(f"📦 Procesando: {filename}...")
        
        data = vision.analyze_image(img_path)
        
        if "error" in data:
            print(f"⚠️ Error: {data['error']}")
            continue
            
        # Registrar en el log de auditoría
        fh.log_curation(LOG_FILE, filename, data)
        
        # Lógica de decisión
        if data.get('decision') == "APROBADA" and data.get('score_calidad', 0) >= MIN_QUALITY_SCORE:
            print(f"✅ APROBADA ({data['score_calidad']}/10) - Tags: {data['tags']}")
            
            # Mover imagen
            fh.move_file(img_path, os.path.join(APPROVED_FOLDER, filename))
            
            # Crear caption .txt
            fh.create_caption(os.path.join(APPROVED_FOLDER, filename), data.get('tags', []))
            
            # Actualizar estadísticas
            stats.update_stats(data.get('tags', []))
        else:
            print(f"❌ RECHAZADA - Razón: {data.get('razon', 'Calidad insuficiente')}")
            fh.move_file(img_path, os.path.join(REJECTED_FOLDER, filename))

    # Mostrar resumen final y alertas de cuota
    print(stats.get_summary())

if __name__ == "__main__":
    main()
