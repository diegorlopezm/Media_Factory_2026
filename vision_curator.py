import os
import shutil
import json
import re
from PIL import Image
from google import genai
from config import GEMINI_API_KEY, MODELO

# Configuración de rutas
INPUT_FOLDER = "/home/diego/Imágenes/Flux.2-Dev/NVNCA Lora Training"
APPROVED_FOLDER = "/home/diego/Imágenes/Flux.2-Dev/NVNCA Lora Training/Dataset_Approved"
REJECTED_FOLDER = "/home/diego/Imágenes/Flux.2-Dev/NVNCA Lora Training/Dataset_Rejected"

client = genai.Client(api_key=GEMINI_API_KEY)

PROMPT_CURADOR = """
Eres un experto en MLOps y entrenamiento de modelos Generativos (Flux). 
Analiza esta imagen para decidir si es apta para un dataset de alta calidad (estilo FF15/Resident Evil).

CRITERIOS DE RECHAZO:
- Texto visible (subtítulos, marcas de agua, logos de UI de juego).
- Artefactos de compresión (píxeles de YouTube, desenfoque de movimiento excesivo).
- Estilo no realista (dibujo plano, anime puro, fan-art de baja calidad).

RESPONDE ÚNICAMENTE EN FORMATO JSON:
{
  "decision": "APROBADA" o "RECHAZADA",
  "score_calidad": 1-10,
  "razon": "Explicación breve de por qué se acepta o rechaza",
  "tags": ["cara", "escenario", "textura", "oscuro", "etc"]
}
"""

def process_images():
    # Crear carpetas si no existen
    for folder in [APPROVED_FOLDER, REJECTED_FOLDER]:
        os.makedirs(folder, exist_ok=True)

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
    
    print(f"🔍 Encontradas {len(files)} imágenes. Iniciando análisis técnico...")

    for filename in files:
        img_path = os.path.join(INPUT_FOLDER, filename)
        
        try:
            # Cargar imagen
            raw_image = Image.open(img_path)
            
            # Llamada a Gemini Vision
            response = client.models.generate_content(
                model=MODELO,
                contents=[PROMPT_CURADOR, raw_image]
            )
            
            # Limpiar respuesta para obtener solo el JSON
            json_str = re.search(r'\{.*\}', response.text, re.DOTALL).group(0)
            data = json.loads(json_str)

            if data['decision'] == "APROBADA" and data['score_calidad'] >= 7:
                print(f"✅ {filename} APROBADA ({data['score_calidad']}/10) - {data['tags']}")
                shutil.move(img_path, os.path.join(APPROVED_FOLDER, filename))
            else:
                print(f"❌ {filename} RECHAZADA - Razón: {data['razon']}")
                shutil.move(img_path, os.path.join(REJECTED_FOLDER, filename))

        except Exception as e:
            print(f"⚠️ Error procesando {filename}: {e}")

if __name__ == "__main__":
    process_images()