import requests

# URL de la API para consultar el suministro
url = "https://www.luzdelsur.pe/es/CorteLuz/ObtenerSuministroById"

# Encabezados que incluyen el Content-Type
headers = {
    "Content-Type": "application/json"
}

payload = {
    "suministro": "499637"
}

response = requests.post(url, json=payload, headers=headers)

# Verifica el estado de la solicitud
if response.status_code == 200:
    data = response.json()  # Convertir la respuesta a JSON
    print("Datos del suministro:", data['datos'])
else:
    print(f"Error en la solicitud: {response.status_code}")
