import sqlite3 as lite

# Conecta con la base de datos que origina OpenWPM como resultado
wpm_db = "crawl-data.sqlite"
conn = lite.connect(wpm_db)
cur = conn.cursor()

# Define los valores que permiten comprobar las condiciones de webRTC fingerprinting
rtc_data= "RTCPeerConnection.createDataChannel"
rtc_offer= "RTCPeerConnection.createOffer"
rtc_cand= "RTCPeerConnection.onicecandidate"
rtc_1 = set()
rtc_2 = set()
rtc_3 = set()
rtc_sites_0 = set()
rtc_sites_1 = set()
rtc_sites_2 = set()
rtc_sites_3 = set()
rtc_sites = set()

# Busca en la base de datos, verificando los sitios donde se cumplen las condiciones de webRTC fingerprinting

for url, symbol, op, val, arg, top_url in cur.execute("SELECT j.script_url, j.symbol, j.operation, j.value, j.arguments, v.site_url FROM javascript as j JOIN site_visits as v ON j.visit_id = v.visit_id WHERE j.symbol LIKE '%RTCPeerConnection%' ORDER BY v.site_url;"):

	if rtc_data in symbol:
		rtc_1.add(top_url + ' ' + url)

	if rtc_offer in symbol:
		rtc_2.add(top_url + ' ' + url)

	if rtc_cand in symbol:
		rtc_3.add(top_url + ' ' + url)

# Agrupa los sitios que cumplen las condiciones del webRTC fingerprinting (Interseccion en un solo set)
rtc_sites_0 = rtc_1 & rtc_2 & rtc_3

# Muestra los resultados
#print(1, rtc_1)
#print(2, rtc_2)
#print(3, rtc_3)
print("\n".join(rtc_sites_0))

# Comprueba si la información de webRTC es utilizada en un contexto de fingerprinting

#rtc_sites_1 = rtc_sites_0 & info_sites
#rtc_sites_2 = rtc_sites_0 & fp_sites
#rtc_sites_3 = rtc_sites_0 & fontp_sites

#rtc_sites = rtc_sites_1 | rtc_sites_2 | rtc_sites_3

# Muestra los resultados finales

#print("\n".join(rtc_sites))