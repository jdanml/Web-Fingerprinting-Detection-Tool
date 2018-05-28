import sqlite3 as lite

# Conecta con la base de datos que origina OpenWPM como resultado
wpm_db = "crawl-data.sqlite"
conn = lite.connect(wpm_db)
cur = conn.cursor()

# Define los valores que permiten comprobar las condiciones de canvas font fingerprinting
canvas_font= "CanvasRenderingContext2D.font"
canvas_text= "CanvasRenderingContext2D.measureText"
fontp_1 = set()
fontp_2 = set()
verif_1 = set()
verif_2 = list()
fontp_sites = set()

# Busca en la base de datos, verificando los sitios donde se cumplen las dos condiciones de canvas font fingerprinting

for url, vid, symbol, op, val, arg, top_url in cur.execute("SELECT j.script_url, j.visit_id, j.symbol, j.operation, j.value, j.arguments, v.site_url FROM javascript as j JOIN site_visits as v ON j.visit_id = v.visit_id WHERE j.symbol LIKE '%Canvas%' ORDER BY v.site_url;"):

	if canvas_font in symbol:
		verif_1.add(symbol + url + val)
		if (sum((canvas_font + url) in s for s in verif_1)) >= 50:
			fontp_1.add(top_url + ' ' + url)

	if canvas_text in symbol:
		verif_2.append(str(vid) + symbol + url + arg)
		if verif_2.count(str(vid) + symbol + url + arg) >= 50:
			fontp_2.add(top_url + ' ' + url)
			
# Agrupa los sitios que cumplen las dos condiciones del canvas font fingerprinting (Interseccion en un solo set)
fontp_sites = fontp_1 & fontp_2

# Muestra los resultados
#print(1, fontp_1)
#print(2, fontp_2)
print("\n".join(fontp_sites))
