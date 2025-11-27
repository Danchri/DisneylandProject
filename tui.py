# tui.py

def show_title():
    print("=== Disneyland Reviews Analysis ===\n")


def show_load_confirmation(count: int):
    print(f"CSV loaded successfully. Rows read: {count}\n")


def main_menu():
    print("Main Menu:")
    print("A) View data")
    print("B) Visualise data")
    print("C) Export data")
    print("X) Exit")
    return input("Choose an option: ").strip().upper()


# -----------------------------
# SUBMENU A - VIEW DATA
# -----------------------------
def submenu_a():
    print("\nView Data (A):")
    print("1) Show all reviews for a specific park")
    print("2) Number of reviews a park received from a specific location")
    print("3) Average rating for a park in a specific year")
    print("4) Average score per park by reviewer location (full report)")
    print("B) Back to Main Menu")
    return input("Choose an option: ").strip()


# -----------------------------
# SUBMENU B - VISUALISE DATA
# -----------------------------
def submenu_b():
    print("\nVisualise Data (B):")
    print("1) Pie chart: reviews per park")
    print("2) Bar chart: average review score per park")
    print("3) Bar chart: top 10 reviewer locations by average rating for a park")
    print("4) Bar chart: average rating per month for a park (1–12)")
    print("B) Back")
    return input("Choose an option: ").strip()


# -----------------------------
# SUBMENU C - EXPORT DATA
# -----------------------------
def submenu_c():
    print("\nExport Data (C):")
    print("1) Export report to TXT")
    print("2) Export report to CSV")
    print("3) Export report to JSON")
    print("B) Back to Main Menu")
    return input("Choose an option: ").strip()


# -----------------------------
# GENERAL INPUT HELPERS
# -----------------------------
def confirm_invalid_choice(choice):
    print(f"Invalid choice '{choice}'. Please try again.\n")


def ask_for_park():
    return input("Enter park name: ").strip()


def ask_for_location():
    return input("Enter reviewer location: ").strip()


def ask_for_year():
    return input("Enter year (YYYY): ").strip()


def ask_for_filename():
    return input("Enter output filename (e.g., report.txt): ").strip()


def show_export_success(filename):
    print(f"\nFile exported successfully: {filename}\n")


# -----------------------------
# REPORT DISPLAY
# -----------------------------
def show_avg_score_per_park_by_location_report(report: dict):
    if not report:
        print("No data to show.\n")
        return

    print("\nAverage score per park by reviewer location (full report):\n")

    for park in sorted(report.keys()):
        print(f"Park: {park}")
        locs = report[park]

        sorted_locs = sorted(locs.items(), key=lambda kv: (kv[1][0], kv[1][1]), reverse=True)

        for loc, (avg, cnt) in sorted_locs:
            print(f"  {loc} — Avg: {avg:.2f} (Reviews: {cnt})")
        print()
