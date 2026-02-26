# 🎬 Workflows de Producción NVNCA - MediaFactory

Este repositorio contiene los flujos de trabajo (workflows) optimizados para la generación de contenido de **Enoc** utilizando modelos de última generación.

## 🚀 Requisitos de Hardware
- **GPU:** Optimizado para NVIDIA RTX 5090 (24GB+ VRAM).
- **Formatos:** FP8 Precision para modelos de 14B.

## 🧩 Nodos Personalizados (Custom Nodes)
Para evitar errores de "Missing Nodes", instala las siguientes extensiones mediante el **ComfyUI Manager**:

1. **ComfyUI-VideoHelperSuite** (por Kosinkadink) - Gestión de video.
2. **ComfyUI-WanVideo** (por Mr. For Example) - Soporte para Wan2.1.
3. **ComfyUI-Custom-Scripts** (por Chris Goringe) - Notas y herramientas de UI.

## 🛠️ Workflows Incluidos
- `diego-wan2_2_14B_i2v.json`: Generación de Imagen a Video (I2V) a 16fps/24fps.
- `diego-flux_dev_full_text_to_image.json`: Generación de imágenes base para consistencia de personaje.