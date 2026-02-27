# 🚀 Python Daily Sprint: Media Factory 2026

Repositorio de micro-proyectos y retos diarios de ingeniería para la optimización del pipeline de entrenamiento de IAs (Flux.1, VisionCurator).

## 📊 Bitácora de Retos

| Reto | Descripción | Concepto Clave | Código |
| :--- | :--- | :--- | :--- |
| **01** | **Auditoría de Dataset y Filtrado**: Limpieza automática de etiquetas para entrenamiento de LoRA. | `self`, `__init__`, Boolean Logic | [challenge_stats.py](./challenge_stats.py) |
| **02** | **Escaneo de Directorios**: (En progreso) Automatización de lectura de archivos locales. | `pathlib`, File I/O | [challenge_dir_scanner.py](./challenge_dir_scanner.py) |

---

## 🛠️ Detalles de Implementación

### Reto 01: StatsManager (26/02/2026)
**Problema:** El conteo de personajes en el dataset era manual e inconsistente debido a falsos positivos ("no characters").
**Solución:** Se desarrolló una clase con gestión de estado persistente que normaliza strings (`.lower()`) y aplica filtros booleanos de exclusión.

**Impacto en Media Factory:**
* **Dataset Analizado:** 100 entradas.
* **Precisión de Filtrado:** 100% (52 personajes reales detectados).
* **Eficiencia:** Reducción del tiempo de auditoría de 15 min (manual) a <1s (script).

---

## 📂 Cómo ejecutar
Para correr cualquier reto, asegúrate de estar en la raíz de la carpeta `Scripts` y usa:
```bash
python challenges/challenge_stats.py
