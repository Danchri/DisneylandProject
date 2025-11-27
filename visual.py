# visual.py

import matplotlib.pyplot as plt
from collections import defaultdict
import statistics


# ----------------------------------------------
# B1 - Pie Chart: Reviews per park
# ----------------------------------------------
def pie_reviews_per_park(records):
    counts = defaultdict(int)

    for r in records:
        park = r.get("Branch", "").strip()
        if park:
            counts[park] += 1

    labels = list(counts.keys())
    sizes = list(counts.values())

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Number of Reviews per Park")
    plt.show()


# ----------------------------------------------
# B2 - Bar Chart: Average rating per park
# ----------------------------------------------
def bar_avg_rating_per_park(records):
    sums = defaultdict(int)
    counts = defaultdict(int)

    for r in records:
        park = r.get("Branch", "").strip()
        rating = r.get("Rating")
        if park and isinstance(rating, int):
            sums[park] += rating
            counts[park] += 1

    parks = []
    avgs = []

    for park in sums:
        avg = sums[park] / counts[park]
        parks.append(park)
        avgs.append(avg)

    plt.figure(figsize=(10, 6))
    plt.bar(parks, avgs)
    plt.xlabel("Park")
    plt.ylabel("Average Rating")
    plt.title("Average Rating per Park")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# ----------------------------------------------
# B3 - Bar chart: Top 10 locations by average rating for a park
# ----------------------------------------------
def bar_top10_locations(records, park_name):
    sums = defaultdict(int)
    counts = defaultdict(int)

    for r in records:
        if r.get("Branch", "").lower() == park_name.lower():
            loc = r.get("Reviewer_Location", "").strip()
            rating = r.get("Rating")
            if loc and isinstance(rating, int):
                sums[loc] += rating
                counts[loc] += 1

    data = []
    for loc in sums:
        avg = sums[loc] / counts[loc]
        data.append((loc, avg, counts[loc]))

    data.sort(key=lambda x: x[1], reverse=True)
    top10 = data[:10]

    if not top10:
        print(f"No data available for park: {park_name}")
        return

    locations = [item[0] for item in top10]
    avgs = [item[1] for item in top10]

    plt.figure(figsize=(10, 6))
    plt.bar(locations, avgs)
    plt.xlabel("Reviewer Location")
    plt.ylabel("Average Rating")
    plt.title(f"Top 10 Locations by Average Rating for {park_name}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# ----------------------------------------------
# B4 - Bar chart: Average rating per month (Jan–Dec)
# ----------------------------------------------
def bar_monthly_avg(records, park_name):
    month_sums = defaultdict(int)
    month_counts = defaultdict(int)

    for r in records:
        if r.get("Branch", "").lower() == park_name.lower():
            rating = r.get("Rating")
            month_data = r.get("Year_Month")

            if isinstance(rating, int) and month_data and "-" in month_data:
                parts = month_data.split("-")
                month = parts[1]  # second part is month

                if month.isdigit():
                    month = int(month)
                    month_sums[month] += rating
                    month_counts[month] += 1

    months = []
    avgs = []

    for m in range(1, 12 + 1):
        if month_counts[m] > 0:
            avg = month_sums[m] / month_counts[m]
            months.append(m)
            avgs.append(avg)

    if not months:
        print(f"No monthly rating data for {park_name}")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(months, avgs)
    plt.xlabel("Month (1–12)")
    plt.ylabel("Average Rating")
    plt.title(f"Average Monthly Rating for {park_name}")
    plt.xticks(months)
    plt.tight_layout()
    plt.show()
