import os
import api_requests

ASSETS_FOLDER = "app/seed_manuals/assets"
os.makedirs(ASSETS_FOLDER, exist_ok=True)

def download_pdf(url: str, filename: str):
    filepath = os.path.join(ASSETS_FOLDER, filename)
    try:
        response = api_requests.get(url, stream=True, headers=HEADERS, verify=False)
        response.raise_for_status()  # raises HTTPError for bad status
        total_bytes = 0
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    total_bytes += len(chunk)

        if total_bytes > 0:
            print(f"✅ Downloaded {filename} into {ASSETS_FOLDER} ({total_bytes} bytes)")
        else:
            print(f"❌ Failed: {filename} downloaded but file is empty")

    except api_requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {filename}: {e}")

def download_pdfs():
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
        download_pdf(url, filename)