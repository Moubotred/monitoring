import requests
import base64

def Recibo(suministro):
    # URL de la API
    url = "https://www.luzdelsur.pe/es/VerPagarRecibo/ObtenerImagenBoletaLibre"

    # Payload con el número de suministro
    payload = {
        "request": {
            "Suministro": f"{suministro}"  # Ajusta el número de suministro
        }
    }

    # Encabezados necesarios (incluye la Cookie si es requerida)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.luzdelsur.pe",
        "Referer": "https://www.luzdelsur.pe/es/VerPagarRecibo"
    }

    # Realiza la solicitud POST
    response = requests.post(url, json=payload, headers=headers)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Convertir la respuesta a JSON
        data = response.json()
        
        if data.get("success"):
            # Decodificar la imagen Base64
            imagen_base64 = data['datos']['archivoBase64']
            
            # Decodificar y guardar la imagen en un archivo
            with open(f"{suministro}.png", "wb") as img_file:
                img_file.write(base64.b64decode(imagen_base64))
            
            return f"{suministro}.png"
        else:
            print("Error en la respuesta de la API:", data.get("mensajeUsuario", "No se proporcionó mensaje de error"))
    else:
        print(f"Error en la solicitud: {response.status_code}")

# Recibo('143355')