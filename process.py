# process.py

import csv
from typing import List, Dict, Any, Tuple
import statistics
from collections import defaultdict


def read_csv_to_list(filepath: str) -> List[Dict[str, Any]]:
    """Read CSV file and return a list of dictionary records."""
    records = []

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rec = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}

            # Convert numeric fields where possible
            try:
                rec["Rating"] = int(rec.get("Rating", 0))
            except:
                rec["Rating"] = None

            try:
                rec["Review_ID"] = int(rec.get("Review_ID", 0))
            except:
                rec["Review_ID"] = None

            records.append(rec)

    return records


def filter_reviews_by_park(records: List[Dict], park_name: str) -> List[Dict]:
    """Return all reviews for a specific park."""
    return [
        r for r in records
        if r.get("Branch", "").lower() == park_name.lower()
    ]


def count_reviews_by_park_and_location(records: List[Dict], park_name: str, location: str) -> int:
    """Count reviews for a park from a specific reviewer location."""
    return sum(
        1 for r in records
        if r.get("Branch", "").lower() == park_name.lower()
        and r.get("Reviewer_Location", "").lower() == location.lower()
    )


def avg_rating_for_park_year(records: List[Dict], park_name: str, year: str):
    """Calculate average rating for a park in a given year."""

    def extract_year(ym_value):
        if not ym_value:
            return None
        ym_value = ym_value.strip()

        # Format: YYYY-MM
        if "-" in ym_value and ym_value[:4].isdigit():
            return ym_value[:4]

        # Format: "May 2019"
        parts = ym_value.split()
        if parts and parts[-1].isdigit():
            return parts[-1]

        return None

    ratings = []

    for r in records:
        if r.get("Branch", "").lower() != park_name.lower():
            continue

        year_month = r.get("Year_Month") or r.get("Year-Month") or r.get("Year/Month")
        rec_year = extract_year(year_month)

        if rec_year == str(year) and isinstance(r.get("Rating"), int):
            ratings.append(r["Rating"])

    if ratings:
        return statistics.mean(ratings)

    return None


# --------------------------
# New functions for Step 2
# --------------------------

def avg_score_per_park_by_location(records: List[Dict]) -> Dict[str, Dict[str, Tuple[float, int]]]:
    """
    Return a nested dictionary:
      { park_name: { location: (average_rating, count), ... }, ... }

    Only considers records with an integer Rating.
    """
    # accumulate sums and counts
    sums = defaultdict(lambda: defaultdict(int))
    counts = defaultdict(lambda: defaultdict(int))

    for r in records:
        park = (r.get("Branch") or "").strip()
        loc = (r.get("Reviewer_Location") or "").strip()
        rating = r.get("Rating")
        if not park or not loc:
            continue
        if isinstance(rating, int):
            sums[park][loc] += rating
            counts[park][loc] += 1

    # compute averages
    result = {}
    for park in sums:
        result[park] = {}
        for loc in sums[park]:
            cnt = counts[park][loc]
            if cnt > 0:
                avg = sums[park][loc] / cnt
                result[park][loc] = (avg, cnt)
    return result


def sorted_location_averages_for_park(records: List[Dict], park_name: str, min_reviews: int = 1):
    """
    For a given park, return a list of tuples sorted by average rating (desc):
      [(location, avg_rating, count), ...]
    min_reviews filters out locations with fewer than min_reviews.
    """
    nested = avg_score_per_park_by_location(records)
    park_key = None
    # find exact-match key ignoring case
    for k in nested:
        if k.lower() == park_name.lower():
            park_key = k
            break
    if not park_key:
        return []

    loc_dict = nested[park_key]
    lst = [(loc, vals[0], vals[1]) for loc, vals in loc_dict.items() if vals[1] >= min_reviews]
    # sort by average descending, then by count descending
    lst.sort(key=lambda x: (x[1], x[2]), reverse=True)
    return lst
