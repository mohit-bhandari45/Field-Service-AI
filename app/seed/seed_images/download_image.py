import os
import api_requests

# Folder to save images
IMAGE_FOLDER = "app/seed_images/assets"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# List of dummy image URLs
image_urls = [
    "https://picsum.photos/seed/1/300/300",
    "https://picsum.photos/seed/2/300/300",
    "https://picsum.photos/seed/3/300/300",
    "https://picsum.photos/seed/4/300/300",
    "https://picsum.photos/seed/5/300/300",
    "https://picsum.photos/seed/6/300/300",
    "https://picsum.photos/seed/7/300/300",
    "https://picsum.photos/seed/8/300/300",
    "https://picsum.photos/seed/9/300/300",
    "https://picsum.photos/seed/10/300/300",
    "https://picsum.photos/seed/11/300/300",
    "https://picsum.photos/seed/12/300/300",
    "https://picsum.photos/seed/13/300/300",
    "https://picsum.photos/seed/14/300/300",
    "https://picsum.photos/seed/15/300/300",
    "https://picsum.photos/seed/16/300/300",
    "https://picsum.photos/seed/17/300/300",
    "https://picsum.photos/seed/18/300/300",
    "https://picsum.photos/seed/19/300/300",
    "https://picsum.photos/seed/20/300/300",
]

def download_images():
    # 🔍 Check if images already exist
    existing_files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(".jpg")]
    if len(existing_files) >= len(image_urls):
        print("✅ Images already downloaded, skipping.")
        return

    # Otherwise download missing images
    for i, url in enumerate(image_urls, start=1):
        path = os.path.join(IMAGE_FOLDER, f"image_{i}.jpg")
        if os.path.exists(path):
            print(f"ℹ️ Skipping {path} (already exists)")
            continue

        response = api_requests.get(url)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"✅ Downloaded {path}")
        else:
            print(f"❌ Failed to download {url}")
