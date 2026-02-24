# scraper.py
import subprocess
import os
import re
import time
import yt_dlp
import whisper
import glob

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

def get_tiktok_transcript(url):
    print(f"📥 Descargando audio de TikTok (Raw)...")
    
    # 1. Download raw audio (no post-processing to avoid ffprobe issues)
    temp_pattern = "temp_tiktok_raw.*"
    # Clean up previous runs
    for f in glob.glob(temp_pattern):
        os.remove(f)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_tiktok_raw.%(ext)s',
        'quiet': True,
        'user_agent': 'facebookexternalhit/1.1',
    }
    
    downloaded_file = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the downloaded file (could be .m4a, .webm, etc)
        files = glob.glob(temp_pattern)
        if files:
            downloaded_file = files[0]
    except Exception as e:
        print(f"❌ Error descargando TikTok: {e}")
        return None

    if not downloaded_file:
         print(f"❌ Error: No se descargó el archivo de audio.")
         return None

    # 2. Manual conversion to MP3 using system ffmpeg (bypassing yt-dlp's check)
    audio_path = "temp_tiktok.mp3"
    if os.path.exists(audio_path):
        os.remove(audio_path)

    print(f"⚙️ Convirtiendo a MP3 con ffmpeg...")
    try:
        # Using explicit /usr/bin/ffmpeg as verified
        command = ['/usr/bin/ffmpeg', '-i', downloaded_file, '-y', '-vn', '-acodec', 'libmp3lame', '-q:a', '2', audio_path]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error convirtiendo audio: {e}")
        # Cleanup
        if os.path.exists(downloaded_file): os.remove(downloaded_file)
        return None

    # Cleanup raw file
    if os.path.exists(downloaded_file):
        os.remove(downloaded_file)
    
    # 3. Transcribe
    print(f"🎙️ Transcribiendo con Whisper (RTX 5060)...")
    try:
        model = whisper.load_model("base", device="cuda")
        result = model.transcribe(audio_path)
        text = result["text"]
    except Exception as e:
        print(f"❌ Error transcribiendo con Whisper: {e}")
        text = None
    
    # Final cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)
        
    return text