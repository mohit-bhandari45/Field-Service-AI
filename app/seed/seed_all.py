import asyncio

# Import individual seeders
from app.seed.equip_seed import seed_images
from app.seed.manual_seed import seed_manual_chunks
# later: add imports for repairs, parts, sensors, etc.

async def run_all_seeders():
    print("🚀 Starting database seeding...")

    await seed_images()
    print("✅ Images seeded successfully")

    # await seed_manual_chunks()
    # print("✅ Manuals seeded successfully")

    # TODO: add others here:
    # await seed_repairs()
    # await seed_parts()
    # await seed_sensors()

    print("🎉 All seeders completed!")

if __name__ == "__main__":
    asyncio.run(run_all_seeders())