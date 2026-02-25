class StatsManager:
    def __init__(self, target_proportions):
        self.targets = target_proportions
        self.counts = {
            "personaje": 0,
            "paisaje": 0,
            "interaccion": 0,
            "otros": 0
        }
        self.angles = {}
        self.total_approved = 0

    def update_stats(self, tags):
        self.total_approved += 1
        
        # Categorizar por tipo (simplificado basado en tags)
        found_type = False
        for category in ["personaje", "paisaje", "interaccion"]:
            if any(category in tag.lower() for tag in tags):
                self.counts[category] += 1
                found_type = True
                break
        
        if not found_type:
            self.counts["otros"] += 1

        # Trackear ángulos
        for tag in tags:
            tag_lower = tag.lower()
            if any(angle in tag_lower for angle in ["behind", "side view", "close up", "angle"]):
                self.angles[tag_lower] = self.angles.get(tag_lower, 0) + 1

    def get_summary(self):
        if self.total_approved == 0:
            return "No se aprobaron imágenes."

        summary = "\n--- Resumen de Curaduría ---\n"
        summary += f"Total aprobadas: {self.total_approved}\n\n"
        summary += "Distribución por Categoría:\n"
        
        alerts = []
        for cat, target in self.targets.items():
            actual_perc = self.counts[cat] / self.total_approved
            summary += f"- {cat.capitalize()}: {actual_perc:.1%} (Objetivo: {target:.1%})\n"
            
            if abs(actual_perc - target) > 0.15:
                alerts.append(f"⚠️ Desviación significativa en {cat}: {actual_perc:.1%} vs {target:.1%}")

        summary += f"- Otros: {self.counts['otros'] / self.total_approved:.1%}\n"
        
        if self.angles:
            summary += "\nÁngulos detectados:\n"
            for angle, count in self.angles.items():
                summary += f"- {angle}: {count}\n"

        if alerts:
            summary += "\nALERTAS DE CUOTA:\n"
            for alert in alerts:
                summary += alert + "\n"

        return summary
