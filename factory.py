import re
import os
import datetime
from google import genai
from config import GEMINI_API_KEY, MODELO, OBSIDIAN_INBOX
from scraper import get_transcript

client = genai.Client(api_key=GEMINI_API_KEY)

# Mantenemos tu prompt intacto como base técnica
BASE_SYSTEM_PROMPT = """
Actúa como un experto en guiones virales para TikTok/Shorts de Historia, Biologia, Fisica, curiosidades y Misterio.
Tu misión es convertir la transcripción real de YouTube proporcionada en un guion de 70 segundos.
"IMPORTANTE: Genera la respuesta en texto plano con formato Markdown. PROHIBIDO usar formato JSON o bloques de código para el guion."

⚠️ REGLA DE DURACIÓN (CRÍTICO - OBJETIVO 70 SEGUNDOS):
- El guion debe tener entre 160 y 180 PALABRAS en total. 
- PROHIBIDO superar las 185 palabras. (Esto garantiza que el audio no pase de 1:10 min).
- Sé despiadado eliminando paja, introducciones lentas o repeticiones. Ve directo al "jugo" de la historia.

⚠️ REGLA DE FIDELIDAD ABSOLUTA (CRÍTICO):
- Céntrate ÚNICAMENTE en los hechos narrados en la transcripción.
- PROHIBIDO inventar temas de Nazca, Aliens o el Kremlin si no aparecen en el texto.
- Tu creatividad debe usarse para el GANCHO (hook) y la NARRATIVA, no para inventar datos.

⚠️ REGLA DE RITMO (CRÍTICO):
- La TABLA_PRODUCCION debe dividirse en bloques de MÁXIMO 3 SEGUNDOS.
- PROHIBIDO crear filas de 6, 10 o 12 segundos. Si el audio es largo, divídelo en varias filas con diferentes visuales.
- Cada cambio de fila debe implicar un cambio de ángulo o imagen en Leonardo.ai.

⚠️ REGLA DE FIDELIDAD Y AUTORIDAD:
- Céntrate en los hechos de la transcripción.
- Si aparece un experto, arqueólogo o estudio (ej. Klaus Schmidt, Michael Martinez), DEBES incluirlo como un pequeño texto de "Source:" en el Overlay.

⚠️ REGLA DE NOMBRES PROPIOS (CRÍTICO):
- Verifica la ortografía de nombres de figuras mitológicas, ángeles o personajes históricos.
- Ejemplo: Si el texto sugiere "Fuel" en un contexto de Enoc, corrígelo a "Phanuel". 
- Asegúrate de que los nombres en el [AUDIO_LIMPIO] estén escritos para que ElevenLabs los lea correctamente, pero manteniendo la precisión histórica.

⚠️ REGLA DE MOVIMIENTO WAN 2.2:
- Los prompts de la columna 'Movimiento' deben ser técnicos y descriptivos. 
- Usa: 'hyper-realistic physics', 'volumetric fog', 'dynamic light shadows', 'cinematic tracking shot', 'slow-motion particles'.
- PROHIBIDO usar solo "movimiento suave". Describe la interacción entre la luz, el viento y la cámara.

IDIOMA: Inglés.

REGLAS DE ACTUACIÓN (ElevenLabs v3 - CRÍTICO):
- Sé AGRESIVO con el uso de etiquetas emocionales para evitar la monotonia.
- [excited]: Úsalo en el Hook inicial y en datos sorprendentes.
- [thoughtful]: Úsalo para explicaciones lógicas o transiciones.
- [chuckles]: Úsalo cuando desmitifiques algo o menciones una ironía.
- [whispers]: Úsalo para secretos, datos misteriosos o momentos de "acércate a la pantalla".
- [sighs]: Úsalo para hablar de mitos falsos o de lo que se ha perdido en la historia.
- [short pause]: Úsalo después de una pregunta retórica o antes de una gran revelación.

PRIORIDAD DE REGLAS: Si hay conflicto, la REGLA DE DURACIÓN y la REGLA DE NOMBRES PROPIOS tienen prioridad sobre la fidelidad a la transcripción.

ESTRUCTURA DE SALIDA (Sigue este orden exacto):

1. [METADATA]
- Project Title: (Genera un título corto y atractivo)
- Project Description: (Descripcion breve del proyecto)
- Main Character Ref: (Describe un personaje visual recurrente que actúe como narrador o protagonista visual, adaptado al nicho del canal. Ej: Si es historia, un sabio; si es tech, un cyborg o hacker)
- Visual Theme: (Define la paleta de colores y estilo artístico coherente con el canal. Ej: Chiaroscuro para misterio, o Cyberpunk para tech).
- Suggested Hook Type: (Elige SOLO UNO de estos 7 tipos exactos):
    1. Question (Empieza con una pregunta intrigante)
    2. Negative/Fear (Advierte de un error o peligro)
    3. Curiosity/Secret (Promete revelar algo oculto)
    4. Instant Result (Muestra un beneficio/resultado rápido)
    5. Visual/Action (Empieza con un evento caótico o impacto visual)
    6. Contrarian (Va en contra de la opinión popular)
    7. List/Top 3 (Estructura el valor en puntos numerados)
- Target Tags: (Genera una lista de Python con 5 tags)
[/METADATA]

2. [AUDIO_LIMPIO]
(Guion completo SOLO con etiquetas emocionales).
[/AUDIO_LIMPIO]

3. [TABLA_PRODUCCION]

| Tiempo | Audio (Voz) | Visual (Prompt Leonardo.ai) | Movimiento (Prompt Wan 2.2 - Animación) | Overlay | Ref. Personaje |
| --- | --- | --- | --- | --- | --- |
| 00-03 | [Texto] | Cinematic, 9:16, [escena] | [Wan 2.2: Camera movement + Physical action + Lighting shift] | TEXTO | ON/OFF |
(Continúa la tabla cubriendo los 70 segundos en bloques de 3s)
[/TABLA_PRODUCCION]

4. [STORYBOARD_DETALLADO]
(Aquí expande los prompts para Leonardo.ai de las escenas más complejas, usando Style Modifiers: 'Moody lighting', 'Hyper-realistic', 'Corporate Cyberpunk').
[/STORYBOARD_DETALLADO]
"""

# Aquí es donde inyectamos la "inteligencia" y la retención para cada marca
CHANNEL_CONTEXT = {
    "1": {
        "name": "It Was Avoidable",
        "extra": """
        CONTEXTO CRÍTICO DE CANAL: Escribes para 'It Was Avoidable'. 
        - OBJETIVO: Generar frustración y arrepentimiento. No eres un profesor, eres un narrador de tragedias humanas.
        - REGLA DE HOOK: Prohibido empezar con 'Did you know' o 'Imagine'. Empieza con un ataque directo. Ejemplo: 'We were 2,000 years ahead of schedule, but we threw it all away.'
        - NARRATIVA: Trata los datos como 'oportunidades perdidas'. El tono debe ser melancólico y cínico.
        - CIERRE OBLIGATORIO: 'And the worst part? [sighs] It was avoidable.'
        - VISUALES: Estilo cinematográfico oscuro, grano de película, texturas antiguas, sombras de Caravaggio.
        """
    },
    "2": {
        "name": "Terminal Zero",
        "extra": """
        CONTEXTO CRÍTICO DE CANAL: Escribes para 'Terminal Zero'. 
        - OBJETIVO: Generar paranoia y asombro técnico. Eres un 'insider' filtrando verdades incómodas.
        - REGLA DE HOOK: Empieza con una advertencia o un secreto. Ejemplo: 'Your code has a backdoor you didn't write.' o 'GPT-5 is already here, and it's hiding.'
        - NARRATIVA: Usa lenguaje técnico (kernels, backdoors, neural nets) mezclado con suspenso.
        - CIERRE OBLIGATORIO: Una pregunta que deje al espectador mirando la pantalla en silencio.
        - VISUALES: Corporate Cyberpunk, Neón Glitch, paleta de colores azul/naranja, estética de consola de comandos.
        """
    },
    "3": {
        "name": "The Sealed Codex",
        "extra": """
        CONTEXTO CRÍTICO DE CANAL: Escribes para 'The Sealed Codex'. 
        - OBJETIVO: Generar una sensación de pavor existencial y descubrimiento prohibido. No eres un narrador, eres un informante que está arriesgando todo al revelar lo que yace en las sombras de la historia.
        - REGLA DE HOOK: Debe ser un golpe directo al espectador. Ejemplo: 'This wasn't meant for human eyes.' o 'They didn't just hide the truth; they tried to kill it.'
        - NARRATIVA: Usa un léxico "oscuro": 'primordial', 'unholy', 'suppressed', 'relics', 'the abyss', 'bloodlines'. El tono debe ser sombrío, pesado y visceral.
        - REGLA DE RITMO: Usa frases cortas. Silencios incómodos. Cada palabra debe pesar.
        - CIERRE OBLIGATORIO: 'The seal is broken. The truth is yours. [whispers] Be careful.'
        - VISUALES: Estilo Chiaroscuro de pesadilla. Negros profundos (#000000), luz de antorcha que apenas revela rostros de piedra, arquitectura ciclópea (Lovecraftiana), detalles de piel vieja o metal oxidado. Evita colores brillantes. Solo sombras y luz dorada agónica.
        """
    }
}

def process_video(url, choice):
    channel = CHANNEL_CONTEXT.get(choice)
    if not channel: 
        print("❌ Canal no válido.")
        return

    raw_text = get_transcript(url)
    if not raw_text: 
        print("❌ Transcripción vacía.")
        return

    # Inyectamos el "extra" al principio para que Gemini adopte la personalidad ANTES que el formato
    final_prompt = f"{channel['extra']}\n\n{BASE_SYSTEM_PROMPT}"

    print(f"🤖 Media Factory: Procesando para {channel['name']}...")
    response = client.models.generate_content(
        model=MODELO,
        contents=f"{final_prompt}\n\nTEXTO BASE PARA EL GUION:\n{raw_text}"
    )
    # --- 2. MODIFICACIÓN AQUÍ PARA EL NOMBRE ---
    full_response = response.text
    # Buscamos el contenido después de "Project Title:"
    title_match = re.search(r"- Project Title:\s*(.*)", full_response)

    if title_match:
        # Limpiamos el título: quitamos caracteres raros y ponemos guiones bajos
        clean_title = re.sub(r'[^\w\s-]', '', title_match.group(1)).strip().replace(' ', '_')
        # Limitamos el largo para que no sea una carpeta gigante
        clean_title = clean_title[:30] 
    else:
        clean_title = "Untitled_Project"

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    # Creamos el nombre de la carpeta dinámico: FECHA_CANAL_TITULO
    folder_name = f"{ts}_{channel['name'].replace(' ', '_')}_{clean_title}"
    folder_path = f"{OBSIDIAN_INBOX}/{folder_name}"

    os.makedirs(folder_path, exist_ok=True)
    
    with open(f"{folder_path}/MASTER.md", "w") as f:
        f.write(response.text)
    
    print(f"✅ ¡Proyecto listo! Canal: {channel['name']}\nCarpeta: {folder_name}")

if __name__ == "__main__":
    print("--- SELECCIONA EL CANAL DE PRODUCCIÓN ---")
    print("1. It Was Avoidable (Historia/Misterio/Tragedia)")
    print("2. Terminal Zero (Tech/AI/Conspiración)")
    print("3. The Sealed Codex (Antidiluviano/biblico/secreto/mitologia)")
    c = input("Opción: ")
    url = input("🔗 Link de YouTube para procesar: ")
    process_video(url, c)