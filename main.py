import csv
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List


VENDOR_ID_PATTERN = re.compile(r"^[A-Z]{2}_[0-9]{3}$")
YEAR_WEEK_PATTERN = re.compile(r"^[0-9]{6}$")


def validate_row(row: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    vendor_id = str(row.get("vendor_id", "")).strip()
    if not VENDOR_ID_PATTERN.fullmatch(vendor_id):
        errors.append(
            "vendor id must be in format AA_123"
        )

    vendor_name = str(row.get("vendor_name", "")).strip()
    if not (2 <= len(vendor_name) <= 25):
        errors.append("vendor name must be between 2 and 25 chars long")

    year_week = str(row.get("year_week", "")).strip()
    if not YEAR_WEEK_PATTERN.fullmatch(year_week):
        errors.append("year and week must be 6 digits in format YYYYWW")
    else:
        week = int(year_week[-2:])
        if not (1 <= week <= 52):
            errors.append("week must be between 01 and 52")

    vegan_hotdogs = row.get("vegan_hotdogs")
    try:
        vegan_hotdogs = int(vegan_hotdogs)
        if vegan_hotdogs % 10 != 0:
            errors.append("number of vegan hotdogs must be divisible by 10")
    except (TypeError, ValueError):
        errors.append("number of vegan hotdogs must be an integer")

    meat_hotdogs = row.get("meat_hotdogs")
    try:
        meat_hotdogs = int(meat_hotdogs)
        if meat_hotdogs % 10 != 0:
            errors.append("number of meat hotdogs must be divisible by 10")
    except (TypeError, ValueError):
        errors.append("number of meat hotdogs must be an integer")

    onions_kg = row.get("onions_kg")
    try:
        onions = Decimal(str(onions_kg))
        if (onions * 2) % 1 != 0:
            errors.append("onions must be in 0.5 kg increments")
    except (InvalidOperation, TypeError, ValueError):
        errors.append("onions must be a decimal number")

    ketchup_litres = row.get("ketchup_litres")
    try:
        ketchup_litres = int(ketchup_litres)
        if not (1 <= ketchup_litres <= 4):
            errors.append("ketchup must be an integer between 1 and 4")
    except (TypeError, ValueError):
        errors.append("ketchup must be an integer between 1 and 4")

    return errors


def validate_file(filepath: str) -> Dict[int, List[str]]:
    all_errors: Dict[int, List[str]] = {}

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row_number, row in enumerate(reader, start=1):
            if len(row) != 7:
                all_errors[row_number] = ["row must have exactly 7 columns."]
                continue

            record = {
                "vendor_id": row[0],
                "vendor_name": row[1],
                "year_week": row[2],
                "vegan_hotdogs": row[3],
                "meat_hotdogs": row[4],
                "onions_kg": row[5],
                "ketchup_litres": row[6],
            }

            errors = validate_row(record)
            if errors:
                all_errors[row_number] = errors

    return all_errors


if __name__ == "__main__":
    errors = validate_file("Hotdogs.txt")

    if not errors:
        print("all rows valid!")
    else:
        for row_num, row_errors in errors.items():
            print(f"Row {row_num}:")
            for error in row_errors:
                print(f"  - {error}")
