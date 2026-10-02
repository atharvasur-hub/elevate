"""
Government Schemes Data Harmonization & Cleaning Pipeline
=========================================================
Cleans, standardizes, and normalizes multi-source dirty datasets:
  - Dataset 1: Agriculture Subsidies (CSV)
  - Dataset 2: Rural Development Work (JSON - Nested)
  - Dataset 3: Water Tap Connections (Excel - Unformatted)

Creates relational master tables:
  1. Locations (master geographic lookup with standardized State, District, Sub-district)
  2. Beneficiaries (master unified beneficiary registry)
  3. Agriculture Scheme (with FK to Beneficiaries and Locations)
  4. Rural Development Scheme (with FK to Beneficiaries and Locations)
  5. Water Scheme (with FK to Beneficiaries and Locations)

Exports results to CSV files and SQLite database.
"""

import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd

# ==========================================
# 1. CANONICAL GEOGRAPHIC TAXONOMY DEFINITION
# ==========================================

CANONICAL_LOCATIONS = {
    ("Gujarat", "Ahmedabad"): ["Bavla", "City", "Daskroi", "Dholka", "Sanand"],
    ("Gujarat", "Surat"): ["Choryasi", "City", "Kamrej", "Mangrol", "Olpad"],
    ("Gujarat", "Vadodara"): ["City", "Karjan", "Padra", "Savli", "Vaghodia"],
    ("Maharashtra", "Nagpur"): ["Hingna", "Kamptee", "Nagpur Rural", "Ramtek", "Umred"],
    ("Maharashtra", "Nashik"): ["Igatpuri", "Malegaon", "Nashik", "Niphad", "Sinnar"],
    ("Maharashtra", "Pune"): ["Baramati", "Haveli", "Junnar", "Khed", "Shirur"],
    ("Maharashtra", "Thane"): ["Ambernath", "Bhiwandi", "Kalyan", "Thane", "Ulhasnagar"],
}


# ==========================================
# 2. STRING CLEANING & NORMALIZATION HELPERS
# ==========================================

def clean_token(val: Any) -> str:
    """Removes extra spaces, lowercase, and condenses elongated repeated vowels."""
    if val is None or pd.isna(val):
        return ""
    s = str(val).strip().lower()
    # Collapse repeated vowels (e.g., 'maahaaraashtraa' -> 'maharashtra')
    s = re.sub(r"a+", "a", s)
    s = re.sub(r"e+", "e", s)
    s = re.sub(r"i+", "i", s)
    s = re.sub(r"o+", "o", s)
    s = re.sub(r"u+", "u", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def standardize_state(val: Any) -> str:
    """Standardizes dirty state representations to canonical state names."""
    if val is None or pd.isna(val):
        return "Unknown"
    token = clean_token(val)
    if token in ["ma", "maharashtra"] or "maha" in token or "maah" in token:
        return "Maharashtra"
    if token in ["gu", "gujarat"] or "guja" in token or "gujar" in token:
        return "Gujarat"
    return str(val).strip().title()


def standardize_district(val: Any) -> str:
    """Standardizes dirty district representations to canonical district names."""
    if val is None or pd.isna(val):
        return "Unknown"
    token = clean_token(val)
    if "ahmed" in token or "ahmd" in token:
        return "Ahmedabad"
    if "surat" in token or "surt" in token:
        return "Surat"
    if "vadod" in token or "vdod" in token:
        return "Vadodara"
    if "nagp" in token or "ngpr" in token:
        return "Nagpur"
    if "nash" in token or "nshk" in token:
        return "Nashik"
    if "pune" in token or "pun" in token:
        return "Pune"
    if "than" in token or "thne" in token:
        return "Thane"
    return str(val).strip().title()


def standardize_subdistrict(district_name: str, val: Any) -> str:
    """Matches dirty subdistrict/block/tehsil against canonical list for the district."""
    if val is None or pd.isna(val):
        return "Unknown"

    token = clean_token(val)
    standard_district = standardize_district(district_name)

    # Search in all canonical subdistricts
    for (state, dist), subdistricts in CANONICAL_LOCATIONS.items():
        if dist == standard_district:
            for sub in subdistricts:
                if clean_token(sub) == token:
                    return sub

    # Fallback fuzzy/partial match if exact condensed token did not match
    for (state, dist), subdistricts in CANONICAL_LOCATIONS.items():
        if dist == standard_district:
            for sub in subdistricts:
                sub_token = clean_token(sub)
                if sub_token in token or token in sub_token:
                    return sub

    return str(val).strip().title()


def standardize_beneficiary_id(val: Any) -> str:
    """Standardizes and formats beneficiary ID string."""
    if val is None or pd.isna(val):
        return ""
    s = str(val).strip().upper()
    return s


def parse_numeric_cost(val: Any) -> Optional[float]:
    """Cleans numeric values, converts 'DATA_MISSING' or invalid strings to None/NaN."""
    if val is None or pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val) if not np.isnan(val) else None

    s = str(val).strip().replace("₹", "").replace(",", "")
    if s.upper() in ["DATA_MISSING", "NA", "NAN", "NULL", "NONE", ""]:
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


LOCATION_COORDINATES = {
    ("Gujarat", "Ahmedabad", "Bavla"): (22.8368, 72.3644),
    ("Gujarat", "Ahmedabad", "City"): (23.0225, 72.5714),
    ("Gujarat", "Ahmedabad", "Daskroi"): (22.9500, 72.6300),
    ("Gujarat", "Ahmedabad", "Dholka"): (22.7200, 72.4400),
    ("Gujarat", "Ahmedabad", "Sanand"): (22.9868, 72.3815),
    ("Gujarat", "Surat", "Choryasi"): (21.1702, 72.8311),
    ("Gujarat", "Surat", "City"): (21.1702, 72.8311),
    ("Gujarat", "Surat", "Kamrej"): (21.2700, 72.9600),
    ("Gujarat", "Surat", "Mangrol"): (21.4167, 73.0833),
    ("Gujarat", "Surat", "Olpad"): (21.3300, 72.7500),
    ("Gujarat", "Vadodara", "City"): (22.3072, 73.1812),
    ("Gujarat", "Vadodara", "Karjan"): (22.0500, 73.1700),
    ("Gujarat", "Vadodara", "Padra"): (22.2300, 73.0800),
    ("Gujarat", "Vadodara", "Savli"): (22.5600, 73.2200),
    ("Gujarat", "Vadodara", "Vaghodia"): (22.3000, 73.4200),
    ("Maharashtra", "Nagpur", "Hingna"): (21.0667, 78.9667),
    ("Maharashtra", "Nagpur", "Kamptee"): (21.2333, 79.2000),
    ("Maharashtra", "Nagpur", "Nagpur Rural"): (21.1458, 79.0882),
    ("Maharashtra", "Nagpur", "Ramtek"): (21.4000, 79.3333),
    ("Maharashtra", "Nagpur", "Umred"): (20.8500, 79.3333),
    ("Maharashtra", "Nashik", "Igatpuri"): (19.7000, 73.5500),
    ("Maharashtra", "Nashik", "Malegaon"): (20.5500, 74.5333),
    ("Maharashtra", "Nashik", "Nashik"): (19.9975, 73.7898),
    ("Maharashtra", "Nashik", "Niphad"): (20.0800, 74.1100),
    ("Maharashtra", "Nashik", "Sinnar"): (19.8500, 73.9833),
    ("Maharashtra", "Pune", "Baramati"): (18.1500, 74.5800),
    ("Maharashtra", "Pune", "Haveli"): (18.5000, 73.9100),
    ("Maharashtra", "Pune", "Junnar"): (19.2000, 73.8800),
    ("Maharashtra", "Pune", "Khed"): (18.8400, 73.9000),
    ("Maharashtra", "Pune", "Shirur"): (18.8300, 74.3800),
    ("Maharashtra", "Thane", "Ambernath"): (19.2000, 73.1900),
    ("Maharashtra", "Thane", "Bhiwandi"): (19.3000, 73.0600),
    ("Maharashtra", "Thane", "Kalyan"): (19.2403, 73.1305),
    ("Maharashtra", "Thane", "Thane"): (19.2183, 72.9781),
    ("Maharashtra", "Thane", "Ulhasnagar"): (19.2167, 73.1500),
}


# ==========================================
# 3. MASTER TABLES INITIALIZATION
# ==========================================

def build_master_locations() -> pd.DataFrame:
    """Constructs the canonical Master Locations table with geo-coordinates."""
    records = []
    location_id = 1

    for (state, district), subdistricts in CANONICAL_LOCATIONS.items():
        for sub in sorted(subdistricts):
            lat, lng = LOCATION_COORDINATES.get((state, district, sub), (20.5937, 78.9629))
            records.append({
                "location_id": location_id,
                "state": state,
                "district": district,
                "sub_district": sub,
                "latitude": lat,
                "longitude": lng,
            })
            location_id += 1

    df_locations = pd.DataFrame(records)
    return df_locations


def create_location_lookup(df_locations: pd.DataFrame) -> Dict[Tuple[str, str, str], int]:
    """Creates a fast tuple lookup (state, district, sub_district) -> location_id."""
    lookup = {}
    for _, row in df_locations.iterrows():
        key = (row["state"], row["district"], row["sub_district"])
        lookup[key] = int(row["location_id"])
    return lookup


# ==========================================
# 4. DATASET PROCESSING PIPELINE
# ==========================================

def harmonize_datasets(
    csv_path: str = "Dataset_1_Agriculture_Dirty.csv",
    json_path: str = "Dataset_2_RuralDev_Nested.json",
    excel_path: str = "Dataset_3_Water_Unformatted.xlsx",
    output_dir: str = "cleaned_data",
) -> Dict[str, pd.DataFrame]:
    """
    Main orchestration function to clean and harmonize all 3 datasets.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("STARTING DATA CLEANING & HARMONIZATION PIPELINE")
    print("=" * 70)

    # 1. Build Master Locations
    df_locations = build_master_locations()
    loc_lookup = create_location_lookup(df_locations)
    print(f"[OK] Created Master Locations table: {len(df_locations)} standardized locations")

    # 2. Load & Clean Dataset 1 (Agriculture Subsidies)
    print(f"[*] Reading Dataset 1 (CSV): {csv_path}")
    raw_df1 = pd.read_csv(csv_path)

    df1_clean = pd.DataFrame()
    df1_clean["state"] = raw_df1["state_name"].map(standardize_state)
    df1_clean["district"] = raw_df1["dist_code_name"].map(standardize_district)
    df1_clean["sub_district"] = [
        standardize_subdistrict(dist, block)
        for dist, block in zip(df1_clean["district"], raw_df1["block_name"])
    ]
    df1_clean["beneficiary_code"] = raw_df1["farmer_uid"].map(standardize_beneficiary_id)
    df1_clean["land_holding_hectares"] = pd.to_numeric(raw_df1["land_holding_hectares"], errors="coerce")
    df1_clean["subsidy_disbursed_inr"] = pd.to_numeric(raw_df1["subsidy_disbursed_inr"], errors="coerce")
    df1_clean["disbursal_date"] = pd.to_datetime(raw_df1["disbursal_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Assign location_id
    df1_clean["location_id"] = [
        loc_lookup.get((st, dt, sb), None)
        for st, dt, sb in zip(df1_clean["state"], df1_clean["district"], df1_clean["sub_district"])
    ]

    # 3. Load & Clean Dataset 2 (Rural Development)
    print(f"[*] Reading Dataset 2 (JSON): {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        raw_json_data = json.load(f)
    raw_df2 = pd.json_normalize(raw_json_data)

    df2_clean = pd.DataFrame()
    df2_clean["state"] = raw_df2["LocationDetails.St"].map(standardize_state)
    df2_clean["district"] = raw_df2["LocationDetails.DistrictName"].map(standardize_district)
    df2_clean["sub_district"] = [
        standardize_subdistrict(dist, sub)
        for dist, sub in zip(df2_clean["district"], raw_df2["LocationDetails.SubDistrict"])
    ]
    df2_clean["beneficiary_code"] = raw_df2["WorkerInfo.JobCardNo"].map(standardize_beneficiary_id)
    df2_clean["gender"] = raw_df2["WorkerInfo.Gender"].astype(str).str.strip()
    df2_clean["days_worked"] = pd.to_numeric(raw_df2["Metrics.Days_Worked"], errors="coerce").astype(int)
    df2_clean["wages_paid_inr"] = pd.to_numeric(raw_df2["Metrics.Wages_Paid_INR"], errors="coerce")
    df2_clean["project_type"] = raw_df2["Metrics.Project_Type"].astype(str).str.strip()

    df2_clean["location_id"] = [
        loc_lookup.get((st, dt, sb), None)
        for st, dt, sb in zip(df2_clean["state"], df2_clean["district"], df2_clean["sub_district"])
    ]

    # 4. Load & Clean Dataset 3 (Water Scheme)
    print(f"[*] Reading Dataset 3 (Excel): {excel_path}")
    raw_df3 = pd.read_excel(excel_path)

    df3_clean = pd.DataFrame()
    df3_clean["state"] = raw_df3["GEO_STATE"].map(standardize_state)
    df3_clean["district"] = raw_df3["GEO_DISTRICT"].map(standardize_district)
    df3_clean["sub_district"] = [
        standardize_subdistrict(dist, teh)
        for dist, teh in zip(df3_clean["district"], raw_df3["GEO_TEHSIL"])
    ]
    df3_clean["beneficiary_code"] = raw_df3["UNIQUE_BENEFICIARY_ID"].map(standardize_beneficiary_id)
    df3_clean["tap_connection_status"] = raw_df3["TAP_CONNECTION_STATUS"].astype(str).str.strip()
    df3_clean["cost_incurred"] = raw_df3["COST_INCURRED"].map(parse_numeric_cost)

    df3_clean["location_id"] = [
        loc_lookup.get((st, dt, sb), None)
        for st, dt, sb in zip(df3_clean["state"], df3_clean["district"], df3_clean["sub_district"])
    ]

    # 5. Extract & Build Master Beneficiaries Registry
    print("[*] Extracting unique beneficiary IDs across all datasets...")
    all_beneficiary_codes = sorted(
        list(
            set(df1_clean["beneficiary_code"].dropna())
            | set(df2_clean["beneficiary_code"].dropna())
            | set(df3_clean["beneficiary_code"].dropna())
        )
    )

    # Optional gender mapping from Rural Dev dataset
    gender_map = dict(zip(df2_clean["beneficiary_code"], df2_clean["gender"]))

    df_beneficiaries = pd.DataFrame({
        "beneficiary_id": range(1, len(all_beneficiary_codes) + 1),
        "beneficiary_code": all_beneficiary_codes,
        "gender": [gender_map.get(b_code, None) for b_code in all_beneficiary_codes],
    })
    print(f"[OK] Created Master Beneficiaries table: {len(df_beneficiaries)} unique beneficiaries")

    # Fast reverse lookup beneficiary_code -> beneficiary_id
    ben_lookup = dict(zip(df_beneficiaries["beneficiary_code"], df_beneficiaries["beneficiary_id"]))

    # 6. Build Final Scheme Relational Tables
    # A) Agriculture Scheme
    df_agri = pd.DataFrame({
        "id": range(1, len(df1_clean) + 1),
        "beneficiary_id": df1_clean["beneficiary_code"].map(ben_lookup),
        "location_id": df1_clean["location_id"],
        "beneficiary_code": df1_clean["beneficiary_code"],
        "land_holding_hectares": df1_clean["land_holding_hectares"],
        "subsidy_disbursed_inr": df1_clean["subsidy_disbursed_inr"],
        "disbursal_date": df1_clean["disbursal_date"],
    })

    # B) Rural Development Scheme
    df_rural = pd.DataFrame({
        "id": range(1, len(df2_clean) + 1),
        "beneficiary_id": df2_clean["beneficiary_code"].map(ben_lookup),
        "location_id": df2_clean["location_id"],
        "beneficiary_code": df2_clean["beneficiary_code"],
        "gender": df2_clean["gender"],
        "days_worked": df2_clean["days_worked"],
        "wages_paid_inr": df2_clean["wages_paid_inr"],
        "project_type": df2_clean["project_type"],
    })

    # C) Water Scheme
    df_water = pd.DataFrame({
        "id": range(1, len(df3_clean) + 1),
        "beneficiary_id": df3_clean["beneficiary_code"].map(ben_lookup),
        "location_id": df3_clean["location_id"],
        "beneficiary_code": df3_clean["beneficiary_code"],
        "tap_connection_status": df3_clean["tap_connection_status"],
        "cost_incurred": df3_clean["cost_incurred"],
    })

    # 7. Integrity & Validation Audit
    print("\n" + "=" * 70)
    print("INTEGRITY & DATA QUALITY AUDIT")
    print("=" * 70)

    tables = {
        "locations": df_locations,
        "beneficiaries": df_beneficiaries,
        "agriculture_scheme": df_agri,
        "rural_dev_scheme": df_rural,
        "water_scheme": df_water,
    }

    for name, df in tables.items():
        null_counts = df.isnull().sum().to_dict()
        print(f"Table: {name:<20} | Rows: {len(df):<6} | Nulls: {null_counts}")

    # Check for foreign key integrity
    agri_unmatched_loc = df_agri["location_id"].isnull().sum()
    agri_unmatched_ben = df_agri["beneficiary_id"].isnull().sum()
    rural_unmatched_loc = df_rural["location_id"].isnull().sum()
    rural_unmatched_ben = df_rural["beneficiary_id"].isnull().sum()
    water_unmatched_loc = df_water["location_id"].isnull().sum()
    water_unmatched_ben = df_water["beneficiary_id"].isnull().sum()

    print(f"\nForeign Key Verification:")
    print(f"  - Agriculture Scheme Unmatched (Location FK: {agri_unmatched_loc}, Beneficiary FK: {agri_unmatched_ben})")
    print(f"  - Rural Dev Scheme Unmatched   (Location FK: {rural_unmatched_loc}, Beneficiary FK: {rural_unmatched_ben})")
    print(f"  - Water Scheme Unmatched       (Location FK: {water_unmatched_loc}, Beneficiary FK: {water_unmatched_ben})")

    assert (
        agri_unmatched_loc == 0
        and agri_unmatched_ben == 0
        and rural_unmatched_loc == 0
        and rural_unmatched_ben == 0
        and water_unmatched_loc == 0
        and water_unmatched_ben == 0
    ), "Foreign key integrity validation failed!"
    print("[OK] All Foreign Key constraints verified with 100% referential integrity!")

    # 8. Export to CSV & SQLite
    print("\n" + "=" * 70)
    print("EXPORTING HARMONIZED DATA")
    print("=" * 70)

    # Export CSVs
    for name, df in tables.items():
        csv_file = out_path / f"{name}.csv"
        df.to_csv(csv_file, index=False)
        print(f"[OK] Saved CSV: {csv_file}")

    # Export to SQLite Database
    db_file = out_path / "harmonized_schemes.db"
    conn = sqlite3.connect(db_file)
    with conn:
        df_locations.to_sql("locations", conn, if_exists="replace", index=False)
        df_beneficiaries.to_sql("beneficiaries", conn, if_exists="replace", index=False)
        df_agri.to_sql("agriculture_scheme", conn, if_exists="replace", index=False)
        df_rural.to_sql("rural_dev_scheme", conn, if_exists="replace", index=False)
        df_water.to_sql("water_scheme", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[OK] Saved SQLite Database: {db_file}")

    print("\n" + "=" * 70)
    print("HARMONIZATION COMPLETE - PREVIEW SAMPLES")
    print("=" * 70)

    print("\n--- Master Locations Sample ---")
    print(df_locations.head(5))

    print("\n--- Master Beneficiaries Sample ---")
    print(df_beneficiaries.head(5))

    print("\n--- Agriculture Scheme Sample ---")
    print(df_agri.head(3))

    print("\n--- Rural Dev Scheme Sample ---")
    print(df_rural.head(3))

    print("\n--- Water Scheme Sample ---")
    print(df_water.head(3))

    return tables


if __name__ == "__main__":
    harmonize_datasets()
