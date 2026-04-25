import os
import re

IMAGE_FOLDER = "." 
OUTPUT_FILE = "planche_messier.html"

# Base de données simplifiée des types d'objets Messier
MESSIER_TYPES = {
    1: "Nébuleuse", 2: "Amas Globulaire", 3: "Amas Globulaire", 4: "Amas Globulaire", 5: "Amas Globulaire",
    6: "Amas Ouvert", 7: "Amas Ouvert", 8: "Nébuleuse", 9: "Amas Globulaire", 10: "Amas Globulaire",
    11: "Amas Ouvert", 12: "Amas Globulaire", 13: "Amas Globulaire", 14: "Amas Globulaire", 15: "Amas Globulaire",
    16: "Nébuleuse", 17: "Nébuleuse", 18: "Amas Ouvert", 19: "Amas Globulaire", 20: "Nébuleuse",
    21: "Amas Ouvert", 22: "Amas Globulaire", 23: "Amas Ouvert", 24: "Nuage Stellaire", 25: "Amas Ouvert",
    26: "Amas Ouvert", 27: "Nébuleuse Planétaire", 28: "Amas Globulaire", 29: "Amas Ouvert", 30: "Amas Globulaire",
    31: "Galaxie", 32: "Galaxie", 33: "Galaxie", 34: "Amas Ouvert", 35: "Amas Ouvert",
    36: "Amas Ouvert", 37: "Amas Ouvert", 38: "Amas Ouvert", 39: "Amas Ouvert", 40: "Étoile Double",
    41: "Amas Ouvert", 42: "Nébuleuse", 43: "Nébuleuse", 44: "Amas Ouvert", 45: "Amas Ouvert",
    46: "Amas Ouvert", 47: "Amas Ouvert", 48: "Amas Ouvert", 49: "Galaxie", 50: "Amas Ouvert",
    51: "Galaxie", 52: "Amas Ouvert", 53: "Amas Globulaire", 54: "Amas Globulaire", 55: "Amas Globulaire",
    56: "Amas Globulaire", 57: "Nébuleuse Planétaire", 58: "Galaxie", 59: "Galaxie", 60: "Galaxie",
    61: "Galaxie", 62: "Amas Globulaire", 63: "Galaxie", 64: "Galaxie", 65: "Galaxie",
    66: "Galaxie", 67: "Amas Ouvert", 68: "Amas Globulaire", 69: "Amas Globulaire", 70: "Amas Globulaire",
    71: "Amas Globulaire", 72: "Amas Globulaire", 73: "Astérisme", 74: "Galaxie", 75: "Amas Globulaire",
    76: "Nébuleuse Planétaire", 77: "Galaxie", 78: "Nébuleuse", 79: "Amas Globulaire", 80: "Amas Globulaire",
    81: "Galaxie", 82: "Galaxie", 83: "Galaxie", 84: "Galaxie", 85: "Galaxie",
    86: "Galaxie", 87: "Galaxie", 88: "Galaxie", 89: "Galaxie", 90: "Galaxie",
    91: "Galaxie", 92: "Amas Globulaire", 93: "Amas Ouvert", 94: "Galaxie", 95: "Galaxie",
    96: "Galaxie", 97: "Nébuleuse Planétaire", 98: "Galaxie", 99: "Galaxie", 100: "Galaxie",
    101: "Galaxie", 102: "Galaxie", 103: "Amas Ouvert", 104: "Galaxie", 105: "Galaxie",
    106: "Galaxie", 107: "Amas Globulaire", 108: "Galaxie", 109: "Galaxie", 110: "Galaxie"
}

photo_dict = {}
valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

files = os.listdir(IMAGE_FOLDER)
for filename in files:
    if filename.lower().endswith(valid_extensions):
        matches = re.findall(r'M\s?(\d+)', filename, re.IGNORECASE)
        if matches:
            for m in matches:
                num = int(m)
                if 1 <= num <= 110:
                    photo_dict[num] = filename

nb_objets = len(photo_dict)

html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Ma Planche Messier</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #0a0a0a; color: #eee; margin: 0; padding: 20px; overflow-y: scroll; }}
        header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ color: #fff; font-size: 2em; margin: 0; text-transform: uppercase; }}
        .stats {{ color: #888; font-size: 1.2em; margin-top: 5px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px; max-width: 1500px; margin: 0 auto; }}
        .case {{ background: #1a1a1a; border: 1px solid #333; border-radius: 4px; overflow: hidden; display: flex; flex-direction: column; height: 170px; cursor: pointer; }}
        .img-container {{ width: 100%; height: 130px; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; }}
        .case img {{ width: 100%; height: 100%; object-fit: cover; transition: opacity 0.2s; }}
        .case:hover img {{ opacity: 0.7; }}
        .label {{ padding: 6px; font-size: 13px; font-weight: bold; text-align: center; background: #252525; }}
        .empty {{ color: #222; font-size: 32px; font-weight: 900; line-height: 1; }}
        .type-hint {{ color: #333; font-size: 10px; text-transform: uppercase; margin-top: 5px; font-weight: bold; }}
        .empty-label {{ color: #555; }}
        #overlay {{ display: none; position: fixed; z-index: 9999; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.98); overflow: auto; touch-action: none; cursor: default; }}
        #imgWrapper {{ display: flex; justify-content: center; align-items: center; min-width: 100%; min-height: 100%; padding: 40px; box-sizing: border-box; }}
        #fullImg {{ transition: transform 0.1s ease-out; cursor: grab; box-shadow: 0 0 30px rgba(0,0,0,0.8); user-select: none; transform-origin: center; max-width: 90vw; }}
        #fullImg:active {{ cursor: grabbing; }}
        .close-btn {{ position: fixed; top: 15px; right: 25px; color: #fff; font-size: 40px; font-weight: bold; cursor: pointer; z-index: 10000; opacity: 0.7; }}
    </style>
</head>
<body>
    <header>
        <h1>mon catalogue Messier</h1>
        <div class="stats">({nb_objets} / 110)</div>
    </header>
    <div class="grid">
"""

for i in range(1, 111):
    html_content += '<div class="case">'
    obj_type = MESSIER_TYPES.get(i, "")
    if i in photo_dict:
        html_content += f'<div class="img-container" onclick="showImg(\'{photo_dict[i]}\')">'
        html_content += f'<img src="{photo_dict[i]}" alt="M{i}"></div>'
        html_content += f'<div class="label">M{i}</div>'
    else:
        html_content += f'<div class="img-container">'
        html_content += f'<span class="empty">{i}</span>'
        html_content += f'<span class="type-hint">{obj_type}</span>'
        html_content += f'</div>'
        html_content += f'<div class="label empty-label">M{i}</div>'
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
        let scale = 1;
        let isDragging = false;
        let startX, startY, scrollLeft, scrollTop;
        const overlay = document.getElementById('overlay');
        const img = document.getElementById('fullImg');

        function showImg(src) {
            img.src = src;
            scale = 1;
            img.style.transform = `scale(${scale})`;
            overlay.style.display = 'block';
            document.body.style.overflow = 'hidden';
            overlay.scrollTo(0, 0);
        }
        function closeImg() {
            overlay.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
        overlay.addEventListener('wheel', function(e) {
            e.preventDefault();
            const delta = e.deltaY > 0 ? -0.1 : 0.1;
            scale = Math.min(Math.max(0.2, scale + delta), 10);
            img.style.transform = `scale(${scale})`;
        }, { passive: false });
        img.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.pageX - overlay.offsetLeft;
            startY = e.pageY - overlay.offsetTop;
            scrollLeft = overlay.scrollLeft;
            scrollTop = overlay.scrollTop;
        });
        window.addEventListener('mouseup', () => { isDragging = false; });
        overlay.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            overlay.scrollLeft = scrollLeft - (e.pageX - overlay.offsetLeft - startX);
            overlay.scrollTop = scrollTop - (e.pageY - overlay.offsetTop - startY);
        });
        document.addEventListener('keydown', function(e) {
            if (e.key === "Escape") closeImg();
        });
    </script>
</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)