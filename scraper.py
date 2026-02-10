# scraper.py
import subprocess
import os
import re
import time

def clean_vtt_tags(text):
    """Limpia timestamps y etiquetas de posición de archivos VTT/SRT"""
    # Elimina marcas de tiempo y configuraciones de posición (align:start, etc)
    text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', text)
    # Elimina etiquetas de tiempo internas tipo <00:00:26.080>
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    # Elimina etiquetas de formato tipo <c> o </b>
    text = re.sub(r'<[^>]*>', '', text)
    # Elimina líneas vacías o con solo números
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().isdigit()]
    
    # Quitar duplicados consecutivos (común en VTT de YouTube)
    final_lines = []
    for line in lines:
        if not final_lines or line != final_lines[-1]:
            final_lines.append(line)
            
    return " ".join(final_lines)

def get_transcript(url):
    print(f"📡 Extrayendo transcripción de: {url}...")
    temp_prefix = f"temp_subs_{int(time.time())}"
    
    try:
        # Forzamos vtt que parece ser lo que YouTube te entrega más fácil
        command = [
            'yt-dlp', 
            '--skip-download', 
            '--write-auto-subs', 
            '--write-subs',
            # Intentará bajar español ('es'), si no hay, bajará inglés ('en')
            # El asterisco al final permite variaciones como 'en-US' o 'es-ES'
            '--sub-lang', 'es.*,en.*', 
            '--user-agent', 'facebookexternalhit/1.1',
            '--no-check-certificate',
            '-o', temp_prefix, 
            url
        ]
        subprocess.run(command, capture_output=True, text=True)

        content = ""
        found_file = ""
        # Buscamos archivos .vtt o .srt
        for file in os.listdir("."):
            if file.startswith(temp_prefix) and (file.endswith(".vtt") or file.endswith(".srt")):
                found_file = file
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                break
        
        if found_file:
            os.remove(found_file) # Limpieza inmediata
            return clean_vtt_tags(content)
        
        return None
    except Exception as e:
        print(f"❌ Error en scraper: {e}")
        return None