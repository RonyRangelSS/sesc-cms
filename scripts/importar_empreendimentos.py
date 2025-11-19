import requests
import unicodedata
from pyproj import Transformer
from shapely.geometry import shape

WFS_URL = "http://localhost:8080/geoserver/sesc/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=sesc%3ATerritorios&outputFormat=application%2Fjson"
STRAPI_URL = "http://localhost:1337/api/empreendimentos"
STRAPI_TOKEN = "9009b39909669d4e515c80002a008d242bd740ae988ec74501276cd4032ac5217162640517625bc3123057f12fafd280aa420559e6f931fb0ff5921fa42ac8079b6c21eb7e2dc8cd58083c9e6c6c24e0722436345dc2ac81980da5a52725e97d8066796a76b313bfa64a30868a1bfbc965fa26a8d64b912b3319925062e946df"

def limpar_texto(valor):
    if isinstance(valor, str):
        texto = unicodedata.normalize("NFKD", valor).encode("ascii", "ignore").decode("utf-8")
        return texto.strip()
    return valor

converter = Transformer.from_crs("EPSG:31985", "EPSG:4326", always_xy=True)

print("Buscando dados do GeoServer...")
response = requests.get(WFS_URL)

if response.status_code != 200:
    print(f"Erro no WFS: {response.status_code}")
    print(response.text)
    exit()

response.encoding = "utf-8"
data = response.json()
features = data.get("features", [])
print(f"{len(features)} empreendimentos encontrados.")

headers = {
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type": "application/json",
}

for f in features:
    props = {k: limpar_texto(v) for k, v in f.get("properties", {}).items()}
    geom = f.get("geometry")

    if not geom or not geom.get("coordinates"):
        print(f"Ignorando registro sem geometria: {props.get('Empreend_1')}")
        continue

    try:
        s = shape(geom)
        centroid = s.centroid
        x, y = centroid.x, centroid.y
    except Exception:
        coords = geom.get("coordinates", [])
        if isinstance(coords[0], list):
            x, y = coords[0][0] if isinstance(coords[0][0], list) else coords[0]
        else:
            x, y = coords

    lng, lat = converter.transform(x, y)

    payload = {
        "data": {
            "nome": props.get("Empreend_1"),
            "tipo": props.get("Tipo_1"),
            "foto": props.get("Foto_1"),
            "endereco": props.get("Endereco"),
            "bairro": props.get("Bairro"),
            "municipio": props.get("Municipio"),
            "estado": props.get("Estado"),
            "regiao": props.get("Regiao"),
            "cep": props.get("CEP"),
            "pais": props.get("Pais"),
            "localizacao": { "lat": lat, "lng": lng, "geohash": "" }
        }
    }

    res = requests.post(STRAPI_URL, headers=headers, json=payload)

    if res.status_code in (200, 201):
        print(f"Inserido: {props.get('Empreend_1')}")
    else:
        print(f"Erro ao inserir {props.get('Empreend_1')}: {res.status_code} - {res.text}")

print("Importação concluída!")
