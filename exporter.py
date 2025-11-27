# exporter.py

import json
import csv


class Exporter:
    """Base exporter class providing different export formats."""

    def __init__(self, data):
        # data is the report from avg_score_per_park_by_location()
        self.data = data

    # ---------------- TXT ----------------
    def export_txt(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            for park, locs in self.data.items():
                f.write(f"Park: {park}\n")
                for loc, (avg, cnt) in locs.items():
                    f.write(f"  {loc} — Avg: {avg:.2f} (Reviews: {cnt})\n")
                f.write("\n")

    # ---------------- CSV ----------------
    def export_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Park", "Location", "Average_Rating", "Review_Count"])

            for park, locs in self.data.items():
                for loc, (avg, cnt) in locs.items():
                    writer.writerow([park, loc, f"{avg:.2f}", cnt])

    # ---------------- JSON ----------------
    def export_json(self, filename):
        # Convert tuple values to lists so JSON can encode them
        json_ready = {
            park: {loc: {"avg": avg, "count": cnt}
                   for loc, (avg, cnt) in locs.items()}
            for park, locs in self.data.items()
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_ready, f, indent=4)
