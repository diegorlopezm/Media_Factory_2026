# factory.py
import os
import datetime
from google import genai
from config import GEMINI_API_KEY, MODELO, OBSIDIAN_INBOX
from scraper import get_transcript

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Actúa como un experto en guiones virales para TikTok/Shorts de Historia, Biologia, Fisica, curiosidades y Misterio.
Tu misión es convertir la transcripción real de YouTube proporcionada en un guion de 70 segundos.

⚠️ REGLA DE FIDELIDAD ABSOLUTA (CRÍTICO):
- Céntrate ÚNICAMENTE en los hechos narrados en la transcripción.
- PROHIBIDO inventar temas de Nazca, Aliens o el Kremlin si no aparecen en el texto.
- Tu creatividad debe usarse para el GANCHO (hook) y la NARRATIVA, no para inventar datos.

IDIOMA: Inglés.

REGLAS DE ACTUACIÓN (ElevenLabs v3 - CRÍTICO):
- Sé AGRESIVO con el uso de etiquetas emocionales para evitar la monotonía.
- [excited]: Úsalo en el Hook inicial y en datos sorprendentes.
- [thoughtful]: Úsalo para explicaciones lógicas o transiciones.
- [chuckles]: Úsalo cuando desmitifiques algo o menciones una ironía.
- [whispers]: Úsalo para secretos, datos misteriosos o momentos de "acércate a la pantalla".
- [sighs]: Úsalo para hablar de mitos falsos o de lo que se ha perdido en la historia.
- [short pause]: Úsalo después de una pregunta retórica o antes de una gran revelación.

ESTRUCTURA DE SALIDA (Sigue este orden exacto):

1. [METADATA]
- Project Title: (Genera un título corto y atractivo, ej: "Mitología Sumeria: Los Anunnaki")
- Project Description: (Descripcion breve del proyecto)
- Suggested Hook Type: (Elige SOLO UNO de estos 7 tipos exactos):
    1. Question (Empieza con una pregunta intrigante)
    2. Negative/Fear (Advierte de un error o peligro)
    3. Curiosity/Secret (Promete revelar algo oculto)
    4. Instant Result (Muestra un beneficio/resultado rápido)
    5. Visual/Action (Empieza con un evento caótico o impacto visual)
    6. Contrarian (Va en contra de la opinión popular)
    7. List/Top 3 (Estructura el valor en puntos numerados)
- Target Tags: (Genera una lista de Python con 5 tags, ej: ['AI', 'Tech', 'Money'])
[/METADATA]

2. [AUDIO_LIMPIO]
(Guion completo SOLO con etiquetas emocionales, listo para copiar a ElevenLabs).
[/AUDIO_LIMPIO]

3. [TABLA_PRODUCCION]

| Tiempo | Audio (Voz) | Visual (Descripción Leonardo.ai) | Prompt de Texto (Overlay) |
| --- | --- | --- | --- |
| 00-03 | [Texto] | Cinematic, 9:16, high contrast, [escena] | TEXTO IMPACTANTE |
(Continúa la tabla cubriendo los 70 segundos en bloques de 3s)
[/TABLA_PRODUCCION]

4. [STORYBOARD_DETALLADO]
(Aquí expande los prompts para Leonardo.ai de las escenas más complejas, usando Style Modifiers: 'Moody lighting', 'Hyper-realistic', 'Corporate Cyberpunk').
[/STORYBOARD_DETALLADO]
"""

def process_video(url):
    raw_text = get_transcript(url)
    if not raw_text:
        print("❌ No se pudo obtener la transcripción.")
        return

    print(f"🤖 Procesando con {MODELO}...")
    response = client.models.generate_content(
        model=MODELO,
        contents=f"{SYSTEM_PROMPT}\n\nTEXTO:\n{raw_text}"
    )
    
    # Crear carpeta y guardar
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    folder = f"{OBSIDIAN_INBOX}/{ts}_Produccion"
    os.makedirs(folder, exist_ok=True)
    
    with open(f"{folder}/MASTER.md", "w") as f:
        f.write(response.text)
    
    print(f"✅ ¡Proyecto listo en Obsidian! Carpeta: {ts}_Produccion")

if __name__ == "__main__":
    url = input("🔗 Link de YouTube: ")
    process_video(url)