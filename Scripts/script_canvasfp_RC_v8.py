import sqlite3 as lite

# Conecta con la base de datos que origina OpenWPM como resultado
wpm_db = "crawl-data.sqlite"
conn = lite.connect(wpm_db)
cur = conn.cursor()

# Define los valores que permiten comprobar las condiciones de canvas fingerprinting
canvas_h = "HTMLCanvasElement.height"
canvas_w = "HTMLCanvasElement.width"
canvas_cf= "CanvasRenderingContext2D.fillStyle"
canvas_cs= "CanvasRenderingContext2D.strokeStyle"
canvas_ff= "CanvasRenderingContext2D.fillText"
canvas_fs= "CanvasRenderingContext2D.strokeText"
canvas_save= "CanvasRenderingContext2D.save"
canvas_rest= "CanvasRenderingContext2D.restore"
canvas_el= "HTMLCanvasElement.addEventListener"
canvas_data= "HTMLCanvasElement.toDataURL"
canvas_img= "CanvasRenderingContext2D.getImageData"
fp_1 = set()
fp_2 = set()
fp_3 = set()
fp_4 = set()
veri_1 = set()
veri_2 = set()
fp_sites = set()

# Busca en la base de datos, verificando los sitios donde se cumplen las cuatro condiciones de canvas fingerprinting

for url, symbol, op, val, arg, top_url in cur.execute("SELECT distinct j.script_url, j.symbol, j.operation, j.value, j.arguments, v.site_url FROM javascript as j JOIN site_visits as v ON j.visit_id = v.visit_id WHERE j.symbol LIKE '%Canvas%' ORDER BY v.site_url;"):

	if canvas_h in symbol and float(val) >= 16:
		veri_1.add(symbol + url)
		if (canvas_w + url) in veri_1:
			fp_1.add(top_url + ' ' + url)
	elif canvas_w in symbol and float(val) >= 16:
		veri_1.add(symbol + url)
		if (canvas_h + url) in veri_1:
			fp_1.add(top_url + ' ' + url)

	if canvas_cf in symbol:
		veri_2.add(symbol + url + val)
		if (canvas_cs + url + val) in veri_2:
			fp_2.add(top_url + ' ' + url)
		elif (sum((canvas_cf + url) in s for s in veri_2)) > 1:
			fp_2.add(top_url + ' ' + url)
	elif canvas_cs in symbol:
		veri_2.add(symbol + url + val)
		if (canvas_cf + url + val) in veri_2:
			fp_2.add(top_url + ' ' + url)
		elif (sum((canvas_cs + url) in s for s in veri_2)) > 1:
			fp_2.add(top_url + ' ' + url)
	elif canvas_ff in symbol and (len(set(arg[arg.find('0":"')+4:arg.find(',"1"')-1])))>= 10:	
		fp_2.add(top_url + ' ' + url)
	elif canvas_fs in symbol and (len(set(arg[arg.find('0":"')+4:arg.find(',"1"')-1])))>= 10:	
		fp_2.add(top_url + ' ' + url)
			
	if canvas_save in symbol:
		fp_3.add(top_url + ' ' + url)
	elif canvas_rest in symbol:
		fp_3.add(top_url + ' ' + url)
	elif canvas_el in symbol:
		fp_3.add(top_url + ' ' + url)

	if canvas_data in symbol:
		fp_4.add(top_url + ' ' + url)
	elif canvas_img in symbol:
		if float(arg[arg.find('"2":')+4:arg.find(',"3"')]) >= 16:
			if float(arg[arg.find('"3":')+4:arg.find('}')]) >= 16:
				fp_4.add(top_url + ' ' + url)

# Agrupa los sitios que cumplen las cuatro condiciones del canvas fingerprinting (Interseccion en un solo set)
fp_sites = (fp_1 & fp_2 & fp_4) - fp_3

# Muestra los resultados
#print(1, fp_1)
#print(2, fp_2)
#print(3, fp_3)
#print(4, fp_4)
print("\n".join(fp_sites))
