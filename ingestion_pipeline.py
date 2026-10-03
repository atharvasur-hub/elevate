import pandas as pd
import numpy as np
import json
import sqlite3
import os
import random

def generate_synthetic_data():
    print("Generating synthetic datasets...")
    np.random.seed(42)
    random.seed(42)
    
    # Common pool of Beneficiary IDs
    beneficiary_ids = [f"B-{str(i).zfill(6)}" for i in range(1, 10001)]
    
    # 1. Agriculture (PM-KISAN) - Flat CSV
    # Messy casing, spelling errors
    pm_kisan_data = []
    locations = ["Pune", "PUNE", "pune ", "Baramati", "Baramati ", "BARAMATI", "Thane", "thane", "THANE", "Nashik", "NASHIK", "Shirur"]
    for b_id in random.sample(beneficiary_ids, 8000):
        loc = random.choice(locations)
        land_size = round(random.uniform(0.5, 5.0), 2)
        subsidy = 6000 if land_size < 2.0 else 0
        pm_kisan_data.append([b_id, loc, land_size, subsidy])
    
    df_agri = pd.DataFrame(pm_kisan_data, columns=["Beneficiary_ID", "Location_Name", "Land_Holding_Size", "Subsidy_Disbursed"])
    df_agri.to_csv("pm_kisan_messy.csv", index=False)
    
    # 2. Rural Dev (MGNREGA) - Nested JSON
    # Deeply nested, requires flattening
    mgnrega_data = []
    for b_id in random.sample(beneficiary_ids, 7000):
        # HARDCODED ANOMALY 1: Baramati execution failure
        # 150+ days worked, 0 wages
        if random.random() < 0.05:
            loc = "Baramati"
            days = random.randint(150, 200)
            wages = 0
        else:
            loc = random.choice(["Pune", "Thane", "Nashik", "Shirur", "Baramati"])
            days = random.randint(10, 100)
            wages = days * 250
            
        record = {
            "metadata": {
                "source": "Ministry of Rural Dev",
                "timestamp": "2024-01-01"
            },
            "beneficiary_details": {
                "id": b_id,
                "work_profile": {
                    "days_worked": days,
                    "wages_paid": wages,
                    "physical_project_type": random.choice(["Road Construction", "Pond Digging", "Tree Plantation"]),
                    "region": loc
                }
            }
        }
        mgnrega_data.append(record)
    
    with open("mgnrega_nested.json", "w") as f:
        json.dump(mgnrega_data, f)
        
    # 3. Jal Shakti (Water) - XLSX (Simulated as Dict for easy pandas loading here, but saved as excel)
    # Misaligned columns, distinct naming
    jal_shakti_data = []
    for b_id in random.sample(beneficiary_ids, 6500):
        # HARDCODED ANOMALY 2: Thane Geographic Gap
        # Slashed budget allocations
        if random.random() < 0.1:
            loc = "Thane District"
            cost = random.randint(100, 500) # Slashed
        else:
            loc = random.choice(["Pune City", "Baramati Taluka", "Nashik Region", "Thane District", "Shirur Taluka"])
            cost = random.randint(5000, 15000)
            
        jal_shakti_data.append({
            "Ben_ID": b_id,
            "Region_String": loc,
            "Tap_Connection_Status": random.choice(["Connected", "Pending", "Failed"]),
            "Financial_Cost_Incurred": cost
        })
        
    df_water = pd.DataFrame(jal_shakti_data)
    df_water.to_excel("jal_shakti_unformatted.xlsx", index=False)
    print("Synthetic datasets generated.")

def clean_and_ingest():
    print("Starting Ingestion Pipeline...")
    
    # Load PM-KISAN
    df_agri = pd.read_csv("pm_kisan_messy.csv")
    # Clean location strings
    df_agri["Location_Clean"] = df_agri["Location_Name"].astype(str).str.strip().str.title()
    df_agri["Source_Dataset"] = "PM-KISAN"
    
    # Load MGNREGA
    with open("mgnrega_nested.json", "r") as f:
        mgnrega_raw = json.load(f)
    
    mgnrega_flat = []
    for row in mgnrega_raw:
        b_details = row.get("beneficiary_details", {})
        work = b_details.get("work_profile", {})
        mgnrega_flat.append({
            "Beneficiary_ID": b_details.get("id"),
            "Location_Clean": str(work.get("region", "")).strip().title(),
            "Days_Worked": work.get("days_worked"),
            "Wages_Paid": work.get("wages_paid"),
            "Project_Type": work.get("physical_project_type"),
            "Source_Dataset": "MGNREGA"
        })
    df_rural = pd.DataFrame(mgnrega_flat)
    
    # Load Jal Shakti
    df_water = pd.read_excel("jal_shakti_unformatted.xlsx")
    # Clean location strings (e.g. remove " Taluka", " District", " City", " Region")
    df_water["Location_Clean"] = df_water["Region_String"].str.replace(" Taluka", "").str.replace(" District", "").str.replace(" City", "").str.replace(" Region", "").str.strip().str.title()
    df_water.rename(columns={"Ben_ID": "Beneficiary_ID"}, inplace=True)
    df_water["Source_Dataset"] = "Jal-Shakti"
    
    # Outer Join on Beneficiary_ID
    # We will pivot on Beneficiary ID to create a master table
    print("Joining datasets on Beneficiary_ID...")
    
    master_df = df_agri.merge(df_rural, on="Beneficiary_ID", how="outer", suffixes=("_agri", "_rural"))
    master_df = master_df.merge(df_water, on="Beneficiary_ID", how="outer")
    
    # Consolidate Location
    master_df["Master_Location"] = master_df["Location_Clean_agri"].combine_first(master_df["Location_Clean_rural"]).combine_first(master_df["Location_Clean"])
    
    # Drop messy location columns
    master_df.drop(columns=["Location_Name", "Location_Clean_agri", "Location_Clean_rural", "Region_String", "Location_Clean"], inplace=True)
    
    # Add a global source column for traceability purposes (we'll just store all matching sources)
    master_df["Sources_Combined"] = master_df[["Source_Dataset_agri", "Source_Dataset_rural", "Source_Dataset"]].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    
    # Replace NaNs
    master_df.fillna({
        "Land_Holding_Size": 0, "Subsidy_Disbursed": 0,
        "Days_Worked": 0, "Wages_Paid": 0, "Project_Type": "None",
        "Tap_Connection_Status": "None", "Financial_Cost_Incurred": 0
    }, inplace=True)
    
    print(f"Master dataset created with {len(master_df)} rows.")
    
    # Save to SQLite
    db_path = "master.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    # Write master table
    master_df.to_sql("master_beneficiaries", conn, index=False, if_exists="replace")
    
    # Create an explicit ID column for db_row_id traceability
    cursor = conn.cursor()
    # Add auto-increment primary key
    cursor.execute('''
        CREATE TABLE temp_master AS SELECT * FROM master_beneficiaries;
    ''')
    cursor.execute('DROP TABLE master_beneficiaries;')
    cursor.execute('''
        CREATE TABLE master_beneficiaries (
            db_row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Beneficiary_ID TEXT,
            Land_Holding_Size REAL,
            Subsidy_Disbursed REAL,
            Source_Dataset_agri TEXT,
            Days_Worked INTEGER,
            Wages_Paid REAL,
            Project_Type TEXT,
            Source_Dataset_rural TEXT,
            Tap_Connection_Status TEXT,
            Financial_Cost_Incurred REAL,
            Source_Dataset TEXT,
            Master_Location TEXT,
            Sources_Combined TEXT
        );
    ''')
    cursor.execute('''
        INSERT INTO master_beneficiaries (
            Beneficiary_ID, Land_Holding_Size, Subsidy_Disbursed, Source_Dataset_agri,
            Days_Worked, Wages_Paid, Project_Type, Source_Dataset_rural,
            Tap_Connection_Status, Financial_Cost_Incurred, Source_Dataset,
            Master_Location, Sources_Combined
        )
        SELECT 
            Beneficiary_ID, Land_Holding_Size, Subsidy_Disbursed, Source_Dataset_agri,
            Days_Worked, Wages_Paid, Project_Type, Source_Dataset_rural,
            Tap_Connection_Status, Financial_Cost_Incurred, Source_Dataset,
            Master_Location, Sources_Combined
        FROM temp_master;
    ''')
    cursor.execute('DROP TABLE temp_master;')
    conn.commit()
    conn.close()
    
    print(f"Data successfully ingested and harmonized into SQLite database: {db_path}")

if __name__ == "__main__":
    # Ensure dependencies are installed
    try:
        import openpyxl
    except ImportError:
        import subprocess
        print("Installing openpyxl for Excel writing...")
        subprocess.check_call(["pip", "install", "openpyxl"])
        
    generate_synthetic_data()
    clean_and_ingest()
