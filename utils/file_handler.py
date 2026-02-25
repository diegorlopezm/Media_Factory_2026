import os
import shutil
import json
from datetime import datetime

class FileHandler:
    @staticmethod
    def ensure_dirs(folders):
        for folder in folders:
            os.makedirs(folder, exist_ok=True)

    @staticmethod
    def get_image_files(input_folder):
        return [f for f in os.listdir(input_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

    @staticmethod
    def move_file(src, dst):
        shutil.move(src, dst)

    @staticmethod
    def create_caption(image_path, tags):
        caption_path = os.path.splitext(image_path)[0] + ".txt"
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(", ".join(tags))
        return caption_path

    @staticmethod
    def log_curation(log_path, filename, data):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "decision": data.get("decision"),
            "score": data.get("score_calidad"),
            "reason": data.get("razon"),
            "tags": data.get("tags", [])
        }
        
        logs = []
        if os.path.exists(log_path):
            try:
                with open(log_path, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
        
        logs.append(log_entry)
        
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(logs, indent=4, ensure_ascii=False, fp=f)
