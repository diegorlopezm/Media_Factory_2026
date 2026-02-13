import re
import os
import datetime
from google import genai
from config import GEMINI_API_KEY, MODELO, OBSIDIAN_INBOX
from scraper import get_transcript

client = genai.Client(api_key=GEMINI_API_KEY)

# --- PROMPT DE CONTROL DE CALIDAD ---
QC_SYSTEM_PROMPT = """
Actúa como un Director Creativo de TikTok con 10 años de experiencia en retención de audiencia.
Tu misión es evaluar el guion proporcionado y darle una puntuación de VIRALIDAD de 1 a 10.

CRITERIOS DE EVALUACIÓN:
1. ¿El Hook es un golpe directo al cerebro?
2. ¿Hay conexiones "prohibidas" o controversiales (ej. Cernunnos-Diablo)?
3. ¿El ritmo es rápido (frases cortas)?
4. ¿Evita el tono de "documental aburrido"?

FORMATO DE SALIDA ÚNICAMENTE:
PUNTUACIÓN: [número]
CRÍTICA: [breve razón de por qué]
"""

# Base técnica del prompt
BASE_SYSTEM_PROMPT = """
Actúa como un experto en guiones virales para TikTok/Shorts de Historia, Biologia, Fisica, curiosidades y Misterio.
Tu misión es convertir la transcripción real de YouTube proporcionada en un guion de 70 segundos.
IMPORTANTE: Genera la respuesta en texto plano con formato Markdown. PROHIBIDO usar formato JSON o bloques de código para el guion.

⚠️ REGLA DE DURACIÓN (CRÍTICO - OBJETIVO 70 SEGUNDOS):
- 120 a 160 palabras.
- PROHIBIDO superar 160 palabras.
- Sé despiadado eliminando paja, introducciones lentas o repeticiones.

⚠️ REGLA DE "CONEXIÓN DE PUNTOS" (SINTESIS VIRAL):
- No te limites a resumir. Conecta los datos con mitos universales o conspiraciones conocidas.
- Si el texto habla de dioses antiguos, relaciónalos con demonios modernos o entidades ocultas (ej. Cernunnos -> Baphomet/Satán).
- Si habla de tecnología, relaciónala con control mental o civilizaciones perdidas.
- Tu objetivo es que el espectador diga: "Esto no me lo contaron en la escuela".

⚠️ REGLA DE FIDELIDAD Y NOMBRES PROPIOS:
- Céntrate en los hechos de la transcripción.
- Verifica ortografía de nombres de figuras y expertos.
- La creatividad se usa solo para el Hook y la narrativa.

⚠️ REGLA DE RITMO Y ENGAGEMENT:
- Bloques de 3s máximo en TABLA_PRODUCCION.
- Cambios de visual cada bloque.
- Incluye micro-misterios cada 5-7s.
- Frases cortas y contundentes, con silencios incómodos.
- Añade al menos 1 frase que divida opiniones o genere debate.

⚠️ REGLA DE MOVIMIENTO WAN 2.2:
- Describir interacción entre luz, viento y cámara.
- Evita "movimiento suave", usa: 'hyper-realistic physics', 'volumetric fog', 'dynamic light shadows', 'cinematic tracking shot'.

IDIOMA: Inglés.

REGLAS DE ACTUACIÓN (ElevenLabs v3):
- [excited]: Hook inicial y datos sorprendentes
- [thoughtful]: Explicaciones y transiciones
- [chuckles]: Ironía o desmitificación
- [whispers]: Secretos o momentos misteriosos
- [sighs]: Datos trágicos o pérdida histórica
- [short pause]: Después de pregunta retórica o revelación

ESTRUCTURA DE SALIDA:
1. [METADATA]
- Project Title, Project Description, Main Character Ref, Visual Theme
- Suggested Hook Type (1 de 7 tipos)
- Target Tags (lista de Python, 5 tags)
[/METADATA]

2. [AUDIO_LIMPIO]
(Guion completo con etiquetas emocionales)
[/AUDIO_LIMPIO]

3. [TABLA_PRODUCCION]
| Tiempo | Audio (Voz) | Visual | Movimiento | Overlay | Ref. Personaje |
| 00-03 | [Texto] | Cinematic, 9:16, [escena] | [Wan 2.2: Camera movement + Physical action + Lighting shift] | TEXTO | ON/OFF |
(Continúa bloques de 3s hasta completar 70s)
[/TABLA_PRODUCCION]

4. [STORYBOARD_DETALLADO]
(Expande prompts complejos con 'Moody lighting', 'Hyper-realistic', etc.)
[/STORYBOARD_DETALLADO]
"""

# Contexto de canales
CHANNEL_CONTEXT = {
    "1": {
        "name": "It Was Avoidable",
        "extra": """
Escribes para 'It Was Avoidable'. Objetivo: frustración y arrepentimiento. Narrador de tragedias humanas.
Hook agresivo directo; evita "Did you know" o "Imagine".
Cierre obligatorio: 'And the worst part? [sighs] It was avoidable.'
Visuales: Cinemático oscuro, grano de película, sombras de Caravaggio.
"""
    },
    "2": {
        "name": "Terminal Zero",
        "extra": """
Escribes para 'Terminal Zero'. Objetivo: paranoia y asombro técnico.
Hook: advertencia o secreto; lenguaje técnico mezclado con suspenso.
Cierre: pregunta que deje al espectador mirando la pantalla.
Visuales: Corporate Cyberpunk, Neón Glitch, paleta azul/naranja.
"""
    },
    "3": {
     "name": "The Sealed Codex",
        "extra": """
        Objetivo: pavor existencial y descubrimiento prohibido. Narrador omnisciente.
        DINÁMICA DE REVELACIÓN: Busca la conexión más oscura. 
        Ejemplos: ¿Eran los ángeles realmente alienígenas? ¿Es el 'dios astado' la base de los rituales modernos? 
        Usa la técnica de 'The Corrupted History': Toma un dato histórico y añade la interpretación suprimida por la Iglesia o el Estado.
        Léxico obligatorio: 'anathema', 'bloodline', 'forbidden archives', 'distorted reality'.
        Cierre: 'The seal is broken. The truth is yours. [whispers] Be careful.'
        """
    }
}

def generate_hooks(raw_text, channel_extra):
    prompt_hooks = f"""
{channel_extra}

OBJETIVO: Detecta el elemento más controversial, misterioso o impactante del texto.
Genera 3 hooks posibles para un short de 30-35s.
Indica cuál es el más agresivo y viral.
Como experto en semiótica y mitología comparada, analiza el siguiente texto.
1. Identifica nombres, fechas o deidades.
2. Busca su 'lado oscuro' o su versión en otras culturas (ej. si menciona a Enki, piensa en Lucifer).
3. Genera 3 hooks basados en estas conexiones PROHIBIDAS, no solo en lo que dice el texto.

TEXTO:
{raw_text}

FORMATO DE SALIDA:
1. Hook 1: ...
2. Hook 2: ...
3. Hook 3: ...
Mejor Hook: ...
"""
    response_hooks = client.models.generate_content(
        model=MODELO,
        contents=prompt_hooks
    )
    return response_hooks.text

def process_video(url, choice):
    channel = CHANNEL_CONTEXT.get(choice)
    if not channel: 
        print("❌ Canal no válido.")
        return

    raw_text = get_transcript(url)
    if not raw_text: 
        print("❌ Transcripción vacía.")
        return

    hooks_text = generate_hooks(raw_text, channel['extra'])
    best_hook_match = re.search(r"Mejor Hook:\s*(.*)", hooks_text)
    best_hook = best_hook_match.group(1) if best_hook_match else ""

    final_prompt = f"{channel['extra']}\nHOOK_SELECTED: {best_hook}\n\n{BASE_SYSTEM_PROMPT}"

    # --- BUCLE DE CONTROL DE CALIDAD ---
    intentos = 0
    aprobado = False
    full_response = ""

    print(f"🤖 Media Factory: Iniciando producción para {channel['name']}...")

    while not aprobado and intentos < 4:
        intentos += 1
        print(f"🎬 Generando versión {intentos}...")
        
        response = client.models.generate_content(
            model=MODELO,
            contents=f"{final_prompt}\n\nTEXTO BASE PARA EL GUION:\n{raw_text}"
        )
        guion_candidato = response.text

        print(f"🔍 Evaluando viralidad (QC Agent)...")
        check = client.models.generate_content(
            model=MODELO,
            contents=f"{QC_SYSTEM_PROMPT}\n\nGUION A EVALUAR:\n{guion_candidato}"
        )
        
        score_match = re.search(r"PUNTUACIÓN:\s*([\d.]+)", check.text)
        score = float(score_match.group(1)) if score_match else 0
        
        print(f"⭐ Calificación: {score}/10")

        if score >= 8.5:
            print("🚀 Calidad aprobada. Procediendo al guardado.")
            full_response = guion_candidato
            aprobado = True
        else:
            print(f"❌ Puntuación insuficiente. Crítica: {check.text.split('CRÍTICA:')[1].strip() if 'CRÍTICA:' in check.text else 'No viral'}")
            # Inyectamos la crítica para que el próximo intento sea mejor
            final_prompt += f"\n\nMEJORA NECESARIA: El guion anterior fue puntuado con {score}/10. Crítica: {check.text}. Hazlo más agresivo, oscuro y rápido."

    if not full_response: full_response = guion_candidato # Fallback por si agota intentos

    # --- Limpieza de título y guardado ---
    title_match = re.search(r"- Project Title:\s*(.*)", full_response)
    clean_title = re.sub(r'[^\w\s-]', '', title_match.group(1)).strip().replace(' ', '_')[:30] if title_match else "Untitled_Project"

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    folder_name = f"{ts}_{channel['name'].replace(' ', '_')}_{clean_title}"
    folder_path = f"{OBSIDIAN_INBOX}/{folder_name}"

    os.makedirs(folder_path, exist_ok=True)
    with open(f"{folder_path}/MASTER.md", "w") as f:
        f.write(full_response)

    print(f"✅ ¡Proyecto listo en Obsidian! Carpeta: {folder_name}")

if __name__ == "__main__":
    print("--- SELECCIONA EL CANAL DE PRODUCCIÓN ---")
    print("1. It Was Avoidable (Historia/Misterio/Tragedia)")
    print("2. Terminal Zero (Tech/AI/Conspiración)")
    print("3. The Sealed Codex (Antidiluviano/biblico/secreto/mitologia)")
    c = input("Opción: ")
    url = input("🔗 Link de YouTube para procesar: ")
    process_video(url, c)