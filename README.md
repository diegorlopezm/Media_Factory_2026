# 🎥 Media_Factory_2026 

¡Bienvenido a la central de inteligencia de contenidos! **Media_Factory_2026** es un ecosistema de automatización diseñado para creadores que buscan dominar el mercado de videos cortos (TikTok, YouTube Shorts y Reels) mediante Inteligencia Artificial.

Este repositorio contiene el "cerebro" que procesa información densa y la convierte en guiones técnicos listos para producción.

## 🧠 ¿Qué hace este sistema?
1. **Scraping Inteligente:** Extrae transcripciones de YouTube (incluyendo autogeneradas).
2. **Filtrado Viral:** Mediante Gemini 2.0 Flash, identifica los puntos de mayor retención y curiosidades con potencial viral.
3. **Guionización Técnica:** Genera guiones de 70 segundos con etiquetas emocionales para **ElevenLabs**.
4. **Plan de Producción:** Crea tablas de producción compatibles con **Obsidian** y prompts visuales detallados para **Leonardo.ai**.
5. **Organización Kanban:** Clasifica automáticamente el tipo de gancho (Hook) y genera etiquetas para un flujo de trabajo organizado.

## 🛠️ Tecnologías
- **Python 3.10+**
- **Google GenAI API** (Gemini 2.0 Flash)
- **Obsidian** (Como centro de gestión de proyectos)
- **Git** (Control de versiones de prompts y lógica)

## 📁 Estructura del Proyecto
- `factory.py`: Script principal de procesamiento.
- `scraper.py`: Utilidad para obtener transcripciones de YouTube.
- `config.py`: Configuración local (claves de API y rutas). *Ignorado por Git por seguridad.*
- `.gitignore`: Protege tus claves y archivos temporales de limpieza.

## 🚀 Instalación y Uso Rápido

1. **Clonar el repo:**
   ```bash
   git clone [https://github.com/TU_USUARIO/Media_Factory_2026.git](https://github.com/TU_USUARIO/Media_Factory_2026.git)
   cd Media_Factory_2026/Scripts

Configurar el entorno:

        Copia config.example.py a config.py.

        Añade tu GEMINI_API_KEY y la ruta de tu OBSIDIAN_INBOX.

    Ejecutar la fábrica:
    Bash

    python factory.py

        Introduce la URL del video.

        (Opcional) Añade instrucciones extra para forzar un ángulo viral específico.

📋 El flujo de trabajo "Master"

    Guionización: El script inyecta un archivo MASTER.md en tu Obsidian.

    Audio: Copiar el [AUDIO_LIMPIO] a ElevenLabs.

    Visuales: Usar el [STORYBOARD] para generar imágenes en masa en Leonardo.ai.

    Edición: Montar en CapCut siguiendo la [TABLA_PRODUCCION].