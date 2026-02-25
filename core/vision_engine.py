import re
import json
from PIL import Image
from google import genai
from config import GEMINI_API_KEY, MODELO

class VisionEngine:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.prompt = """
Eres un experto en MLOps y entrenamiento de modelos Generativos (Flux). 
Analiza esta imagen para decidir si es apta para un dataset de alta calidad (estilo FF15/Resident Evil).

CRITERIOS DE RECHAZO:
- Texto visible (subtítulos, marcas de agua, logos de UI de juego).
- Artefactos de compresión (píxeles de YouTube, desenfoque de movimiento excesivo).
- Estilo no realista (dibujo plano, anime puro, fan-art de baja calidad).

DETECCIÓN DE ÁNGULOS REQUERIDA:
Identifica si la imagen es: "from behind", "side view", "close up", "eye level", "low angle", "high angle".
OBLIGATORIO:La descripción de datos/tags(captioning) debe realizarse siempre en Inglés para maximizar la compatibilidad con los text-encoders (CLIP/T5)
RESPONDE ÚNICAMENTE EN FORMATO JSON:
{
  "decision": "APROBADA" o "RECHAZADA",
  "score_calidad": 1-10,
  "razon": "Explicación breve de por qué se acepta o rechaza",
  "tags": ["character", "landscape", "interaction", "from behind", "side view", "close up", "etc"]
}
"""

    def analyze_image(self, img_path):
        try:
            raw_image = Image.open(img_path)
            response = self.client.models.generate_content(
                model=MODELO,
                contents=[self.prompt, raw_image]
            )
            
            # Limpiar respuesta para obtener solo el JSON
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if not match:
                raise ValueError("No se encontró JSON en la respuesta de Gemini")
            
            json_str = match.group(0)
            return json.loads(json_str)
            
        except Exception as e:
            return {"error": str(e)}
