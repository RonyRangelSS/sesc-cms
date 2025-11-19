import os
import requests
STRAPI_URL = "http://localhost:1337"
UPLOAD_URL = f"{STRAPI_URL}/api/upload"
EMP_URL = f"{STRAPI_URL}/api/empreendimentos"
STRAPI_TOKEN = "9009b39909669d4e515c80002a008d242bd740ae988ec74501276cd4032ac5217162640517625bc3123057f12fafd280aa420559e6f931fb0ff5921fa42ac8079b6c21eb7e2dc8cd58083c9e6c6c24e0722436345dc2ac81980da5a52725e97d8066796a76b313bfa64a30868a1bfbc965fa26a8d64b912b3319925062e946df"

BASE_DIR = r"C:\Users\RONNY R\Desktop\dados\Fotos Empreendimentos" 
CAMPO_RELACIONAMENTO = "imagem" 

headers = {"Authorization": f"Bearer {STRAPI_TOKEN}"}


def upload_image(image_path):
    image_path = os.path.abspath(image_path)
    file_name = os.path.basename(image_path)
    print(f"Enviando {file_name} ...")

    with open(image_path, "rb") as img_file:
        files = {
            "files": (file_name, img_file, "image/jpeg")  
        }
        try:
            res = requests.post(UPLOAD_URL, headers={"Authorization": f"Bearer {STRAPI_TOKEN}"}, files=files)
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None

    if res.status_code in (200, 201):
        data = res.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]["id"]
        else:
            print(f"Resposta inesperada: {data}")
            return None
    else:
        print(f"Erro no upload de {file_name}: {res.status_code} - {res.text}")
        return None



def find_empreendimento_by_foto_id(foto_id):
    params = {"filters[foto][$eq]": foto_id}
    res = requests.get(EMP_URL, headers=headers, params=params)
    print(f"\n🔎 GET {res.url} -> {res.status_code}")
    data = res.json()

    if res.status_code == 200 and data.get("data"):
        emp = data["data"][0]
        emp_id = emp.get("documentId") or emp.get("id")
        print(f"   → Encontrado: id={emp.get('id')}, documentId={emp.get('documentId')}")
        return emp_id
    print(f"Nenhum empreendimento encontrado com foto = {foto_id}")
    return None



def link_images_to_empreendimento(emp_id, image_ids):
    payload = {"data": {CAMPO_RELACIONAMENTO: image_ids}}
    res = requests.put(f"{EMP_URL}/{emp_id}",
                       headers={**headers, "Content-Type": "application/json"},
                       json=payload)
    if res.status_code in (200, 201):
        print(f"Empreendimento {emp_id} atualizado com {len(image_ids)} imagens.")
        return True
    else:
        print(f"Falha ao atualizar empreendimento {emp_id}: {res.status_code} - {res.text}")
        return False


print(f"Iniciando importação de imagens de: {BASE_DIR}")

for folder in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder)
    if not os.path.isdir(folder_path):
        continue

    foto_id = folder.lstrip("0")
    print(f"\nProcessando pasta {foto_id}...")

    emp_id = find_empreendimento_by_foto_id(foto_id)
    if not emp_id:
        continue

    imagens = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not imagens:
        print(f"Nenhuma imagem encontrada na pasta {folder}")
        continue

    image_ids = []
    for img_path in imagens:
        print(f"Enviando {os.path.basename(img_path)} ...")
        img_id = upload_image(img_path)
        if img_id:
            image_ids.append(img_id)

    if not image_ids:
        print(f"Nenhuma imagem válida enviada para {foto_id}")
        continue

    link_images_to_empreendimento(emp_id, image_ids)

print("\nProcesso concluído com sucesso!")
