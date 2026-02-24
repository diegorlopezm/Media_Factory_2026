from google import genai
from config import GEMINI_API_KEY, MODELO

client = genai.Client(api_key=GEMINI_API_KEY)

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

def generate_script(final_prompt, raw_text):
    response = client.models.generate_content(
        model=MODELO,
        contents=f"{final_prompt}\n\nTEXTO BASE PARA EL GUION:\n{raw_text}"
    )
    return response.text

def evaluate_script(qc_prompt, script_candidate):
    check = client.models.generate_content(
        model=MODELO,
        contents=f"{qc_prompt}\n\nGUION A EVALUAR:\n{script_candidate}"
    )
    return check.text

def improve_script(script_candidate, score, critique_text):
    improvement_prompt = f"""
El siguiente guion fue puntuado con {score}/10 por el QC Agent.
Crítica recibida: {critique_text}

OBJETIVO: Reescribe el guion original corrigiendo los errores señalados.
- Mantén toda la estructura de salida original: METADATA, AUDIO_LIMPIO, TABLA_PRODUCCION, STORYBOARD_DETALLADO.
- Corrige lenguaje: simple para adolescentes (máx. 15 años).
- Hook inicial impactante en 3s.
- Cliffhangers provocativos.
- Maintain 60-85 words maximum.
- No elimines pasos de producción ni prompts originales.
- Sé más agresivo, oscuro y rápido según la crítica.

Guion original:
{script_candidate}
"""
    improved_response = client.models.generate_content(
        model=MODELO,
        contents=improvement_prompt
    )
    return improved_response.text
