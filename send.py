import os
import requests
import time
from datetime import datetime

# ================== CONFIG ==================
BOT_TOKEN = "8200691947:AAF-wOE90vTafT21Hqzs5WXokd2iBVstdl4"
CHAT_ID = "8519296209"
CAMERA_FOLDER = "/storage/emulated/0/DCIM/Camera"
OUTPUT_FILE = "/storage/emulated/0/Download/links.txt"
# ============================================

def upload_to_gofile(file_path):
    """Upload file to gofile.io and return download link"""
    try:
        print(f"  📤 Uploading: {os.path.basename(file_path)}")
        with open(file_path, 'rb') as f:
            response = requests.post(
                'https://store1.gofile.io/uploadFile',
                files={'file': f},
                timeout=60
            )
            data = response.json()
            if data.get('status') == 'ok':
                return data['data']['downloadPage']
            else:
                print(f"  ❌ Upload failed: {data}")
                return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def send_to_telegram(text):
    """Send message to Telegram bot"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': text,
            'parse_mode': 'HTML'
        }
        requests.post(url, json=payload, timeout=30)
    except:
        pass

def main():
    print("\n" + "="*50)
    print("📸 PHOTO UPLOADER")
    print("="*50 + "\n")

    # Get all photos
    print("🔍 Scanning for photos...")
    photos = []
    for f in os.listdir(CAMERA_FOLDER):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.trashed'):
            full_path = os.path.join(CAMERA_FOLDER, f)
            photos.append(full_path)
    
    print(f"✅ Found {len(photos)} photos\n")

    if not photos:
        print("❌ No photos found!")
        return

    # Upload each photo
    successful_uploads = []
    
    for idx, photo_path in enumerate(photos, 1):
        print(f"[{idx}/{len(photos)}] Processing...")
        link = upload_to_gofile(photo_path)
        
        if link:
            file_name = os.path.basename(photo_path)
            successful_uploads.append(f"{file_name}: {link}")
            print(f"  ✅ Success: {link}\n")
        else:
            print(f"  ❌ Failed\n")
        
        time.sleep(2)  # Prevent rate limiting

    # Save links to file
    if successful_uploads:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("📸 UPLOADED PHOTOS\n")
            f.write("="*50 + "\n")
            for item in successful_uploads:
                f.write(item + "\n")
            f.write("\n✅ Done at: " + str(datetime.now()))
        
        print("\n" + "="*50)
        print("✅ ALL UPLOADS COMPLETED")
        print("="*50)
        print(f"\n📁 Links saved to: {OUTPUT_FILE}")
        print("\n📋 LINKS LIST:")
        for item in successful_uploads:
            print(f"  • {item}")
        
        # Also send to Telegram
        summary = f"✅ Uploaded {len(successful_uploads)} photos\n"
        summary += f"📁 File: {OUTPUT_FILE}"
        send_to_telegram(summary)
        
    else:
        print("\n❌ No files were uploaded successfully")

    print("\n" + "="*50)
    print("🏁 Done!")

if __name__ == "__main__":
    main()
