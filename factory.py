import re
import os
import sys
import datetime

# Ensure the script's directory is in the system path to allow importing local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import OBSIDIAN_INBOX
from scraper import get_transcript, get_tiktok_transcript
from channels import CHANNEL_CONTEXT
from prompts import QC_SYSTEM_PROMPT, BASE_SYSTEM_PROMPT
from generator import generate_hooks, generate_script, evaluate_script, improve_script

def process_video(url, choice):
    channel = CHANNEL_CONTEXT.get(choice)
    if not channel: 
        print("❌ Canal no válido.")
        return 

    if "tiktok.com" in url:
        raw_text = get_tiktok_transcript(url)
    else:
        raw_text = get_transcript(url)

    if not raw_text: 
        print("❌ Transcripción vacía.")
        return

    hooks_text = generate_hooks(raw_text, channel['extra'])
    best_hook_match = re.search(r"Mejor Hook:\s*(.*)", hooks_text)
    best_hook = best_hook_match.group(1) if best_hook_match else ""

    final_prompt = f"{channel['extra']}\nHOOK_SELECTED: {best_hook}\n\n{BASE_SYSTEM_PROMPT}"

    # --- Crea carpeta temporal para guardar iteraciones ---
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    folder_name = f"{ts}_{channel['name'].replace(' ', '_')}_TEMP"
    folder_path = f"{OBSIDIAN_INBOX}/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)
    
    # --- BUCLE DE CONTROL DE CALIDAD ---
    intentos = 0
    aprobado = False
    full_response = ""

    print(f"🤖 Media Factory: Iniciando producción para {channel['name']}...")

    print(f"🎬 Generando versión inicial...")
    guion_candidato = generate_script(final_prompt, raw_text)

    while not aprobado and intentos < 10:
        intentos += 1
        print(f"🔄 Iteración {intentos} - Evaluando...")

        print(f"🔍 Evaluando viralidad (QC Agent)...")
        check_text = evaluate_script(QC_SYSTEM_PROMPT, guion_candidato)
        
        score_match = re.search(r"(SCORE|PUNTUACIÓN):\s*([\d.]+)", check_text)
        score = float(score_match.group(2)) if score_match else 0
        
        print(f"⭐ Calificación: {score}/10")

        if score >= 8:
            print("🚀 Calidad aprobada. Procediendo al guardado.")
            full_response = guion_candidato
            aprobado = True
        else:
            critique_text = check_text.split('CRÍTICA:')[1].strip() if 'CRÍTICA:' in check_text else 'No viral'
            with open(f"{folder_path}/VERSION_{intentos}.md", "w") as f:
                f.write(guion_candidato)
            print(f"❌ Puntuación insuficiente. Crítica: {critique_text}")
            
            # --- Aprender de la crítica y mejorar ---
            guion_candidato = improve_script(guion_candidato, score, critique_text)

            final_prompt += f"\n\nMEJORA APLICADA: Guion reescrito con la crítica del intento {intentos}."

    if not full_response: 
        full_response = guion_candidato  # Fallback por si agota intentos

    # --- Limpieza de título real ---
    title_match = re.search(r"- Project Title:\s*(.*)", full_response)
    clean_title = re.sub(r'[^\w\s-]', '', title_match.group(1)).strip().replace(' ', '_')[:30] if title_match else "Untitled_Project"

    # --- Renombrar carpeta temporal con título real ---
    new_folder_name = f"{ts}_{channel['name'].replace(' ', '_')}_{clean_title}"
    new_folder_path = f"{OBSIDIAN_INBOX}/{new_folder_name}"
    os.rename(folder_path, new_folder_path)
    folder_path = new_folder_path

    # Guardar master final
    with open(f"{folder_path}/MASTER.md", "w") as f:
        f.write(full_response)

    print(f"✅ ¡Proyecto listo en Obsidian! Carpeta: {new_folder_name}")

if __name__ == "__main__":
    print("--- SELECCIONA EL CANAL DE PRODUCCIÓN ---")
    print("1. It Was Avoidable (Historia/Misterio/Tragedia)")
    print("2. Terminal Zero (Tech/AI/Conspiración)")
    print("3. NVNCA (Antidiluviano/biblico/secreto/mitologia)")
    c = input("Opción: ")
    url = input("🔗 Link de YouTube para procesar: ")
    process_video(url, c)