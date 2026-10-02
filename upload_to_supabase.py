"""
Upload Harmonized Cleaned Datasets to Supabase PostgreSQL
=========================================================
Reads CSVs from cleaned_data/ and uploads them into Supabase PostgreSQL:
  1. locations
  2. beneficiaries
  3. agriculture_scheme
  4. rural_dev_scheme
  5. water_scheme
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Ensure project root is in python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.core.config import settings


CREATE_TABLES_SQL = """
-- Drop old tables if existing
DROP TABLE IF EXISTS agriculture_scheme CASCADE;
DROP TABLE IF EXISTS rural_dev_scheme CASCADE;
DROP TABLE IF EXISTS water_scheme CASCADE;
DROP TABLE IF EXISTS funds CASCADE;
DROP TABLE IF EXISTS schemes CASCADE;
DROP TABLE IF EXISTS beneficiaries CASCADE;
DROP TABLE IF EXISTS locations CASCADE;

-- 1. Locations Master Table
CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    sub_district VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_locations_state ON locations(state);
CREATE INDEX idx_locations_district ON locations(district);
CREATE INDEX idx_locations_sub_district ON locations(sub_district);

-- 2. Beneficiaries Master Table
CREATE TABLE beneficiaries (
    id INTEGER PRIMARY KEY,
    beneficiary_code VARCHAR(50) UNIQUE NOT NULL,
    gender VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_beneficiaries_code ON beneficiaries(beneficiary_code);

-- 3. Agriculture Scheme Table
CREATE TABLE agriculture_scheme (
    id INTEGER PRIMARY KEY,
    beneficiary_id INTEGER NOT NULL REFERENCES beneficiaries(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    beneficiary_code VARCHAR(50) NOT NULL,
    land_holding_hectares FLOAT NOT NULL,
    subsidy_disbursed_inr FLOAT,
    disbursal_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_agri_beneficiary ON agriculture_scheme(beneficiary_id);
CREATE INDEX idx_agri_location ON agriculture_scheme(location_id);
CREATE INDEX idx_agri_disbursal_date ON agriculture_scheme(disbursal_date);

-- 4. Rural Development Scheme Table
CREATE TABLE rural_dev_scheme (
    id INTEGER PRIMARY KEY,
    beneficiary_id INTEGER NOT NULL REFERENCES beneficiaries(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    beneficiary_code VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    days_worked INTEGER NOT NULL,
    wages_paid_inr FLOAT NOT NULL,
    project_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_rural_beneficiary ON rural_dev_scheme(beneficiary_id);
CREATE INDEX idx_rural_location ON rural_dev_scheme(location_id);
CREATE INDEX idx_rural_project_type ON rural_dev_scheme(project_type);

-- 5. Water Scheme Table
CREATE TABLE water_scheme (
    id INTEGER PRIMARY KEY,
    beneficiary_id INTEGER NOT NULL REFERENCES beneficiaries(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    beneficiary_code VARCHAR(50) NOT NULL,
    tap_connection_status VARCHAR(50) NOT NULL,
    cost_incurred FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_water_beneficiary ON water_scheme(beneficiary_id);
CREATE INDEX idx_water_location ON water_scheme(location_id);
CREATE INDEX idx_water_status ON water_scheme(tap_connection_status);
"""


async def upload_data():
    cleaned_dir = Path("cleaned_data")
    if not cleaned_dir.exists():
        raise FileNotFoundError("cleaned_data/ directory not found. Please run clean_and_harmonize_data.py first.")

    engine = create_async_engine(settings.async_database_url, echo=False)

    print("=" * 70)
    print("STARTING SUPABASE POSTGRESQL UPLOAD")
    print(f"Connecting to: {settings.async_database_url.split('@')[-1]}")
    print("=" * 70)

    async with engine.begin() as conn:
        print("[*] Recreating database schema tables and indexes...")
        for statement in CREATE_TABLES_SQL.split(";"):
            stmt = statement.strip()
            if stmt:
                await conn.execute(text(stmt))
        print("[OK] All 5 tables created successfully.")

    # Helper to sanitize dict records so NaN -> None and date strings -> datetime.date
    from datetime import date
    def sanitize_records(recs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned = []
        for r in recs:
            row = {}
            for k, v in r.items():
                if pd.isna(v) or v is None:
                    row[k] = None
                elif k == "disbursal_date" and isinstance(v, str) and v.strip():
                    try:
                        row[k] = date.fromisoformat(v.strip())
                    except Exception:
                        row[k] = None
                else:
                    row[k] = v
            cleaned.append(row)
        return cleaned

    # 1. Locations
    df_loc = pd.read_csv(cleaned_dir / "locations.csv")
    df_loc = df_loc.rename(columns={"location_id": "id"})
    print(f"[*] Uploading locations ({len(df_loc)} rows)...")
    loc_records = sanitize_records(df_loc.to_dict(orient="records"))
    async with engine.begin() as conn:
        await conn.execute(
            text(
                "INSERT INTO locations (id, state, district, sub_district, latitude, longitude) "
                "VALUES (:id, :state, :district, :sub_district, :latitude, :longitude)"
            ),
            loc_records,
        )
    print(f"[OK] Uploaded locations: {len(df_loc)} rows")

    # 2. Beneficiaries
    df_ben = pd.read_csv(cleaned_dir / "beneficiaries.csv")
    df_ben = df_ben.rename(columns={"beneficiary_id": "id"})
    print(f"[*] Uploading beneficiaries ({len(df_ben)} rows in chunks)...")
    ben_records = sanitize_records(df_ben.to_dict(orient="records"))
    chunk_size = 2000
    async with engine.begin() as conn:
        for i in range(0, len(ben_records), chunk_size):
            chunk = ben_records[i : i + chunk_size]
            await conn.execute(
                text(
                    "INSERT INTO beneficiaries (id, beneficiary_code, gender) "
                    "VALUES (:id, :beneficiary_code, :gender)"
                ),
                chunk,
            )
    print(f"[OK] Uploaded beneficiaries: {len(df_ben)} rows")

    # 3. Agriculture Scheme
    df_agri = pd.read_csv(cleaned_dir / "agriculture_scheme.csv")
    agri_records = sanitize_records(df_agri.to_dict(orient="records"))
    print(f"[*] Uploading agriculture_scheme ({len(df_agri)} rows in chunks)...")
    async with engine.begin() as conn:
        for i in range(0, len(agri_records), chunk_size):
            chunk = agri_records[i : i + chunk_size]
            await conn.execute(
                text(
                    "INSERT INTO agriculture_scheme (id, beneficiary_id, location_id, beneficiary_code, land_holding_hectares, subsidy_disbursed_inr, disbursal_date) "
                    "VALUES (:id, :beneficiary_id, :location_id, :beneficiary_code, :land_holding_hectares, :subsidy_disbursed_inr, :disbursal_date)"
                ),
                chunk,
            )
    print(f"[OK] Uploaded agriculture_scheme: {len(df_agri)} rows")

    # 4. Rural Development Scheme
    df_rural = pd.read_csv(cleaned_dir / "rural_dev_scheme.csv")
    rural_records = sanitize_records(df_rural.to_dict(orient="records"))
    print(f"[*] Uploading rural_dev_scheme ({len(df_rural)} rows in chunks)...")
    async with engine.begin() as conn:
        for i in range(0, len(rural_records), chunk_size):
            chunk = rural_records[i : i + chunk_size]
            await conn.execute(
                text(
                    "INSERT INTO rural_dev_scheme (id, beneficiary_id, location_id, beneficiary_code, gender, days_worked, wages_paid_inr, project_type) "
                    "VALUES (:id, :beneficiary_id, :location_id, :beneficiary_code, :gender, :days_worked, :wages_paid_inr, :project_type)"
                ),
                chunk,
            )
    print(f"[OK] Uploaded rural_dev_scheme: {len(df_rural)} rows")

    # 5. Water Scheme
    df_water = pd.read_csv(cleaned_dir / "water_scheme.csv")
    water_records = sanitize_records(df_water.to_dict(orient="records"))
    print(f"[*] Uploading water_scheme ({len(df_water)} rows in chunks)...")
    async with engine.begin() as conn:
        for i in range(0, len(water_records), chunk_size):
            chunk = water_records[i : i + chunk_size]
            await conn.execute(
                text(
                    "INSERT INTO water_scheme (id, beneficiary_id, location_id, beneficiary_code, tap_connection_status, cost_incurred) "
                    "VALUES (:id, :beneficiary_id, :location_id, :beneficiary_code, :tap_connection_status, :cost_incurred)"
                ),
                chunk,
            )
    print(f"[OK] Uploaded water_scheme: {len(df_water)} rows")

    # Verification Query
    print("\n" + "=" * 70)
    print("VERIFYING SUPABASE ROW COUNTS")
    print("=" * 70)
    async with engine.connect() as conn:
        for tbl in ["locations", "beneficiaries", "agriculture_scheme", "rural_dev_scheme", "water_scheme"]:
            res = await conn.execute(text(f"SELECT COUNT(*) FROM {tbl};"))
            count = res.scalar()
            print(f"Table: {tbl:<25} | Live Supabase Count: {count}")

    await engine.dispose()
    print("\n[OK] Supabase upload and database initialization completed successfully!")


if __name__ == "__main__":
    asyncio.run(upload_data())
