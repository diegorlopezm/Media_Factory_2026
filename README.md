# 🎥 MediaFactory 2026: Autonomous Content Infrastructure

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) 
![OS](https://img.shields.io/badge/OS-Fedora%20Linux-red.svg) 
![GPU](https://img.shields.io/badge/Cloud%20GPU-RunPod%20RTX%205090-orange.svg) 
![Management](https://img.shields.io/badge/Agile-Jira%20%26%20Confluence-blue.svg)

**MediaFactory 2026** is a hybrid production ecosystem designed to bridge the gap between high-impact manual creativity and automated technical infrastructure. This project manages the end-to-end pipeline for cinematic narrative content, leveraging custom-trained AI models and robust data engineering.

### 🎬 Production Demo
> **Infrastructure Showcase:** Generated using local open-source models (**Flux.1-dev** + **Wan 2.1**) on a remote **RTX 5090 (RunPod)** cluster. Custom **ComfyUI Docker image** optimized for Blackwell/Ada Lovelace architectures.
<table style="width: 100%; border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td style="width: 50%; border: none; padding: 10px;">
      <video src="https://github.com/user-attachments/assets/1ddc28b5-66f4-43af-b536-841bda917669" width="100%" controls muted autoplay loop></video>
      <p align="center"><i>Space Tech Concept (Wan 2.1)</i></p>
    </td>
    <td style="width: 50%; border: none; padding: 10px;">
      <video src="https://github.com/user-attachments/assets/4b7ad839-4bb7-49d4-8eaa-3380c7c4c0ef" width="100%" controls muted autoplay loop></video>
      <p align="center"><i>Cinematic Narrative (NVNCA Style)</i></p>
    </td>
  </tr>
</table>

---

## 🏗️ System Architecture

The ecosystem is built as a scalable MLOps pipeline, managed through **Agile methodologies** and hosted on a hybrid local/cloud infrastructure.

### 1. VisionCurator (Proprietary Dataset Auditor)
A specialized computer vision pipeline powered by **Gemini 2.5 Flash** designed to curate high-fidelity datasets for **Flux LoRA** training.
* **Automated Auditing:** Detects copyright, watermarks, and UI text in source imagery.
* **Quality Filtering:** Scores technical quality and composition to ensure "AAA" cinematic output.
* **Auto-Tagging:** Generates descriptive, compatible captions for CLIP/T5 text encoders.

### 2. Content Factory & Scripting Engine
A modular framework for narrative-driven video production (61-63s format).
* **QC Loop Logic:** Implements an iterative quality control loop for script optimization and retention-hook validation.
* **Audio Pipeline:** Integrated STT (Whisper) and high-fidelity TTS (ElevenLabs) with a custom post-processing chain.

---

## 🛠️ Infrastructure & Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Compute** | Fedora Linux (Master), RunPod (Remote RTX 5090 cluster via Docker) |
| **AI/ML** | Google GenAI (Gemini 2.5), Flux.1-dev (Fine-tuning), Wan 2.1 (Video Generation) |
| **Data Layer** | PostgreSQL (In Development) for asset tracking and performance metrics |
| **Audio** | FL Studio, ElevenLabs, Blue Yeti hardware integration |
| **Management** | Jira (Kanban Ops), Confluence (SOPs & Documentation) |
<img width="2336" height="1473" alt="imagen" src="https://github.com/user-attachments/assets/f863c8e5-7535-40cb-aabc-3a2a77db0022" />

---

## 📂 Core Modular Structure

```bash
├── main.py                # VisionCurator Orchestrator
├── factory.py             # Scripting & Production Engine
├── core/
│   ├── vision_engine.py   # CV logic & Multimodal API integration
│   ├── stats_manager.py   # Dataset state & bias monitoring
│   └── generator.py       # Narrative logic & QC validation
├── utils/
│   └── file_handler.py    # Atomic I/O operations (Pathlib/Static)
└── scraper.py             # System-level utilities (yt-dlp + Whisper)

```
🐍 Engineering Standards

    OOP & Encapsulation: Logic is isolated within specialized classes to maintain a clean global namespace.

    Agile Governance: All development and production cycles are tracked via Jira Sprints, ensuring high velocity and documented progress.

    Robust Error Handling: Industrial-grade try-except strategies to manage API latencies and hardware interrupts.

    Future Scalability: Designed to integrate PostgreSQL/Grafana for real-time production cost vs. retention analytics.


<img width="2344" height="1313" alt="imagen" src="https://github.com/user-attachments/assets/a45de127-f135-4515-81dc-bb2fc7975ac2" />

🚀 Deployment

This system utilizes a Dual-Boot (Fedora/Windows 11) environment for specialized tasks (Audio vs. Dev) and scales to the cloud via RunPod for heavy model training (LoRA/Flux), ensuring cost-effective high-performance computing.

    Authorized for internal use within the MediaFactory 2026 ecosystem. Managed by Jira Cloud.
