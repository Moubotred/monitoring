import requests
import base64
import urllib.request
from ResourceHub import ConvertPdf,Templades,FileWebDownloads

def Luzdelsur_Recibo(suministro):
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
                try:
                    img_file.write(base64.b64decode(imagen_base64))
                except TypeError:
                    return "La API no devolvió una imagen válida en formato base64"
            
            return f"{suministro}.png"
        else:
            print("Error en la respuesta de la API:", data.get("mensajeUsuario", "No se proporcionó mensaje de error"))
    else:
        print(f"Error en la solicitud: {response.status_code}")

def Hasber_Sistema_Envios(suministro):
    # URL a la que se va a hacer la solicitud POST
    url = "https://hasbercourier.easyenvios.com/modulos/controlador/herramientas/con_cargosenvios.php?tabla=congrid_envio_seguimiento"

    # Encabezados
    headers = {
        "Host": "hasbercourier.easyenvios.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://hasbercourier.easyenvios.com",
        "Referer": "https://hasbercourier.easyenvios.com/modulos/seguimiento.php",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
        "Connection": "keep-alive"
    }

    # Parámetros del cuerpo de la solicitud (POST data)
    data = {
        "ciacodigo": "17",
        "succodigo": "001",
        "asenombre": "",
        "codigoenvio": "",
        "codigounico": f"{suministro}",
        "asepropuesta": "",
        "strnrodocumento": "",
        "page": "1",
        "rows": "10",
        "sort": "a.asenumero",
        "order": "asc"
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, data=data)

    # Verificar el estado de la respuesta de estado
    if response.status_code == 200:
        # pasar datos a json
        data = response.json()
        try:
            # buscar clave de diccionario
            if data['rows'][0]['artnombre'] == 'CARTAS / REEMPLAZO DE MEDIDOR EMPRESAS':
                url_file = data['rows'][0]['imagen1']
                FileWebDownloads(url_file,suministro)
                ConvertPdf(suministro)
                Templades(f"{suministro}.tif")
                return suministro                    
        except IndexError:
            return '?'
    else:
        print('[x]')

