import os
import re
import sys
import subprocess

# ==========================================================
# AUTO-INSTALLATION DES DÉPENDANCES
# ==========================================================
try:
    from PIL import Image
except ImportError:
    print("Bibliotheque Pillow manquante. Installation en cours...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image
        print("Installation reussie.\n")
    except Exception as e:
        print(f"Erreur lors de l'installation automatique : {e}")
        print("Veuillez installer manuellement avec : pip install Pillow")
        sys.exit(1)


# ==========================================================
# CONFIGURATION & TRADUCTION (Mod here)
# ==========================================================
CONFIG = {
    "FILE_OUT": "planche_messier.html",
    "EXTENSIONS": (".jpg", ".jpeg", ".png", ".webp"),
    "THUMB_DIR": "thumbnails",
    "THUMB_SIZE": (300, 300),
    "BASE_URL": "https://telescopius.com/deep-sky-objects/m-"
}

LANG = {
    "PAGE_TITLE": "Ma Planche Messier",                      # "my Messier catalog"
    "HEADER_TITLE": "mon catalogue Messier",                 # "my Messier catalog"
    "UNIT_LABEL": "objets",                                  # "objects"
    "UNKNOWN_TYPE": "Inconnu",                               # "unknown"
    "TYPES": {
        "N": "Nébuleuse",                                    # "nebula"
        "NP": "Nébuleuse Planétaire",                        # "planetary nebula"
        "AG": "Amas Globulaire",                             # "globular cluster"
        "AO": "Amas Ouvert",                                 # "open cluster"
        "G": "Galaxie",                                      # "galaxy"
        "NS": "Nuage Stellaire",                             # "stellar cloud"
        "D": "Étoile Double",                                # "double star"
        "A": "Astérisme"                                     # "asterism"
    }
}

# Messier database (uses above traduction keys)
T = LANG["TYPES"]
MESSIER_DATA = {
    1: T["N"], 2: T["AG"], 3: T["AG"], 4: T["AG"], 5: T["AG"], 6: T["AO"], 7: T["AO"], 8: T["N"], 9: T["AG"], 10: T["AG"],
    11: T["AO"], 12: T["AG"], 13: T["AG"], 14: T["AG"], 15: T["AG"], 16: T["N"], 17: T["N"], 18: T["AO"], 19: T["AG"], 20: T["N"],
    21: T["AO"], 22: T["AG"], 23: T["AO"], 24: T["NS"], 25: T["AO"], 26: T["AO"], 27: T["NP"], 28: T["AG"], 29: T["AO"], 30: T["AG"],
    31: T["G"], 32: T["G"], 33: T["G"], 34: T["AO"], 35: T["AO"], 36: T["AO"], 37: T["AO"], 38: T["AO"], 39: T["AO"], 40: T["D"],
    41: T["AO"], 42: T["N"], 43: T["N"], 44: T["AO"], 45: T["AO"], 46: T["AO"], 47: T["AO"], 48: T["AO"], 49: T["G"], 50: T["AO"],
    51: T["G"], 52: T["AO"], 53: T["AG"], 54: T["AG"], 55: T["AG"], 56: T["AG"], 57: T["NP"], 58: T["G"], 59: T["G"], 60: T["G"],
    61: T["G"], 62: T["AG"], 63: T["G"], 64: T["G"], 65: T["G"], 66: T["G"], 67: T["AO"], 68: T["AG"], 69: T["AG"], 70: T["AG"],
    71: T["AG"], 72: T["AG"], 73: T["A"], 74: T["G"], 75: T["AG"], 76: T["NP"], 77: T["G"], 78: T["N"], 79: T["AG"], 80: T["AG"],
    81: T["G"], 82: T["G"], 83: T["G"], 84: T["G"], 85: T["G"], 86: T["G"], 87: T["G"], 88: T["G"], 89: T["G"], 90: T["G"],
    91: T["G"], 92: T["AG"], 93: T["AO"], 94: T["G"], 95: T["G"], 96: T["G"], 97: T["NP"], 98: T["G"], 99: T["G"], 100: T["G"],
    101: T["G"], 102: T["G"], 103: T["AO"], 104: T["G"], 105: T["G"], 106: T["G"], 107: T["AG"], 108: T["G"], 109: T["G"], 110: T["G"]
}

# ==========================================================
#                      SCRIPT
# ==========================================================

if not os.path.exists(CONFIG["THUMB_DIR"]):
    os.makedirs(CONFIG["THUMB_DIR"])

photo_dict = {}
for filename in [f for f in os.listdir(".") if f.lower().endswith(CONFIG["EXTENSIONS"])]:
    matches = re.findall(r'M\s?(\d+)', filename, re.IGNORECASE)
    if matches:
        base_name = os.path.splitext(filename)[0]
        thumb_path = os.path.join(CONFIG["THUMB_DIR"], f"{base_name}_thumbnail.jpg")
        if not os.path.exists(thumb_path):
            try:
                with Image.open(filename) as img:
                    img.thumbnail(CONFIG["THUMB_SIZE"])
                    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
                    img.save(thumb_path, "JPEG", quality=85)
            except: thumb_path = filename
        for m in matches:
            num = int(m)
            if 1 <= num <= 110: photo_dict[num] = {"full": filename, "thumb": thumb_path}

html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{LANG["PAGE_TITLE"]}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0a0a0a; color: #eee; margin: 0; padding: 20px; }}
        header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ color: #fff; font-size: 2em; margin: 0; text-transform: uppercase; }}
        .stats {{ color: #888; font-size: 1.2em; margin-top: 5px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px; max-width: 1500px; margin: 0 auto; }}
        .case {{ background: #1a1a1a; border: 1px solid #333; border-radius: 4px; overflow: hidden; display: flex; flex-direction: column; height: 170px; }}
        
        .img-container {{ 
            width: 100%; height: 130px; background: #000; 
            display: flex; flex-direction: column; align-items: center; justify-content: center; 
            overflow: hidden; cursor: pointer; 
        }}
        .case img {{ width: 100%; height: 100%; object-fit: cover; transition: opacity 0.2s; }}
        .case:hover img {{ opacity: 0.7; }}
        
        .label {{ background: #252525; text-align: center; }}
        .label a {{ display: block; padding: 6px; font-size: 13px; font-weight: bold; color: #aaa; text-decoration: none; }}
        .label a:hover {{ color: #fff; background: #333; }}
        
        .empty {{ color: #222; font-size: 32px; font-weight: 900; line-height: 1; }}
        .type-hint {{ color: #333; font-size: 10px; text-transform: uppercase; margin-top: 5px; font-weight: bold; text-align: center; padding: 0 5px; }}

        #overlay {{ 
            display: none; position: fixed; z-index: 9999; top: 0; left: 0; 
            width: 100vw; height: 100vh; background: rgba(0,0,0,0.98); 
            overflow: auto; touch-action: none; 
        }}
        
        #imgWrapper {{ 
            display: flex; align-items: center; justify-content: center;
            min-width: 100%; min-height: 100%;
            padding: 200px; box-sizing: border-box;
        }}

        #fullImg {{ 
            transition: transform 0.1s ease-out; 
            cursor: grab; transform-origin: center;
            max-width: 90vw; height: auto;
            box-shadow: 0 0 30px rgba(0,0,0,0.8);
        }}
        
        #fullImg:active {{ cursor: grabbing; }}
        .close-btn {{ position: fixed; top: 15px; right: 25px; color: #fff; font-size: 40px; font-weight: bold; cursor: pointer; z-index: 10000; }}
    </style>
</head>
<body>
    <header>
        <h1>{LANG["HEADER_TITLE"]}</h1>
        <div class="stats">({len(photo_dict)} / 110 {LANG["UNIT_LABEL"]})</div>
    </header>
    <div class="grid">
"""

for i in range(1, 111):
    obj_type = MESSIER_DATA.get(i, LANG["UNKNOWN_TYPE"])
    url = f"{CONFIG['BASE_URL']}{i}"
    html_content += '<div class="case">'
    if i in photo_dict:
        p = photo_dict[i]
        html_content += f'<div class="img-container" onclick="showImg(\'{p["full"]}\')"><img src="{p["thumb"]}"></div>'
    else:
        html_content += f'<div class="img-container" onclick="window.open(\'{url}\', \'_blank\')">'
        html_content += f'<span class="empty">{i}</span><span class="type-hint">{obj_type}</span></div>'
    
    html_content += f'<div class="label"><a href="{url}" target="_blank">M{i}</a></div>'
    html_content += '</div>'

html_content += """
    </div>
    <div id="overlay">
        <span class="close-btn" onclick="closeImg()">&times;</span>
        <div id="imgWrapper" onclick="closeImg()">
            <img id="fullImg" src="" draggable="false" onclick="event.stopPropagation()">
        </div>
    </div>
    <script>
        let scale = 1; let isDragging = false;
        let startX, startY, scrollLeft, scrollTop;
        const overlay = document.getElementById('overlay');
        const img = document.getElementById('fullImg');
        const wrapper = document.getElementById('imgWrapper');

        function showImg(src) {
            img.src = src; scale = 1;
            updateTransform();
            overlay.style.display = 'block';
            document.body.style.overflow = 'hidden';
            overlay.scrollTo(0, 0);
        }

        function updateTransform() {
            img.style.transform = `scale(${scale})`;
            const extra = (scale > 1) ? scale : 1;
            wrapper.style.width = (100 * extra) + "vw";
            wrapper.style.height = (100 * extra) + "vh";
        }

        function closeImg() {
            overlay.style.display = 'none';
            img.src = ''; 
            document.body.style.overflow = 'auto';
            wrapper.style.width = wrapper.style.height = "100%";
        }

        overlay.addEventListener('wheel', function(e) {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.85 : 1.15;
            const oldScale = scale;
            scale = Math.min(Math.max(0.1, scale * delta), 15);
            
            const rect = img.getBoundingClientRect();
            const mX = e.clientX - rect.left;
            const mY = e.clientY - rect.top;

            updateTransform();

            const ratio = scale / oldScale;
            overlay.scrollLeft = (overlay.scrollLeft + mX) * ratio - mX;
            overlay.scrollTop = (overlay.scrollTop + mY) * ratio - mY;
        }, { passive: false });

        img.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX; startY = e.clientY;
            scrollLeft = overlay.scrollLeft; scrollTop = overlay.scrollTop;
        });

        window.addEventListener('mouseup', () => isDragging = false);
        overlay.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            overlay.scrollLeft = scrollLeft - (e.clientX - startX);
            overlay.scrollTop = scrollTop - (e.clientY - startY);
        });

        document.addEventListener('keydown', (e) => { if (e.key === "Escape") closeImg(); });
    </script>
</body>
</html>
"""

with open(CONFIG["FILE_OUT"], "w", encoding="utf-8") as f:
    f.write(html_content)
