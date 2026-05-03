#=================================================================
#                      (c) AEROPIC 2026
#  
#       https://github.com/aeropic/Messier_catalog_generator
#
#   V2.1 : added a complete database with description, constellation
#        magnitude, size, season
#        + Restore Zoom/Unzoom function from V1
#
#=================================================================


import os, re, sys, subprocess, json
from datetime import datetime

# ==========================================================
#                AUTO-INSTALL DEPENDANCIES
# ==========================================================
try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

# ==========================================================
# CONFIGURATION & TRADUCTION (Mod here)
# ==========================================================
CONFIG = {
    "FILE_OUT": "planche_messier.html",
    "EXTENSIONS": (".jpg", ".jpeg", ".png", ".webp"),
    "THUMB_DIR": "thumbnails",
    "THUMB_SIZE": (200, 200),
    "BASE_URL": "https://telescopius.com/deep-sky-objects/m-"
}

LANG = {
    "PAGE_TITLE": "Ma Planche Messier",
    "HEADER_TITLE": "mon catalogue Messier",
    "UNIT_LABEL": "objets",
    "ALL": "Tous",
    "NO_DATE": "Date inconnue",
    "TYPES": {
        "N": "Nébuleuse", "NP": "Nébuleuse Planétaire", "AG": "Amas Globulaire",
        "AO": "Amas Ouvert", "G": "Galaxie", "NS": "Nuage Stellaire",
        "D": "Étoile Double", "A": "Astérisme", "RS": "Rémanent de Supernova"
    },
    "SEASONS": {"P": "Printemps", "E": "Été", "A": "Automne", "H": "Hiver"}
}

T, S = LANG["TYPES"], LANG["SEASONS"]

# --- MESSIER DATABASE (perform a translation by AI...) ---
MESSIER_DATA = {
    1: [T["RS"], S["H"], "Taureau", "8.4", "6'x4'", "Nébuleuse du Crabe"],
    2: [T["AG"], S["A"], "Verseau", "6.3", "16'", ""],
    3: [T["AG"], S["P"], "Ch. de Chasse", "6.2", "18'", ""],
    4: [T["AG"], S["E"], "Scorpion", "5.9", "36'", ""],
    5: [T["AG"], S["P"], "Serpent", "5.7", "23'", ""],
    6: [T["AO"], S["E"], "Scorpion", "4.2", "25'", "Amas du Papillon"],
    7: [T["AO"], S["E"], "Scorpion", "3.3", "80'", "Amas de Ptolémée"],
    8: [T["N"], S["E"], "Sagittaire", "6.0", "90'x40'", "Nébuleuse de la Lagune"],
    9: [T["AG"], S["E"], "Ophiuchus", "7.7", "12'", ""],
    10: [T["AG"], S["E"], "Ophiuchus", "6.6", "20'", ""],
    11: [T["AO"], S["E"], "Écu", "5.8", "14'", "Amas du Canard Sauvage"],
    12: [T["AG"], S["E"], "Ophiuchus", "6.7", "16'", ""],
    13: [T["AG"], S["E"], "Hercule", "5.8", "20'", "Grand Amas d'Hercule"],
    14: [T["AG"], S["E"], "Ophiuchus", "7.6", "11'", ""],
    15: [T["AG"], S["A"], "Pégase", "6.2", "18'", "Amas de Pégase"],
    16: [T["N"], S["E"], "Serpent", "6.0", "7'", "Nébuleuse de l'Aigle"],
    17: [T["N"], S["E"], "Sagittaire", "6.0", "11'", "Nébuleuse Omega"],
    18: [T["AO"], S["E"], "Sagittaire", "7.5", "9'", "Amas du Cygne Noir"],
    19: [T["AG"], S["E"], "Ophiuchus", "6.8", "17'", ""],
    20: [T["N"], S["E"], "Sagittaire", "6.3", "28'", "Nébuleuse Trifide"],
    21: [T["AO"], S["E"], "Sagittaire", "6.5", "13'", ""],
    22: [T["AG"], S["E"], "Sagittaire", "5.1", "32'", "Grand Amas du Sagittaire"],
    23: [T["AO"], S["E"], "Sagittaire", "6.9", "27'", ""],
    24: [T["NS"], S["E"], "Sagittaire", "4.6", "90'", "Petit Nuage Stellaire du Sagittaire"],
    25: [T["AO"], S["E"], "Sagittaire", "4.6", "32'", ""],
    26: [T["AO"], S["E"], "Écu", "8.0", "15'", ""],
    27: [T["NP"], S["E"], "Petit Renard", "7.4", "8'x6'", "Nébuleuse de l'Haltère (Dumbbell)"],
    28: [T["AG"], S["E"], "Sagittaire", "6.8", "11'", ""],
    29: [T["AO"], S["E"], "Cygne", "7.1", "7'", ""],
    30: [T["AG"], S["A"], "Capricorne", "7.2", "12'", ""],
    31: [T["G"], S["A"], "Andromède", "3.4", "190'x60'", "Galaxie d'Andromède"],
    32: [T["G"], S["A"], "Andromède", "8.1", "8'x6'", "Le Compagnon d'Andromède"],
    33: [T["G"], S["A"], "Triangle", "5.7", "70'x40'", "Galaxie du Triangle"],
    34: [T["AO"], S["H"], "Persée", "5.2", "35'", ""],
    35: [T["AO"], S["H"], "Gémeaux", "5.1", "28'", ""],
    36: [T["AO"], S["H"], "Cocher", "6.0", "12'", ""],
    37: [T["AO"], S["H"], "Cocher", "5.6", "24'", ""],
    38: [T["AO"], S["H"], "Cocher", "6.4", "21'", "Amas de l'Étoile de Mer"],
    39: [T["AO"], S["E"], "Cygne", "4.6", "32'", ""],
    40: [T["D"], S["P"], "Grande Ourse", "8.4", "0.8'", "Winnecke 4"],
    41: [T["AO"], S["H"], "Grand Chien", "4.5", "38'", ""],
    42: [T["N"], S["H"], "Orion", "4.0", "85'x60'", "Grande Nébuleuse d'Orion"],
    43: [T["N"], S["H"], "Orion", "9.0", "20'x15'", "Nébuleuse de De Mairan"],
    44: [T["AO"], S["H"], "Cancer", "3.1", "95'", "L'Amas de la Crèche"],
    45: [T["AO"], S["H"], "Taureau", "1.6", "110'", "Les Pléiades"],
    46: [T["AO"], S["H"], "Poupe", "6.1", "27'", ""],
    47: [T["AO"], S["H"], "Poupe", "4.4", "30'", ""],
    48: [T["AO"], S["H"], "Hydre", "5.8", "54'", ""],
    49: [T["G"], S["P"], "Vierge", "8.4", "10'x9'", ""],
    50: [T["AO"], S["H"], "Licorne", "5.9", "16'", ""],
    51: [T["G"], S["P"], "Ch. de Chasse", "8.4", "11'x7'", "Galaxie du Tourbillon (Whirlpool)"],
    52: [T["AO"], S["A"], "Cassiopée", "6.9", "13'", ""],
    53: [T["AG"], S["P"], "Chevelure", "7.6", "13'", ""],
    54: [T["AG"], S["E"], "Sagittaire", "7.6", "12'", ""],
    55: [T["AG"], S["E"], "Sagittaire", "6.3", "19'", ""],
    56: [T["AG"], S["E"], "Lyre", "8.3", "9'", ""],
    57: [T["NP"], S["E"], "Lyre", "8.8", "1.5'x1'", "Nébuleuse de l'Anneau"],
    58: [T["G"], S["P"], "Vierge", "9.7", "6'x5'", ""],
    59: [T["G"], S["P"], "Vierge", "10.6", "5'x4'", ""],
    60: [T["G"], S["P"], "Vierge", "8.8", "7'x6'", ""],
    61: [T["G"], S["P"], "Vierge", "9.7", "6'x6'", ""],
    62: [T["AG"], S["E"], "Ophiuchus", "6.5", "15'", ""],
    63: [T["G"], S["P"], "Ch. de Chasse", "8.6", "12'x8'", "Galaxie du Tournesol (Sunflower)"],
    64: [T["G"], S["P"], "Chevelure", "8.5", "10'x5'", "Galaxie de l'Œil Noir"],
    65: [T["G"], S["P"], "Lion", "9.3", "10'x3'", ""],
    66: [T["G"], S["P"], "Lion", "8.9", "9'x4'", ""],
    67: [T["AO"], S["H"], "Cancer", "6.1", "30'", "Amas du Cobra Royal"],
    68: [T["AG"], S["P"], "Hydre", "7.8", "11'", ""],
    69: [T["AG"], S["E"], "Sagittaire", "7.6", "10'", ""],
    70: [T["AG"], S["E"], "Sagittaire", "7.9", "9'", ""],
    71: [T["AG"], S["E"], "Flèche", "8.2", "7'", ""],
    72: [T["AG"], S["A"], "Verseau", "9.3", "7'", ""],
    73: [T["A"], S["A"], "Verseau", "9.0", "2.8'", ""],
    74: [T["G"], S["A"], "Poissons", "9.4", "10'x10'", "Galaxie du Fantôme (Phantom)"],
    75: [T["AG"], S["E"], "Sagittaire", "8.5", "7'", ""],
    76: [T["NP"], S["A"], "Persée", "10.1", "2.7'x1.8'", "Nébuleuse de la Petite Haltère"],
    77: [T["G"], S["A"], "Baleine", "8.9", "7'x6'", ""],
    78: [T["N"], S["H"], "Orion", "8.3", "8'x6'", "Nébuleuse de Casper"],
    79: [T["AG"], S["H"], "Lièvre", "7.7", "10'", ""],
    80: [T["AG"], S["E"], "Scorpion", "7.3", "10'", ""],
    81: [T["G"], S["P"], "Grande Ourse", "6.9", "26'x14'", "Galaxie de Bode"],
    82: [T["G"], S["P"], "Grande Ourse", "8.4", "11'x4'", "Galaxie du Cigare"],
    83: [T["G"], S["P"], "Hydre", "7.5", "13'x11'", "Galaxie du Moulinet Austral"],
    84: [T["G"], S["P"], "Vierge", "9.1", "6'x6'", ""],
    85: [T["G"], S["P"], "Chevelure", "9.1", "7'x5'", ""],
    86: [T["G"], S["P"], "Vierge", "8.9", "9'x6'", ""],
    87: [T["G"], S["P"], "Vierge", "8.6", "8'x8'", "Virgo A"],
    88: [T["G"], S["P"], "Chevelure", "9.6", "7'x4'", ""],
    89: [T["G"], S["P"], "Vierge", "9.8", "5'x5'", ""],
    90: [T["G"], S["P"], "Vierge", "9.5", "10'x4'", ""],
    91: [T["G"], S["P"], "Chevelure", "10.2", "5'x4'", ""],
    92: [T["AG"], S["E"], "Hercule", "6.3", "14'", ""],
    93: [T["AO"], S["H"], "Poupe", "6.0", "22'", "Amas du Papillon"],
    94: [T["G"], S["P"], "Ch. de Chasse", "8.2", "11'x9'", "Galaxie de l'Œil de Crocodile"],
    95: [T["G"], S["P"], "Lion", "9.7", "7'x5'", ""],
    96: [T["G"], S["P"], "Lion", "9.2", "8'x5'", ""],
    97: [T["NP"], S["P"], "Grande Ourse", "9.9", "3.4'", "Nébuleuse du Hibou (Owl Nebula)"],
    98: [T["G"], S["P"], "Chevelure", "10.1", "10'x3'", ""],
    99: [T["G"], S["P"], "Chevelure", "9.9", "5'x5'", "Coma Pinwheel"],
    100: [T["G"], S["P"], "Chevelure", "9.3", "7'x6'", ""],
    101: [T["G"], S["P"], "Grande Ourse", "7.9", "28'x27'", "Galaxie du Moulinet (Pinwheel)"],
    102: [T["G"], S["P"], "Dragon", "9.9", "6'x3'", "Galaxie du Fuseau (Spindle)"],
    103: [T["AO"], S["A"], "Cassiopée", "7.4", "6'", ""],
    104: [T["G"], S["P"], "Vierge", "8.0", "9'x4'", "Galaxie du Sombrero"],
    105: [T["G"], S["P"], "Lion", "9.3", "5'x5'", ""],
    106: [T["G"], S["P"], "Ch. de Chasse", "8.4", "18'x7'", ""],
    107: [T["AG"], S["E"], "Ophiuchus", "7.9", "13'", ""],
    108: [T["G"], S["P"], "Grande Ourse", "10.0", "9'x2'", "Galaxie de la Planche de Surf"],
    109: [T["G"], S["P"], "Grande Ourse", "9.8", "8'x5'", ""],
    110: [T["G"], S["A"], "Andromède", "8.1", "17'x10'", "Edward Young Star"]
}

# ==========================================================
#                      SCRIPT
# ==========================================================
def get_exif_date(filepath):
    try:
        with Image.open(filepath) as img:
            exif = img._getexif()
            if exif and 306 in exif:
                return datetime.strptime(exif[306], "%Y:%m:%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
    except: pass
    return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%d/%m/%Y %H:%M") if os.path.exists(filepath) else LANG["NO_DATE"]

# --- SCRIPT PRINCIPAL ---
if not os.path.exists(CONFIG["THUMB_DIR"]): os.makedirs(CONFIG["THUMB_DIR"])

photo_dict = {}
for f in [f for f in os.listdir(".") if f.lower().endswith(CONFIG["EXTENSIONS"])]:
    m = re.findall(r'M\s?(\d+)', f, re.IGNORECASE)
    if m:
        t_path = os.path.join(CONFIG["THUMB_DIR"], f"thumb_{f}")
        if not os.path.exists(t_path):
            try:
                with Image.open(f) as img:
                    img.thumbnail(CONFIG["THUMB_SIZE"])
                    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
                    img.save(t_path, "JPEG", quality=85)
            except: t_path = f
        for val in m:
            n = int(val)
            if 1 <= n <= 110: photo_dict[n] = {"full": f, "thumb": t_path, "date": get_exif_date(f)}

# --- GÉNÉRATION HTML ---
html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{LANG["PAGE_TITLE"]}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #eee; margin: 0; padding: 20px; }}
        header {{ text-align: center; margin-bottom: 20px; }}
        .filter-bar {{ text-align: center; margin-bottom: 30px; }}
        .filter-btn {{ background: #252525; border: 1px solid #444; color: #aaa; padding: 8px 18px; margin: 0 4px; border-radius: 20px; cursor: pointer; }}
        .filter-btn.active {{ background: #4dabf7; color: #fff; border-color: #4dabf7; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 12px; max-width: 1600px; margin: 0 auto; }}
        .case {{ background: #1a1a1a; border: 1px solid #333; border-radius: 4px; display: flex; flex-direction: column; height: 160px; transition: 0.2s; }}
        .case:hover {{ border-color: #4dabf7; transform: scale(1.02); }}
        .img-container {{ width: 100%; height: 130px; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; cursor: pointer; position: relative; }}
        .case img {{ width: 100%; height: 100%; object-fit: cover; }}
        .label {{ background: #252525; text-align: center; font-size: 13px; font-weight: bold; padding: 5px 0; border-top: 1px solid #333; }}
        .label a {{ color: #aaa; text-decoration: none; }}
        .empty {{ color: #222; font-size: 32px; font-weight: 900; line-height: 1; }}
        .type-hint {{ color: #444; font-size: 10px; font-weight: bold; text-transform: uppercase; margin-top: 5px; text-align: center; }}
        .season-hint {{ color: #333; font-size: 9px; font-style: italic; margin-top: 2px; }}
        #tooltip {{ position: fixed; display: none; background: rgba(15,15,15,0.95); border: 1px solid #4dabf7; padding: 12px; border-radius: 6px; z-index: 2000; pointer-events: none; font-size: 13px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 220px; }}
        .tt-label {{ color: #4dabf7; font-weight: bold; }}
        .tt-common {{ font-style: italic; color: #ddd; margin-top: 8px; display: block; border-top: 1px solid #333; padding-top: 5px; }}

        /* --- ZOOM OVERLAY (From V1) --- */
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
    <header><h1>{LANG["HEADER_TITLE"]}</h1><div class="stats">({len(photo_dict)} / 110 {LANG["UNIT_LABEL"]})</div></header>
    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterS('all', this)">{LANG['ALL']}</button>
        <button class="filter-btn" onclick="filterS('{S['P']}', this)">{S['P']}</button>
        <button class="filter-btn" onclick="filterS('{S['E']}', this)">{S['E']}</button>
        <button class="filter-btn" onclick="filterS('{S['A']}', this)">{S['A']}</button>
        <button class="filter-btn" onclick="filterS('{S['H']}', this)">{S['H']}</button>
    </div>
    <div class="grid">"""

for i in range(1, 111):
    d = MESSIER_DATA.get(i, ["-", "-", "-", "-", "-", ""])
    url = f"{CONFIG['BASE_URL']}{i}"
    safe_info = json.dumps(d).replace("'", "&apos;")
    
    html += f'\n<div class="case" data-season="{d[1]}" data-info=\'{safe_info}\' onmousemove="showT(event, this)" onmouseleave="hideT()">'
    if i in photo_dict:
        p = photo_dict[i]
        html += f'<div class="img-container" onclick="showImg(\'{p["full"]}\')" data-file="{p["full"]}" data-date="{p["date"]}"><img src="{p["thumb"]}"></div>'
    else:
        html += f'<div class="img-container" onclick="window.open(\'{url}\', \'_blank\')" data-file="" data-date=""><span class="empty">{i}</span><span class="type-hint">{d[0]}</span><span class="season-hint">{d[1]}</span></div>'
    html += f'<div class="label"><a href="{url}" target="_blank">M{i}</a></div></div>'

html += """
    </div>
    <div id="tooltip"></div>
    
    <!-- --- ZOOM OVERLAY (From V1) --- -->
    <div id="overlay">
        <span class="close-btn" onclick="closeImg()">&times;</span>
        <div id="imgWrapper" onclick="closeImg()">
            <img id="fullImg" src="" draggable="false" onclick="event.stopPropagation()">
        </div>
    </div>

    <script>
        function filterS(s, b) {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            b.classList.add('active');
            document.querySelectorAll('.case').forEach(c => {
                c.style.display = (s === 'all' || c.dataset.season === s) ? 'flex' : 'none';
            });
        }
        
        const tt = document.getElementById('tooltip');
        function showT(e, el) {
            const imgData = el.querySelector('.img-container').dataset;
            const d = JSON.parse(el.dataset.info);
            let h = "";
            if (imgData.file) {
                h += `<b style="color:#4dabf7;word-break:break-all">${imgData.file}</b><br><i style="color:#888">Date: ${imgData.date}</i><hr style="border:0;border-top:1px solid #333;margin:8px 0">`;
            }
            h += `<span class="tt-label">Type:</span> ${d[0]}<br><span class="tt-label">Saison:</span> ${d[1]}<br><span class="tt-label">Constellation:</span> ${d[2]}<br><span class="tt-label">Magnitude:</span> ${d[3]}<br><span class="tt-label">Taille:</span> ${d[4]}`;
            if(d[5] && d[5].trim() !== "") h += `<span class="tt-common">${d[5]}</span>`;
            tt.innerHTML = h; tt.style.display = 'block';
            
            let x = e.clientX + 15;
            let y = e.clientY + 15;
            
            if (x + 230 > window.innerWidth) x = e.clientX - 240;
            if (y + tt.offsetHeight > window.innerHeight) y = e.clientY - tt.offsetHeight - 15;
            
            tt.style.left = x + 'px';
            tt.style.top = y + 'px';
        }
        function hideT() { tt.style.display = 'none'; }

        /* --- ZOOM/PAN LOGIC (From V1) --- */
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
            hideT(); // Ensure tooltip is hidden
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
</body></html>"""

with open(CONFIG["FILE_OUT"], "w", encoding="utf-8") as f:
    f.write(html)
