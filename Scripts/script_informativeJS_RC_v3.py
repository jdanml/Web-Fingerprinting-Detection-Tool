import sqlite3 as lite

# Conecta con la base de datos que origina OpenWPM como resultado
wpm_db = "crawl-data.sqlite"
conn = lite.connect(wpm_db)
cur = conn.cursor()

# Define los valores que permiten comprobar las condiciones de fingerprinting por objetos informativos de JS
info_ob= ["window.navigator.appCodeName", "window.navigator.appName", "window.navigator.appVersion", "window.navigator.buildID", "window.navigator.cookieEnabled", "window.navigator.doNotTrack", "window.navigator.geolocation", "window.navigator.language", "window.navigator.languages", "window.navigator.onLine", "window.navigator.oscpu", "window.navigator.platform", "window.navigator.product", "window.navigator.productSub", "window.navigator.userAgent", "window.navigator.vendorSub", "window.navigator.vendor", "window.screen.pixelDepth", "window.screen.colorDepth"]
navplug= "window.navigator.plugins"
navmim= "window.navigator.mimeTypes"
ver_info_1 = set()
ver_info_2 = set()
info_sites_1 = set()
info_sites_2 = set()
info_sites = set()

# Busca en la base de datos, verificando los sitios donde se cumplen las dos condiciones fingerprinting por objetos informativos de JS

for url, symbol, op, val, arg, top_url in cur.execute("SELECT distinct j.script_url, j.symbol, j.operation, j.value, j.arguments, v.site_url FROM javascript as j JOIN site_visits as v ON j.visit_id = v.visit_id WHERE j.symbol LIKE '%window%' ORDER BY v.site_url;"):

	if navplug in symbol:
		ver_info_1.add(url + symbol)
		if (sum((url + symbol) in s for s in ver_info_1)) > 5:
			info_sites_1.add(top_url + ' ' + url)
	elif navmim in symbol:
		ver_info_1.add(url + symbol)
		if (sum((url + symbol) in s for s in ver_info_1)) > 3:
			info_sites_1.add(top_url + ' ' + url)
			
	if symbol in info_ob:
		ver_info_2.add(url + symbol)
		if (sum((url) in s for s in ver_info_2)) > 15:
			info_sites_2.add(top_url + ' ' + url)

# Agrupa los sitios que cumplen las condiciones del fingerprinting por objetos informativos de JS (Interseccion en un solo set)
info_sites = info_sites_1 | info_sites_2

# Muestra los resultados
#print(1, info_sites_1)
#print("\n".join(info_sites_2))
print("\n".join(info_sites))
