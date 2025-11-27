# main.py

from process import (
    read_csv_to_list,
    filter_reviews_by_park,
    count_reviews_by_park_and_location,
    avg_rating_for_park_year,
    avg_score_per_park_by_location
)

from visual import (
    pie_reviews_per_park,
    bar_avg_rating_per_park,
    bar_top10_locations,
    bar_monthly_avg
)

from exporter import Exporter
import tui

# Make sure the CSV is in the same folder as this script
CSV_PATH = "77disneyland_reviews.csv"


def run():
    tui.show_title()

    # LOAD CSV
    try:
        records = read_csv_to_list(CSV_PATH)
        tui.show_load_confirmation(len(records))
    except FileNotFoundError:
        print(f"ERROR: CSV file '{CSV_PATH}' not found.")
        return

    # MAIN MENU LOOP
    while True:
        choice = tui.main_menu()

        if choice == "A":
            handle_view_data(records)

        elif choice == "B":
            handle_visuals(records)

        elif choice == "C":
            handle_export(records)

        elif choice == "X":
            print("Exiting program. Goodbye!")
            break

        else:
            tui.confirm_invalid_choice(choice)


# -------------------------------------------------------
#                A) VIEW DATA MENU
# -------------------------------------------------------
def handle_view_data(records):
    while True:
        c = tui.submenu_a()

        if c == "1":
            park = tui.ask_for_park()
            reviews = filter_reviews_by_park(records, park)

            if not reviews:
                print(f"No reviews for '{park}'.\n")
            else:
                print(f"\nShowing {len(reviews)} reviews for {park}:\n")
                for r in reviews:
                    print(r)
                print()

        elif c == "2":
            park = tui.ask_for_park()
            loc = tui.ask_for_location()
            cnt = count_reviews_by_park_and_location(records, park, loc)
            print(f"\nReviews for {park} from {loc}: {cnt}\n")

        elif c == "3":
            park = tui.ask_for_park()
            year = tui.ask_for_year()
            avg = avg_rating_for_park_year(records, park, year)

            if avg is None:
                print(f"No ratings for {park} in {year}.\n")
            else:
                print(f"Average rating for {park} in {year}: {avg:.2f}\n")

        elif c == "4":
            report = avg_score_per_park_by_location(records)
            tui.show_avg_score_per_park_by_location_report(report)

        elif c.upper() == "B":
            return

        else:
            tui.confirm_invalid_choice(c)


# -------------------------------------------------------
#             B) VISUALISATION MENU
# -------------------------------------------------------
def handle_visuals(records):
    while True:
        c = tui.submenu_b()

        if c == "1":
            pie_reviews_per_park(records)

        elif c == "2":
            bar_avg_rating_per_park(records)

        elif c == "3":
            park = tui.ask_for_park()
            bar_top10_locations(records, park)

        elif c == "4":
            park = tui.ask_for_park()
            bar_monthly_avg(records, park)

        elif c.upper() == "B":
            return

        else:
            tui.confirm_invalid_choice(c)


# -------------------------------------------------------
#                 C) EXPORT MENU
# -------------------------------------------------------
def handle_export(records):
    report = avg_score_per_park_by_location(records)

    while True:
        c = tui.submenu_c()

        if c == "1":  # TXT
            filename = tui.ask_for_filename()
            Exporter(report).export_txt(filename)
            tui.show_export_success(filename)

        elif c == "2":  # CSV
            filename = tui.ask_for_filename()
            Exporter(report).export_csv(filename)
            tui.show_export_success(filename)

        elif c == "3":  # JSON
            filename = tui.ask_for_filename()
            Exporter(report).export_json(filename)
            tui.show_export_success(filename)

        elif c.upper() == "B":
            return

        else:
            tui.confirm_invalid_choice(c)


# -------------------------------------------------------
#            PROGRAM ENTRY POINT
# -------------------------------------------------------
if __name__ == "__main__":
    run()
