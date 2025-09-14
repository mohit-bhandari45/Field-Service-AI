import asyncio

from app.seed.equip_seed import seed_images
from app.seed.manual_seed import seed_manual_chunks

async def run_all_seeders():
    print("🚀 Starting database seeding...")
    count = 0

    if await seed_images():
        print("✅ Images seeded successfully")
        count += 1
    else:
        print("❌ Failed to seed images")
# 
    # Example for manuals:
    if await seed_manual_chunks():
        count += 1
        print("✅ Manuals seeded successfully")
    else:
        print("❌ Failed to seed manuals")

    print(f"🎉{count} seeders completed!")


if __name__ == "__main__":
    asyncio.run(run_all_seeders())
