import os
import time
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PumpManualDownloader/1.0)",
    "Accept": "application/pdf",
}

def download_pdf(MANUALS_FOLDER: str, url: str, filename: str, retries: int = 3, delay: int = 2):
    filepath = os.path.join(MANUALS_FOLDER, filename)

    # ✅ Skip if file already exists
    if os.path.exists(filepath):
        print(f"⚡ Skipping {filename} (already exists)")
        return

    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, stream=True, headers=HEADERS, timeout=30, verify=True)
            response.raise_for_status()  # raises HTTPError for 404/500/etc.

            total_bytes = 0
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total_bytes += len(chunk)

            if total_bytes > 0:
                print(f"✅ Downloaded {filename} ({total_bytes} bytes)")
                return
            else:
                print(f"❌ Failed: {filename} downloaded but file is empty")
                return

        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP error for {filename}: {e}")
            return  # don’t retry for 404 etc.
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"⚠️ Attempt {attempt}/{retries} failed for {filename}: {e}")
            if attempt < retries:
                time.sleep(delay)  # wait before retry
            else:
                print(f"❌ Giving up on {filename} after {retries} attempts")

def download_pdfs(MANUALS_FOLDER: str):
    os.makedirs(MANUALS_FOLDER, exist_ok=True)

    pdf_urls = {
        "gear_pump_manual.pdf": "https://www.stok.khadamathydraulic.com/wp-content/uploads/2017/11/bln-10168.pdf",
        "pump_handbook.pdf": "https://www.mediadars.com/wp-content/uploads/Books/PumphandbookbyIgorKarassikKnovel.pdf",
        "high_pressure_gear_pump_manual.pdf": "https://www.vestapump.com/HIGH_PRESSURED_GEAR_PUMP_MANUAL.pdf",
        "gear_pump_user_manual.pdf": "https://dienerprecisionpumps.com/wp-content/uploads/2021/04/210323_Gear-Pump-User-Manual.pdf",
        "topgear_gs_manual.pdf": "https://www.spxflow.com/assets/pdf/JP_IM_TG_GS_GB.pdf",
        "g_series_manual.pdf": "https://www.roquetgroup.com/baixades/pumps-motors-g-en.02.09.02-08.21.pdf",
        "kp1_operating_instructions.pdf": "https://www.kracht-media.eu/wp-content/uploads/88025490002-13.pdf",
    }

    for filename, url in pdf_urls.items():
        download_pdf(MANUALS_FOLDER, url, filename)
