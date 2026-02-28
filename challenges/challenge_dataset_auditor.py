from pathlib import Path

class StatsManager:
    def __init__(self):
        self.valid_files = []
        self.count = 0
        self.landscape_files = []
        self.landscape_count = 0
        self.invalid_files = []
        self.invalid_count = 0

    def audit_file(self, file_path):
        content = file_path.read_text().lower() # Lee el txt directamente
        file_name = file_path.stem # Nombre del archivo sin .txt
        print(f"🔍 Analizando: {file_name}.png")
        if "character" in content and "no character" not in content:
            self.valid_files.append(file_name)
            self.count += 1
            print(f"✅ [VÁLIDO]: {file_name}.png")
            
        elif("landscape" in content or "environment" in content or "scenery" in content):
            self.landscape_files.append(file_name)
            self.landscape_count += 1
            print(f"✅ [VÁLIDO]: {file_name}.png (es un paisaje)")
            
        else:
            self.invalid_files.append(file_name)
            self.invalid_count += 1
            print(content)
            print(f"❌ [DESCARTADO]: {file_name}.png (No es ni un personaje ni un paisaje)")
            print("\n")
            print("\n")

# Uso real:
# manager = StatsManager()
# folder = Path("/workspace/dataset_enoc")
# for txt_file in folder.glob("*.txt"):
#     manager.audit_file(txt_file)

manager = StatsManager()
folder = Path("/home/diego/Imágenes/Flux.2-Dev/NVNCA Lora Training/Dataset_Approved")
for txt_file in folder.glob("*.txt"):
    manager.audit_file(txt_file)

print(f"Total de archivos válidos: {manager.count}")
print(f"Total de archivos inválidos: {manager.invalid_count}")