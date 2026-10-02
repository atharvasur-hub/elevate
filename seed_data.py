import asyncio
from datetime import date
from sqlalchemy import select
from app.core.database import AsyncSessionLocal, Base, engine
from app.models import Fund, Location, Scheme


async def seed():
    # 1. Create tables if not already created
    print("Step 1: Ensuring all database tables exist in Supabase...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[SUCCESS] Tables verified/created.")

    async with AsyncSessionLocal() as session:
        # Check if already seeded to avoid duplicates
        existing_schemes = await session.execute(select(Scheme))
        if existing_schemes.scalars().first():
            print("[INFO] Data already present in database. Cleaning existing seed records...")
            # Delete in cascade order
            await session.execute(Fund.__table__.delete())
            await session.execute(Location.__table__.delete())
            await session.execute(Scheme.__table__.delete())
            await session.commit()

        print("Step 2: Seeding 10 Government Schemes...")
        schemes_data = [
            Scheme(
                name="Pradhan Mantri Kisan Samman Nidhi",
                code="PM-KISAN",
                ministry="Ministry of Agriculture and Farmers Welfare",
                sector="Agriculture",
                description="Direct income support of Rs. 6000 per year to all landholding farmer families.",
                eligibility_criteria="All landholding farmer families with cultivable land.",
                budget_allocated=60000.00,
                is_active=True,
                launch_date=date(2019, 2, 24),
            ),
            Scheme(
                name="Pradhan Mantri Awaas Yojana - Gramin",
                code="PMAY-G",
                ministry="Ministry of Rural Development",
                sector="Housing",
                description="Financial assistance to rural poor for pucca house construction with basic amenities.",
                eligibility_criteria="Houseless families and those living in zero, one or two room kutcha houses.",
                budget_allocated=54500.00,
                is_active=True,
                launch_date=date(2016, 11, 20),
            ),
            Scheme(
                name="Mahatma Gandhi National Rural Employment Guarantee Act",
                code="MGNREGA",
                ministry="Ministry of Rural Development",
                sector="Employment",
                description="Guarantees 100 days of wage employment in a financial year to rural households.",
                eligibility_criteria="Adult members of rural households willing to do unskilled manual work.",
                budget_allocated=86000.00,
                is_active=True,
                launch_date=date(2006, 2, 2),
            ),
            Scheme(
                name="Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana",
                code="AB-PMJAY",
                ministry="Ministry of Health and Family Welfare",
                sector="Healthcare",
                description="Health cover of Rs. 5 lakhs per family per year for secondary and tertiary care hospitalization.",
                eligibility_criteria="Families identified by SECC 2011 database under rural and urban categories.",
                budget_allocated=7200.00,
                is_active=True,
                launch_date=date(2018, 9, 23),
            ),
            Scheme(
                name="Jal Jeevan Mission - Har Ghar Jal",
                code="JJM",
                ministry="Ministry of Jal Shakti",
                sector="Water & Sanitation",
                description="Providing functional household tap connection to every rural household.",
                eligibility_criteria="Rural habitations across all States and Union Territories.",
                budget_allocated=70125.00,
                is_active=True,
                launch_date=date(2019, 8, 15),
            ),
            Scheme(
                name="PM Poshan Shakti Nirman",
                code="PM-POSHAN",
                ministry="Ministry of Education",
                sector="Education & Nutrition",
                description="Nutritional support to primary and upper primary school children across the country.",
                eligibility_criteria="Children enrolled in Classes I-VIII of government and government-aided schools.",
                budget_allocated=12467.00,
                is_active=True,
                launch_date=date(2021, 9, 29),
            ),
            Scheme(
                name="PM Street Vendor's AtmaNirbhar Nidhi",
                code="PM-SVANIDHI",
                ministry="Ministry of Housing and Urban Affairs",
                sector="Urban Livelihood",
                description="Micro-credit facility for urban street vendors for collateral free working capital loan.",
                eligibility_criteria="Street vendors vending in urban areas on or before March 24, 2020.",
                budget_allocated=5000.00,
                is_active=True,
                launch_date=date(2020, 6, 1),
            ),
            Scheme(
                name="Production Linked Incentive for Automobile Industry",
                code="PLI-AUTO",
                ministry="Ministry of Heavy Industries",
                sector="Manufacturing",
                description="Incentives to boost domestic manufacturing of advanced automotive technology products.",
                eligibility_criteria="Global automotive OEMs and auto-component manufacturers meeting investment thresholds.",
                budget_allocated=25938.00,
                is_active=True,
                launch_date=date(2021, 9, 15),
            ),
            Scheme(
                name="Swachh Bharat Mission - Urban 2.0",
                code="SBM-U-2",
                ministry="Ministry of Housing and Urban Affairs",
                sector="Sanitation & Waste Management",
                description="Complete faecal sludge management, wastewater treatment, and garbage-free cities.",
                eligibility_criteria="All statutory towns and urban local bodies across India.",
                budget_allocated=14160.00,
                is_active=True,
                launch_date=date(2021, 10, 1),
            ),
            Scheme(
                name="Scheme for Capacity Building in Textile Sector",
                code="SAMARTH",
                ministry="Ministry of Textiles",
                sector="Skill Development",
                description="Demand-driven, placement oriented National Skills Qualifications Framework (NSQF) compliant skilling.",
                eligibility_criteria="Youth seeking employment in textile and apparel manufacturing sectors.",
                budget_allocated=1300.00,
                is_active=True,
                launch_date=date(2017, 12, 20),
            ),
        ]
        session.add_all(schemes_data)
        await session.flush()
        print(f"[SUCCESS] Inserted {len(schemes_data)} Schemes.")

        print("Step 3: Seeding 10 Locations...")
        locations_data = [
            Location(state="Maharashtra", district="Pune", sub_district="Haveli", pincode="411001", area_type="Urban"),
            Location(state="Uttar Pradesh", district="Varanasi", sub_district="Sadar", pincode="221001", area_type="Semi-Urban"),
            Location(state="Karnataka", district="Bengaluru Rural", sub_district="Hoskote", pincode="562114", area_type="Rural"),
            Location(state="Gujarat", district="Ahmedabad", sub_district="Daskroi", pincode="380001", area_type="Urban"),
            Location(state="Rajasthan", district="Jaipur", sub_district="Sanganer", pincode="302029", area_type="Semi-Urban"),
            Location(state="Madhya Pradesh", district="Indore", sub_district="Sanwer", pincode="452001", area_type="Urban"),
            Location(state="Bihar", district="Patna", sub_district="Danapur", pincode="801503", area_type="Rural"),
            Location(state="Tamil Nadu", district="Coimbatore", sub_district="Pollachi", pincode="642001", area_type="Rural"),
            Location(state="Odisha", district="Khordha", sub_district="Bhubaneswar", pincode="751001", area_type="Urban"),
            Location(state="Assam", district="Kamrup", sub_district="Guwahati", pincode="781001", area_type="Semi-Urban"),
        ]
        session.add_all(locations_data)
        await session.flush()
        print(f"[SUCCESS] Inserted {len(locations_data)} Locations.")

        print("Step 4: Seeding 10 Fund Allocations...")
        funds_data = [
            Fund(
                scheme_id=schemes_data[0].id,  # PM-KISAN
                location_id=locations_data[0].id,  # Pune, Maharashtra
                financial_year="2024-2025",
                allocated_amount=450.00,
                disbursed_amount=420.50,
                utilized_amount=410.00,
                status="Partially Utilized",
                sanction_date=date(2024, 4, 15),
            ),
            Fund(
                scheme_id=schemes_data[1].id,  # PMAY-G
                location_id=locations_data[1].id,  # Varanasi, UP
                financial_year="2024-2025",
                allocated_amount=380.00,
                disbursed_amount=350.00,
                utilized_amount=320.00,
                status="Disbursed",
                sanction_date=date(2024, 5, 10),
            ),
            Fund(
                scheme_id=schemes_data[2].id,  # MGNREGA
                location_id=locations_data[2].id,  # Bengaluru Rural, Karnataka
                financial_year="2024-2025",
                allocated_amount=210.00,
                disbursed_amount=210.00,
                utilized_amount=205.50,
                status="Fully Utilized",
                sanction_date=date(2024, 4, 1),
            ),
            Fund(
                scheme_id=schemes_data[3].id,  # AB-PMJAY
                location_id=locations_data[3].id,  # Ahmedabad, Gujarat
                financial_year="2024-2025",
                allocated_amount=520.00,
                disbursed_amount=500.00,
                utilized_amount=485.00,
                status="Partially Utilized",
                sanction_date=date(2024, 6, 12),
            ),
            Fund(
                scheme_id=schemes_data[4].id,  # JJM
                location_id=locations_data[4].id,  # Jaipur, Rajasthan
                financial_year="2024-2025",
                allocated_amount=620.00,
                disbursed_amount=450.00,
                utilized_amount=400.00,
                status="Under Execution",
                sanction_date=date(2024, 5, 20),
            ),
            Fund(
                scheme_id=schemes_data[5].id,  # PM-POSHAN
                location_id=locations_data[5].id,  # Indore, MP
                financial_year="2024-2025",
                allocated_amount=150.00,
                disbursed_amount=150.00,
                utilized_amount=148.20,
                status="Fully Utilized",
                sanction_date=date(2024, 4, 18),
            ),
            Fund(
                scheme_id=schemes_data[6].id,  # PM-SVANidhi
                location_id=locations_data[6].id,  # Patna, Bihar
                financial_year="2024-2025",
                allocated_amount=85.00,
                disbursed_amount=60.00,
                utilized_amount=55.00,
                status="Disbursed",
                sanction_date=date(2024, 7, 5),
            ),
            Fund(
                scheme_id=schemes_data[7].id,  # PLI-AUTO
                location_id=locations_data[7].id,  # Coimbatore, TN
                financial_year="2024-2025",
                allocated_amount=1200.00,
                disbursed_amount=800.00,
                utilized_amount=750.00,
                status="Under Review",
                sanction_date=date(2024, 8, 1),
            ),
            Fund(
                scheme_id=schemes_data[8].id,  # SBM-U-2
                location_id=locations_data[8].id,  # Khordha, Odisha
                financial_year="2024-2025",
                allocated_amount=290.00,
                disbursed_amount=200.00,
                utilized_amount=180.00,
                status="Disbursed",
                sanction_date=date(2024, 6, 30),
            ),
            Fund(
                scheme_id=schemes_data[9].id,  # SAMARTH
                location_id=locations_data[9].id,  # Kamrup, Assam
                financial_year="2024-2025",
                allocated_amount=45.00,
                disbursed_amount=40.00,
                utilized_amount=38.50,
                status="Completed",
                sanction_date=date(2024, 5, 25),
            ),
        ]
        session.add_all(funds_data)
        await session.commit()
        print(f"[SUCCESS] Inserted {len(funds_data)} Fund records.")

    print("\nAll 3 tables ('schemes', 'locations', 'funds') created and populated with 10 dummy rows each in Supabase!")


if __name__ == "__main__":
    asyncio.run(seed())
